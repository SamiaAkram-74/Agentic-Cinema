from utils.schemas import ProductionPlan, ProductionReadiness, ScriptAnalysis, ShootingSchedule


def calculate_readiness(analysis, plan, schedule) -> dict:
    analysis = ScriptAnalysis.model_validate(analysis)
    plan = ProductionPlan.model_validate(plan)
    schedule = ShootingSchedule.model_validate(schedule)
    risks = []
    actions = []
    permit_count = sum(location.permit_required for location in plan.required_locations)
    high_complexity = sum(location.complexity.lower() == "high" for location in plan.required_locations)
    score = 100
    if not analysis.scenes:
        score -= 20
        risks.append("Scene-level breakdown is incomplete")
        actions.append("Review scene boundaries before locking the schedule")
    if permit_count:
        score -= min(15, permit_count * 7)
        risks.append(f"{permit_count} location permit requirement(s)")
        actions.append("Start permit applications and traffic-control planning")
    if high_complexity:
        score -= min(15, high_complexity * 5)
        risks.append("High-complexity location work")
        actions.append("Book a technical scout and backup lighting plan")
    if len(schedule.schedule) < plan.estimated_shooting_days:
        score -= 15
        risks.append("Schedule does not cover all estimated shooting days")
        actions.append("Reconcile schedule days with the production estimate")
    if not risks:
        label = "Ready to schedule"
    elif score >= 70:
        label = "Review before lock"
    else:
        label = "Needs production review"
    return ProductionReadiness(
        score=max(0, score),
        label=label,
        risk_flags=risks,
        next_actions=actions,
        agent_trace=["PDF Reader", "Script Analysis Agent", "Production Planning Agent", "Scheduling Agent", "Readiness Evaluator"],
    ).model_dump()
