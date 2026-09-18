"""Verify every number in slides.html still agrees with results/results.json.

NON-DESTRUCTIVE. Reads both files, writes nothing. Safe to run at any time,
including after hand-editing the deck's prose.

Division of labour this supports:
  - Jakub edits phrasing directly in slides.html
  - Claude runs this to confirm no figure has drifted from the analysis

Exit code 0 = all figures agree. 1 = at least one mismatch.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
R = json.loads((ROOT / "results/results.json").read_text())
HTML = (ROOT / "slides.html").read_text()

# ---------------------------------------------------------------- expectations
reg = R["regional_comparison"]
alt = R["alternative_cutoff_counts"]
flagged = R["ranked_flagged_residues"]
series = R["per_residue_plddt_94_312"]
nterm = R["n_terminal_18_28_validation_project"]

n_flag = R["summary"]["passing_count"]
n_tail = sum(1 for f in flagged if f["residue"] >= 293)
n_core = sum(1 for f in flagged if f["residue"] <= 292)
cut = R["scope"]["cutoff"]["value"]

# ---------------------------------------------------- 1. the embedded data blob
m = re.search(r"const DATA = (\{.*?\});\n", HTML, re.S)
blob_errors = []
if not m:
    blob_errors.append("could not find the embedded `const DATA = {...}` block")
else:
    D = json.loads(m.group(1))
    if len(D.get("series", [])) != len(series):
        blob_errors.append(f"chart series has {len(D.get('series',[]))} points, "
                           f"results.json has {len(series)}")
    else:
        bad = [(a, b) for (a, b), s in zip(D["series"], series)
               if a != s["residue"] or abs(b - s["plddt"]) > 1e-9]
        if bad:
            blob_errors.append(f"{len(bad)} chart points disagree with results.json")
    if len(D.get("flagged", [])) != n_flag:
        blob_errors.append(f"chart marks {len(D.get('flagged',[]))} flagged points, "
                           f"results.json has {n_flag}")
    else:
        bad = [(a, b) for (a, b), f in zip(D["flagged"], flagged)
               if a != f["residue"] or abs(b - f["plddt"]) > 1e-9]
        if bad:
            blob_errors.append(f"{len(bad)} flagged markers disagree with results.json")
    if D.get("cut") != cut:
        blob_errors.append(f"chart cut-off {D.get('cut')} != results.json {cut}")

# ----------------------------------------------- 2. figures written in the prose
# strip the embedded structure and data blob so we only scan visible copy
prose = HTML
prose = re.sub(r"const CIF = `.*?`;", "", prose, flags=re.S)
prose = re.sub(r"const DATA = \{.*?\};", "", prose, flags=re.S)
prose = re.sub(r"<style>.*?</style>", "", prose, flags=re.S)

CHECKS = [
    ("flagged count",            str(n_flag),                          "22 positions / 22 flagged"),
    ("flagged in 293-312",       str(n_tail),                          "20 of them"),
    ("flagged inside the fold",  str(n_core),                          "only N hits inside the fold"),
    ("core mean pLDDT",          f'{reg["94-292"]["mean_plddt"]:.2f}', "95.29"),
    ("tail mean pLDDT",          f'{reg["293-312"]["mean_plddt"]:.2f}', "46.63"),
    ("core percent below 70",    f'{reg["94-292"]["below_70_percent"]:.2f}', "1.01%"),
    ("cut-off",                  str(int(cut)),                        "cut-off of 70"),
    ("scope start",              "94",                                 "positions 94-312"),
    ("scope end",                "312",                                "positions 94-312"),
    ("boundary residue",         "293",                                "the drop at 293"),
    ("sequence length",          "393",                                "393 positions"),
    ("excluded region start",    "18",                                 "18-28 out of scope"),
    ("excluded region end",      "28",                                 "18-28 out of scope"),
    ("N-terminal mean pLDDT",    f'{nterm["mean_plddt"]:.2f}',         "68.88, the helix she almost shipped"),
    ("named MDM2 contact",       "Phe19",                              "Phe19 sits below the cut-off"),
    ("named MDM2 contact",       "Leu26",                              "Leu26 sits below the cut-off"),
]

missing = [(label, val, hint) for label, val, hint in CHECKS if val not in prose]

# the "disappears at 65" claim is only true if nothing in the fold flags below 65
claim_errors = []
if reg["94-292"]["below_65_count"] != 0 and "65" in prose:
    claim_errors.append(
        f'deck says the core hits vanish at 65, but results.json reports '
        f'{reg["94-292"]["below_65_count"]} core residues below 65')
# the N-terminal slide claims her helix scores below the line she gave us for the core,
# and that the two side chains it names sit under it
if nterm["mean_plddt"] >= cut:
    claim_errors.append(
        f'deck says the 18-28 helix scores below the cut-off, but its mean pLDDT is '
        f'{nterm["mean_plddt"]} against a cut-off of {cut}')
under = {c["residue"] for c in nterm["mdm2_contact_residues"] if c["plddt"] < cut}
for residue, name in ((19, "Phe19"), (26, "Leu26")):
    if name in prose and residue not in under:
        contact = next(c for c in nterm["mdm2_contact_residues"] if c["residue"] == residue)
        claim_errors.append(
            f'deck names {name} as sitting below {cut}, but results.json reports '
            f'{contact["plddt"]}')
if nterm["mean_plddt"] >= reg["94-292"]["mean_plddt"]:
    claim_errors.append("deck contrasts the helix with a better-scoring core, but the "
                        "core no longer scores higher")

if alt["below_65"] != 19 or alt["below_80"] != 26:
    claim_errors.append(f'sensitivity counts changed: <65={alt["below_65"]}, <80={alt["below_80"]}')

# ------------------------------------------------------------------- report
print(f"slides.html  {len(HTML)/1024:.0f} KB   results.json  "
      f"{len(flagged)} flagged of {R['summary']['core_residues_screened']}")
print()

ok = True
if blob_errors:
    ok = False
    print("CHART DATA — MISMATCH")
    for e in blob_errors:
        print(f"   {e}")
else:
    print(f"CHART DATA — ok ({len(series)} points, {n_flag} markers, cut-off {cut})")

if missing:
    ok = False
    print("\nFIGURES IN PROSE — NOT FOUND IN THE DECK")
    for label, val, hint in missing:
        print(f"   {label:26} expected {val!r}   ({hint})")
    print("\n   A missing figure usually means the deck was reworded around it,")
    print("   or the analysis changed and the deck was not updated. Check which.")
else:
    print(f"FIGURES IN PROSE — ok (all {len(CHECKS)} present)")

if claim_errors:
    ok = False
    print("\nCLAIMS — CHECK")
    for e in claim_errors:
        print(f"   {e}")
else:
    print("CLAIMS — ok (sensitivity at 65/80 unchanged; core hits still vanish below 65)")

print()
print("PASS — every figure in the deck agrees with the analysis" if ok
      else "FAIL — see above")
sys.exit(0 if ok else 1)
