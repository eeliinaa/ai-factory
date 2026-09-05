from pathlib import Path

from ai_product_factory.db import initialize_database
from ai_product_factory.domain import (
    CandidateRecommendationStatus,
    CandidateScore,
    ListingDraft,
    ProductType,
    Run,
    RunContext,
    RunStatus,
    SelectedProduct,
)
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


def test_compare_runs_returns_scores_and_artifact_counts(tmp_path: Path) -> None:
    db_path = tmp_path / "app.db"
    initialize_database(db_path)
    repo = SQLiteRepository(db_path)

    repo.save_run(make_run("run-1", "etsy planners", RunStatus.COMPLETED, tmp_path / "r1", 1.2))
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
    repo.save_scores(
        "run-1",
        [
            CandidateScore(
                candidate_id="candidate-1",
                demand_score=7,
                competition_score=6,
                production_speed_score=8,
                price_potential_score=7,
                series_potential_score=8,
                automation_fit_score=8,
                weighted_final_score=7.5,
                recommendation_status=CandidateRecommendationStatus.SELECTED,
                risk_notes="ok",
            )
        ],
    )

    rows = repo.compare_runs(["run-1"])

    assert len(rows) == 1
    assert rows[0]["product_title"] == "Planner Pack"
    assert rows[0]["selected_score"] == 7.5


def test_list_best_runs_sorts_by_score(tmp_path: Path) -> None:
    db_path = tmp_path / "app.db"
    initialize_database(db_path)
    repo = SQLiteRepository(db_path)

    for run_id, topic, cost, score in [
        ("run-1", "topic a", 1.0, 7.5),
        ("run-2", "topic b", 0.8, 8.2),
    ]:
        repo.save_run(make_run(run_id, topic, RunStatus.COMPLETED, tmp_path / run_id, cost))
        repo.save_selected_product(
            run_id,
            SelectedProduct(
                candidate_id=f"candidate-{run_id}",
                product_type=ProductType.TEMPLATE_BUNDLE,
                product_title=f"Product {run_id}",
                product_summary="summary",
                buyer_problem="problem",
                solution_promise="promise",
                packaging_strategy="bundle",
            ),
        )
        repo.save_scores(
            run_id,
            [
                CandidateScore(
                    candidate_id=f"candidate-{run_id}",
                    demand_score=7,
                    competition_score=6,
                    production_speed_score=8,
                    price_potential_score=7,
                    series_potential_score=8,
                    automation_fit_score=8,
                    weighted_final_score=score,
                    recommendation_status=CandidateRecommendationStatus.SELECTED,
                    risk_notes="ok",
                )
            ],
        )

    rows = repo.list_best_runs(limit=10, sort_by="score")

    assert rows[0]["id"] == "run-2"
    assert rows[1]["id"] == "run-1"
