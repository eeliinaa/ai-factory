from pathlib import Path

from pydantic import BaseModel, Field

from ..domain import WorkflowStage


class BudgetSnapshot(BaseModel):
    total_limit: float
    research_limit: float
    product_creation_limit: float
    listing_preview_limit: float
    spent_total: float = 0.0
    spent_by_stage: dict[str, float] = Field(default_factory=dict)

    def register_spend(self, stage: WorkflowStage, amount: float) -> None:
        self.spent_total += amount
        key = stage.value
        self.spent_by_stage[key] = self.spent_by_stage.get(key, 0.0) + amount

    def assert_within_limits(self, stage: WorkflowStage) -> None:
        if self.spent_total > self.total_limit:
            raise ValueError("Total budget limit exceeded.")

        if stage == WorkflowStage.RESEARCH and self.spent_by_stage.get(stage.value, 0.0) > self.research_limit:
            raise ValueError("Research budget limit exceeded.")

        if stage in {WorkflowStage.PRODUCT_ARCHITECTURE, WorkflowStage.PRODUCT_CREATION}:
            spent = self.spent_by_stage.get(WorkflowStage.PRODUCT_ARCHITECTURE.value, 0.0) + self.spent_by_stage.get(
                WorkflowStage.PRODUCT_CREATION.value, 0.0
            )
            if spent > self.product_creation_limit:
                raise ValueError("Product creation budget limit exceeded.")

        if stage in {WorkflowStage.LISTING, WorkflowStage.PREVIEW}:
            spent = self.spent_by_stage.get(WorkflowStage.LISTING.value, 0.0) + self.spent_by_stage.get(
                WorkflowStage.PREVIEW.value, 0.0
            )
            if spent > self.listing_preview_limit:
                raise ValueError("Listing/preview budget limit exceeded.")


class PipelineState(BaseModel):
    topic: str
    context_text: str
    current_stage: WorkflowStage = WorkflowStage.INPUT
    completed_stages: list[WorkflowStage] = Field(default_factory=list)
    failures: list[str] = Field(default_factory=list)
    budget: BudgetSnapshot
    output_root: Path

    def advance(self, stage: WorkflowStage) -> None:
        self.current_stage = stage
        self.completed_stages.append(stage)

    def fail(self, message: str) -> None:
        self.failures.append(message)
