from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

from .enums import ArtifactGenerationStatus


class ArtifactPlanItem(BaseModel):
    artifact_type: str
    file_name: str
    file_format: str
    purpose: str
    is_required: bool = True
    generation_instructions: str


class TextArtifactSpec(BaseModel):
    kind: Literal["text"] = "text"
    content: str


class PdfArtifactSection(BaseModel):
    heading: str
    body: str
    bullet_points: list[str] = Field(default_factory=list)


class PdfArtifactSpec(BaseModel):
    kind: Literal["pdf"] = "pdf"
    title: str
    sections: list[PdfArtifactSection] = Field(default_factory=list)
    page_size: str = "letter"


class SpreadsheetColumnSpec(BaseModel):
    header: str
    width: int | None = None


class SpreadsheetSheetSpec(BaseModel):
    name: str
    columns: list[SpreadsheetColumnSpec] = Field(default_factory=list)
    rows: list[list[str]] = Field(default_factory=list)


class SpreadsheetArtifactSpec(BaseModel):
    kind: Literal["spreadsheet"] = "spreadsheet"
    workbook_title: str
    sheets: list[SpreadsheetSheetSpec] = Field(default_factory=list)


class BundleArtifactSpec(BaseModel):
    kind: Literal["bundle"] = "bundle"
    notes: str = "Assembled by packaging code."


ArtifactRenderSpec = TextArtifactSpec | PdfArtifactSpec | SpreadsheetArtifactSpec | BundleArtifactSpec


class ArtifactRecord(BaseModel):
    artifact_type: str
    file_path: Path
    file_format: str
    is_required: bool = True
    generation_status: ArtifactGenerationStatus = ArtifactGenerationStatus.PENDING


class RenderableArtifactPayload(BaseModel):
    artifact_type: str
    file_name: str
    render_spec: ArtifactRenderSpec