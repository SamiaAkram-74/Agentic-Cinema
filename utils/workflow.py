from utils.pdf_reader import read_pdf
from utils.script_agent import script_agent
from utils.production_agent import production_agent
from utils.schedule_agent import schedule_agent
from utils.schemas import AnalysisResult
from utils.readiness import calculate_readiness


def run_workflow(file):

    # 1. Read screenplay
    script = read_pdf(file)

    print("\n===== SCRIPT LOADED =====")

    # 2. Analyze screenplay
    script_analysis = script_agent(script)

    print("\n===== SCRIPT ANALYSIS =====")
    print(script_analysis)

    # 3. Create production plan
    production_plan = production_agent(script_analysis)

    print("\n===== PRODUCTION PLAN =====")
    print(production_plan)

    # 4. Create shooting schedule
    schedule = schedule_agent(
        script_analysis,
        production_plan
    )

    readiness = calculate_readiness(script_analysis, production_plan, schedule)

    print("\n===== SHOOTING SCHEDULE =====")
    print(schedule)

    return AnalysisResult(
        script_analysis=script_analysis,
        production_plan=production_plan,
        schedule=schedule,
        readiness=readiness,
    ).model_dump()
