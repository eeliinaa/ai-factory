from pathlib import Path
import re


TEXT_RENDERED_EXTENSIONS = {"md", "txt", "json", "csv", "html"}
UNSUPPORTED_BINARY_EXTENSIONS = {"png", "jpg", "jpeg", "canva"}


def normalize_artifact_file_name(file_name: str) -> str:
    cleaned = file_name.strip().replace(" ", "_")
    cleaned = re.sub(r"[^A-Za-z0-9._/~-]", "_", cleaned)
    cleaned = re.sub(r"/+", "/", cleaned).strip("/")
    return cleaned or "artifact.txt"


def resolve_render_target(file_name: str, declared_format: str | None) -> tuple[str, str]:
    normalized_name = normalize_artifact_file_name(file_name)
    suffix = Path(normalized_name).suffix.replace(".", "").lower()
    requested_format = (declared_format or suffix or "txt").lower()

    if requested_format in TEXT_RENDERED_EXTENSIONS:
        return normalized_name, requested_format

    if requested_format in UNSUPPORTED_BINARY_EXTENSIONS:
        return f"{normalized_name}.md", "md"

    return normalized_name, requested_format


def artifact_output_path(output_dir: Path, file_name: str, declared_format: str | None = None) -> tuple[Path, str]:
    resolved_name, resolved_format = resolve_render_target(file_name, declared_format)
    return output_dir / resolved_name, resolved_format