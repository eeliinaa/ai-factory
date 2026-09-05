from pydantic import ValidationError

from ..domain import (
    EvaluationResponsePayload,
    ProductArchitectureResponsePayload,
    ProductCreationResponsePayload,
    ResearchCandidate,
    ResearchResponsePayload,
    StageParseResult,
)
from ..utils import extract_json_object


class ResponseParser:
    def parse_research_response(self, response_text: str) -> StageParseResult:
        return self._parse_payload(response_text, ResearchResponsePayload)

    def parse_evaluation_response(self, response_text: str) -> StageParseResult:
        return self._parse_payload(response_text, EvaluationResponsePayload)

    def parse_product_architecture_response(self, response_text: str) -> StageParseResult:
        return self._parse_payload(response_text, ProductArchitectureResponsePayload)

    def parse_product_creation_response(self, response_text: str) -> StageParseResult:
        return self._parse_payload(response_text, ProductCreationResponsePayload)

    def _parse_payload(self, response_text: str, payload_model) -> StageParseResult:
        try:
            payload = extract_json_object(response_text)
            validated_payload = payload_model.model_validate(payload)
            return StageParseResult(parsed=True, payload=validated_payload.model_dump())
        except (ValueError, ValidationError) as exc:
            return StageParseResult(parsed=False, error=str(exc))

    def select_candidate_by_id(
        self,
        candidates: list[ResearchCandidate],
        candidate_id: str | None,
    ) -> ResearchCandidate | None:
        if candidate_id is None:
            return None
        return next((candidate for candidate in candidates if candidate.id == candidate_id), None)

    def select_candidates_by_ids(
        self,
        candidates: list[ResearchCandidate],
        candidate_ids: list[str],
    ) -> list[ResearchCandidate]:
        candidate_map = {candidate.id: candidate for candidate in candidates}
        return [candidate_map[candidate_id] for candidate_id in candidate_ids if candidate_id in candidate_map]
