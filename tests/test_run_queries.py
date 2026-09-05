from pathlib import Path

from ai_product_factory.db import initialize_database
from ai_product_factory.domain import ListingDraft, ProductType, Run, RunContext, RunStatus, SelectedProduct
from ai_product_factory.storage import SQLiteRepository


def make_run(run_id: str, topic: str, status: RunStatus, output_path: Path, total_cost: float = 0.0) -> RunContext:
    run = Run(
        id=run_id,
        topic=topic,
        status=status,
        output_path=output_path,
        total_cost=total_cost,
        selected_product_type=ProductType.TEMPLATE_BUNDLE if status == RunStatus.COMPLETED else None,
    )
    return RunContext(run=run)


def test_list_runs_filters_and_limits(tmp_path: Path) -> None:
    db_path = tmp_path / "app.db"
    initialize_database(db_path)
    repo = SQLiteRepository(db_path)

    repo.save_run(make_run("run-1", "etsy planners", RunStatus.COMPLETED, tmp_path / "r1", 1.2))
    repo.save_run(make_run("run-2", "wedding checklists", RunStatus.FAILED, tmp_path / "r2", 0.4))

    runs = repo.list_runs(limit=1)
    assert len(runs) == 1

    completed = repo.list_runs(limit=10, status="completed")
    assert len(completed) == 1
    assert completed[0]["id"] == "run-1"

    filtered = repo.list_runs(limit=10, topic_contains="wedding")
    assert len(filtered) == 1
    assert filtered[0]["id"] == "run-2"


def test_get_run_details_returns_related_records(tmp_path: Path) -> None:
    db_path = tmp_path / "app.db"
    initialize_database(db_path)
    repo = SQLiteRepository(db_path)

    run_context = make_run("run-1", "etsy planners", RunStatus.COMPLETED, tmp_path / "r1", 1.2)
    repo.save_run(run_context)
    repo.save_selected_product(
        "run-1",
        SelectedProduct(
            candidate_id="candidate-1",
            product_type=ProductType.TEMPLATE_BUNDLE,
            product_title="Planner Pack",
            product_summary="summary",
            buyer_problem="problem",
            solution_promise="promise",
            packaging_strategy="bundle",
        ),
    )
    repo.save_listing(
        "run-1",
        ListingDraft(title="Planner Pack", description="desc", tags=["planner"]),
    )

    details = repo.get_run_details("run-1")

    assert details is not None
    assert details["selected_product"]["product_title"] == "Planner Pack"
    assert details["listing"]["title"] == "Planner Pack"
