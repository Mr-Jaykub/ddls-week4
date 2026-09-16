# p53 confidence screen

A small FastAPI + Tailwind/3Dmol.js viewer for the reproducible pLDDT screen. The app reads `results/results.json` on every request and serves the supplied mmCIF without a database.

## Run

```bash
uv venv
uv run uvicorn app:app --host 127.0.0.1 --port 8000
```

Open <http://127.0.0.1:8000/>.
