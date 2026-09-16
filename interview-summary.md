# Interview summary — Dr. Margit Holló, p53

**Source:** `ddls-week4-interview.md` (two rounds, exported 14:03 and 14:13, 16 Sep 2026)
**Owner:** Dr. Margit Holló, Karolinska Institutet — structural cancer biology
**Written from the transcript.** §7 is separated because it was checked *after* the interview closed.

---

## 1. The short version

She has human p53 and its AlphaFold model. She spotted what looks like a **clean helix at
residues 18–28**, near the front of the protein, and initially thought it could be a fixed
drug-design target for a medicinal-chemistry collaborator.

**During the interview she talked herself out of it.** She now treats that helix as a separate
*validation project*, not a target, because the N-terminus is floppy in solution and probably
only forms that helix when bound to MDM2.

**So the actual job she wants is different and much narrower:** screen the **DNA-binding core,
residues 94–312**, for residues whose model-assigned confidence is unusually poor, rank them
worst-first, apply a cut-off declared in advance, and hand back a table. That table is a
**caution list** — positions the chemist should not treat as reliable anchors.

The single most important thing she said: she has **never opened the numerical companion file**
and does not know what is in it. Interpreting it is explicitly delegated.

---

## 2. What she wants — settled, stated repeatedly

| Item | Her specification |
|---|---|
| **Scope** | Residues **94–312**, inclusive, on the canonical 393-residue sequence |
| **Task** | Find residues with unusually poor model-assigned values; report exact positions and values |
| **Ranking** | Worst first (smallest value first, *if* smaller means weaker) |
| **Cut-off** | Declared **before** looking at results; justified from the in-scope values only |
| **Ties** | Kept as ties at a shared rank. Never broken arbitrarily |
| **Anomalies** | Flagged, never silently dropped. Report how many and why |
| **Excluded** | Residues **18–28**, entirely. Separate project, must not be mixed in |
| **Forbidden** | Substituting a whole-protein average for residue-level results |
| **Output** | residue number · amino acid · value · field + units (or "unitless") · rank · cut-off + reason · count passing · ties · anomalies |
| **Also** | Preserve raw values alongside rounded display values |

Plus a one-line rule the chemist can apply without coming back to ask.

---

## 3. What the list is *for* — she corrected an assumption here

It is a **caution and triage list, not an exclusion list.**

> A poor-scoring residue "should not be used as a fixed geometric anchor without additional
> evidence; it may still be useful at a flexible interface."

So the chemist isn't told to avoid these positions. They're told: *don't build the design around
this residue's exact coordinates without checking it first.* Mark them as **requiring validation
or cautious interpretation**.

---

## 4. The four rules she pre-declared for cases she hasn't seen

This is the valuable part of round two. She committed to rules **before** anyone looked at the
data, which makes them binding and reproducible.

**① If the companion file has no residue-level field.**
> "Do not substitute an arbitrary column. If the companion file lacks a documented residue-level
> field, inspect the CIF metadata; use a CIF field **only if** it is explicitly defined, one value
> per residue, and maps cleanly to the 393-residue sequence. Otherwise **stop before ranking** and
> report the schema gap to me."

A three-part gate, not blanket permission.

**② If the poor values cluster at one end instead of scattering.**
> "Both, but in sequence. Treat it as a valid 94–312 shortlist under the predeclared rule;
> **do not move the boundary after seeing the result.** Then examine whether the concentration is
> at an edge — **particularly near 305–312** — because that may indicate a **domain transition**
> rather than isolated problematic residues. Send the chemist the ranked list **with the positional
> clustering flagged, not as a clean target set.**"

She named 305–312 herself, unprompted, and even asked: *"Is the concentration at 94–100 or 305–312?"*

**③ Ranking direction is conditional, not yet fixed.**
> "I want the field definition first. Once it explicitly states that smaller values represent
> weaker model assignment, fix the rule as smallest to largest, with ties retained; until then it
> is only a conditional plan, not a declared ranking rule."

**④ If the files can't support the request at all.**
> "State it plainly as the result: **no defensible residue-level shortlist can be produced from
> these files.** Do not manufacture a substitute ranking or quietly change the field, scope, or
> cutoff; you may append the closest supported descriptive result separately, clearly labelled as
> non-equivalent and not suitable for target selection."

---

## 5. Where the 94–312 boundary comes from

Asked directly, she was clear it is **not** read off the picture:

> "An **operational definition** of the p53 DNA-binding core... the canonical folded-domain region
> used in p53 structural work; individual experimental constructs may start or end differently."

And she already expects the two ends to behave differently:

> At residue **150** — "the central, compact DNA-binding fold."
> At **305–312** — "the **edge** of that fold and its short C-terminal extension, closer to the
> **transition toward the tetramerisation region** — not necessarily the same compact geometry."
> "Keep both in scope because the brief says 94–312, but do not interpret their numerical values
> without checking how the field behaves."

**So the boundary is a task boundary, not a claim that everything inside it is equally folded.**

---

## 6. What she flagged as risks, in her own words

- **Numbering** — confirm canonical 393-residue P04637; an isoform or offset shifts every position
- **Scope** — keep 94–312 separate from 18–28; don't let a whole-chain summary drive the core list
- **The companion grid** — establish whether rows/columns are residue-indexed, whether indexing is
  0- or 1-based, whether dimensions match 393. *"Do not treat every number as a residue annotation."*
- **Model interpretation** — coordinates are one proposed conformation, not proof contacts exist in solution
- **Ranking rule** — declare the cut-off before selecting; report values and ties; don't substitute an average
- **Chain identity** — one p53 chain, **not** an MDM2–p53 complex. A feature in a single-chain model
  must not be described as an experimentally established partner interface

Her stated worst case: *"sending the chemist residues that are numerically selected but incorrectly
mapped, or mixing the N-terminal validation question into the core analysis."*

---

## 7. Verification run after the interview closed

Kept separate so the record above stays a record of what she **claimed**. All of the following is
**measured**, not asserted by her.

**Her gate ① — tested, and it passes.**

The companion JSON (`p53_alphafold_pae.json`) contains exactly two top-level keys:
`predicted_aligned_error` (393×393) and `max_predicted_aligned_error` (scalar). It is **pairwise**
error in ångström. **There is no per-residue field in it** — her assumption about that file was wrong.

Falling through to her CIF condition, all three parts are satisfied:

| Her requirement | Result |
|---|---|
| "explicitly defined" | ✅ `_ma_qa_metric` declares metric 2 as **`local` `pLDDT`** |
| "one value per residue" | ✅ `_ma_qa_metric_local` has exactly **393 rows** |
| "maps cleanly to the 393-residue sequence" | ✅ seq_id 1–393 contiguous, no gaps, no duplicates |

Also confirmed: values are identical to the mmCIF B-factor column; range 32.78–98.69; no nulls,
no NaN, nothing out of range. **pLDDT is unitless 0–100, higher = better** — so smaller *does* mean
weaker assignment, which satisfies her condition ③ and fixes the ranking rule as **smallest first**.

**One thing to note.** The CIF also carries `_ma_qa_metric_global.metric_value = 75.05` — a
whole-protein average sitting right there in the file. That is precisely the number she forbade
substituting. It should not appear anywhere in the shortlist logic.

**Sequence check.** Model = bundled FASTA = canonical UniProt P04637, verified residue-by-residue,
zero differences. 393 residues, single chain A. So her numbering concern is clean, and there is no
mutant in play.

---

## 8. Where this leaves the analysis

Her pre-declared rules now determine every step, with nothing left to negotiate:

1. Rank residues **94–312** by **local pLDDT**, smallest first, ties at shared rank
2. Declare the cut-off **before** selecting, justified from in-scope values only
3. Exclude **18–28** entirely
4. Report residue · AA · raw value · rank · rule · count passing · ties · anomalies
5. If results cluster at an edge — keep the boundary, deliver the list, **flag the clustering as a
   possible domain transition**, and do not present it as a clean target set
6. Present as a **caution/triage list**, not an exclusion list

**Still to decide (Jakub's call, per her delegation):** the cut-off value and its justification.
That is the one genuinely open item, and it must be written down before the ranking is looked at.
