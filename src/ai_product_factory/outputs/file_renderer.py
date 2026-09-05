from pathlib import Path
import re

from ..domain import ArtifactPlanItem, ArtifactRecord, ArtifactGenerationStatus


TEXT_RENDERED_EXTENSIONS = {"md", "txt", "json", "csv", "html"}
UNSUPPORTED_BINARY_EXTENSIONS = {"pdf", "png", "jpg", "jpeg", "zip", "canva"}


def normalize_artifact_file_name(file_name: str) -> str:
    cleaned = file_name.strip().replace(" ", "_")
    cleaned = re.sub(r"[^A-Za-z0-9._/~-]", "_", cleaned)
    cleaned = re.sub(r"/+", "/", cleaned).strip("/")
    return cleaned or "artifact.txt"


def validate_artifact_content(item: dict) -> None:
    if not item.get("file_name"):
        raise ValueError("Artifact file_name is required.")
    if not item.get("content") or not item["content"].strip():
        raise ValueError(f"Artifact content is empty for {item['file_name']}")


def resolve_render_target(file_name: str, declared_format: str | None) -> tuple[str, str]:
    normalized_name = normalize_artifact_file_name(file_name)
    suffix = Path(normalized_name).suffix.replace(".", "").lower()
    requested_format = (declared_format or suffix or "txt").lower()

    if requested_format in TEXT_RENDERED_EXTENSIONS:
        return normalized_name, requested_format

    if requested_format in UNSUPPORTED_BINARY_EXTENSIONS:
        return f"{normalized_name}.md", "md"

    if suffix in TEXT_RENDERED_EXTENSIONS:
        return normalized_name, suffix

    return f"{normalized_name}.txt", "txt"


def render_artifacts(output_dir: Path, artifact_contents: list[dict]) -> list[ArtifactRecord]:
    output_dir.mkdir(parents=True, exist_ok=True)
    artifact_records: list[ArtifactRecord] = []

    for item in artifact_contents:
        validate_artifact_content(item)
        render_name, rendered_format = resolve_render_target(item["file_name"], item.get("file_format"))
        file_path = output_dir / render_name
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(item["content"], encoding="utf-8")
        artifact_records.append(
            ArtifactRecord(
                artifact_type=item["artifact_type"],
                file_path=file_path,
                file_format=rendered_format,
                is_required=item.get("is_required", True),
                generation_status=ArtifactGenerationStatus.GENERATED,
            )
        )

    return artifact_records



def artifact_plan_to_manifest(artifact_plan: list[ArtifactPlanItem]) -> list[dict]:
    return [item.model_dump() for item in artifact_plan]