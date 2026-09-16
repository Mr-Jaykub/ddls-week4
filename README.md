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
