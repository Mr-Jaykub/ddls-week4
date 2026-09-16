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
- `data/p53_alphafold_pae.json`: pairwise predicted aligned error (PAE) matrix, 393 × 393. PAE is the matching confidence for claims about the relative placement of parts/domains.

## Exact claim and residues

The owner wants the core range **94–312** screened and ranked from worst-assigned to best-assigned, once the field definition confirms that smaller values mean weaker model assignment. The output must contain residue number, amino-acid identity, raw value, display value, rank, cutoff rule, and the number passing. Ties retain a shared rank; they must not be broken arbitrarily.

Residues **18–28** are explicitly out of scope for this ranking. They are the proposed N-terminal transactivation-region helix, including the biologically relevant MDM2-contact residues around 18–26 (especially Phe19, Trp23, and Leu26). The exact claim about that feature is not that the supplied model proves a fixed free-standing drug target: its existence and usable geometry require independent structural/solution evidence and partner-binding or mutation evidence. The AlphaFold model is a monomer and cannot establish an MDM2 interface or a stable isolated helix.

## Matching confidence

- For a local fold or region claim, report the relevant per-residue pLDDT, not the global average. The core fold claim is supported only to the extent shown by pLDDT for the residues concerned.
- For a claim about how domains or other parts sit together, report the corresponding PAE values. High pLDDT in two separate domains does not establish their relative geometry.
- For the N-terminal 18–28 feature, report its residue-level pLDDT before making any structural statement, and do not call it a fixed target without independent evidence. A partner-bound interface claim would require relevant partner/complex evidence; the supplied monomer and PAE cannot provide that.

The ranking direction is conditional until the field schema is inspected: if the selected residue-level field explicitly means model assignment/confidence with smaller values weaker, rank smallest first. The cutoff is not supplied by the owner; declare and justify it using only the 94–312 values, before selecting residues, and show how many pass. If no documented residue-level field maps cleanly to the canonical sequence, report that no defensible shortlist can be produced rather than substituting an arbitrary column.

## Checks that could break the conclusion

Verify FASTA/model identity, canonical numbering, chain identity, and 393-residue dimensions. Check JSON keys, array dimensions, indexing convention, units or lack thereof, missing/null/non-numeric values, duplicates, ties, and anomalous values. Preserve raw values; flag and explain anything excluded from ranking.

Keep 94–312 fixed after inspecting results. If poor values cluster at an edge such as 305–312, flag that positional pattern as a possible domain-transition issue, but do not redefine the boundary retrospectively. Do not infer a tetramer interface, DNA contact, or inter-domain pocket from this monomer. Do not use a whole-protein confidence average.

## Done means

A completed result has a reproducible, ranked table for 94–312 mapped to the verified canonical sequence; exact raw and displayed values; amino-acid identities; rank, ties, cutoff, rationale, and pass count; all schema/indexing/data-quality issues reported; and the N-terminal 18–28 feature clearly separated as a validation project. It states the confidence matching every structural claim and the monomer/assembly limitation. If the files cannot support the requested field, it plainly says no defensible residue-level shortlist can be produced.
