# Analysis specification

## Decision

Decide whether the supplied files support a defensible residue-level shortlist for the medicinal-chemistry collaborator. The immediate brief is to screen p53 residues **94–312 inclusive** for unusually poor model-assigned values, report exact positions and values, rank them, and apply a reproducible cutoff. This is a caution/triage list, not an automatic exclusion list or a list of biologically attractive targets.

The N-terminal feature is a separate validation project and must not be mixed into the shortlist. Do not commit chemistry to the N-terminal helix from the model alone.

## Protein and model

The protein is human p53/TP53, UniProt P04637: the canonical wild-type sequence, 393 residues, one polypeptide chain. The supplied AlphaFold model is predicted, not an experimental structure. The files contain one chain (`A`) and no DNA, MDM2, or second p53 copy: it is a monomeric model, not the biological tetramer or a partner assembly.

The sequence/model identity check must confirm that the FASTA and model are the same 393-residue canonical P04637 sequence before residue-level reporting. The supplied inventory records an exact sequence match.

## Files

- `data/p53.fasta`: canonical wild-type TP53/P04637 sequence, 393 aa.
- `data/p53_alphafold_model.cif`: AlphaFold mmCIF coordinates for chain A, residues 1–393. The mmCIF defines local pLDDT in `_ma_qa_metric_local`; pLDDT is also in the atom `_atom_site.B_iso_or_equiv` B-factor column. This is local confidence, not experimental measurement.
- `data/p53_alphafold_pae.json`: a top-level list containing one object with `predicted_aligned_error` (a 393 × 393 pairwise matrix) and `max_predicted_aligned_error` (a scalar). It is pairwise predicted aligned error (PAE), in Ångströms, not a per-residue confidence file. The owner's belief that it contains residue-level values is incorrect. PAE is the matching confidence for claims about the relative placement of parts/domains; local pLDDT for residue-level claims comes from the mmCIF.

## Exact claim and residues

The owner wants the core range **94–312** screened and ranked from worst-assigned to best-assigned, once the field definition confirms that smaller values mean weaker model assignment. The output must contain residue number, amino-acid identity, raw value, display value, rank, cutoff rule, and the number passing. Ties retain a shared rank; they must not be broken arbitrarily.

Residues **18–28** are explicitly out of scope for this ranking. They are the proposed N-terminal transactivation-region helix, including the biologically relevant MDM2-contact residues around 18–26 (especially Phe19, Trp23, and Leu26). The exact claim about that feature is not that the supplied model proves a fixed free-standing drug target: its existence and usable geometry require independent structural/solution evidence and partner-binding or mutation evidence. The AlphaFold model is a monomer and cannot establish an MDM2 interface or a stable isolated helix.

## Matching confidence

- For a local fold or region claim, report the relevant per-residue pLDDT, not the global average. The core fold claim is supported only to the extent shown by pLDDT for the residues concerned.
- For a claim about how domains or other parts sit together, report the corresponding PAE values. High pLDDT in two separate domains does not establish their relative geometry.
- For the N-terminal 18–28 feature, report its residue-level pLDDT before making any structural statement, and do not call it a fixed target without independent evidence. A partner-bound interface claim would require relevant partner/complex evidence; the supplied monomer and PAE cannot provide that.

The field definition has been verified: the mmCIF declares metric 2 as local pLDDT, with one contiguous value per residue mapped to the 393-residue sequence. pLDDT is unitless on a 0–100 scale, with higher values indicating better local model confidence. Therefore the ranking direction is fixed: rank residues 94–312 by local pLDDT from smallest to largest, retaining shared ranks for ties. **Cutoff:** flag every residue in 94–312 with local pLDDT < 70.0, then rank flagged residues by ascending raw pLDDT. The 70.0 value is a conventional, interpretable middle caution threshold, not a value statistically derived from this dataset, experimentally calibrated, or biologically optimal. A threshold of 65 would flag only more extreme low-confidence cases; 80 would be more conservative and flag more borderline cases. The files had already been loaded and inspected before 70.0 was selected, so it is a fixed, reproducible post-inspection threshold—not a prospectively pre-declared or blinded cutoff. Do not describe it as pre-declared. This is a caution/triage threshold, not an automatic exclusion rule; report zero passing residues explicitly if none pass. Show how many pass. The JSON PAE file is pairwise and is not a substitute for local pLDDT: do not compute or use PAE row/column means, minima, maxima, or any other per-residue summary for this shortlist. Use PAE only for claims about relative placement of residues or parts.

## Checks that could break the conclusion

Verify FASTA/model identity, canonical numbering, chain identity, and 393-residue dimensions. Check the PAE JSON's actual top-level/container schema, matrix dimensions, indexing convention, units, missing/null/non-numeric values, duplicates, and anomalous values. Record that the owner's initial description of the PAE file was incorrect and that the file's contents were checked before selecting the cutoff. Preserve raw values; flag and explain anything excluded from ranking. Never derive the shortlist from the PAE matrix or from any row/column aggregation of it; if local pLDDT cannot be loaded from the mmCIF, stop and report that no defensible residue-level shortlist can be produced.

Keep 94–312 fixed after inspecting results. If poor values cluster at an edge such as 305–312, flag that positional pattern as a possible domain-transition issue, but do not redefine the boundary retrospectively. Do not infer a tetramer interface, DNA contact, or inter-domain pocket from this monomer. Do not use a whole-protein confidence average.

## Done means

A completed result has a reproducible, ranked table for 94–312 mapped to the verified canonical sequence; exact raw and displayed values; amino-acid identities; rank, ties, cutoff, rationale, pass count, and cutoff provenance. It must state that the `< 70.0` cutoff was selected after the files had already been loaded and inspected, so it is not prospectively pre-declared. All schema/indexing/data-quality issues must be reported; the N-terminal 18–28 feature must remain clearly separated as a validation project. It states the confidence matching every structural claim and the monomer/assembly limitation. If the files cannot support the requested field, it plainly says no defensible residue-level shortlist can be produced.
