from utils.schemas import ProductionPlan, ScriptAnalysis, ShootingSchedule


def demo_script_analysis(text: str) -> ScriptAnalysis:
    return ScriptAnalysis(
        title="THE LAST SIGNAL",
        characters=["Sarah", "John"],
        locations=["Laboratory", "Street"],
        scenes=["Sarah discovers the machine", "Sarah runs outside to meet John"],
        summary="Sarah discovers a mysterious machine in a laboratory and runs outside to meet John.",
    )


def demo_production_plan(analysis: ScriptAnalysis) -> ProductionPlan:
    return ProductionPlan(
        shooting_complexity="medium to high",
        required_locations=[
            {"name":"Laboratory","type":"indoor","complexity":"medium","lighting":"controlled","permit_required":False,"notes":["Prepare the machine prop."]},
            {"name":"Street","type":"outdoor","complexity":"high","lighting":"natural","permit_required":True,"notes":["Arrange permit and traffic control."]},
        ],
        production_notes=["Prepare the mysterious machine prop.", "Secure a street permit and traffic control."],
        estimated_shooting_days=2,
    )


def demo_schedule(analysis: ScriptAnalysis, plan: ProductionPlan) -> ShootingSchedule:
    scenes = analysis.scenes or [f"Scenes at {location}" for location in analysis.locations]
    first_scene = scenes[0] if scenes else "Primary laboratory scene"
    second_scene = scenes[1] if len(scenes) > 1 else "Primary street scene"
    return ShootingSchedule(total_shooting_days=2, schedule=[
        {"day":1,"location":"Laboratory","scenes":[first_scene],"notes":"Controlled lighting and machine prop setup."},
        {"day":2,"location":"Street","scenes":[second_scene],"notes":"Permit, traffic control, and natural-light plan required."},
    ])
