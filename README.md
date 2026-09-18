# p53 confidence screen

A small FastAPI + Tailwind/3Dmol.js viewer for the reproducible pLDDT screen. The app reads `results/results.json` on every request and serves the supplied mmCIF without a database.

## Run

From a clean checkout:

```bash
uv venv
uv pip install -r requirements.txt
uv run uvicorn app:app --host 127.0.0.1 --port 8000
```

`uv run` uses the project environment, and the app reads `results/results.json` from disk at request time.

Open <http://127.0.0.1:8000/>.

## Reproduce the analysis

```bash
uv run python screen.py        # rebuilds results/results.json from data/
uv run python check_slides.py  # verifies slides.html and report.md against it
```

`screen.py` is the only thing that writes `results/results.json`. `check_slides.py` writes nothing:
it re-reads the deck and the report and fails if any figure in either has drifted from the
analysis, which is what makes it safe to edit their prose by hand.

## What is where

| Path | What it is |
|---|---|
| `spec.md` | the agreed analysis specification |
| `report.md` | the written answer for the data owner |
| `slides.html` | the seminar deck, self-contained (no network needed) |
| `interview-summary.md` | what the owner claimed, and what was measured afterwards |
| `notes/verification/` | the independent reimplementation used as a cross-check |
