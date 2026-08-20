import os
import tempfile
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from utils.workflow import run_workflow
from utils.clickhouse_agent import clickhouse_agent
from utils.schemas import AssistantRequest, AssistantResponse


# 1. Initialize FastAPI app
app = FastAPI(
    title="Agentic Cinema API",
    description="API for multi-agent script analysis, production planning, and scheduling.",
    version="1.0.0"
)

# 2. Allow requests from Replit / frontend (CORS setup)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "online", "message": "Agentic Cinema API is running!"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/assistant", response_model=AssistantResponse)
def assistant_endpoint(request: AssistantRequest):
    try:
        answer = clickhouse_agent(request.question)
        return AssistantResponse(answer=answer, source="production assistant")
    except Exception as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

@app.post("/analyze")
async def analyze_script_endpoint(file: UploadFile = File(...)):
    """
    Upload a script PDF to execute the complete agentic workflow.
    """
    filename = file.filename or ""
    if Path(filename).suffix.lower() != ".pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    temp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(prefix="agentic_cinema_", suffix=".pdf", delete=False) as buffer:
            temp_file_path = buffer.name
            while chunk := await file.read(1024 * 1024):
                buffer.write(chunk)

        result = run_workflow(temp_file_path)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        # Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
