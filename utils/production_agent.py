from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import json
from utils.tools.location_tool import get_location_info
from utils.agent_helpers import demo_mode, parse_model_json, require_api_key
from utils.demo_data import demo_production_plan
from utils.schemas import ProductionPlan, ScriptAnalysis


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = None


def production_agent(script_analysis):
    analysis = ScriptAnalysis.model_validate(script_analysis)
    if demo_mode():
        return demo_production_plan(analysis).model_dump()

    global client
    client = client or genai.Client(api_key=require_api_key())

    prompt = f"""
    You are an AI film production planner.

    Analyze the following screenplay analysis:

    {script_analysis}

    Create a production plan.

    For every filming location, use the available
    location information tool to obtain real production
    information.

    Your output must contain:

    - shooting_complexity
    - required_locations
    - production_notes
    - estimated_shooting_days

    Return the result as JSON.
    """

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[get_location_info]
        )
    )

    text = response.text.strip()

    if text.startswith("```json"):
        text = text[7:]

    if text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    return parse_model_json(text, ProductionPlan).model_dump()
