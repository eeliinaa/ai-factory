import json
import zipfile
from pathlib import Path

from .file_renderer import artifact_plan_to_manifest
from .validators import validate_artifact_records
from ..domain import ArtifactPlanItem, ArtifactRecord


PACKAGE_DIR_NAME = "package-ready"
PACKAGE_SUMMARY_NAME = "PACKAGE_SUMMARY.md"
DELIVERABLE_ZIP_NAME = "deliverables.zip"


def build_package_summary(artifacts: list[ArtifactRecord], validation_findings: list[str]) -> str:
    lines = ["# Package Summary", "", f"Artifacts: {len(artifacts)}", ""]
    if validation_findings:
        lines.append("## Validation Findings")
        lines.extend(f"- {finding}" for finding in validation_findings)
    else:
        lines.append("## Validation Findings")
        lines.append("- None")
    return "\n".join(lines) + "\n"


def _copy_artifacts_into_package(package_path: Path, artifacts: list[ArtifactRecord]) -> list[str]:
    copied_files: list[str] = []
    for artifact in artifacts:
        source = Path(artifact.file_path)
        if not source.exists() or source.is_dir():
            continue
        destination = package_path / source.name
        destination.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
        copied_files.append(destination.name)
    return copied_files


def _build_zip_archive(package_path: Path) -> Path:
    zip_path = package_path / DELIVERABLE_ZIP_NAME
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for file_path in sorted(package_path.rglob("*")):
            if file_path.is_dir() or file_path == zip_path:
                continue
            archive.write(file_path, arcname=file_path.relative_to(package_path))
    return zip_path



def build_output_package(
    output_dir: Path,
    artifacts: list[ArtifactRecord],
    artifact_plan: list[ArtifactPlanItem],
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "manifest.json"
    package_path = output_dir / PACKAGE_DIR_NAME
    package_path.mkdir(parents=True, exist_ok=True)

    validation_findings = validate_artifact_records(artifacts)
    copied_files = _copy_artifacts_into_package(package_path, artifacts)
    zip_path = _build_zip_archive(package_path)
    manifest = {
        "artifact_plan": artifact_plan_to_manifest(artifact_plan),
        "artifacts": [
            {
                "artifact_type": artifact.artifact_type,
                "file_path": str(artifact.file_path),
                "file_format": artifact.file_format,
                "is_required": artifact.is_required,
                "generation_status": artifact.generation_status.value,
            }
            for artifact in artifacts
        ],
        "validation_findings": validation_findings,
        "package": {
            "package_path": str(package_path),
            "zip_path": str(zip_path),
            "copied_files": copied_files,
        },
    }
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (package_path / PACKAGE_SUMMARY_NAME).write_text(
        build_package_summary(artifacts, validation_findings),
        encoding="utf-8",
    )
    return package_path, manifest_path