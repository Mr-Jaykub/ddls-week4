# AlphaFold DB API — verified response shapes

Checked live against `P69905` (haemoglobin α, 142 aa) on 16 Sep 2026, AFDB **v6**.
Everything below is observed, not assumed.

## Endpoint

```
GET https://alphafold.ebi.ac.uk/api/prediction/<ACCESSION>
```

Returns a **JSON list**; the entry is element `[0]`.

### Fields that matter

| Field | Example | Note |
|---|---|---|
| `cifUrl` | `.../AF-P69905-F1-model_v6.cif` | mmCIF — **B-factor column holds pLDDT** (verified) |
| `pdbUrl` | `.../AF-P69905-F1-model_v6.pdb` | same model, PDB format |
| `plddtDocUrl` | `.../AF-P69905-F1-confidence_v6.json` | per-residue confidence |
| `paeDocUrl` | `.../AF-P69905-F1-predicted_aligned_error` | PAE matrix |
| `msaUrl` | `.../AF-P69905-F1-msa_v6.a3m` | the MSA the prediction used |
| `sequence` / `uniprotSequence` | `MVLSPADKTN…` | **the canonical UniProt sequence** |
| `sequenceStart` / `sequenceEnd` | 1 / 142 | residue range covered |
| `globalMetricValue` | `98.06` | **global mean pLDDT — the number NOT to quote** (see below) |
| `isComplex` | `false` | AFDB entries are **monomers** |
| `chainId` | `A` | single chain |
| `fractionPlddtVeryHigh` / `Confident` / `Low` / `VeryLow` | 0.993 / 0.0 / 0.007 / 0.0 | summary fractions |
| `organismScientificName`, `gene`, `uniprotDescription` | *Homo sapiens*, HBA1, … | identity cross-check |
| `toolUsed` | `AlphaFold Monomer v2.0 pipeline` | |

## Parsing

**mmCIF → per-residue pLDDT** (biotite):

```python
import requests, io
import biotite.structure.io.pdbx as pdbx

cif = requests.get(entry["cifUrl"], timeout=60).text
f   = pdbx.CIFFile.read(io.StringIO(cif))
arr = pdbx.get_structure(f, model=1, extra_fields=["b_factor"])
ca  = arr[arr.atom_name == "CA"]     # one per residue
plddt = ca.b_factor                  # verified: equals the confidence JSON
```

**Confidence JSON** — a dict, not a list:
```python
{"residueNumber": [...], "confidenceScore": [...], "confidenceCategory": [...]}
```

**PAE JSON** — a list of one dict:
```python
{"predicted_aligned_error": [[...]],        # (L, L) nested list
 "max_predicted_aligned_error": 31.75}
```
Indexing is `PAE[i][j]` = expected error in residue *i*'s position when the structure is
aligned on residue *j*. **Not symmetric.** For an interface, take the **off-diagonal block**
between the two chains' residue ranges, both directions.

## The trap, visible in this very example

For P69905:

```
per-residue pLDDT:  min = 65.38   mean = 98.06   max = 98.88
API globalMetricValue = 98.06     (== the mean, confirmed)
```

The global score the API hands you *is* the mean. A 98 mean is compatible with residues down
at 65. **If the owner's claim is about a specific region, the mean is not evidence — report
min and mean over exactly the claimed residues.**

## Consequences for this lab

1. **AFDB is monomer-only** (`isComplex: false`, single `chainId`). If the owner's protein is a
   functional dimer, the AFDB model *cannot* show the interface, and "surface" residues on it
   may be buried in the real assembly. Use the course GPU fold service for the complex.
2. **AFDB gives the canonical UniProt sequence.** If the owner has a mutant, truncation, or
   tagged construct, the AFDB model is not their protein. Always diff `entry["sequence"]`
   against the owner's FASTA.
3. **A monomer PAE cannot answer a binding question.** Inter-chain PAE only exists for a model
   that actually contains both chains.
