from pathlib import Path

from ..domain import (
    ArtifactGenerationStatus,
    ArtifactRecord,
    PdfArtifactSpec,
    RenderableArtifactPayload,
    SpreadsheetArtifactSpec,
    TextArtifactSpec,
)
from .pdf_renderer import render_pdf_artifact
from .spreadsheet_renderer import render_spreadsheet_artifact
from .text_renderer import render_text_artifact


BUNDLE_RENDER_FORMATS = {"zip"}


def render_artifact_payloads(output_dir: Path, artifact_payloads: list[RenderableArtifactPayload], artifact_requirements: dict[str, bool]) -> list[ArtifactRecord]:
    output_dir.mkdir(parents=True, exist_ok=True)
    artifact_records: list[ArtifactRecord] = []

    for payload in artifact_payloads:
        render_spec = payload.render_spec
        if isinstance(render_spec, TextArtifactSpec):
            file_path, rendered_format = render_text_artifact(output_dir, payload.file_name, render_spec)
        elif isinstance(render_spec, PdfArtifactSpec):
            file_path, rendered_format = render_pdf_artifact(output_dir, payload.file_name, render_spec)
        elif isinstance(render_spec, SpreadsheetArtifactSpec):
            file_path, rendered_format = render_spreadsheet_artifact(output_dir, payload.file_name, render_spec)
        else:
            file_path = output_dir / payload.file_name
            rendered_format = Path(payload.file_name).suffix.replace(".", "").lower() or "zip"
            if rendered_format in BUNDLE_RENDER_FORMATS:
                file_path.parent.mkdir(parents=True, exist_ok=True)
            else:
                file_path.write_text(render_spec.notes, encoding="utf-8")

        artifact_records.append(
            ArtifactRecord(
                artifact_type=payload.artifact_type,
                file_path=file_path,
                file_format=rendered_format,
                is_required=artifact_requirements.get(payload.artifact_type, True),
                generation_status=ArtifactGenerationStatus.GENERATED,
            )
        )

    return artifact_records