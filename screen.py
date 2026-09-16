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
            },
        },
        "summary": {
            "core_residues_screened": len(core),
            "passing_count": len(flagged),
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
        "pLDDT_180_190": [
            {"residue": i, "amino_acid": sequence[i - 1], "plddt": round(plddt[i], 2)}
            for i in range(180, 191)
        ],
        "ranked_flagged_residues": flagged,
        "pae": {
            "file": "data/p53_alphafold_pae.json",
            "use": "not used for this local-confidence shortlist; PAE is pairwise relative-placement confidence",
        },
        "limitations": [
            "pLDDT supports local residue placement, not modifications, binding, partner interactions, or assembly state.",
            "The model is a monomer and contains no DNA, ligand, partner, or tetramer.",
            "The 293-312 cluster is an edge/linker confidence pattern, not a clean target set.",
        ],
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(f"Wrote {OUT.relative_to(ROOT)}")
    print(f"Flagged residues (<70): {len(flagged)}")


if __name__ == "__main__":
    main()
