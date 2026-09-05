import json
from datetime import datetime
from pathlib import Path


def write_batch_summary(output_dir: Path, results: list[dict]) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = output_dir / "batch-summary.json"
    summary = {
        "generated_at": datetime.utcnow().isoformat(),
        "total_runs": len(results),
        "completed_runs": sum(1 for item in results if item["status"] == "completed"),
        "failed_runs": sum(1 for item in results if item["status"] == "failed"),
        "results": results,
    }
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary_path
