from pathlib import Path

from ..domain import ArtifactPlanItem, ArtifactRecord, QaResult
from ..renderers.pathing import resolve_render_target


class QaValidator:
    def validate_artifact_outputs(
        self,
        artifact_plan: list[ArtifactPlanItem],
        artifacts: list[ArtifactRecord],
    ) -> QaResult:
        findings: list[str] = []
        technical_findings: list[str] = []

        artifact_by_type = {artifact.artifact_type: artifact for artifact in artifacts}

        for plan_item in artifact_plan:
            artifact = artifact_by_type.get(plan_item.artifact_type)
            if artifact is None:
                if plan_item.is_required:
                    message = f"Missing artifact for planned type: {plan_item.artifact_type}"
                    findings.append(message)
                    technical_findings.append(message)
                continue

            expected_name, expected_format = resolve_render_target(plan_item.file_name, plan_item.file_format)

            if Path(artifact.file_path).name != Path(expected_name).name:
                message = (
                    f"Artifact filename mismatch for {plan_item.artifact_type}: "
                    f"expected {Path(expected_name).name}, got {Path(artifact.file_path).name}"
                )
                findings.append(message)
                technical_findings.append(message)

            if artifact.file_format != expected_format:
                message = (
                    f"Artifact format mismatch for {plan_item.artifact_type}: "
                    f"expected {expected_format}, got {artifact.file_format}"
                )
                findings.append(message)
                technical_findings.append(message)

            if plan_item.is_required and artifact.is_required != plan_item.is_required:
                message = (
                    f"Artifact required flag mismatch for {plan_item.artifact_type}: "
                    f"expected {plan_item.is_required}, got {artifact.is_required}"
                )
                findings.append(message)
                technical_findings.append(message)

            file_path = Path(artifact.file_path)
            if not file_path.exists():
                message = f"Artifact file missing on disk: {file_path}"
                findings.append(message)
                technical_findings.append(message)
                continue

            if artifact.file_format in {"pdf", "xlsx", "zip"}:
                if file_path.stat().st_size <= 0:
                    message = f"Artifact binary file is empty: {file_path}"
                    findings.append(message)
                    technical_findings.append(message)
                continue

            if not file_path.read_text(encoding="utf-8").strip():
                message = f"Artifact file is empty: {file_path}"
                findings.append(message)
                technical_findings.append(message)

        passed = len(technical_findings) == 0
        if passed:
            technical_findings.append("All planned artifacts were generated and validated.")
            findings.append("All planned artifacts were generated and validated.")

        return QaResult(
            passed=passed,
            findings=findings,
            technical_findings=technical_findings,
        )