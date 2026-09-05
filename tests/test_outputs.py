from pathlib import Path

import pytest

from ai_product_factory.outputs import (
    build_output_package,
    normalize_artifact_file_name,
    render_artifacts,
    validate_artifact_content,
    validate_artifact_records,
)


def test_normalize_artifact_file_name() -> None:
    assert normalize_artifact_file_name(" My File!.md ") == "My_File_.md"



def test_validate_artifact_content_rejects_empty() -> None:
    with pytest.raises(ValueError):
        validate_artifact_content({"file_name": "a.md", "content": "   "})



def test_render_artifacts_normalizes_name(tmp_path: Path) -> None:
    records = render_artifacts(
        tmp_path,
        [{"artifact_type": "guide", "file_name": " My File!.md ", "content": "hello"}],
    )

    assert records[0].file_path.name == "My_File_.md"
    assert records[0].file_path.exists()



def test_validate_artifact_records_detects_missing_and_empty(tmp_path: Path) -> None:
    records = render_artifacts(
        tmp_path,
        [{"artifact_type": "guide", "file_name": "guide.md", "content": "hello"}],
    )
    records[0].file_path.write_text("", encoding="utf-8")

    findings = validate_artifact_records(records)

    assert findings
    assert "Empty artifact file" in findings[0]



def test_build_output_package_writes_summary(tmp_path: Path) -> None:
    records = render_artifacts(
        tmp_path,
        [{"artifact_type": "guide", "file_name": "guide.md", "content": "hello"}],
    )

    package_path, manifest_path = build_output_package(tmp_path, records, [])

    assert manifest_path.exists()
    assert (package_path / "PACKAGE_SUMMARY.md").exists()
