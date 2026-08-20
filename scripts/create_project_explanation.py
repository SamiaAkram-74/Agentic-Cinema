from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle, PageBreak


OUTPUT = Path(__file__).resolve().parents[1] / "output" / "pdf" / "agentic_cinema_project_explanation.pdf"


def build_pdf():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    ink = colors.HexColor("#18212B")
    gold = colors.HexColor("#B8923F")
    muted = colors.HexColor("#5B6672")
    pale = colors.HexColor("#F3EFE7")
    title = ParagraphStyle("Title", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=26, leading=31, alignment=TA_CENTER, textColor=ink, spaceAfter=12)
    subtitle = ParagraphStyle("Subtitle", parent=styles["Normal"], fontSize=11, leading=16, alignment=TA_CENTER, textColor=muted, spaceAfter=25)
    h1 = ParagraphStyle("H1", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=17, leading=21, textColor=ink, spaceBefore=17, spaceAfter=8)
    h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=gold, spaceBefore=10, spaceAfter=4)
    body = ParagraphStyle("Body", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.7, leading=14, textColor=ink, spaceAfter=7)
    bullet = ParagraphStyle("Bullet", parent=body, leftIndent=15, firstLineIndent=-9, spaceAfter=4)
    quote = ParagraphStyle("Quote", parent=body, fontName="Helvetica-Oblique", fontSize=11, leading=16, leftIndent=18, rightIndent=18, textColor=ink, backColor=pale, borderPadding=10, spaceBefore=7, spaceAfter=10)
    small = ParagraphStyle("Small", parent=body, fontSize=8.5, leading=12, textColor=muted)

    def bullets(items):
        return [Paragraph(f"- {item}", bullet) for item in items]

    story = [Spacer(1, 0.35 * inch), Paragraph("AGENTIC CINEMA", title), Paragraph("Project Explanation", subtitle), Paragraph("An AI-powered production planning system that transforms a screenplay into practical filmmaking intelligence.", quote), Paragraph("This document explains the project in simple, presentation-ready language. It focuses on what the system does, how the agents work together, and why the project is useful for filmmakers.", body)]

    story += [Paragraph("1. The Project in One Sentence", h1), Paragraph("Agentic Cinema reads a screenplay PDF and automatically creates a production plan containing script analysis, filming requirements, risks, and a shooting schedule.", quote)]

    story += [Paragraph("2. The Problem", h1), Paragraph("A screenplay describes the story, but a production team must convert that story into practical filming decisions. Producers normally have to read the entire script and manually identify locations, characters, permits, lighting, equipment, complexity, and shooting days.", body), Paragraph("This manual process can be slow, repetitive, and vulnerable to missed details. A small detail in a screenplay, such as a crowded public street or a night scene, can create important production requirements.", body), Paragraph("Agentic Cinema helps identify those requirements earlier, before filming begins.", body)]

    story += [Paragraph("3. The Solution", h1), Paragraph("The filmmaker uploads a screenplay PDF. The system reads it, analyzes the story, plans production requirements, creates a schedule, evaluates readiness, and provides an interactive production assistant.", body)]
    story += bullets(["Script analysis", "Characters and locations", "Production complexity", "Permit and lighting requirements", "Production notes", "Shooting-day schedule", "Risk alerts", "Recommended next actions", "Production-data questions"])

    story += [Paragraph("4. How the System Works", h1)]
    workflow = [[Paragraph("Stage", h2), Paragraph("What happens", h2)], [Paragraph("Screenplay upload", body), Paragraph("The filmmaker uploads a screenplay PDF through the dashboard.", body)], [Paragraph("Text extraction", body), Paragraph("The PDF reader extracts the screenplay text so the agents can process it.", body)], [Paragraph("Script analysis", body), Paragraph("The Script Analysis Agent identifies the title, characters, locations, scenes, and story summary.", body)], [Paragraph("Production planning", body), Paragraph("The Production Planning Agent determines filming complexity, permits, lighting, locations, and notes.", body)], [Paragraph("Scheduling", body), Paragraph("The Scheduling Agent groups scenes into practical shooting days, usually organizing scenes by location.", body)], [Paragraph("Readiness evaluation", body), Paragraph("The Readiness Evaluator produces a score, risk alerts, and next actions.", body)], [Paragraph("Dashboard", body), Paragraph("The results are presented in a production dashboard where the filmmaker can review and ask questions.", body)]]
    table = Table(workflow, colWidths=[1.55 * inch, 4.8 * inch], repeatRows=1)
    table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), pale), ("TEXTCOLOR", (0, 0), (-1, 0), gold), ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D5D0C5")), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    story.append(table)

    story += [PageBreak(), Paragraph("5. The Specialized Agents", h1), Paragraph("Agentic Cinema uses several specialized agents. Each agent has a focused responsibility instead of asking one chatbot to perform every task.", body)]
    story += [Paragraph("Script Analysis Agent", h2), Paragraph("This agent understands the screenplay. It extracts the title, characters, locations, scenes, and a summary. Its job is to convert unstructured story text into organized screenplay information.", body), Paragraph("Production Planning Agent", h2), Paragraph("This agent thinks like a production manager. It looks at each filming location and determines the likely complexity, lighting requirements, permits, production notes, and estimated shooting days.", body), Paragraph("Scheduling Agent", h2), Paragraph("This agent creates a day-by-day shooting schedule. It groups scenes by location when practical, reducing unnecessary travel, setup changes, and equipment movement.", body), Paragraph("Readiness Evaluator", h2), Paragraph("This agent evaluates whether the project is ready to move toward production. It creates a readiness score, identifies risks, and recommends the next actions for the production team.", body), Paragraph("Production Assistant", h2), Paragraph("This assistant answers practical questions about locations, permits, lighting, complexity, and shooting requirements. It can use local production rules or live production data.", body)]

    story += [Paragraph("6. What Makes It Agentic?", h1), Paragraph("Agentic Cinema is not simply a chatbot that generates a paragraph. The agents make decisions about what information they need and can use tools to retrieve that information.", body), Paragraph("For example, when a filmmaker asks about a street scene, the assistant identifies that location information is needed. It can then use a location tool or production database to retrieve permit, lighting, and complexity details before forming its recommendation.", body), Paragraph("This creates a cycle of understanding, tool use, reasoning, and response.", quote)]

    story += [Paragraph("7. Tools and Production Data", h1), Paragraph("The location tool provides structured knowledge about common filming locations. It can identify whether a location is indoor or outdoor, whether a permit is likely required, what lighting approach is expected, and how complex the location may be.", body), Paragraph("ClickHouse is used as a production database. It can store project-specific records such as which scene is filmed at which location, the planned shooting day, complexity, permit status, and lighting approach.", body), Paragraph("This allows the assistant to combine AI reasoning with structured production information.", body)]

    story += [Paragraph("8. What the Filmmaker Receives", h1), Paragraph("After analysis, the filmmaker receives a complete production overview:", body)]
    story += bullets(["A summary of the screenplay", "The main characters and locations", "Location-by-location filming requirements", "Shooting complexity", "Permit and lighting considerations", "Production notes", "Estimated shooting days", "A location-based schedule", "Production readiness score", "Risk alerts and recommended actions", "An interactive production assistant"])

    story += [PageBreak(), Paragraph("9. Production Readiness", h1), Paragraph("The Production Readiness Score is an additional decision-support feature. It summarizes how complete and practical the current production plan appears to be.", body), Paragraph("The evaluator considers whether scenes were identified, whether locations require permits, whether locations are highly complex, and whether the schedule covers the estimated production days.", body), Paragraph("The result is not a replacement for a human producer. It is an early warning system that helps the production team decide what needs attention first.", body)]
    story += [Paragraph("Example output", h2), Paragraph("Readiness score: 88 out of 100", quote), Paragraph("Risk alerts may include a required street permit or high-complexity outdoor filming. Recommended actions may include beginning permit applications, arranging traffic control, booking a technical scout, or preparing a backup lighting plan.", body)]

    story += [Paragraph("10. The Dashboard", h1), Paragraph("The React dashboard brings the full workflow into one interface. It contains an upload screen, analysis results, production planning, shooting schedule, readiness information, and a Production Assistant.", body)]
    story += bullets(["Upload a screenplay PDF", "View the screenplay analysis", "Review production requirements", "Inspect risk alerts and next actions", "View the agent activity trace", "Browse the shooting schedule", "Ask production questions", "Export the production plan", "Print a production report", "Switch between light and dark themes"])

    story += [Paragraph("11. Demonstration Flow", h1), Paragraph("For a presentation, upload the sample screenplay and walk through the result in this order:", body)]
    story += bullets(["Show the title, characters, locations, and summary.", "Open the production view and explain permits, lighting, and complexity.", "Show the readiness score and risk register.", "Open the schedule and explain why scenes are grouped by location.", "Ask the Production Assistant about the Street scene.", "Show the returned recommendation and explain how a tool or database can support the answer.", "Export or print the generated plan."])

    story += [Paragraph("12. Why the Project Is Valuable", h1), Paragraph("For producers, the system reduces manual script breakdown work and highlights production risks earlier. For directors, it provides a clearer view of how story decisions affect filming. For production teams, it creates a shared planning document with locations, requirements, risks, and shooting days in one place.", body), Paragraph("The larger goal is to reduce the gap between creative screenplay writing and practical production planning.", quote)]

    story += [Paragraph("13. Current and Future Scope", h1), Paragraph("The current system focuses on screenplay understanding, production planning, scheduling, tool use, readiness evaluation, and interactive recommendations.", body), Paragraph("Future versions could add budget estimation, crew and equipment breakdowns, weather-aware scheduling, calendar export, team collaboration, project history, user accounts, location availability, and permit workflow management.", body)]

    story += [Paragraph("14. Final Explanation", h1), Paragraph("Agentic Cinema transforms screenplay intelligence into production intelligence. It reads a screenplay, uses specialized agents to understand it, retrieves production information through tools, creates a shooting plan, identifies risks, and gives filmmakers practical recommendations before filming begins.", quote), Paragraph("In simple words: the system helps a filmmaker move from a story on paper to a clearer plan for making that story real.", body), Spacer(1, 12), Paragraph("Prepared for Agentic Cinema project presentation", small)]

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(gold)
        canvas.line(doc.leftMargin, 0.55 * inch, LETTER[0] - doc.rightMargin, 0.55 * inch)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(muted)
        canvas.drawString(doc.leftMargin, 0.35 * inch, "Agentic Cinema")
        canvas.drawRightString(LETTER[0] - doc.rightMargin, 0.35 * inch, f"Page {doc.page}")
        canvas.restoreState()

    doc = SimpleDocTemplate(str(OUTPUT), pagesize=LETTER, rightMargin=0.72 * inch, leftMargin=0.72 * inch, topMargin=0.65 * inch, bottomMargin=0.78 * inch, title="Agentic Cinema Project Explanation", author="Agentic Cinema")
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(OUTPUT)


if __name__ == "__main__":
    build_pdf()
