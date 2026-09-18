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
pae_blocks = R["pae_relative_placement"]["blocks"]
pae_schema = R["pae_relative_placement"]["schema"]
ver = R["verification"]["plddt_two_sources"]

core_pae = pae_blocks["core_internal_94_292"]["mean_pae"]
tail_pae = pae_blocks["tail_rows_to_core_columns"]["mean_pae"]

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
    ("N-terminal worst pLDDT",   f'{nterm["min_plddt"]:.2f}',          "57.66, worst position in 18-28"),
    ("N-terminal below-70 count", f'{nterm["below_70_count"]} of its {nterm["count"]}',
                                                                       "5 of its 11 positions"),
    ("core-internal mean PAE",   str(core_pae),                        "3.6 angstrom within the core"),
    ("tail-to-core mean PAE",    str(tail_pae),                        "28.1 angstrom, tail vs core"),
    ("PAE declared maximum",     str(pae_schema["declared_max"]),      "31.75, the top of the scale"),
    ("fold end residue",         "292",                                "the confident fold ends near 292"),
    ("pLDDT sources compared",   f'{ver["residues_compared"]} of {ver["residues_compared"]}',
                                                                       "393 of 393 agree"),
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

# the PAE slide claims the tail's placement against the core is near the top of the file's
# own scale, and that the core is placed against itself far more confidently
if tail_pae <= core_pae:
    claim_errors.append(
        f'deck says the tail is placed far less confidently than the core is against itself, '
        f'but tail-to-core PAE is {tail_pae} and core-internal PAE is {core_pae}')
if tail_pae < 0.8 * pae_schema["declared_max"]:
    claim_errors.append(
        f'deck says tail-to-core PAE sits near the declared maximum '
        f'{pae_schema["declared_max"]}, but it is {tail_pae}')
if any(c["row_residue"] in range(94, 293) and c["column_residue"] in range(94, 293)
       for c in R["pae_relative_placement"]["anomalies"]["above_declared_max_cells"]):
    claim_errors.append("a PAE cell above the declared maximum now falls inside the core block, "
                        "so results.json can no longer say no block mean depends on them")

# the verification slide is only worth making if the two pLDDT sources still agree exactly
if ver["disagreements"] != 0 and "zero differences" in prose:
    claim_errors.append(
        f'deck says the two pLDDT columns agree exactly, but results.json reports '
        f'{ver["disagreements"]} disagreements')

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
