from enum import StrEnum


class RunStatus(StrEnum):
    PENDING = "pending"
    RESEARCHING = "researching"
    EVALUATING = "evaluating"
    DESIGNING = "designing"
    CREATING = "creating"
    QA = "qa"
    PACKAGING = "packaging"
    COMPLETED = "completed"
    FAILED = "failed"


class RecommendationStatus(StrEnum):
    SELECTED = "selected"
    BACKUP = "backup"
    REJECTED = "rejected"


class ArtifactGenerationStatus(StrEnum):
    PENDING = "pending"
    GENERATED = "generated"
    FAILED = "failed"


class ProductType(StrEnum):
    WORKSHEET_BUNDLE = "WORKSHEET_BUNDLE"
    TEMPLATE_BUNDLE = "TEMPLATE_BUNDLE"
    PDF_TOOLKIT = "PDF_TOOLKIT"
    PROMPT_TEMPLATE_HYBRID = "PROMPT_TEMPLATE_HYBRID"
    CHECKLIST_PACK = "CHECKLIST_PACK"
    MIXED_PROFESSIONAL_BUNDLE = "MIXED_PROFESSIONAL_BUNDLE"
    NOTION_WORKSPACE = "NOTION_WORKSPACE"


class WorkflowStage(StrEnum):
    INPUT = "input"
    RESEARCH = "research"
    EVALUATION = "evaluation"
    PRODUCT_ARCHITECTURE = "product_architecture"
    PRODUCT_CREATION = "product_creation"
    AI_QA = "ai_qa"
    TECHNICAL_BUILD_PACKAGING = "technical_build_packaging"
    TECHNICAL_QA = "technical_qa"
    LISTING = "listing"
    PREVIEW = "preview"
    FINAL_PACKAGE = "final_package"
