from ai_product_factory.core.stage_executor import StructuredStageExecutor
from ai_product_factory.core.errors import StructuredOutputError
from ai_product_factory.domain import StageParseResult, WorkflowStage
from ai_product_factory.providers import LLMResponse


def test_stage_executor_success_on_first_try() -> None:
    executor = StructuredStageExecutor(max_retries=1)
    metadata: dict[str, dict] = {}

    payload = executor.execute(
        WorkflowStage.RESEARCH,
        generator=lambda attempt: LLMResponse(model="m", content='{"ok": true}', metadata={"attempt": attempt, "mode": "live"}),
        parser=lambda content: StageParseResult(parsed=True, payload={"ok": True}),
        stage_metadata=metadata,
    )

    assert payload["ok"] is True
    assert metadata[WorkflowStage.RESEARCH.value]["attempt"] == 1
    assert metadata[WorkflowStage.RESEARCH.value]["parsed_successfully"] is True


def test_stage_executor_retries_then_succeeds() -> None:
    executor = StructuredStageExecutor(max_retries=1)
    metadata: dict[str, dict] = {}

    def generator(attempt: int) -> LLMResponse:
        return LLMResponse(model="m", content=str(attempt), metadata={"attempt": attempt, "mode": "live"})

    def parser(content: str) -> StageParseResult:
        if content == "1":
            return StageParseResult(parsed=False, error="bad json")
        return StageParseResult(parsed=True, payload={"attempt": int(content)})

    payload = executor.execute(WorkflowStage.RESEARCH, generator, parser, metadata)

    assert payload["attempt"] == 2
    assert metadata[WorkflowStage.RESEARCH.value]["attempt"] == 2
    assert metadata[WorkflowStage.RESEARCH.value]["parsed_successfully"] is True


def test_stage_executor_raises_after_all_retries() -> None:
    executor = StructuredStageExecutor(max_retries=1)
    metadata: dict[str, dict] = {}

    try:
        executor.execute(
            WorkflowStage.RESEARCH,
            generator=lambda attempt: LLMResponse(model="m", content="bad", metadata={"attempt": attempt, "mode": "live"}),
            parser=lambda content: StageParseResult(parsed=False, error="still bad"),
            stage_metadata=metadata,
        )
    except StructuredOutputError as exc:
        assert "after 2 attempts" in str(exc)
    else:
        raise AssertionError("StructuredOutputError was not raised")
