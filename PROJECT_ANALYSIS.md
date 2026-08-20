# Agentic Cinema Project Analysis

## Current architecture

The prototype has two interfaces over the same Python workflow:

1. `utils.pdf_reader` extracts text from an uploaded screenplay PDF.
2. `utils.script_agent` asks Gemini for title, characters, locations, and summary.
3. `utils.production_agent` asks Gemini to plan production and can call the local location tool.
4. `utils.schedule_agent` turns the analysis and production plan into shooting days.
5. `utils.clickhouse_agent` lets Gemini decide when to query production records through `utils.tools.clickhouse_tool`.
6. `app.py` exposes `/analyze` through FastAPI; `frontend.py` provides a Streamlit interface; `src/` contains a React dashboard.

## What is implemented

- PDF upload and text extraction.
- Three planning agents with JSON output contracts.
- A deterministic location information tool.
- A Gemini tool-calling example for ClickHouse production data.
- FastAPI and React upload flow.
- A production dashboard with analysis, production, and schedule views.
- A small set of manual smoke-test scripts.

## Gaps and risks

- There was no Python dependency manifest, so the backend could not be installed reproducibly.
- External clients were created at import time, making missing credentials or services prevent unrelated modules from loading.
- The API used a predictable temporary filename based on the upload name and did not validate content type or size.
- The React client hard-coded the API URL, which makes deployment configuration awkward.
- The workflow has no stable schema validation or retry/repair path when Gemini returns malformed JSON.
- ClickHouse is required even for script analysis because its client is imported eagerly.
- Existing tests are executable scripts rather than isolated automated tests, and require live Gemini/ClickHouse services.
- The ClickHouse assistant is implemented in Streamlit but is not exposed through a FastAPI endpoint for the React dashboard.

## Recommended completion order

1. Make configuration, external clients, and uploads safe and lazy.
2. Add typed schemas and JSON parsing/repair around every agent boundary.
3. Add a FastAPI assistant endpoint and connect it to the React dashboard.
4. Add deterministic tests for PDF extraction, tools, schemas, and API validation; keep live-agent tests opt-in.
5. Add persistence/job status if long screenplay analysis needs to run asynchronously.
6. Add ClickHouse migrations/seed data and deployment instructions.

## Verification baseline

- Python source compiles successfully.
- React production build succeeds.
- The Python test command is currently blocked until dependencies are installed from `requirements.txt`.
