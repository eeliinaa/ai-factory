from pathlib import Path

from ai_product_factory.config import AppSettings
from ai_product_factory.core import AIService, QaValidationError
from ai_product_factory.pipeline import PipelineRunner
from ai_product_factory.providers import ModelPolicy, OpenAIProvider


class FailingOnceQaRunner(PipelineRunner):
    def __init__(self, settings, context_text, ai_service):
        super().__init__(settings, context_text, ai_service)
        self.qa_calls = 0

    def run_qa_stage(self, state, artifact_plan, artifacts, stage_metadata):
        self.qa_calls += 1
        if self.qa_calls == 1:
            raise QaValidationError("forced QA failure")
        return super().run_qa_stage(state, artifact_plan, artifacts, stage_metadata)


class AlwaysFailQaRunner(PipelineRunner):
    def run_qa_stage(self, state, artifact_plan, artifacts, stage_metadata):
        raise QaValidationError("always failing QA")


class NoProgressQaRunner(PipelineRunner):
    def run_qa_stage(self, state, artifact_plan, artifacts, stage_metadata):
        raise QaValidationError("Missing artifact: guide.md")



def test_refinement_retries_after_qa_failure(tmp_path: Path) -> None:
    settings = AppSettings(
        APP_ENV="development",
        OPENAI_API_KEY=None,
        AI_PRODUCT_FACTORY_DB_PATH=tmp_path / "app.db",
        AI_PRODUCT_FACTORY_RUNS_DIR=tmp_path / "runs",
        AI_PRODUCT_FACTORY_ALLOW_PLACEHOLDER_FALLBACK=True,
        AI_PRODUCT_FACTORY_MAX_REFINEMENT_CYCLES=1,
    )
    provider = OpenAIProvider(api_key=None, allow_placeholder_fallback=True)
    model_policy = ModelPolicy(settings)
    ai_service = AIService(provider=provider, model_policy=model_policy, structured_output_retries=1)
    runner = FailingOnceQaRunner(settings, context_text="context", ai_service=ai_service)

    result = runner.run(topic="professional workflow products")

    assert result["run_context"].run.status.value == "completed"
    assert result["refinement_stop_reason"] == "qa_passed"
    assert runner.qa_calls == 2
    assert result["refinement_history"]



def test_refinement_stops_after_max_cycles(tmp_path: Path) -> None:
    settings = AppSettings(
        APP_ENV="development",
        OPENAI_API_KEY=None,
        AI_PRODUCT_FACTORY_DB_PATH=tmp_path / "app.db",
        AI_PRODUCT_FACTORY_RUNS_DIR=tmp_path / "runs",
        AI_PRODUCT_FACTORY_ALLOW_PLACEHOLDER_FALLBACK=True,
        AI_PRODUCT_FACTORY_MAX_REFINEMENT_CYCLES=1,
    )
    provider = OpenAIProvider(api_key=None, allow_placeholder_fallback=True)
    model_policy = ModelPolicy(settings)
    ai_service = AIService(provider=provider, model_policy=model_policy, structured_output_retries=1)
    runner = AlwaysFailQaRunner(settings, context_text="context", ai_service=ai_service)

    result = runner.run(topic="professional workflow products")

    assert result["run_context"].run.status.value == "failed"
    assert result["refinement_stop_reason"] == "max_refinement_cycles_reached"



def test_refinement_stops_on_no_progress(tmp_path: Path) -> None:
    settings = AppSettings(
        APP_ENV="development",
        OPENAI_API_KEY=None,
        AI_PRODUCT_FACTORY_DB_PATH=tmp_path / "app.db",
        AI_PRODUCT_FACTORY_RUNS_DIR=tmp_path / "runs",
        AI_PRODUCT_FACTORY_ALLOW_PLACEHOLDER_FALLBACK=True,
        AI_PRODUCT_FACTORY_MAX_REFINEMENT_CYCLES=3,
    )
    provider = OpenAIProvider(api_key=None, allow_placeholder_fallback=True)
    model_policy = ModelPolicy(settings)
    ai_service = AIService(provider=provider, model_policy=model_policy, structured_output_retries=1)
    runner = NoProgressQaRunner(settings, context_text="context", ai_service=ai_service)

    result = runner.run(topic="professional workflow products")

    assert result["run_context"].run.status.value == "failed"
    assert result["refinement_stop_reason"] == "no_progress"
