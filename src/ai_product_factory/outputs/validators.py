from pathlib import Path

from ..domain import ArtifactRecord


BINARY_FORMATS = {"pdf", "xlsx", "zip", "png", "jpg", "jpeg"}


def validate_artifact_records(artifacts: list[ArtifactRecord]) -> list[str]:
    findings: list[str] = []
    for artifact in artifacts:
        path = Path(artifact.file_path)

        if not path.exists():
            findings.append(f"Missing artifact file: {artifact.file_path}")
            continue

        if path.suffix.replace(".", "").lower() != artifact.file_format:
            findings.append(f"Format mismatch for artifact: {artifact.file_path}")
            continue

        if artifact.file_format in BINARY_FORMATS:
            if path.stat().st_size <= 0:
                findings.append(f"Empty artifact file: {artifact.file_path}")
            continue

        content = path.read_text(encoding="utf-8")
        if not content.strip():
            findings.append(f"Empty artifact file: {artifact.file_path}")

    return findings