import os
from dotenv import load_dotenv
import clickhouse_connect

load_dotenv()


def _get_client():
    """Create the ClickHouse client only when a database lookup is requested."""
    host = os.getenv("CLICKHOUSE_HOST")
    if not host:
        raise RuntimeError("CLICKHOUSE_HOST is not configured.")

    return clickhouse_connect.get_client(
        host=host,
        username=os.getenv("CLICKHOUSE_USER"),
        password=os.getenv("CLICKHOUSE_PASSWORD"),
        database=os.getenv("CLICKHOUSE_DATABASE", "default"),
        secure=True
    )


def get_production_data(location: str) -> dict:
    """
    Get production information for a filming location.

    Args:
        location: Name of the filming location.

    Returns:
        Production information from ClickHouse.
    """

    query = """
        SELECT
            movie,
            scene,
            location,
            shooting_day,
            complexity,
            permit_required,
            lighting
        FROM production_scenes
        WHERE location = {location:String}
    """

    result = _get_client().query(
        query,
        parameters={"location": location}
    )

    rows = result.result_rows

    if not rows:
        return {
            "found": False,
            "location": location,
            "message": "No production data found."
        }

    columns = [
        "movie",
        "scene",
        "location",
        "shooting_day",
        "complexity",
        "permit_required",
        "lighting"
    ]

    data = [dict(zip(columns, row)) for row in rows]

    return {
        "found": True,
        "data": data
    }
