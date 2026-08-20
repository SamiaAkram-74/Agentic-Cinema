**Steps to Run Agentic Cinema**
-------------------------------

Open the Project in VS Code

Start the Backend
-----------------

 Open a VS Code terminal and run:

 pip install -r requirements.txt

 $env:AGENTIC_CINEMA_LIVE="0"

 uvicorn app:app --reload --port 8000

Keep this terminal running.

The backend should be available at: http://127.0.0.1:8000

Start the Frontend
------------------

Open a second VS Code terminal and run:

 npm install

 npm.cmd run dev

Keep this terminal running.

Open the Application
Open:

http://127.0.0.1:5173

The header should show that the backend is online.

Enable Live Gemini and ClickHouse
Local mode is recommended for demonstrations. To use real Gemini and ClickHouse:

$env:AGENTIC_CINEMA_LIVE="1"

uvicorn app:app --reload --port 8000

Your .env must contain valid Gemini and ClickHouse credentials.
