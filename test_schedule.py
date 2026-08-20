from utils.schedule_agent import schedule_agent
import json

script_analysis = {
    "title": "THE LAST SIGNAL",
    "characters": ["Sarah", "John"],
    "locations": ["Laboratory", "Street"],
    "summary": "Sarah discovers a mysterious machine in a laboratory and runs outside to meet John."
}


production_plan = {
    "shooting_complexity": "Medium to High",

    "required_locations": [
        {
            "name": "Laboratory",
            "type": "indoor",
            "complexity": "medium",
            "lighting": "controlled",
            "permit_required": False
        },
        {
            "name": "Street",
            "type": "outdoor",
            "complexity": "high",
            "lighting": "natural",
            "permit_required": True
        }
    ],

    "production_notes": [
        "Laboratory requires the mysterious machine prop.",
        "Street requires permits and traffic control."
    ],

    "estimated_shooting_days": 2
}


result = schedule_agent(
    script_analysis,
    production_plan
)


print("\n===== SCHEDULE AGENT =====")
print(json.dumps(result, indent=2))