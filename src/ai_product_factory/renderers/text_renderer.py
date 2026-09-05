from pathlib import Path

from ..domain import TextArtifactSpec
from ..outputs.file_renderer import normalize_artifact_file_name


def render_text_artifact(output_dir: Path, file_name: str, spec: TextArtifactSpec) -> tuple[Path, str]:
    normalized_name = normalize_artifact_file_name(file_name)
    file_path = output_dir / normalized_name
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(spec.content, encoding="utf-8")
    rendered_format = Path(normalized_name).suffix.replace(".", "").lower() or "txt"
    return file_path, rendered_format