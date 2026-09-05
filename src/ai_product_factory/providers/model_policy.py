from ..domain import WorkflowStage
from ..config import AppSettings


class ModelPolicy:
    def __init__(self, settings: AppSettings) -> None:
        self.settings = settings

    def for_stage(self, stage: WorkflowStage) -> str:
        if stage == WorkflowStage.RESEARCH:
            return self.settings.research_model or self.settings.default_model
        if stage == WorkflowStage.EVALUATION:
            return self.settings.evaluation_model or self.settings.default_model
        if stage in {WorkflowStage.PRODUCT_ARCHITECTURE, WorkflowStage.PRODUCT_CREATION}:
            return self.settings.product_creation_model or self.settings.default_model
        if stage == WorkflowStage.LISTING:
            return self.settings.listing_model or self.settings.default_model
        if stage in {WorkflowStage.AI_QA, WorkflowStage.TECHNICAL_QA}:
            return self.settings.qa_model or self.settings.default_model
        return self.settings.default_model
