import json
from pathlib import Path

from ..core import PipelineState
from ..domain import ArtifactPlanItem, ArtifactRecord, ListingDraft, PackagingResult, QaResult, RunContext, SelectedProduct


def write_run_report(
    output_dir: Path,
    run_context: RunContext,
    state: PipelineState,
    selected_product: SelectedProduct | None,
    listing: ListingDraft | None,
    qa_result: QaResult | None,
    packaging: PackagingResult | None,
    artifacts: list[ArtifactRecord],
    artifact_plan: list[ArtifactPlanItem],
    stage_metadata: dict[str, dict] | None = None,
    final_outcome_reason: str | None = None,
    environment: str | None = None,
    refinement_cycles_used: int = 0,
    refinement_stop_reason: str | None = None,
    refinement_history: list[dict] | None = None,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / "run-report.json"
    report = {
        "run": {
            "id": run_context.run.id,
            "topic": run_context.run.topic,
            "status": run_context.run.status.value,
            "created_at": run_context.run.created_at.isoformat(),
            "output_path": str(run_context.run.output_path),
            "total_cost": run_context.run.total_cost,
            "selected_product_type": (
                run_context.run.selected_product_type.value if run_context.run.selected_product_type else None
            ),
        },
        "environment": environment,
        "final_outcome_reason": final_outcome_reason,
        "refinement_cycles_used": refinement_cycles_used,
        "refinement_stop_reason": refinement_stop_reason,
        "refinement_history": refinement_history or [],
        "completed_stages": [stage.value for stage in state.completed_stages],
        "failures": state.failures,
        "budget": {
            "spent_total": state.budget.spent_total,
            "spent_by_stage": state.budget.spent_by_stage,
            "total_limit": state.budget.total_limit,
            "research_limit": state.budget.research_limit,
            "product_creation_limit": state.budget.product_creation_limit,
            "listing_preview_limit": state.budget.listing_preview_limit,
        },
        "selected_product": selected_product.model_dump() if selected_product else None,
        "listing": listing.model_dump() if listing else None,
        "qa": qa_result.model_dump() if qa_result else None,
        "packaging": packaging.model_dump() if packaging else None,
        "artifact_plan": [item.model_dump() for item in artifact_plan],
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
        "stage_metadata": stage_metadata or {},
    }
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report_path
