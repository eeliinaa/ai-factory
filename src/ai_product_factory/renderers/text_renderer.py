from pathlib import Path

from ..domain import TextArtifactSpec
from .pathing import artifact_output_path


def render_text_artifact(output_dir: Path, file_name: str, spec: TextArtifactSpec) -> tuple[Path, str]:
    file_path, rendered_format = artifact_output_path(output_dir, file_name)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(spec.content, encoding="utf-8")
    return file_path, rendered_format