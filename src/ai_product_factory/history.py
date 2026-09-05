import json
from typing import Any


def format_runs_list(runs: list[dict[str, Any]]) -> str:
    if not runs:
        return "No runs found."
    lines = ["Runs", "===="]
    for run in runs:
        lines.append(
            f"- {run['id']} | {run['status']} | {run['topic']} | cost={run['total_cost']} | created={run['created_at']}"
        )
    return "\n".join(lines)


def format_run_detail(run: dict[str, Any]) -> str:
    lines = ["Run Detail", "=========="]
    lines.append(f"ID: {run['id']}")
    lines.append(f"Topic: {run['topic']}")
    lines.append(f"Status: {run['status']}")
    lines.append(f"Created: {run['created_at']}")
    lines.append(f"Output: {run['output_path']}")
    lines.append(f"Total cost: {run['total_cost']}")
    lines.append(f"Selected product type: {run.get('selected_product_type')}")
    if run.get("selected_product"):
        lines.append(f"Selected product: {run['selected_product'].get('product_title')}")
    if run.get("listing"):
        lines.append(f"Listing title: {run['listing'].get('title')}")
    lines.append(f"Artifacts: {len(run.get('artifacts', []))}")
    return "\n".join(lines)


def format_run_comparison(runs: list[dict[str, Any]]) -> str:
    if not runs:
        return "No runs found for comparison."
    lines = ["Run Comparison", "=============="]
    for run in runs:
        lines.append(
            f"- {run['id']} | {run['status']} | {run['topic']} | "
            f"selected={run.get('product_title') or 'N/A'} | "
            f"type={run.get('product_type') or 'N/A'} | "
            f"score={run.get('selected_score')} | cost={run['total_cost']} | artifacts={run.get('artifact_count', 0)}"
        )
    return "\n".join(lines)


def format_best_runs(runs: list[dict[str, Any]]) -> str:
    if not runs:
        return "No successful runs found."
    lines = ["Best Runs", "========="]
    for run in runs:
        lines.append(
            f"- {run['id']} | {run['topic']} | selected={run.get('product_title') or 'N/A'} | "
            f"score={run.get('selected_score')} | cost={run['total_cost']} | created={run['created_at']}"
        )
    return "\n".join(lines)


def format_json(data: Any) -> str:
    return json.dumps(data, indent=2)
