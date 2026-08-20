from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


OUTPUT = Path(__file__).resolve().parents[1] / "output" / "pdf" / "agentic_cinema_functionality_overview.pdf"


def build_pdf():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    gold = colors.HexColor("#B8923F")
    ink = colors.HexColor("#1A1A1A")
    muted = colors.HexColor("#5C6470")
    title = ParagraphStyle("Title", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=25, leading=30, alignment=TA_CENTER, textColor=ink, spaceAfter=10)
    subtitle = ParagraphStyle("Subtitle", parent=styles["Normal"], fontSize=11, leading=16, alignment=TA_CENTER, textColor=muted, spaceAfter=26)
    h1 = ParagraphStyle("H1", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=16, leading=20, textColor=ink, spaceBefore=18, spaceAfter=9)
    h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=gold, spaceBefore=9, spaceAfter=5)
    body = ParagraphStyle("Body", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.5, leading=14, textColor=ink, spaceAfter=6)
    bullet = ParagraphStyle("Bullet", parent=body, leftIndent=14, firstLineIndent=-8, bulletIndent=0, spaceAfter=4)
    small = ParagraphStyle("Small", parent=body, fontSize=8.5, leading=12, textColor=muted)

    def bullets(items):
        return [Paragraph(f"- {item}", bullet) for item in items]

    story = [Spacer(1, 0.35 * inch), Paragraph("AGENTIC CINEMA", title), Paragraph("Project Functionality Overview", subtitle), Paragraph("An agentic AI production-planning system for turning screenplay PDFs into practical filmmaking plans.", body), Spacer(1, 8)]

    story += [Paragraph("1. Original Functionality", h1), Paragraph("The prototype established the core screenplay-to-production workflow:", body)]
    story += bullets([
        "Upload a screenplay PDF and extract its text.",
        "Use a Script Analysis Agent to identify the title, characters, locations, scenes, and story summary.",
        "Use a Production Planning Agent to determine shooting complexity, required locations, permits, lighting, production notes, and estimated shooting days.",
        "Use a Scheduling Agent to create a practical, location-based shooting schedule.",
        "Use a deterministic location information tool for production facts such as indoor or outdoor type, lighting, complexity, and permit requirements.",
        "Use a ClickHouse tool to retrieve stored production records for locations and scenes.",
        "Provide FastAPI, Streamlit, and React interfaces for the workflow.",
        "Display script analysis, production planning, and shooting schedule results in a dashboard.",
    ])

    story += [Paragraph("2. Agentic System", h1), Paragraph("The system is composed of specialized agents rather than one general chatbot:", body)]
    flow = [[Paragraph("Input", h2), Paragraph("Agent or Tool", h2), Paragraph("Output", h2)], [Paragraph("Screenplay PDF", body), Paragraph("PDF Reader", body), Paragraph("Extracted screenplay text", body)], [Paragraph("Screenplay text", body), Paragraph("Script Analysis Agent", body), Paragraph("Characters, locations, scenes, summary", body)], [Paragraph("Script analysis", body), Paragraph("Production Planning Agent + Location Tool", body), Paragraph("Production requirements and notes", body)], [Paragraph("Analysis + production plan", body), Paragraph("Scheduling Agent", body), Paragraph("Shooting days and location schedule", body)], [Paragraph("Filmmaker question", body), Paragraph("ClickHouse Production Assistant", body), Paragraph("Database-backed recommendation", body)]]
    table = Table(flow, colWidths=[1.55 * inch, 2.25 * inch, 2.55 * inch], repeatRows=1)
    table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F0ECE4")), ("TEXTCOLOR", (0, 0), (-1, 0), gold), ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D5D1C8")), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    story += [table]

    story += [Paragraph("3. Functionality Added", h1)]
    story += bullets([
        "Typed validation schemas for script analysis, production plans, schedules, readiness results, and assistant requests.",
        "Reliable JSON parsing for Gemini responses, including Markdown-wrapped JSON.",
        "Demo mode for running the complete workflow without Gemini or ClickHouse credentials.",
        "Production Readiness Score out of 100.",
        "Readiness status such as Ready to schedule, Review before lock, or Needs production review.",
        "Risk Register for permits, high-complexity locations, missing scene details, and schedule mismatches.",
        "Recommended next production actions generated from the plan.",
        "AI Agent Execution Trace showing which specialized steps completed.",
        "Production Assistant connected to the React dashboard through the /assistant endpoint.",
        "Health monitoring through the /health endpoint.",
        "Export the complete production plan as JSON and print a production report.",
        "Backward-compatible frontend fallback when an older backend response does not yet include readiness data.",
        "Automated tests, Python dependency management, ClickHouse schema and seed data, and a testing screenplay PDF.",
    ])

    story += [Paragraph("4. Current Dashboard Capabilities", h1)]
    story += bullets([
        "Screenplay upload and analysis workflow.",
        "Script title, summary, characters, locations, and scenes.",
        "Production complexity and estimated shooting days.",
        "Location requirements, permits, lighting, and production notes.",
        "Risk alerts and next actions.",
        "Agent activity trace.",
        "Day-by-day shooting schedule.",
        "AI production assistant for location and permit questions.",
        "JSON export and print report actions.",
        "Light and dark theme support.",
    ])

    story += [Paragraph("5. End-to-End Workflow", h1), Paragraph("Screenplay PDF -> PDF Reader -> Script Analysis Agent -> Production Planning Agent -> Location Tool / ClickHouse -> Scheduling Agent -> Readiness Evaluator -> Production Dashboard -> Production Assistant", body)]
    story += [Paragraph("6. Demonstration Mode", h1), Paragraph("For competition demonstrations, the system can run locally without external services by setting:", body), Paragraph("AGENTIC_CINEMA_DEMO=1", ParagraphStyle("Code", parent=body, fontName="Courier-Bold", backColor=colors.HexColor("#F0ECE4"), borderPadding=7, spaceAfter=10))]
    story += [Paragraph("This produces a complete sample analysis, production plan, schedule, readiness score, risk register, and assistant response.", body), Spacer(1, 12), Paragraph("Prepared for Agentic Cinema project presentation", small)]

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(gold)
        canvas.line(doc.leftMargin, 0.55 * inch, LETTER[0] - doc.rightMargin, 0.55 * inch)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(muted)
        canvas.drawString(doc.leftMargin, 0.35 * inch, "Agentic Cinema")
        canvas.drawRightString(LETTER[0] - doc.rightMargin, 0.35 * inch, f"Page {doc.page}")
        canvas.restoreState()

    doc = SimpleDocTemplate(str(OUTPUT), pagesize=LETTER, rightMargin=0.72 * inch, leftMargin=0.72 * inch, topMargin=0.65 * inch, bottomMargin=0.78 * inch, title="Agentic Cinema Functionality Overview", author="Agentic Cinema")
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(OUTPUT)


if __name__ == "__main__":
    build_pdf()
