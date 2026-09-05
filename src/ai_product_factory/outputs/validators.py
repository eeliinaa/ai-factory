from pathlib import Path

from ..domain import ArtifactRecord


def validate_artifact_records(artifacts: list[ArtifactRecord]) -> list[str]:
    findings: list[str] = []
    for artifact in artifacts:
        if not Path(artifact.file_path).exists():
            findings.append(f"Missing artifact file: {artifact.file_path}")
            continue
        if Path(artifact.file_path).suffix.replace(".", "") != artifact.file_format:
            findings.append(f"Format mismatch for artifact: {artifact.file_path}")
        content = Path(artifact.file_path).read_text(encoding="utf-8")
        if not content.strip():
            findings.append(f"Empty artifact file: {artifact.file_path}")
    return findings
