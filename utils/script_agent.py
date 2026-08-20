from google import genai
from dotenv import load_dotenv
import os
import json
from utils.agent_helpers import demo_mode, parse_model_json, require_api_key
from utils.demo_data import demo_script_analysis
from utils.schemas import ScriptAnalysis

load_dotenv()

client = None


def script_agent(script):
    if demo_mode():
        return demo_script_analysis(script).model_dump()

    global client
    client = client or genai.Client(api_key=require_api_key())

    prompt = f"""
    You are a professional screenplay analyst.

    Analyze the following screenplay.

    Return ONLY valid JSON.

    The JSON must contain exactly these fields:

    {{
        "title": "string",
        "characters": ["character 1", "character 2"],
        "locations": ["location 1", "location 2"],
        "summary": "short summary"
    }}

    Do not add markdown.
    Do not add explanations outside the JSON.

    Screenplay:
    {script}
    """

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    return parse_model_json(response.text, ScriptAnalysis).model_dump()
