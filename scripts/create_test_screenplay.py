from pathlib import Path

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer


OUTPUT = Path(__file__).resolve().parents[1] / "output" / "pdf" / "agentic_cinema_test_screenplay.pdf"


def build_pdf() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    title = ParagraphStyle("Title", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=20, leading=24, alignment=TA_CENTER, spaceAfter=18)
    subtitle = ParagraphStyle("Subtitle", parent=styles["Normal"], fontName="Helvetica", fontSize=10, leading=14, alignment=TA_CENTER, textColor="#666666", spaceAfter=28)
    scene = ParagraphStyle("Scene", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=11, leading=14, spaceBefore=16, spaceAfter=10)
    action = ParagraphStyle("Action", parent=styles["BodyText"], fontName="Courier", fontSize=10, leading=14, leftIndent=0, rightIndent=0, spaceAfter=9)
    character = ParagraphStyle("Character", parent=action, alignment=TA_CENTER, spaceBefore=8, spaceAfter=2)
    dialogue = ParagraphStyle("Dialogue", parent=action, leftIndent=1.1 * inch, rightIndent=1.1 * inch, spaceAfter=8)

    story = [
        Spacer(1, 1.25 * inch),
        Paragraph("THE LAST SIGNAL", title),
        Paragraph("A short test screenplay for Agentic Cinema", subtitle),
        Paragraph("Written for production-planning workflow testing", subtitle),
        PageBreak(),
        Paragraph("FADE IN:", action),
        Paragraph("INT. RESEARCH LABORATORY - NIGHT", scene),
        Paragraph("Banks of monitors flicker in the dark. SARAH, 30s, a systems engineer, adjusts a coil of copper wire beside a humming experimental transmitter. The room is filled with controlled blue light and a large machine prop.", action),
        Paragraph("A warning light turns red. Sarah reaches for the emergency switch, but the transmitter sends one final pulse.", action),
        Paragraph("SARAH", character),
        Paragraph("That signal came from outside the building.", dialogue),
        Paragraph("The monitors display a street map with one location blinking.", action),
        Paragraph("INT. RESEARCH LABORATORY - MORNING", scene),
        Paragraph("Morning sunlight cuts through the blinds. Sarah packs a recorder, a flashlight, and the transmitter's portable power unit into a field case.", action),
        Paragraph("JOHN, late 30s, a journalist and Sarah's longtime friend, enters carrying two paper cups of coffee.", action),
        Paragraph("JOHN", character),
        Paragraph("You said this could wait until daylight.", dialogue),
        Paragraph("SARAH", character),
        Paragraph("It did. The signal did not.", dialogue),
        Paragraph("EXT. CITY STREET - DAY", scene),
        Paragraph("A busy public street surrounds them. Cars pass, pedestrians cross, and construction noise competes with the portable transmitter. A small camera crew sets up beside the curb.", action),
        Paragraph("Sarah checks the map. John watches a traffic officer approach. This scene requires a public-location permit and traffic coordination.", action),
        Paragraph("TRAFFIC OFFICER", character),
        Paragraph("You have ten minutes before the lane needs to reopen.", dialogue),
        Paragraph("Sarah raises the antenna. Natural daylight reflects off the equipment.", action),
        Paragraph("SARAH", character),
        Paragraph("There. The signal is moving.", dialogue),
        Paragraph("INT. ABANDONED WAREHOUSE - LATE AFTERNOON", scene),
        Paragraph("The warehouse is vast and dusty. Shafts of warm sunlight enter through broken windows. The crew carries the transmitter through rows of empty shelving.", action),
        Paragraph("A sudden metallic sound echoes from the far end. John switches on a practical flashlight while Sarah powers up the machine.", action),
        Paragraph("JOHN", character),
        Paragraph("Whatever sent the signal knows we are here.", dialogue),
        Paragraph("The transmitter projects a three-dimensional image into the air. It shows the laboratory from the night before.", action),
        Paragraph("EXT. RIVERSIDE PARK - SUNSET", scene),
        Paragraph("Sarah and John stand beside the river as the last natural light fades. The portable transmitter rests on a tripod. A small battery-powered LED panel provides a soft fill.", action),
        Paragraph("The signal resolves into a voice: Sarah's own voice, recorded tomorrow.", action),
        Paragraph("SARAH", character),
        Paragraph("If you can hear this, do not turn the machine on again.", dialogue),
        Paragraph("Sarah looks at John. The transmitter begins to count down.", action),
        Paragraph("JOHN", character),
        Paragraph("What happens at zero?", dialogue),
        Paragraph("The screen goes black. Across the river, a distant light answers.", action),
        Paragraph("FADE OUT.", action),
    ]

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColorRGB(0.45, 0.45, 0.45)
        canvas.drawCentredString(LETTER[0] / 2, 0.45 * inch, f"THE LAST SIGNAL  |  {doc.page}")
        canvas.restoreState()

    doc = SimpleDocTemplate(str(OUTPUT), pagesize=LETTER, rightMargin=1.0 * inch, leftMargin=1.0 * inch, topMargin=0.8 * inch, bottomMargin=0.7 * inch, title="The Last Signal")
    doc.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    build_pdf()
    print(OUTPUT)
