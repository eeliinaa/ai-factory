from pydantic import ValidationError

from ..domain import (
    BundleArtifactSpec,
    EvaluationResponsePayload,
    PdfArtifactSpec,
    ProductArchitectureResponsePayload,
    ProductCreationResponsePayload,
    RenderableArtifactPayload,
    ResearchCandidate,
    ResearchResponsePayload,
    SpreadsheetArtifactSpec,
    StageParseResult,
    TextArtifactSpec,
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
        parsed = self._parse_payload(response_text, ProductCreationResponsePayload)
        if not parsed.parsed:
            return parsed

        payload = ProductCreationResponsePayload.model_validate(parsed.payload)
        normalized_artifacts: list[RenderableArtifactPayload] = []
        for artifact in payload.created_artifacts:
            render_spec_payload = artifact.render_spec or self._infer_legacy_render_spec(artifact.file_name, artifact.content)
            normalized_artifacts.append(
                RenderableArtifactPayload(
                    artifact_type=artifact.artifact_type,
                    file_name=artifact.file_name,
                    render_spec=self._parse_render_spec(render_spec_payload),
                )
            )

        return StageParseResult(
            parsed=True,
            payload={
                "created_artifacts": [artifact.model_dump() for artifact in payload.created_artifacts],
                "renderable_artifacts": [artifact.model_dump(mode="json") for artifact in normalized_artifacts],
            },
        )

    def _parse_payload(self, response_text: str, payload_model) -> StageParseResult:
        try:
            payload = extract_json_object(response_text)
            validated_payload = payload_model.model_validate(payload)
            return StageParseResult(parsed=True, payload=validated_payload.model_dump())
        except (ValueError, ValidationError) as exc:
            return StageParseResult(parsed=False, error=str(exc))

    def _infer_legacy_render_spec(self, file_name: str, content: str | None) -> dict:
        suffix = file_name.rsplit(".", 1)[-1].lower() if "." in file_name else "txt"
        if suffix == "pdf":
            return {
                "kind": "pdf",
                "title": file_name,
                "sections": [{"heading": "Generated Content", "body": content or "", "bullet_points": []}],
                "page_size": "letter",
            }
        if suffix == "xlsx":
            rows = [[line] for line in (content or "").splitlines() if line.strip()]
            return {
                "kind": "spreadsheet",
                "workbook_title": file_name,
                "sheets": [{"name": "Sheet1", "columns": [{"header": "Content", "width": 40}], "rows": rows}],
            }
        if suffix == "zip":
            return {"kind": "bundle", "notes": content or "Assembled by packaging code."}
        return {"kind": "text", "content": content or ""}

    def _parse_render_spec(self, payload: dict) -> TextArtifactSpec | PdfArtifactSpec | SpreadsheetArtifactSpec | BundleArtifactSpec:
        kind = payload.get("kind", "text")
        if kind == "pdf":
            return PdfArtifactSpec.model_validate(payload)
        if kind == "spreadsheet":
            return SpreadsheetArtifactSpec.model_validate(payload)
        if kind == "bundle":
            return BundleArtifactSpec.model_validate(payload)
        return TextArtifactSpec.model_validate(payload)

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