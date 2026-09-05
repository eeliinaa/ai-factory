from pathlib import Path

from reportlab.lib.pagesizes import A4, LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import ListFlowable, ListItem, Paragraph, SimpleDocTemplate, Spacer

from ..domain import PdfArtifactSpec
from ..outputs.file_renderer import normalize_artifact_file_name


PAGE_SIZES = {
    "a4": A4,
    "letter": LETTER,
    "us_letter": LETTER,
}


def render_pdf_artifact(output_dir: Path, file_name: str, spec: PdfArtifactSpec) -> tuple[Path, str]:
    normalized_name = normalize_artifact_file_name(file_name)
    file_path = output_dir / normalized_name
    file_path.parent.mkdir(parents=True, exist_ok=True)

    page_size = PAGE_SIZES.get(spec.page_size.lower(), LETTER)
    document = SimpleDocTemplate(str(file_path), pagesize=page_size)
    styles = getSampleStyleSheet()
    story = [Paragraph(spec.title, styles["Title"]), Spacer(1, 12)]

    for section in spec.sections:
        story.append(Paragraph(section.heading, styles["Heading2"]))
        story.append(Spacer(1, 6))
        story.append(Paragraph(section.body or "", styles["BodyText"]))
        story.append(Spacer(1, 6))
        if section.bullet_points:
            story.append(
                ListFlowable(
                    [ListItem(Paragraph(point, styles["BodyText"])) for point in section.bullet_points],
                    bulletType="bullet",
                )
            )
            story.append(Spacer(1, 12))

    document.build(story)
    return file_path, "pdf"