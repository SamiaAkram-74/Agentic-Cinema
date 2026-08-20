from google import genai
from dotenv import load_dotenv
import os
import json
from utils.agent_helpers import demo_mode, parse_model_json, require_api_key
from utils.demo_data import demo_schedule
from utils.schemas import ProductionPlan, ScriptAnalysis, ShootingSchedule

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = None


def schedule_agent(script_analysis, production_plan):
    analysis = ScriptAnalysis.model_validate(script_analysis)
    plan = ProductionPlan.model_validate(production_plan)
    if demo_mode():
        return demo_schedule(analysis, plan).model_dump()

    global client
    client = client or genai.Client(api_key=require_api_key())

    prompt = f"""
    You are a professional film scheduling agent.

    Create a practical shooting schedule based on the
    screenplay analysis and production plan.

    Return ONLY valid JSON with exactly these fields:

    {{
        "total_shooting_days": 0,
        "schedule": [
            {{
                "day": 1,
                "location": "location name",
                "scenes": ["scene names"],
                "notes": "short note"
            }}
        ]
    }}

    SCREENPLAY ANALYSIS:
    {script_analysis}

    PRODUCTION PLAN:
    {production_plan}

    Important:
    - Group scenes by location when practical.
    - Use the production requirements and location complexity.
    - Keep the schedule realistic.
    - Do not invent scenes that are not in the screenplay.
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    # Remove Markdown JSON fences if Gemini adds them
    if text.startswith("```json"):
        text = text[7:]

    if text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    return parse_model_json(text, ShootingSchedule).model_dump()
