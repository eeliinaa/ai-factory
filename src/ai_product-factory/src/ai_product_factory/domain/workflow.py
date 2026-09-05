from pydantic import BaseModel

from .candidate import CandidateScore, ResearchCandidate
from .product import ProductPlan


class ResearchResult(BaseModel):
    evidence_summary: str
    candidates: list[ResearchCandidate]


class EvaluationResult(BaseModel):
    selected_candidate: ResearchCandidate | None = None
    backup_candidates: list[ResearchCandidate] = []
    rejected_candidates: list[ResearchCandidate] = []
    scores: list[CandidateScore] = []
    failure_reason: str | None = None


class QaResult(BaseModel):
    passed: bool
    findings: list[str] = []


class PackagingResult(BaseModel):
    package_path: str
    manifest_path: str


class ProductCreationResult(BaseModel):
    plan: ProductPlan
    created_artifacts: list[str] = []
