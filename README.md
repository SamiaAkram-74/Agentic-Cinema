# Agentic Cinema

## Local setup

```powershell
pip install -r requirements.txt
$env:AGENTIC_CINEMA_DEMO="1"
uvicorn app:app --reload --port 8000
```

In another terminal:

```powershell
npm install
npm run dev
```

Open `http://localhost:5173`. Local mode exercises the complete workflow and assistant without external service delays. For live Gemini and ClickHouse agents, explicitly set `AGENTIC_CINEMA_LIVE=1`, `GEMINI_API_KEY`, and the ClickHouse variables from `.env`.

## Tests

```powershell
pytest -q
```

The ClickHouse table can be created and seeded with `sql/001_production_scenes.sql`.
