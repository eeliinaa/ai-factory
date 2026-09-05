from typing import Callable

from ..core.errors import StructuredOutputError
from ..domain import StageParseResult, WorkflowStage
from ..providers import LLMResponse


class StructuredStageExecutor:
    def __init__(self, max_retries: int = 1) -> None:
        self.max_retries = max_retries

    def execute(
        self,
        stage: WorkflowStage,
        generator: Callable[[int], LLMResponse],
        parser: Callable[[str], StageParseResult],
        stage_metadata: dict[str, dict],
    ) -> dict:
        last_error: str | None = None

        for attempt in range(1, self.max_retries + 2):
            response = generator(attempt)
            parsed = parser(response.content)
            stage_metadata[stage.value] = {
                "model": response.model,
                "mode": response.metadata.get("mode"),
                "prompt_version": response.metadata.get("prompt_version"),
                "attempt": response.metadata.get("attempt", attempt),
                "prompt_tokens": response.prompt_tokens,
                "completion_tokens": response.completion_tokens,
                "estimated_cost": response.estimated_cost,
                "parsed_successfully": parsed.parsed,
                "error": parsed.error,
            }
            if parsed.parsed:
                return parsed.payload
            last_error = parsed.error

        raise StructuredOutputError(
            f"Structured output parsing failed for stage '{stage.value}' after {self.max_retries + 1} attempts: {last_error}"
        )
