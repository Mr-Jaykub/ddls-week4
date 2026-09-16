# p53 model-confidence screen

## Answer first

Do not send the 22 flagged positions to the chemist as a clean target set. Under the declared screen, residues 94–312 produce a caution/triage list, but 20 of the 22 flags are the continuous 293–312 tail of the requested range. The folded core, residues 94–292, is uniformly well modelled overall; only residues 183 and 185 fall below pLDDT 70.00. The immediate recommendation is to treat 293–312 as a boundary/linker warning and validate the isolated 183/185 result before using either as a fixed geometric anchor.

The chemist should use the list to avoid relying on these coordinates without additional evidence—not to automatically exclude the residues. The app’s **Headline answer**, **Confidence matching the claim**, **Interactive region screen**, and **Ranked caution / triage list** panels show this distinction directly.

## 1. The question

Dr. Margit Holló asked for a residue-level caution list, in her terms: screen residues **94–312** for unusually poor model-assigned values, report the exact residue, amino-acid identity, value, and rank, and apply one reproducible cutoff. The decision is whether a residue should be treated as a reliable geometric anchor for the medicinal-chemistry collaborator’s design work.

The chemist acts on the result. The list changes which residues require validation before a design is built around their exact coordinates. It does not decide whether p53 is druggable, and it does not select biologically attractive core targets.

The proposed helix at residues **18–28** is outside this screen. It remains a separate validation project, not a fixed target.

## 2. Protein and files

The supplied protein is canonical wild-type human p53/TP53, UniProt **P04637**, **393 aa**. The supplied structure is an AlphaFold prediction in `data/p53_alphafold_model.cif`, one chain (`A`). The FASTA is `data/p53.fasta`.

The confidence companion is `data/p53_alphafold_pae.json`. It is not a per-residue confidence file. Its top-level container holds `predicted_aligned_error`, a **393 × 393** pairwise matrix, and `max_predicted_aligned_error`; its units are **Ångströms**. PAE is appropriate for relative placement of parts, not for this local residue screen. The app’s **PAE not used for this claim** note records why it was refused.

The model contains protein coordinates only. It contains no DNA, ligand, MDM2, ubiquitin, SUMO, or second p53 chain. It cannot establish a partner-bound complex, a tetramer interface, or a modified-state structure. The course fold service was never needed: the supplied sequence, mmCIF, and confidence files were sufficient for this screen.

## 3. The right confidence, stated plainly, before the answer

This is a local residue/fold claim. The matching confidence is local pLDDT from `_ma_qa_metric_local.metric_value` (metric 2) in the mmCIF, also represented by the atom B-factor column. It is **unitless**, on a **0–100** scale: higher means better local model confidence, so the worst residues rank smallest first.

The rule is local pLDDT **<70.00** for residues 94–312, ranked ascending, with ties retained. The AlphaFold Database bands recorded in `results/results.json` are: **<50 very low**, **50–<70 low**, **70–<90 confident**, and **≥90 very high**. Exactly 70.00 is not flagged by the strict rule. The threshold is a caution boundary, not an automatic exclusion rule.

The threshold was selected after the files had already been loaded and inspected. It is fixed and reproducible, but it was not prospectively pre-declared or blinded. The app’s **Confidence matching the claim** panel shows the per-residue chart, threshold line, and flagged points.

## 4. Structure check

The model sequence matches the FASTA and canonical P04637 residue-for-residue: **393 aa**, no overhang, and no differing positions. The model is one protein chain and a monomer. p53 functions as a tetramer, but this file does not contain that assembly.

There is no sequence mismatch to explain or invalidate the residue numbering. The relevant limitation is assembly, not identity: local pLDDT supports local residue placement in this monomer model, not how residues sit in the biological tetramer or in a partner complex. The app’s **Scope checks** panel displays this compact comparison.

## 5. The trap and the honest truth

The biggest risk is not that the chemist misreads the list. It is that the owner’s operational range **94–312 overruns the confidently folded DNA-binding core**. The screen then rediscovers that boundary: it calls the low-confidence transition/linker tail a set of poor residues, rather than revealing twenty independent problems inside the fold.

I tested the owner’s assumption about the numerical companion file by opening its schema. It contains pairwise PAE, not one value per residue. Her description of the companion file was wrong, and she needs to be told. Her own rule says that a schema gap or unsupported field must be reported back to her rather than replaced with an arbitrary column. The CIF supplied the permitted fallback: an explicitly defined local pLDDT field with one contiguous value per residue, verified against the sequence.

The honest answer to her direct location question is: the concentration is at **305–312**, not **94–100**. More precisely, the flagged boundary block is **293–312**, with all **20** residues below 70.00; **305–312** is its terminal eight-residue portion. The remaining two flags are isolated residues **183** and **185**. The 293–312 region has mean pLDDT **46.63** and **100.00%** below 70.00; residues 94–292 have mean pLDDT **95.29**, with **1.01%** below 70.00. The app’s region cards and positional table make the boundary effect visible.

The threshold is not the whole story. Within 94–292, the counts are **0** below 65.00, **2** below 70.00, and **6** below 80.00. The app’s cutoff slider exposes this dependence. Residue **186** is exactly 70.00 and appears only when the slider moves above 70.00. This is why the result must be described as triage, not as a biological boundary.

## 6. Answer and recommendation

The answer to the owner’s request is: **use the ranked list as a caution list, not an exclusion list or a target list.** At the declared `<70.00` rule there are **22** flags: **17 very low** (`<50`) and **5 low** (`50–<70`). There are no ties and no detected missing, null, non-numeric, duplicate, or out-of-range values.

Trust bounds are explicit:

- Trust the verified sequence mapping and the local pLDDT values as a screen of local model confidence.
- Trust the conclusion that 293–312 is poorly assigned relative to the folded core in this model.
- Do not trust the exact geometry of a flagged residue as a fixed design anchor without independent evidence.
- Do not infer a tetramer interface, DNA contact, MDM2 interface, ligand pocket, modification, or partner-induced conformation from this monomer model or from pLDDT alone.
- Do not treat high pLDDT as proof of a biological interaction or chemical tractability.

The chemist can proceed with caution around the well-modelled core, but any design depending on 183, 185, or 293–312 requires validation. The N-terminal 18–28 feature remains excluded and must not be folded into this shortlist.

## 7. Caveats and next steps

The one biological caveat to carry forward is the pLDDT dip around **183–187**. It co-locates with a UniProt Ser183 phosphorylation annotation, but the supplied files do not show that phosphorylation causes the dip. pLDDT reports local placement confidence for the modeled, unmodified wild-type chain; it does not establish the modification.

With more time, I would test this specific explanation using a modified-state structure or comparative structural/solution evidence before treating Ser183 or nearby residues as a mechanistically meaningful target feature.

## 8. AI use disclosure
Pi wrote the specification and `AGENTS.md` drafts, the analysis script, `results.json`, and the
FastAPI/3Dmol viewer including the interactive cutoff panel, and it found the UniProt Ser183
phosphorylation annotation unprompted while correctly refusing to claim it explains the
confidence dip. Claude was used as a review layer independent of the agent that produced the
results: it found that the companion PAE file contains no per-residue field at all — so the
owner's description of her own file was wrong — identified the areas worth probing and drafted
possible questions for my second round of interviewing, and separately recomputed the screen from
the mmCIF as a cross-check, which agreed with Pi's figures.

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
