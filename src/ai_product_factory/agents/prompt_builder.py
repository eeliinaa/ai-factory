import json

from ..domain import ArtifactPlanItem, SelectedProduct, WorkflowStage


class PromptBuilder:
    def build(self, stage: WorkflowStage, topic: str, context_text: str, objective: str) -> tuple[str, str]:
        system_prompt = (
            "You are an AI product development assistant. "
            "Use the provided project context and follow the workflow stage objective carefully."
        )
        user_prompt = (
            f"Stage: {stage.value}\n"
            f"Topic: {topic}\n"
            f"Objective: {objective}\n\n"
            f"Context:\n{context_text}\n"
        )
        return system_prompt, user_prompt

    def json_enforcement_suffix(self, attempt: int) -> str:
        if attempt <= 1:
            return "Return only valid JSON."
        return "Return only valid JSON matching the schema exactly. No markdown. No commentary. No extra keys."

    def build_research_prompt(self, topic: str, context_text: str, attempt: int = 1) -> tuple[str, str]:
        objective = (
            "Identify exactly 3 viable Etsy-suitable digital product opportunities with strong speed, "
            "practical value, and series potential."
        )
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
        system_prompt = (
            "You are a product opportunity research assistant. "
            "Return only valid JSON and no markdown fences."
        )
        user_prompt = (
            f"Topic: {topic}\n"
            f"Objective: {objective} {self.json_enforcement_suffix(attempt)}\n\n"
            f"Context:\n{context_text}\n\n"
            f"Required JSON schema:\n{json.dumps(schema, indent=2)}"
        )
        return system_prompt, user_prompt

    def build_evaluation_prompt(
        self,
        topic: str,
        context_text: str,
        candidates_payload: str | list[dict],
        attempt: int = 1,
    ) -> tuple[str, str]:
        objective = (
            "Evaluate the provided candidates, select one best option, identify backups and rejected options."
        )
        schema = {
            "selected_candidate_id": "candidate-1",
            "backup_candidate_ids": ["candidate-2"],
            "rejected_candidate_ids": ["candidate-3"],
            "scores": [
                {
                    "candidate_id": "candidate-1",
                    "demand_score": 7.5,
                    "competition_score": 6.0,
                    "production_speed_score": 8.5,
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
            f"Objective: {objective} {self.json_enforcement_suffix(attempt)}\n\n"
            f"Context:\n{context_text}\n\n"
            f"Candidates JSON:\n{payload_text}\n\n"
            f"Required JSON schema:\n{json.dumps(schema, indent=2)}"
        )
        return system_prompt, user_prompt

    def build_product_architecture_prompt(
        self,
        topic: str,
        context_text: str,
        selected_candidate: SelectedProduct | dict,
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
                }
            ]
        }
        system_prompt = (
            "You are a digital product creation assistant. "
            "Return only valid JSON and no markdown fences."
        )
        user_prompt = (
            f"Topic: {topic}\n"
            f"Objective: Create the first draft content for each planned artifact. {self.json_enforcement_suffix(attempt)}\n\n"
            f"Context:\n{context_text}\n\n"
            f"Artifact plan JSON:\n{json.dumps([item.model_dump() for item in artifact_plan], indent=2)}\n\n"
            f"Required JSON schema:\n{json.dumps(schema, indent=2)}"
        )
        return system_prompt, user_prompt
