from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import json

from utils.tools.clickhouse_tool import get_production_data
from utils.tools.location_tool import get_location_info

load_dotenv()

client = None


# Tool declaration
get_production_data_declaration = types.FunctionDeclaration(
    name="get_production_data",
    description="Gets real production information for a filming location from ClickHouse.",
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "location": types.Schema(
                type="STRING",
                description="The filming location, for example Laboratory or Street."
            )
        },
        required=["location"]
    )
)


def clickhouse_agent(user_request):
    normalized = user_request.lower()
    known_locations = ["laboratory", "street", "office", "warehouse", "riverside park"]
    location = next((item for item in known_locations if item in normalized), None)

    # Keep the assistant useful when a local demo has no external credentials.
    live_mode = os.getenv("AGENTIC_CINEMA_LIVE", "0").lower() in {"1", "true", "yes"}
    if not live_mode:
        if location:
            info = get_location_info(location)
            permit = "requires a permit" if info["permit_required"] else "does not require a permit"
            return (
                f"{location.title()} is an {info['type']} location with {info['complexity']} complexity. "
                f"It {permit} and uses {info['lighting']} lighting. "
                "Confirm access, crew requirements, and a backup plan before locking the schedule."
            )
        return "Ask about a specific location, permit, lighting setup, complexity, or shooting day."

    global client
    if not os.getenv("GEMINI_API_KEY"):
        raise RuntimeError("GEMINI_API_KEY is not configured. Set AGENTIC_CINEMA_LIVE=0 for local mode.")
    client = client or genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    tool = types.Tool(
        function_declarations=[get_production_data_declaration]
    )

    # STEP 1: Ask Gemini whether it needs the tool
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=user_request,
        config=types.GenerateContentConfig(
            tools=[tool]
        )
    )

    # STEP 2: Check whether Gemini requested a tool call
    if response.function_calls:

        function_call = response.function_calls[0]

        print("\n===== GEMINI TOOL CALL =====")
        print("Tool:", function_call.name)
        print("Arguments:", function_call.args)

        if function_call.name == "get_production_data":

            location = function_call.args["location"]

            # STEP 3: Actually execute our Python tool
            try:
                result = get_production_data(location)
            except Exception as exc:
                # A database outage should still produce a useful local recommendation.
                result = {"found": False, "location": location, "message": str(exc), "fallback": get_location_info(location)}

            print("\n===== CLICKHOUSE DATA =====")
            print(result)

            # STEP 4: Send the tool result back to Gemini
            tool_response = types.Part.from_function_response(
                name="get_production_data",
                response=result
            )

            final_response = client.models.generate_content(
                model="gemini-flash-latest",
                contents=[
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_text(
                                text=user_request
                            )
                        ]
                    ),
                    response.candidates[0].content,
                    types.Content(
                        role="user",
                        parts=[tool_response]
                    )
                ],
                config=types.GenerateContentConfig(
                    tools=[tool]
                )
            )

            return final_response.text

    return response.text
