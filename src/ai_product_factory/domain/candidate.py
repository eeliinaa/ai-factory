from pydantic import BaseModel

from .enums import RecommendationStatus


class ResearchCandidate(BaseModel):
    id: str
    title: str
    problem_statement: str
    target_audience: str
    product_angle: str
    evidence_summary: str | None = None
    estimated_price_range: str | None = None
    estimated_build_speed: str | None = None
    series_potential_note: str | None = None


class CandidateScore(BaseModel):
    candidate_id: str
    demand_score: float
    competition_score: float
    production_speed_score: float
    price_potential_score: float
    series_potential_score: float
    automation_fit_score: float
    weighted_final_score: float
    recommendation_status: RecommendationStatus = RecommendationStatus.REJECTED
    risk_notes: str | None = None
