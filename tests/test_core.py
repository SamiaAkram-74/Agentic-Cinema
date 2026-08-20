import os

import pytest

from utils.agent_helpers import parse_model_json
from utils.demo_data import demo_production_plan, demo_schedule, demo_script_analysis
from utils.schemas import ProductionPlan, ScriptAnalysis, ShootingSchedule
from utils.tools.location_tool import get_location_info
from utils.clickhouse_agent import clickhouse_agent
from utils.workflow import run_workflow


def test_location_tool_known_and_unknown():
    assert get_location_info("Street")["permit_required"] is True
    assert get_location_info("Unknown")['complexity'] == "unknown"


def test_json_parser_accepts_markdown_fence():
    result = parse_model_json("```json\n{\"title\": \"X\", \"characters\": [], \"locations\": [], \"summary\": \"Y\"}\n```", ScriptAnalysis)
    assert result.title == "X"


def test_demo_workflow_from_pdf():
    os.environ["AGENTIC_CINEMA_DEMO"] = "1"
    result = run_workflow("sample_script.pdf")
    assert result["script_analysis"]["title"] == "THE LAST SIGNAL"
    assert result["schedule"]["total_shooting_days"] == 2
    assert result["readiness"]["score"] == 88


def test_demo_models_validate():
    analysis = demo_script_analysis("")
    plan = demo_production_plan(analysis)
    schedule = demo_schedule(analysis, plan)
    assert isinstance(plan, ProductionPlan)
    assert isinstance(schedule, ShootingSchedule)


def test_assistant_works_without_external_services(monkeypatch):
    monkeypatch.setenv("AGENTIC_CINEMA_LIVE", "0")
    answer = clickhouse_agent("What are the permit and lighting requirements for the Street scene?")
    assert "permit" in answer.lower()
    assert "lighting" in answer.lower()
