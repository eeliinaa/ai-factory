import json

from ..domain import ArtifactPlanItem


class PromptBuilder:
    def json_enforcement_suffix(self, attempt: int) -> str:
        if attempt <= 1:
            return "Return exactly one valid JSON object."
        return "Return exactly one valid JSON object. Do not include markdown fences, commentary, or trailing text."

    def build_research_prompt(self, topic: str, context_text: str, attempt: int = 1) -> tuple[str, str]:
        schema = {
            "evidence_summary": "string",
            "candidates": [
                {
                    "id": "candidate-1",
                    "title": "string",
                    "problem_statement": "string",
                    "target_audience": "string",
                    "product_angle": "string",
                    "evidence_summary": "string",
                    "estimated_price_range": "string",
                    "estimated_build_speed": "string",
                    "series_potential_note": "string",
                }
            ],
        }
        system_prompt = "You are a product research assistant. Return only valid JSON and no markdown fences."
        user_prompt = (
            f"Topic: {topic}\n"
            f"Objective: Research viable Etsy-style digital product opportunities. {self.json_enforcement_suffix(attempt)}\n\n"
            f"Context:\n{context_text}\n\n"
            f"Required JSON schema:\n{json.dumps(schema, indent=2)}"
        )
        return system_prompt, user_prompt

    def build_evaluation_prompt(self, topic: str, context_text: str, candidates_payload, attempt: int = 1) -> tuple[str, str]:
        schema = {
            "selected_candidate_id": "candidate-1",
            "backup_candidate_ids": ["candidate-2"],
            "rejected_candidate_ids": ["candidate-3"],
            "scores": [
                {
                    "candidate_id": "candidate-1",
                    "demand_score": 8.0,
                    "competition_score": 7.0,
                    "production_speed_score": 8.0,
                    "price_potential_score": 7.0,
                    "series_potential_score": 8.0,
                    "automation_fit_score": 8.0,
                    "weighted_final_score": 7.5,
                    "recommendation_status": "selected",
                    "risk_notes": "string",
                }
            ],
            "failure_reason": None,
        }
        payload_text = candidates_payload if isinstance(candidates_payload, str) else json.dumps(candidates_payload, indent=2)
        system_prompt = (
            "You are a product evaluation assistant. "
            "Return only valid JSON and no markdown fences."
        )
        user_prompt = (
            f"Topic: {topic}\n"
            f"Objective: {self.json_enforcement_suffix(attempt)}\n\n"
            f"Context:\n{context_text}\n\n"
            f"Candidates JSON:\n{payload_text}\n\n"
            f"Required JSON schema:\n{json.dumps(schema, indent=2)}"
        )
        return system_prompt, user_prompt

    def build_product_architecture_prompt(
        self,
        topic: str,
        context_text: str,
        selected_candidate,
        attempt: int = 1,
    ) -> tuple[str, str]:
        candidate_payload = (
            selected_candidate.model_dump() if hasattr(selected_candidate, "model_dump") else selected_candidate
        )
        schema = {
            "product_type": "TEMPLATE_BUNDLE",
            "product_title": "string",
            "product_summary": "string",
            "buyer_problem": "string",
            "solution_promise": "string",
            "packaging_strategy": "string",
            "artifact_plan": [
                {
                    "artifact_type": "string",
                    "file_name": "string",
                    "file_format": "md",
                    "purpose": "string",
                    "is_required": True,
                    "generation_instructions": "string",
                }
            ],
        }
        system_prompt = (
            "You are a product architect assistant. "
            "Return only valid JSON and no markdown fences."
        )
        user_prompt = (
            f"Topic: {topic}\n"
            f"Objective: Build a product architecture and artifact plan for the selected candidate. {self.json_enforcement_suffix(attempt)}\n\n"
            f"Context:\n{context_text}\n\n"
            f"Selected candidate JSON:\n{json.dumps(candidate_payload, indent=2)}\n\n"
            f"Required JSON schema:\n{json.dumps(schema, indent=2)}"
        )
        return system_prompt, user_prompt

    def build_product_creation_prompt(
        self,
        topic: str,
        context_text: str,
        artifact_plan: list[ArtifactPlanItem],
        attempt: int = 1,
    ) -> tuple[str, str]:
        schema = {
            "created_artifacts": [
                {
                    "artifact_type": "string",
                    "file_name": "string",
                    "content": "string",
                    "render_spec": {
                        "kind": "text | pdf | spreadsheet | bundle",
                    },
                }
            ]
        }
        system_prompt = (
            "You are a digital product creation assistant. "
            "Return only valid JSON and no markdown fences. "
            "For pdf, xlsx, and zip outputs, populate render_spec with structured fields instead of pretending to return binary file contents. "
            "Use content only for plain text-like artifacts such as md, txt, or json."
        )
        user_prompt = (
            f"Topic: {topic}\n"
            f"Objective: Create the first draft content for each planned artifact. {self.json_enforcement_suffix(attempt)}\n\n"
            f"Context:\n{context_text}\n\n"
            f"Artifact plan JSON:\n{json.dumps([item.model_dump() for item in artifact_plan], indent=2)}\n\n"
            "Rendering instructions:\n"
            "- For md/txt/json artifacts: set render_spec.kind='text' and provide final content in render_spec.content.\n"
            "- For pdf artifacts: set render_spec.kind='pdf' and provide a title plus structured sections with heading, body, and bullet_points.\n"
            "- For xlsx artifacts: set render_spec.kind='spreadsheet' and provide workbook_title plus sheets with name, columns, and rows.\n"
            "- For zip artifacts: set render_spec.kind='bundle'. Do not attempt to provide fake zip bytes or markdown placeholders.\n\n"
            f"Required JSON schema:\n{json.dumps(schema, indent=2)}"
        )
        return system_prompt, user_prompt


__all__ = ["PromptBuilder"]