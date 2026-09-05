from typing import Any

from pydantic import BaseModel, Field

from .artifact import ArtifactPlanItem
from .candidate import CandidateScore, ResearchCandidate
from .product import ProductPlan


class ResearchResult(BaseModel):
    evidence_summary: str
    candidates: list[ResearchCandidate] = Field(default_factory=list)


class EvaluationResult(BaseModel):
    selected_candidate: ResearchCandidate | None = None
    backup_candidates: list[ResearchCandidate] = Field(default_factory=list)
    rejected_candidates: list[ResearchCandidate] = Field(default_factory=list)
    scores: list[CandidateScore] = Field(default_factory=list)
    failure_reason: str | None = None


class ResearchResponsePayload(BaseModel):
    evidence_summary: str
    candidates: list[ResearchCandidate] = Field(default_factory=list)


class EvaluationResponsePayload(BaseModel):
    selected_candidate_id: str | None = None
    backup_candidate_ids: list[str] = Field(default_factory=list)
    rejected_candidate_ids: list[str] = Field(default_factory=list)
    scores: list[CandidateScore] = Field(default_factory=list)
    failure_reason: str | None = None


class ProductArchitectureResponsePayload(BaseModel):
    product_type: str
    product_title: str
    product_summary: str
    buyer_problem: str
    solution_promise: str
    packaging_strategy: str
    artifact_plan: list[ArtifactPlanItem] = Field(default_factory=list)


class ProductCreationArtifactPayload(BaseModel):
    artifact_type: str
    file_name: str
    content: str


class ProductCreationResponsePayload(BaseModel):
    created_artifacts: list[ProductCreationArtifactPayload] = Field(default_factory=list)


class ProductArchitectureResult(BaseModel):
    plan: ProductPlan
    artifact_plan: list[ArtifactPlanItem] = Field(default_factory=list)


class QaResult(BaseModel):
    passed: bool
    findings: list[str] = Field(default_factory=list)


class PackagingResult(BaseModel):
    package_path: str
    manifest_path: str


class ListingResult(BaseModel):
    title: str
    description: str
    tags: list[str] = Field(default_factory=list)


class ProductCreationResult(BaseModel):
    plan: ProductPlan
    created_artifacts: list[str] = Field(default_factory=list)


class StageParseResult(BaseModel):
    parsed: bool
    payload: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None
