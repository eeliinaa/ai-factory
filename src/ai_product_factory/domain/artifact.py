from pathlib import Path

from pydantic import BaseModel

from .enums import ArtifactGenerationStatus


class ArtifactPlanItem(BaseModel):
    artifact_type: str
    file_name: str
    file_format: str
    purpose: str
    is_required: bool = True
    generation_instructions: str


class ArtifactRecord(BaseModel):
    artifact_type: str
    file_path: Path
    file_format: str
    is_required: bool = True
    generation_status: ArtifactGenerationStatus = ArtifactGenerationStatus.PENDING
