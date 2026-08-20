def get_location_info(location: str) -> dict:
    """Get production information about a filming location."""

    locations = {
        "laboratory": {
            "type": "indoor",
            "permit_required": False,
            "lighting": "controlled",
            "complexity": "medium"
        },

        "street": {
            "type": "outdoor",
            "permit_required": True,
            "lighting": "natural",
            "complexity": "high"
        },

        "office": {
            "type": "indoor",
            "permit_required": False,
            "lighting": "controlled",
            "complexity": "low"
        }
    }

    return locations.get(
        location.lower(),
        {
            "type": "unknown",
            "permit_required": True,
            "lighting": "unknown",
            "complexity": "unknown"
        }
    )