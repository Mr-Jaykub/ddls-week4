# DDLS Module 4 — structure + confidence viewer

Computer Lab 4: interview a structural-biology data owner, direct an analyst to trust
(or refuse to trust) an AlphaFold model.

## Run

```bash
uv venv
uv run uvicorn app:app --reload --port 8000
```

Open http://127.0.0.1:8000/.

## Layout

- `data/` — data bundle from the course portal (FASTA, structure, confidence)
- `results/` — analysis outputs the app reads (results.json, structure, PAE)
- `spec.md` — the protein, the exact claim, the matching confidence, the structure check
- `AGENTS.md` — brief for the analysis agent
- `report.md` — structured write-up

## Lab session start

```bash
cd ~/ddls-week4
set -a; source .env; set +a
pi --provider ddls --model gpt-5.6-luna
```

Repo: https://github.com/Mr-Jaykub/ddls-week4
