# Data bundle — factual inventory

**Run 16 Sep 2026, 13:20–13:25, while the interview was in progress.**

> **Read order discipline:** this file was deliberately *not* consulted when drafting
> `interview-summary.md`. That summary records what the owner **claimed**, from the transcript
> alone. This file is what is **actually true**. The gap between the two is the finding.

Everything below is measured from the supplied files. No interpretation of the owner's claim,
because the interview had not finished when this was written.

---

## Files

| File | Size | Contents |
|---|---|---|
| `data/p53.fasta` | 474 B | TP53, *Homo sapiens*, UniProt **P04637**, **393 aa** |
| `data/p53_alphafold_model.cif` | 356 KB | mmCIF, **1 chain (A)**, 3,060 atoms, **393 residues**, resid 1–393 |
| `data/p53_alphafold_pae.json` | 416 KB | PAE matrix **393 × 393**, max_pae 31.75 |

*(The bundle unpacked into a `data 2/` subfolder — Safari duplicate-name rename. Flattened to
`data/`, stray `.DS_Store` removed.)*

## Structure check — PASSES on sequence, but note what that means

```
FASTA length          393
model CIF length      393
model == FASTA        True
UniProt P04637 == model   True      (fetched live from rest.uniprot.org)
```

The model **is** the file's FASTA, and both **are the canonical wild-type UniProt sequence** —
verified residue-by-residue, zero differences.

**So the model contains no mutation of any kind.** All six classic cancer hotspots are
wild-type:

| Position | Observed | Wild-type | pLDDT |
|---|---|---|---|
| 175 | R | R | 96.6 |
| 245 | G | G | 94.8 |
| 248 | R | R | 97.2 |
| 249 | R | R | 97.8 |
| **273** | **R** | **R** | **98.6** |
| 282 | R | R | 97.5 |

⚠️ Note the shape of the hazard: these residues carry the **highest confidence in the whole
protein** (94–98.6). A hotspot position looks maximally trustworthy while being the wrong
residue if the owner works on a mutant. Per the lecture (§7), a point mutation barely changes
the MSA, so it barely changes the prediction — AlphaFold cannot model the mutant anyway.

## Assembly state

**Monomer.** One chain, `chain_id = A`. No second copy, no DNA, no partner.

Biologically, **p53 is obligate-tetrameric** — the tetramerisation domain (323–356) mediates it,
and sequence-specific DNA binding is a tetramer function. A single-chain model cannot show the
tetramer interface, so residues that are "surface" here may be buried in the real assembly.

## Per-residue confidence (pLDDT), by domain

Overall: **min 32.8 · mean 75.1 · max 98.7**

| Domain | Residues | min | mean | % < 70 |
|---|---|---|---|---|
| TAD1 (transactivation) | 1–40 | 34.2 | 50.4 | 85% |
| TAD2 / proline-rich | 41–93 | 35.2 | **46.9** | **100%** |
| **DNA-binding domain** | 94–292 | 68.4 | **95.3** | 1% |
| linker | 293–322 | 38.9 | **46.4** | **100%** |
| **Tetramerisation domain** | 323–356 | 53.1 | **89.1** | 6% |
| C-terminal regulatory | 357–393 | 32.8 | **43.4** | **100%** |

**40% of all residues sit below pLDDT 70. 52% sit above 90.**

This is a bimodal protein: two well-predicted folded domains joined by long, genuinely
disordered segments. **The global mean of 75.1 describes no part of this molecule.** It is the
average of ~95 and ~45.

Per the lecture (§6b), low pLDDT here is not model failure — p53's TAD, PRD, linker and
C-terminal region are *known* intrinsically disordered regions. The model is correctly
reporting disorder.

## Pairwise confidence (PAE), mean Å between domain blocks

| | TAD1 | PRD | DBD | linker | TET | Cterm |
|---|---|---|---|---|---|---|
| **TAD1** | 15.9 | 27.2 | 30.9 | 30.4 | 29.5 | 29.9 |
| **PRD** | 27.4 | 19.1 | 29.4 | 30.7 | 30.4 | 30.9 |
| **DBD** | 28.9 | 25.0 | **3.6** | 21.8 | 20.3 | 27.7 |
| **linker** | 30.3 | 30.8 | 28.9 | 14.9 | 26.0 | 28.9 |
| **TET** | 27.9 | 28.9 | 21.3 | 20.5 | **3.8** | 24.2 |
| **Cterm** | 29.5 | 30.8 | 30.5 | 28.2 | 27.3 | 16.2 |

**The critical row/column pair:**

```
DBD internal   mean PAE =  3.6 Å    confident fold
TET internal   mean PAE =  3.8 Å    confident fold
DBD <-> TET    mean PAE = 20.3 Å    (max possible 31.75) — essentially no information
```

Both domains are individually well-folded **and their positions relative to each other are
unknown.** They float on disordered linkers.

**Consequence:** any claim about the *spatial relationship* between two domains — a pocket
formed between them, a distance, a composite binding surface, an interface — is unsupported by
this model, **even though both domains have pLDDT > 89.** This is exactly the
per-residue-vs-pairwise distinction from lecture §6: pLDDT answers "is this residue placed
well *locally*"; PAE answers "are these two things placed well *relative to each other*".

## What this model can and cannot support

**Can support** (with stated bounds):
- The fold of the DNA-binding domain, 94–292 (mean pLDDT 95.3, internal PAE 3.6 Å)
- The fold of the tetramerisation domain, 323–356 (mean 89.1, internal PAE 3.8 Å)
- Positions of residues *within* either of those domains
- A positive statement that 1–93, 293–322 and 357–393 are disordered

**Cannot support:**
- Anything about a mutant — the model is wild-type at every position
- Any inter-domain geometry (DBD↔TET PAE 20.3 Å)
- Any tetramer interface — the model is a monomer
- Any DNA contact — no DNA in the model
- Any structure in the TAD/PRD/linker/C-term — those are correctly predicted as disordered
- Any claim resting on the global mean pLDDT of 75.1

## Open until the interview lands

Which of these is *the* trap depends entirely on what the owner claims they want to trust.
At least four distinct traps are live in this file. Do not pre-commit — match the trap to the
claim.
