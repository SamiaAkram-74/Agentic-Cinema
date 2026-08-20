from typing import Any

from pydantic import BaseModel, Field


class ScriptAnalysis(BaseModel):
    title: str = "Untitled screenplay"
    characters: list[str] = Field(default_factory=list)
    locations: list[str] = Field(default_factory=list)
    scenes: list[str] = Field(default_factory=list)
    summary: str = ""


class LocationRequirement(BaseModel):
    name: str
    type: str = "unknown"
    complexity: str = "unknown"
    lighting: str = "unknown"
    permit_required: bool = True
    notes: list[str] = Field(default_factory=list)


class ProductionPlan(BaseModel):
    shooting_complexity: str = "medium"
    required_locations: list[LocationRequirement] = Field(default_factory=list)
    production_notes: list[str] = Field(default_factory=list)
    estimated_shooting_days: int = Field(default=1, ge=1)


class ScheduleDay(BaseModel):
    day: int = Field(ge=1)
    location: str
    scenes: list[str] = Field(default_factory=list)
    notes: str = ""


class ShootingSchedule(BaseModel):
    total_shooting_days: int = Field(default=1, ge=1)
    schedule: list[ScheduleDay] = Field(default_factory=list)


class ProductionReadiness(BaseModel):
    score: int = Field(ge=0, le=100)
    label: str
    risk_flags: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)
    agent_trace: list[str] = Field(default_factory=list)


class AnalysisResult(BaseModel):
    script_analysis: ScriptAnalysis
    production_plan: ProductionPlan
    schedule: ShootingSchedule
    readiness: ProductionReadiness


class AssistantRequest(BaseModel):
    question: str = Field(min_length=2, max_length=2000)
    location: str | None = None
    analysis: AnalysisResult | None = None


class AssistantResponse(BaseModel):
    answer: str
    source: str
    data: dict[str, Any] = Field(default_factory=dict)
