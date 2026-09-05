from pathlib import Path

from ai_product_factory.config import AppSettings
from ai_product_factory.core import AIService
from ai_product_factory.pipeline import PipelineRunner
from ai_product_factory.providers import ModelPolicy, OpenAIProvider


def test_pipeline_smoke_placeholder_mode(tmp_path: Path) -> None:
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
    runner = PipelineRunner(settings, context_text="context", ai_service=ai_service)

    result = runner.run(topic="professional workflow products")

    assert result["run_context"].run.status.value == "completed"
    assert result["artifacts"]
    assert Path(result["packaging"].manifest_path).exists()
    assert Path(result["report_path"]).exists()
    assert result["refinement_cycles_used"] >= 0
