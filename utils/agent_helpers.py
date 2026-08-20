import json
import os
import re
from typing import Any, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def demo_mode() -> bool:
    # Local mode is the safe default. Live Gemini calls require an explicit opt-in.
    live = os.getenv("AGENTIC_CINEMA_LIVE", "0").lower() in {"1", "true", "yes"}
    demo = os.getenv("AGENTIC_CINEMA_DEMO", "0").lower() in {"1", "true", "yes"}
    return demo or not live


def require_api_key() -> str:
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY is not configured. Set it or enable AGENTIC_CINEMA_DEMO=1.")
    return key


def parse_model_json(text: str, model: type[T]) -> T:
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        return model.model_validate(json.loads(cleaned))
    except (json.JSONDecodeError, ValueError) as exc:
        raise ValueError(f"Agent returned invalid {model.__name__} JSON: {exc}") from exc
