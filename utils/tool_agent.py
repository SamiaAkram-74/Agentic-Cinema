from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

from utils.tools.location_tool import get_location_info


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def location_agent(location):

    prompt = f"""
    You are a film production assistant.

    The production team wants information about this
    filming location:

    {location}

    Use the available location tool to get the information
    you need, then provide a short production recommendation.
    """

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[get_location_info]
        )
    )

    return response.text