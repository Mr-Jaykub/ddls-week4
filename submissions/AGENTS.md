# AGENTS.md

## Environment and operating rules

- Use `uv` for the Python environment: create it with `uv venv`.
- Run all Python commands with `uv run`; this is the cross-platform command convention.
- The supplied data lives in `data/`; write analysis outputs only to `results/`.
- Before making a big change, commit the current state. Commit again whenever something starts working. Use short, clear commit messages.
- Never commit `.env` or any secret. `.env` is local-only and must remain ignored; before every commit, run `git status` and verify that `.env` is not staged. If it is tracked or staged, untrack it with `git rm --cached .env` (without deleting the local file), confirm `.gitignore` contains `.env`, and do not commit until the working tree is safe.

## Data loading and confidence

The bundle contains the canonical human TP53/p53 (UniProt P04637) sequence in `data/p53.fasta`, an AlphaFold mmCIF model in `data/p53_alphafold_model.cif`, and a PAE matrix in `data/p53_alphafold_pae.json`.

- Load the sequence from the FASTA and verify its length and residue numbering.
- Load the structure from the mmCIF. It is one chain (`A`) with 393 residues. Local pLDDT is explicitly defined in the mmCIF `_ma_qa_metric_local` loop; it is also represented in the atom B-factor (`_atom_site.B_iso_or_equiv`) column. Do not confuse the global pLDDT with per-residue values.
- Load PAE from the JSON and inspect its schema and dimensions before using it. PAE is the confidence measure for how parts of the model sit relative to one another; pLDDT is the matching measure for local residue/fold claims.

Never report an answer about a structure without first reporting the confidence that matches the claim **and** confirming that the model is actually this protein. For a fold or region, report per-residue pLDDT. For how separate parts sit together, report PAE. Also state model scope and assembly limitations: this file is a monomer, not a p53 tetramer or a p53–partner complex.

Do not treat a visual feature as experimentally established, and do not use a whole-protein average as a substitute for residue-level confidence. Preserve raw values and flag schema, indexing, missing, duplicate, or anomalous data.
