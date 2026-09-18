# p53 model-confidence screen

## Answer first

Do not send the 22 flagged positions to the chemist as a clean target set. Under the declared screen, residues 94–312 produce a caution/triage list, but 20 of the 22 flags are the continuous 293–312 tail of the requested range. The folded core, residues 94–292, is uniformly well modelled overall; only residues 183 and 185 fall below pLDDT 70.00. The immediate recommendation is to treat 293–312 as a boundary/linker warning and validate the isolated 183/185 result before using either as a fixed geometric anchor.

The chemist should use the list to avoid relying on these coordinates without additional evidence—not to automatically exclude the residues. The app’s **Headline answer**, **Confidence matching the claim**, **Interactive region screen**, and **Ranked caution / triage list** panels show this distinction directly.

Two independent measures agree on where this turns. Local pLDDT says 293–312 is locally uncertain; PAE says the model does not know where that segment sits relative to the core at all. **The confident fold ends near residue 292, not 312.** Where the screening range ends is therefore a boundary decision for the data owner, not a technical finding of mine—section 5 states the cost of each choice.

## 1. The question

Dr. Margit Holló asked for a residue-level caution list, in her terms: screen residues **94–312** for unusually poor model-assigned values, report the exact residue, amino-acid identity, value, and rank, and apply one reproducible cutoff. The decision is whether a residue should be treated as a reliable geometric anchor for the medicinal-chemistry collaborator’s design work.

The chemist acts on the result. The list changes which residues require validation before a design is built around their exact coordinates. It does not decide whether p53 is druggable, and it does not select biologically attractive core targets.

The proposed helix at residues **18–28** is outside this screen and outside the ranking. It remains a separate validation project, not a fixed target. Section 7 reports its residue-level pLDDT, because this report should not make a structural statement about that segment without first stating the confidence that matches it.

## 2. Protein and files

The supplied protein is canonical wild-type human p53/TP53, UniProt **P04637**, **393 aa**. The supplied structure is an AlphaFold prediction in `data/p53_alphafold_model.cif`, one chain (`A`). The FASTA is `data/p53.fasta`.

The confidence companion is `data/p53_alphafold_pae.json`. It is not a per-residue confidence file. Its top-level container is a one-element list holding `predicted_aligned_error`, a **393 × 393** pairwise matrix, and `max_predicted_aligned_error` (**31.75**); its units are **Ångströms** and the matrix is **not symmetric**, so row-to-column order carries meaning. Values are stored rounded to whole Ångströms.

PAE is appropriate for relative placement of parts, not for this local residue screen. It therefore contributes **nothing** to the ranking: no row mean, column mean, minimum, maximum, or any other per-residue reduction of this matrix was used to select or order a single flagged residue. It is used once, in section 6, for a placement question that local pLDDT cannot answer. The app’s PAE note states both halves of that distinction.

The model contains protein coordinates only. It contains no DNA, ligand, MDM2, ubiquitin, SUMO, or second p53 chain. It cannot establish a partner-bound complex, a tetramer interface, or a modified-state structure. The course fold service was never needed: the supplied sequence, mmCIF, and confidence files were sufficient for this screen.

## 3. The right confidence, stated plainly, before the answer

This is a local residue/fold claim. The matching confidence is local pLDDT from `_ma_qa_metric_local.metric_value` (metric 2) in the mmCIF, also represented by the atom B-factor column; section 9 reports the comparison of those two columns. It is **unitless**, on a **0–100** scale: higher means better local model confidence, so the worst residues rank smallest first.

The rule is local pLDDT **<70.00** for residues 94–312, ranked ascending, with ties retained. The AlphaFold Database bands recorded in `results/results.json` are: **<50 very low**, **50–<70 low**, **70–<90 confident**, and **≥90 very high**. Exactly 70.00 is not flagged by the strict rule. The threshold is a caution boundary, not an automatic exclusion rule.

The threshold was selected after the files had already been loaded and inspected. It is fixed and reproducible, but it was not prospectively pre-declared or blinded. The app’s **Confidence matching the claim** panel shows the per-residue chart, threshold line, and flagged points.

## 4. Structure check

The model sequence matches the FASTA and canonical P04637 residue-for-residue: **393 aa**, no overhang, and no differing positions. The model is one protein chain and a monomer. p53 functions as a tetramer, but this file does not contain that assembly.

There is no sequence mismatch to explain or invalidate the residue numbering. The relevant limitation is assembly, not identity: local pLDDT supports local residue placement in this monomer model, not how residues sit in the biological tetramer or in a partner complex. The app’s **Scope checks** panel displays this compact comparison.

## 5. The boundary, and whose decision it is

The biggest risk is not that the chemist misreads the list. It is that the owner’s operational range **94–312 overruns the confidently folded DNA-binding core**. The screen then rediscovers that boundary: it calls the low-confidence transition/linker tail a set of poor residues, rather than revealing twenty independent problems inside the fold.

That is a finding about the range, so the decision belongs to the owner, not to me. I screened all **219** residues exactly as she specified and did not move the boundary after seeing the results. What the files support is this: **the confidently folded core ends near residue 292.** Her two options, with the cost of each stated:

- **Keep 94–312.** The caution list stands at 22 residues, but 20 of them describe the end of her own range rather than defects inside the fold. The list is then mostly a boundary report, and must be read as one.
- **Screen 94–292 instead.** The caution list becomes **2** residues, 183 and 185, both borderline—and both disappear at a cutoff of 65.00. The honest summary is then that the model is confident about almost the entire folded core.

Either is defensible. What is not defensible is presenting the 22-residue list as twenty-two independent problems in the fold. The boundary must be chosen deliberately and stated, not inherited.

I tested the owner’s assumption about the numerical companion file by opening its schema. It contains pairwise PAE, not one value per residue. Her description of the companion file was wrong, and she needs to be told. Her own rule says that a schema gap or unsupported field must be reported back to her rather than replaced with an arbitrary column. The CIF supplied the permitted fallback: an explicitly defined local pLDDT field with one contiguous value per residue, verified against the sequence.

The honest answer to her direct location question is: the concentration is at **305–312**, not **94–100**. More precisely, the flagged boundary block is **293–312**, with all **20** residues below 70.00; **305–312** is its terminal eight-residue portion. The remaining two flags are isolated residues **183** and **185**. The 293–312 region has mean pLDDT **46.63** and **100.00%** below 70.00; residues 94–292 have mean pLDDT **95.29**, with **1.01%** below 70.00. The app’s region cards and positional table make the boundary effect visible.

The threshold is not the whole story. Within 94–292, the counts are **0** below 65.00, **2** below 70.00, and **6** below 80.00. The app’s cutoff slider exposes this dependence. Residue **186** is exactly 70.00 and appears only when the slider moves above 70.00. This is why the result must be described as triage, not as a biological boundary.

## 6. Relative placement: what PAE says about 293–312

Local pLDDT answers “is this residue placed well?” It cannot answer “does this segment sit reliably against the core?” That is a relative-placement question, and PAE is the matching confidence. The matrix was in the owner’s own file. Block means across regions are a placement statement, not a per-residue reduction, so this use does not breach the rule in section 2.

| Block (rows → columns) | Pairs | Mean PAE (Å) | Median (Å) |
|---|---|---|---|
| 94–292 against itself | 39,601 | **3.60** | 3 |
| 293–312 against 94–292 | 3,980 | **28.10** | 30 |
| 94–292 against 293–312 | 3,980 | 19.56 | 22 |
| 293–312 against itself | 400 | 11.83 | 10 |

Within the folded core the model places residues confidently relative to one another. Between the tail and that core the error is **28.10 Å** against a declared maximum of **31.75 Å**—that is the top of the scale this file can express. The correct reading is not that the model places the tail badly; it is that **the model does not know where the tail goes**.

This matters because it is independent corroboration. pLDDT and PAE answer different questions from different parts of the file, and both turn at residue 293. The boundary in section 5 does not rest on one metric or one threshold.

The limits still hold. PAE describes this monomer model only. It cannot establish an MDM2 interface, a tetramer interface, a DNA contact, or a ligand pocket, and a high-confidence block is not evidence of a biological interaction.

## 7. The N-terminal 18–28 segment, measured

The owner came to this work wanting to point the chemist at a helix she had seen at residues **18–28**. That segment is excluded from the ranking and stays excluded. But excluding it from the shortlist is not a reason to say nothing measurable about it, and this report should not describe it structurally without stating the matching confidence first.

Under the identical field and the identical rule applied to the core:

| | Value |
|---|---|
| Residues | 11 (18–28) |
| Mean local pLDDT | **68.88** |
| Worst residue | **57.66** (Glu28) |
| Best residue | 77.12 (Leu25) |
| Below 70.00 | **5 of 11** |
| Folded core 94–292, for comparison | 95.29 |

The MDM2-contact residues she named score **Phe19 61.56**, **Trp23 73.44**, **Leu26 64.25**. Two of the three fall below the same 70.00 line she set for the core.

PAE adds the placement half: from 18–28 to the core the mean is **30.76 Å**, essentially the ceiling of the scale. The model does not place this segment against the rest of the chain either.

**The verdict, stated plainly: this model does not support residues 18–28 as a rigid drug target.** That is consistent with what the owner herself said once asked—that the region is disordered in solution until it engages MDM2. It is not proof that the helix never forms, and the numbers here are not evidence about MDM2 binding in either direction: this file is a monomer and contains no MDM2. The segment needs independent structural or solution evidence, plus partner-binding or mutation data, before any chemistry is committed to it. Comparison against the core is offered for scale only; the `<70.00` cutoff was declared for 94–312 and is not applied to this segment as a pass/fail rule.

## 8. Answer and recommendation

The answer to the owner’s request is: **use the ranked list as a caution list, not an exclusion list or a target list.** At the declared `<70.00` rule there are **22** flags: **17 very low** (`<50`) and **5 low** (`50–<70`). There are no ties and no detected missing, null, non-numeric, duplicate, or out-of-range values.

Trust bounds are explicit:

- Trust the verified sequence mapping and the local pLDDT values as a screen of local model confidence.
- Trust the conclusion that 293–312 is locally poorly assigned in this model (pLDDT), **and** that the model does not resolve where it sits relative to the folded core (PAE, section 6). These are two separate claims from two separate fields; neither is evidence for the other.
- Do not trust the exact geometry of a flagged residue as a fixed design anchor without independent evidence.
- Do not infer a tetramer interface, DNA contact, MDM2 interface, ligand pocket, modification, or partner-induced conformation from this monomer model or from pLDDT alone.
- Do not treat high pLDDT as proof of a biological interaction or chemical tractability.

The chemist can proceed with caution around the well-modelled core, but any design depending on 183, 185, or 293–312 requires validation. The N-terminal 18–28 feature remains excluded and must not be folded into this shortlist.

## 9. Verification

The shortlist should not rest on one script or one parser, so it was checked three ways before this report was written. All three are reproducible from the shipped files and recorded in `results/results.json`.

**The confidence field was read twice, by two different routes.** The mmCIF carries per-residue pLDDT in the `_ma_qa_metric_local` loop *and* in the `_atom_site.B_iso_or_equiv` atom B-factor column. Both were parsed independently and compared residue by residue: **393 of 393 agree, zero differences**, range 32.78–98.69, and no residue carries inconsistent B-factors across its atoms. A mis-parsed column is the failure mode that would silently corrupt the entire ranking, and this rules it out.

**The screen was reimplemented independently.** A second implementation (`notes/verification/claude_crosscheck.py`) was written separately from `screen.py`, using a different parser and different libraries, and returned the **same 22 flagged residues, the same ranking, and the same values**. This is the strongest evidence in the analysis: agreement between two implementations is a much harder thing to fake than one script run twice.

**Identity was confirmed against the sequence.** The model sequence matches the bundled FASTA and canonical P04637 residue-for-residue at 393 residues, so the residue numbers in the table refer to the residues the owner means.

One data-quality observation, recorded rather than corrected. PAE values are stored rounded to whole Ångströms, so three cells—**(7, 218)**, **(9, 218)**, and **(43, 144)**—hold **32**, exceeding the file’s own declared maximum of 31.75 by 0.25. None falls inside the 94–292 core block, so no figure reported in section 6 depends on them. There are no null, non-numeric, or missing values in either file.

## 10. Caveats and next steps

The one biological caveat to carry forward is the pLDDT dip around **183–187**. It co-locates with a UniProt Ser183 phosphorylation annotation, but the supplied files do not show that phosphorylation causes the dip. pLDDT reports local placement confidence for the modeled, unmodified wild-type chain; it does not establish the modification.

With more time, I would test this specific explanation using a modified-state structure or comparative structural/solution evidence before treating Ser183 or nearby residues as a mechanistically meaningful target feature.

## 11. AI use disclosure
Pi wrote the specification and `AGENTS.md` drafts, the analysis script, `results.json`, and the
FastAPI/3Dmol viewer including the interactive cutoff panel, and it found the UniProt Ser183
phosphorylation annotation unprompted while correctly refusing to claim it explains the
confidence dip. Claude was used as a review layer independent of the agent that produced the
results: it found that the companion PAE file contains no per-residue field at all — so the
owner's description of her own file was wrong — and identified the areas worth probing and drafted
possible questions for my second round of interviewing. It also reimplemented the screen from the
mmCIF independently of `screen.py`; that cross-check, and the two-column confidence check beside
it, are reported as results in section 9 rather than as a credit, because agreement between two
independent implementations is the main reason to believe the table.

I ran the manual review gate on both drafts against the transcript and the files, chose which of
the drafted questions to put to the data owner, and decided the cutoff, the deviation from the
owner's "justify from the core values" phrasing, and which biological caveat to report. The cutoff
was fixed after the files had been inspected, so it is reproducible but not blinded. I did not
read `screen.py` line by line — I checked its outputs against the source files rather than its
logic; I took the AlphaFold confidence-band boundaries from both agents without consulting EBI's
own documentation; and I accepted the owner's statement that 94–312 is the canonical DNA-binding
core without checking it against a paper or construct record, which matters because the finding
concerns exactly where that range ends.
_To be completed by the author._
