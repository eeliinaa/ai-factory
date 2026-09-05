from pathlib import Path
import re

from ..domain import ArtifactPlanItem, ArtifactRecord
from ..renderers import render_artifact_payloads


TEXT_RENDERED_EXTENSIONS = {"md", "txt", "json", "csv", "html"}
UNSUPPORTED_BINARY_EXTENSIONS = {"png", "jpg", "jpeg", "canva"}


def normalize_artifact_file_name(file_name: str) -> str:
    cleaned = file_name.strip().replace(" ", "_")
    cleaned = re.sub(r"[^A-Za-z0-9._/~-]", "_", cleaned)
    cleaned = re.sub(r"/+", "/", cleaned).strip("/")
    return cleaned or "artifact.txt"


def validate_artifact_content(item: dict) -> None:
    if not item.get("file_name"):
        raise ValueError("Artifact file_name is required.")


def resolve_render_target(file_name: str, declared_format: str | None) -> tuple[str, str]:
    normalized_name = normalize_artifact_file_name(file_name)
    suffix = Path(normalized_name).suffix.replace(".", "").lower()
    requested_format = (declared_format or suffix or "txt").lower()

    if requested_format in TEXT_RENDERED_EXTENSIONS:
        return normalized_name, requested_format

    if requested_format in UNSUPPORTED_BINARY_EXTENSIONS:
        return f"{normalized_name}.md", "md"

    return normalized_name, requested_format


def render_artifacts(output_dir: Path, artifact_contents: list[dict], artifact_plan: list[ArtifactPlanItem] | None = None) -> list[ArtifactRecord]:
    output_dir.mkdir(parents=True, exist_ok=True)
    artifact_requirements = {
        item.artifact_type: item.is_required
        for item in (artifact_plan or [])
    }
    return render_artifact_payloads(output_dir, artifact_contents, artifact_requirements)



def artifact_plan_to_manifest(artifact_plan: list[ArtifactPlanItem]) -> list[dict]:
    return [item.model_dump() for item in artifact_plan]