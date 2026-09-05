from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    app_env: str = Field(default="development", alias="APP_ENV")
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    openai_base_url: str | None = Field(default=None, alias="OPENAI_BASE_URL")
    openai_timeout_seconds: float = Field(default=180.0, alias="OPENAI_TIMEOUT_SECONDS")
    ai_structured_output_retries: int = Field(default=1, alias="AI_PRODUCT_FACTORY_STRUCTURED_OUTPUT_RETRIES")
    ai_allow_placeholder_fallback: bool = Field(default=True, alias="AI_PRODUCT_FACTORY_ALLOW_PLACEHOLDER_FALLBACK")
    db_path: Path = Field(default=Path("data/sqlite/app.db"), alias="AI_PRODUCT_FACTORY_DB_PATH")
    runs_dir: Path = Field(default=Path("data/runs"), alias="AI_PRODUCT_FACTORY_RUNS_DIR")
    max_total_cost: float = Field(default=10.0, alias="AI_PRODUCT_FACTORY_MAX_TOTAL_COST")
    max_research_cost: float = Field(default=4.0, alias="AI_PRODUCT_FACTORY_MAX_RESEARCH_COST")
    max_product_creation_cost: float = Field(default=4.0, alias="AI_PRODUCT_FACTORY_MAX_PRODUCT_CREATION_COST")
    max_listing_preview_cost: float = Field(default=2.0, alias="AI_PRODUCT_FACTORY_MAX_LISTING_PREVIEW_COST")
    max_refinement_cycles: int = Field(default=2, alias="AI_PRODUCT_FACTORY_MAX_REFINEMENT_CYCLES")
    default_model: str = Field(default="gpt-5-mini", alias="AI_PRODUCT_FACTORY_DEFAULT_MODEL")
    research_model: str | None = Field(default=None, alias="AI_PRODUCT_FACTORY_RESEARCH_MODEL")
    evaluation_model: str | None = Field(default=None, alias="AI_PRODUCT_FACTORY_EVALUATION_MODEL")
    product_creation_model: str | None = Field(default=None, alias="AI_PRODUCT_FACTORY_PRODUCT_CREATION_MODEL")
    listing_model: str | None = Field(default=None, alias="AI_PRODUCT_FACTORY_LISTING_MODEL")
    qa_model: str | None = Field(default=None, alias="AI_PRODUCT_FACTORY_QA_MODEL")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        populate_by_name=True,
        extra="ignore",
    )

    def validate_runtime_configuration(self) -> None:
        if self.app_env == "production" and not self.openai_api_key and self.ai_allow_placeholder_fallback:
            raise ValueError("Placeholder fallback must be disabled or OPENAI_API_KEY must be set in production.")
