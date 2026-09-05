from pathlib import Path

from ai_product_factory.outputs.batch_report import write_batch_summary


def test_write_batch_summary(tmp_path: Path) -> None:
    path = write_batch_summary(
        tmp_path,
        [
            {"topic": "a", "status": "completed"},
            {"topic": "b", "status": "failed"},
        ],
    )

    assert path.exists()
    content = path.read_text(encoding="utf-8")
    assert '"total_runs": 2' in content
    assert '"completed_runs": 1' in content
    assert '"failed_runs": 1' in content
