from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def create_report(
    filename,
    prediction,
    ats_score,
    skills,
    missing,
    suggestions
):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("<b>ResumeAI Pro Report</b>", styles["Title"]))

    elements.append(Paragraph(f"<b>Category:</b> {prediction}", styles["BodyText"]))

    elements.append(Paragraph(f"<b>ATS Score:</b> {ats_score}%", styles["BodyText"]))

    elements.append(Paragraph(f"<b>Skills:</b> {', '.join(skills)}", styles["BodyText"]))

    elements.append(Paragraph(f"<b>Missing Skills:</b> {', '.join(missing)}", styles["BodyText"]))

    elements.append(Paragraph(f"<b>Suggestions:</b> {'<br/>'.join(suggestions)}", styles["BodyText"]))

    doc.build(elements)