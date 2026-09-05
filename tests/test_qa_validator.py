from pathlib import Path

from ai_product_factory.core.qa_validator import QaValidator
from ai_product_factory.domain import ArtifactGenerationStatus, ArtifactPlanItem, ArtifactRecord


def test_validate_artifact_outputs_pass(tmp_path: Path) -> None:
    validator = QaValidator()
    artifact_path = tmp_path / "guide.md"
    artifact_path.write_text("hello", encoding="utf-8")

    result = validator.validate_artifact_outputs(
        artifact_plan=[
            ArtifactPlanItem(
                artifact_type="buyer_guide",
                file_name="guide.md",
                file_format="md",
                purpose="guide",
                generation_instructions="write guide",
            )
        ],
        artifacts=[
            ArtifactRecord(
                artifact_type="buyer_guide",
                file_path=artifact_path,
                file_format="md",
                generation_status=ArtifactGenerationStatus.GENERATED,
            )
        ],
    )

    assert result.passed is True
    assert "All planned artifacts were generated and validated." in result.findings


def test_validate_artifact_outputs_missing_artifact(tmp_path: Path) -> None:
    validator = QaValidator()

    result = validator.validate_artifact_outputs(
        artifact_plan=[
            ArtifactPlanItem(
                artifact_type="buyer_guide",
                file_name="guide.md",
                file_format="md",
                purpose="guide",
                generation_instructions="write guide",
            )
        ],
        artifacts=[],
    )

    assert result.passed is False
    assert any("Missing artifact" in finding for finding in result.findings)
