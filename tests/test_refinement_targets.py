from ai_product_factory.core.refinement import extract_refinement_targets, should_continue_refinement


def test_extract_refinement_targets_from_findings() -> None:
    targets = extract_refinement_targets([
        "Missing artifact: guide.md",
        "Empty artifact: checklist.md",
    ])

    assert len(targets) == 2
    assert targets[0].artifact_name == "guide.md"
    assert targets[0].reason == "missing_artifact"
    assert targets[1].artifact_name == "checklist.md"
    assert targets[1].reason == "empty_artifact"


def test_should_continue_refinement_stops_on_no_progress() -> None:
    decision = should_continue_refinement(
        previous_findings=["Missing artifact: guide.md"],
        current_findings=["Missing artifact: guide.md"],
        cycle=1,
        max_cycles=3,
    )

    assert decision.should_continue is False
    assert decision.stop_reason == "no_progress"


def test_should_continue_refinement_continues_when_findings_change() -> None:
    decision = should_continue_refinement(
        previous_findings=["Missing artifact: guide.md"],
        current_findings=["Empty artifact: guide.md"],
        cycle=1,
        max_cycles=3,
    )

    assert decision.should_continue is True
    assert decision.stop_reason == "continue"
