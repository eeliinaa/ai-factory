from pathlib import Path

from ..domain import ArtifactPlanItem, ArtifactRecord
from ..renderers import render_artifact_payloads
from ..renderers.pathing import resolve_render_target


def validate_artifact_content(item: dict) -> None:
    if not item.get("file_name"):
        raise ValueError("Artifact file_name is required.")


def render_artifacts(output_dir: Path, artifact_contents: list[dict], artifact_plan: list[ArtifactPlanItem] | None = None) -> list[ArtifactRecord]:
    output_dir.mkdir(parents=True, exist_ok=True)
    artifact_requirements = {
        item.artifact_type: item.is_required
        for item in (artifact_plan or [])
    }
    return render_artifact_payloads(output_dir, artifact_contents, artifact_requirements)



def artifact_plan_to_manifest(artifact_plan: list[ArtifactPlanItem]) -> list[dict]:
    return [item.model_dump() for item in artifact_plan]