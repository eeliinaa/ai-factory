from ai_product_factory.history import format_best_runs, format_run_comparison, format_run_detail, format_runs_list


def test_format_runs_list_empty() -> None:
    assert format_runs_list([]) == "No runs found."


def test_format_run_detail_includes_core_fields() -> None:
    rendered = format_run_detail(
        {
            "id": "run-1",
            "topic": "etsy planners",
            "status": "completed",
            "created_at": "2026-01-01T00:00:00",
            "output_path": "data/runs/run_etsy_planners",
            "total_cost": 1.25,
            "selected_product_type": "TEMPLATE_BUNDLE",
            "selected_product": {"product_title": "Planner Pack"},
            "listing": {"title": "Planner Pack"},
            "artifacts": [],
        }
    )

    assert "Run Detail" in rendered
    assert "Planner Pack" in rendered


def test_format_run_comparison_includes_score() -> None:
    rendered = format_run_comparison(
        [
            {
                "id": "run-1",
                "status": "completed",
                "topic": "etsy planners",
                "product_title": "Planner Pack",
                "product_type": "TEMPLATE_BUNDLE",
                "selected_score": 7.5,
                "total_cost": 1.2,
                "artifact_count": 3,
            }
        ]
    )

    assert "Run Comparison" in rendered
    assert "score=7.5" in rendered


def test_format_best_runs_includes_product() -> None:
    rendered = format_best_runs(
        [
            {
                "id": "run-1",
                "topic": "etsy planners",
                "product_title": "Planner Pack",
                "selected_score": 7.5,
                "total_cost": 1.2,
                "created_at": "2026-01-01T00:00:00",
            }
        ]
    )

    assert "Best Runs" in rendered
    assert "Planner Pack" in rendered
