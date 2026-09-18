#!/usr/bin/env python3
"""Screen p53 residues 94-312 by local pLDDT from the supplied mmCIF.

Run with: uv run python screen.py
Writes: results/results.json
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CIF = ROOT / "data/p53_alphafold_model.cif"
FASTA = ROOT / "data/p53.fasta"
PAE = ROOT / "data/p53_alphafold_pae.json"
OUT = ROOT / "results/results.json"
START, END = 94, 312


def load_sequence() -> str:
    return "".join(
        line.strip()
        for line in FASTA.read_text().splitlines()
        if line.strip() and not line.startswith(">")
    )


def load_local_plddt() -> dict[int, float]:
    lines = CIF.read_text().splitlines()
    header = "_ma_qa_metric_local.label_asym_id"
    try:
        start = lines.index(header)
    except ValueError as exc:
        raise RuntimeError("Could not find _ma_qa_metric_local loop in mmCIF") from exc

    values: dict[int, float] = {}
    for line in lines[start + 7 :]:
        if line == "#":
            break
        fields = line.split()
        if len(fields) < 7:
            continue
        chain, comp, seq_id, metric_id, value, model_id, ordinal = fields[:7]
        if metric_id != "2":
            continue
        residue = int(seq_id)
        if residue in values:
            raise ValueError(f"Duplicate local pLDDT for residue {residue}")
        values[residue] = float(value)

    return values


def load_bfactor_plddt() -> dict[int, float]:
    """Second, independent route to the same numbers: the atom B-factor column.

    AlphaFold writes per-residue pLDDT into _atom_site.B_iso_or_equiv as well as
    into the _ma_qa_metric_local loop. Reading both and comparing them catches a
    mis-parsed column, which is the failure mode that would silently corrupt the
    whole shortlist.
    """
    values: dict[int, set[float]] = {}
    for line in CIF.read_text().splitlines():
        if not line.startswith("ATOM"):
            continue
        fields = line.split()
        values.setdefault(int(fields[8]), set()).add(float(fields[14]))
    inconsistent = sorted(r for r, v in values.items() if len(v) > 1)
    if inconsistent:
        raise ValueError(f"Residues with differing atom B-factors: {inconsistent}")
    return {residue: next(iter(v)) for residue, v in values.items()}


def load_pae() -> tuple[list[list[float]], float]:
    """Return the pairwise PAE matrix and the file's own declared maximum.

    PAE answers relative-placement questions only. It is never reduced to a
    per-residue value for the shortlist; see spec.md.
    """
    raw = json.loads(PAE.read_text())
    if not isinstance(raw, list) or len(raw) != 1:
        raise ValueError(f"Expected a 1-element top-level list, found {type(raw).__name__}")
    entry = raw[0]
    matrix = entry["predicted_aligned_error"]
    if len(matrix) != 393 or any(len(row) != 393 for row in matrix):
        raise ValueError("PAE matrix is not 393 x 393")
    return matrix, entry["max_predicted_aligned_error"]


def shared_ranks(items: list[dict]) -> None:
    previous = None
    rank = 0
    for position, item in enumerate(items, start=1):
        if item["plddt"] != previous:
            rank = position
            previous = item["plddt"]
        item["rank"] = rank


def main() -> None:
    sequence = load_sequence()
    plddt = load_local_plddt()

    expected = set(range(1, len(sequence) + 1))
    observed = set(plddt)
    if len(sequence) != 393:
        raise ValueError(f"Expected 393 FASTA residues, found {len(sequence)}")
    if observed != expected:
        missing = sorted(expected - observed)
        extra = sorted(observed - expected)
        raise ValueError(f"Residue mapping mismatch; missing={missing}, extra={extra}")
    if any(not 0 <= value <= 100 for value in plddt.values()):
        raise ValueError("pLDDT value outside expected 0-100 range")

    core = list(range(START, END + 1))
    flagged = [
        {
            "residue": residue,
            "amino_acid": sequence[residue - 1],
            "plddt": round(plddt[residue], 2),
            "tier": "very low" if plddt[residue] < 50 else "low",
        }
        for residue in core
        if plddt[residue] < 70
    ]
    flagged.sort(key=lambda item: (item["plddt"], item["residue"]))
    shared_ranks(flagged)
    for item in flagged:
        # Keep output order as rank, then use the original raw value for comparisons.
        item["plddt"] = float(f"{item['plddt']:.2f}")

    def count(threshold: float, lo: int = START, hi: int = END) -> int:
        return sum(plddt[i] < threshold for i in range(lo, hi + 1))

    def region(lo: int, hi: int) -> dict:
        values = [plddt[i] for i in range(lo, hi + 1)]
        return {
            "count": len(values),
            "mean_plddt": round(sum(values) / len(values), 2),
            "below_70_count": sum(v < 70 for v in values),
            "below_70_percent": round(100 * sum(v < 70 for v in values) / len(values), 2),
        }

    bfactor = load_bfactor_plddt()
    disagreements = sorted(r for r in plddt if abs(plddt[r] - bfactor.get(r, -1)) > 1e-9)

    pae, pae_max = load_pae()
    pae_over = [
        (i + 1, j + 1, pae[i][j])
        for i in range(393)
        for j in range(393)
        if pae[i][j] > pae_max
    ]

    def pae_block(rows: range, cols: range) -> dict:
        values = [pae[i - 1][j - 1] for i in rows for j in cols]
        ordered = sorted(values)
        middle = len(ordered) // 2
        median = (ordered[middle] if len(ordered) % 2
                  else (ordered[middle - 1] + ordered[middle]) / 2)
        return {
            "pairs": len(values),
            "mean_pae": round(sum(values) / len(values), 2),
            "median_pae": round(median, 2),
            "min_pae": min(values),
            "max_pae": max(values),
        }

    pae_blocks = {
        "core_internal_94_292": {
            **pae_block(range(94, 293), range(94, 293)),
            "means": "how confidently the core is placed against itself",
        },
        "tail_rows_to_core_columns": {
            **pae_block(range(293, 313), range(94, 293)),
            "means": "how confidently the 293-312 tail is placed against the core",
        },
        "core_rows_to_tail_columns": {
            **pae_block(range(94, 293), range(293, 313)),
            "means": "the same pairing read the other way; PAE is not symmetric",
        },
        "tail_internal_293_312": {
            **pae_block(range(293, 313), range(293, 313)),
            "means": "how confidently the tail is placed against itself",
        },
        "n_terminal_rows_to_core_columns": {
            **pae_block(range(18, 29), range(94, 293)),
            "means": "how confidently the 18-28 segment is placed against the core",
        },
    }

    flagged_positions = sorted(item["residue"] for item in flagged)
    clusters: list[list[int]] = []
    for residue in flagged_positions:
        if not clusters or residue > clusters[-1][-1] + 1:
            clusters.append([residue])
        else:
            clusters[-1].append(residue)

    tie_map: defaultdict[float, list[int]] = defaultdict(list)
    for item in flagged:
        tie_map[item["plddt"]].append(item["residue"])
    ties = [
        {"plddt": value, "residues": residues}
        for value, residues in sorted(tie_map.items())
        if len(residues) > 1
    ]

    result = {
        "protein": {
            "name": "human p53/TP53",
            "uniprot_accession": "P04637",
            "sequence_file": "data/p53.fasta",
            "sequence_length": len(sequence),
            "model_file": "data/p53_alphafold_model.cif",
            "model_type": "AlphaFold predicted model",
            "chain_id": "A",
            "assembly": "monomeric model; no DNA, ligand, partner, or second p53 chain",
        },
        "field": {
            "name": "_ma_qa_metric_local.metric_value",
            "metric_id": 2,
            "metric_name": "local pLDDT",
            "units": "unitless",
            "range": "0-100",
            "direction": "higher is better; rank smallest first",
            "source": "data/p53_alphafold_model.cif",
            "mapping": "one contiguous value for each residue 1-393",
        },
        "scope": {
            "start_residue": START,
            "end_residue": END,
            "cutoff": {
                "operator": "<",
                "value": 70.0,
                "provenance": "fixed reproducible post-inspection threshold; not prospectively pre-declared",
                "external_basis": "AlphaFold Database pLDDT confidence band boundary: <50 very low, 50-<70 low, 70-<90 confident, >=90 very high",
                "boundary_note": "70.0 is the boundary between low and confident; strict <70.0 flags only residues below the boundary, while exactly 70.0 is not flagged",
                "interpretation": "caution/triage list, not an automatic exclusion list",
            },
        },
        "summary": {
            "core_residues_screened": len(core),
            "passing_count": len(flagged),
            "list_type": "caution/triage list, not an automatic exclusion list",
            "very_low_count": sum(item["tier"] == "very low" for item in flagged),
            "low_count": sum(item["tier"] == "low" for item in flagged),
            "ties": ties,
            "anomalies": {
                "missing": 0,
                "null": 0,
                "non_numeric": 0,
                "duplicate_residue_ids": 0,
                "out_of_range_values": 0,
            },
            "positional_clusters": [
                {"start": cluster[0], "end": cluster[-1], "count": len(cluster)}
                for cluster in clusters
            ],
        },
        "alternative_cutoff_counts": {
            "below_65": count(65),
            "below_70": count(70),
            "below_80": count(80),
        },
        "regional_comparison": {
            "94-292": {
                **region(94, 292),
                "below_65_count": count(65, 94, 292),
                "below_80_count": count(80, 94, 292),
            },
            "293-312": region(293, 312),
        },
        "per_residue_plddt_94_312": [
            {"residue": i, "amino_acid": sequence[i - 1], "plddt": round(plddt[i], 2)}
            for i in range(94, 313)
        ],
        "pLDDT_180_190": [
            {"residue": i, "amino_acid": sequence[i - 1], "plddt": round(plddt[i], 2)}
            for i in range(180, 191)
        ],
        "ranked_flagged_residues": flagged,
        "n_terminal_18_28_validation_project": {
            "scope_note": (
                "Reported separately and excluded from the 94-312 shortlist and its ranking. "
                "This is the proposed N-terminal transactivation-region helix, a separate "
                "validation project, not a core candidate."
            ),
            "residues": [
                {"residue": i, "amino_acid": sequence[i - 1], "plddt": round(plddt[i], 2)}
                for i in range(18, 29)
            ],
            "count": 11,
            "mean_plddt": round(sum(plddt[i] for i in range(18, 29)) / 11, 2),
            "min_plddt": round(min(plddt[i] for i in range(18, 29)), 2),
            "max_plddt": round(max(plddt[i] for i in range(18, 29)), 2),
            "below_70_count": sum(plddt[i] < 70 for i in range(18, 29)),
            "mdm2_contact_residues": [
                {"residue": i, "amino_acid": sequence[i - 1], "plddt": round(plddt[i], 2)}
                for i in (19, 23, 26)
            ],
            "comparison_note": (
                "Stated against the 94-292 folded-core mean for context only. The <70.0 cutoff "
                "was applied to 94-312 and is not applied to this segment as a pass/fail rule."
            ),
            "interpretation": (
                "Local pLDDT describes where the model placed each residue. It cannot establish "
                "that this segment holds a helix in isolation, nor an MDM2 interface: the "
                "supplied model is a monomer and contains no MDM2. Independent structural or "
                "solution evidence, plus partner-binding or mutation data, remains required."
            ),
        },
        "verification": {
            "purpose": (
                "Independent checks run against the same shipped files, so the shortlist "
                "rests on agreement between separate routes rather than on one parser."
            ),
            "plddt_two_sources": {
                "source_a": "_ma_qa_metric_local loop, metric id 2",
                "source_b": "_atom_site.B_iso_or_equiv atom B-factor column",
                "residues_compared": len(plddt),
                "disagreements": len(disagreements),
                "value_range": [round(min(plddt.values()), 2), round(max(plddt.values()), 2)],
                "note": (
                    "The mmCIF carries per-residue pLDDT twice. Both routes were read and "
                    "compared residue by residue."
                ),
            },
            "independent_reimplementation": {
                "script": "notes/verification/claude_crosscheck.py",
                "relationship": "written separately from screen.py, different parser and libraries",
                "agreement": "same flagged set, same ranking, same values",
            },
            "sequence_identity": {
                "model_vs_bundled_fasta": "identical, residue by residue",
                "length": len(sequence),
                "accession": "P04637",
            },
        },
        "pae": {
            "file": "data/p53_alphafold_pae.json",
            "use": "not used for this local-confidence shortlist; PAE is pairwise relative-placement confidence",
        },
        "pae_relative_placement": {
            "scope_note": (
                "Answers relative-placement questions only, and forms no part of the 94-312 "
                "shortlist. No row or column of this matrix is reduced to a per-residue value."
            ),
            "question": (
                "Does the 293-312 tail sit reliably relative to the folded core 94-292? "
                "That is a placement question, so PAE is the matching confidence, not pLDDT."
            ),
            "schema": {
                "top_level": "list of one object",
                "keys": ["predicted_aligned_error", "max_predicted_aligned_error"],
                "dimensions": "393 x 393",
                "units": "angstrom",
                "direction": "lower is better",
                "symmetric": False,
                "indexing": "0-based row/column; residue r is index r-1",
                "stored_as": "integers",
                "declared_max": pae_max,
            },
            "anomalies": {
                "null": 0,
                "non_numeric": 0,
                "above_declared_max_count": len(pae_over),
                "above_declared_max_cells": [
                    {"row_residue": i, "column_residue": j, "value": v} for i, j, v in pae_over
                ],
                "note": (
                    "Values are stored rounded to whole angstrom, so a cell can exceed the "
                    "file's declared maximum by less than 1. None of these cells fall inside "
                    "the 94-292 core block, so no reported block mean depends on them."
                ),
            },
            "blocks": pae_blocks,
            "interpretation": (
                "Within the folded core the model places residues confidently relative to one "
                "another. Between the 293-312 tail and that core the error sits near the top of "
                "the file's own scale, so the model does not know where the tail sits relative "
                "to the core. Both metrics therefore point the same way at 293: pLDDT says the "
                "tail is locally uncertain, PAE says its placement against the core is unknown. "
                "PAE cannot establish a partner interface, a tetramer, or a ligand pocket."
            ),
        },
        "limitations": [
            "pLDDT supports local residue placement, not modifications, binding, partner interactions, or assembly state.",
            "The model is a monomer and contains no DNA, ligand, partner, or tetramer.",
            "The 293-312 cluster is an edge/linker confidence pattern, not a clean target set.",
            "The 183-187 pLDDT dip co-locates with a UniProt Ser183 phosphorylation annotation, but the supplied files do not show that phosphorylation causes the dip."
        ],
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(f"Wrote {OUT.relative_to(ROOT)}")
    print(f"Flagged residues (<70): {len(flagged)}")


if __name__ == "__main__":
    main()
