import json

from openai import OpenAI

from ..core.errors import ProviderError
from .base import LLMProvider, LLMRequest, LLMResponse
from .pricing import estimate_cost


class OpenAIProvider(LLMProvider):
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout_seconds: float = 180.0,
        allow_placeholder_fallback: bool = True,
    ) -> None:
        self.api_key = api_key
        self.allow_placeholder_fallback = allow_placeholder_fallback
        self.client = (
            OpenAI(api_key=api_key, base_url=base_url, timeout=timeout_seconds) if api_key else None
        )

    def generate(self, request: LLMRequest) -> LLMResponse:
        if self.client is None:
            if self.allow_placeholder_fallback:
                return self._placeholder_response(request)
            raise ProviderError("OPENAI_API_KEY is not configured and placeholder fallback is disabled.")

        try:
            payload = {
                "model": request.model,
                "input": [
                    {"role": "system", "content": request.system_prompt},
                    {"role": "user", "content": request.user_prompt},
                ],
            }

            if request.require_json:
                payload["text"] = {"format": {"type": "json_object"}}

            response = self.client.responses.create(**payload)
        except Exception as exc:
            raise ProviderError(f"OpenAI API call failed: {exc}") from exc

        content = getattr(response, "output_text", "") or ""
        usage = getattr(response, "usage", None)
        prompt_tokens = getattr(usage, "input_tokens", 0) if usage else 0
        completion_tokens = getattr(usage, "output_tokens", 0) if usage else 0
        estimated_cost, cost_mode = estimate_cost(request.model, prompt_tokens, completion_tokens)

        return LLMResponse(
            model=getattr(response, "model", request.model),
            content=content,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            estimated_cost=estimated_cost,
            metadata={
                "provider": "openai",
                "mode": "live",
                "stage_name": request.stage_name,
                "prompt_version": request.prompt_version,
                "cost_estimation": cost_mode,
                "require_json": request.require_json,
            },
        )

    def _placeholder_response(self, request: LLMRequest) -> LLMResponse:
        if request.stage_name == "research":
            content = json.dumps(
                {
                    "evidence_summary": "Placeholder structured research output for MVP pipeline development.",
                    "candidates": [
                        {
                            "id": "candidate-1",
                            "title": "Professional Workflow Toolkit",
                            "problem_statement": "Professionals need repeatable systems for planning and delivery.",
                            "target_audience": "Knowledge workers and freelancers",
                            "product_angle": "Reusable templates and worksheets for recurring workflows",
                            "evidence_summary": "Strong practical utility and easy digital packaging.",
                            "estimated_price_range": "$12-$24",
                            "estimated_build_speed": "fast",
                            "series_potential_note": "Expandable into niche workflow bundles.",
                        },
                        {
                            "id": "candidate-2",
                            "title": "Client Onboarding Template Pack",
                            "problem_statement": "Freelancers lose time onboarding clients manually.",
                            "target_audience": "Freelancers and solo service providers",
                            "product_angle": "Streamlined onboarding documents and checklists",
                            "evidence_summary": "Simple to produce and clear buyer outcome.",
                            "estimated_price_range": "$14-$28",
                            "estimated_build_speed": "fast",
                            "series_potential_note": "Can branch into industry-specific onboarding kits.",
                        },
                        {
                            "id": "candidate-3",
                            "title": "Weekly Planning Dashboard Bundle",
                            "problem_statement": "Busy professionals struggle to prioritize weekly work.",
                            "target_audience": "Remote workers and managers",
                            "product_angle": "Planning sheets and review templates for weekly execution",
                            "evidence_summary": "Broad demand and repeatable design pattern.",
                            "estimated_price_range": "$10-$22",
                            "estimated_build_speed": "fast",
                            "series_potential_note": "Can expand into monthly and quarterly planning systems.",
                        },
                    ],
                }
            )
        elif request.stage_name == "evaluation":
            content = json.dumps(
                {
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
                            "risk_notes": "Balanced opportunity with strong execution speed.",
                        },
                        {
                            "candidate_id": "candidate-2",
                            "demand_score": 7.0,
                            "competition_score": 6.5,
                            "production_speed_score": 8.0,
                            "price_potential_score": 7.0,
                            "series_potential_score": 7.5,
                            "automation_fit_score": 7.5,
                            "weighted_final_score": 7.25,
                            "recommendation_status": "backup",
                            "risk_notes": "Good offer, but slightly narrower market.",
                        },
                        {
                            "candidate_id": "candidate-3",
                            "demand_score": 6.5,
                            "competition_score": 6.0,
                            "production_speed_score": 8.0,
                            "price_potential_score": 6.5,
                            "series_potential_score": 7.0,
                            "automation_fit_score": 7.0,
                            "weighted_final_score": 6.83,
                            "recommendation_status": "rejected",
                            "risk_notes": "Usable but less differentiated than the leading option.",
                        },
                    ],
                    "failure_reason": None,
                }
            )
        elif request.stage_name == "product_architecture":
            content = json.dumps(
                {
                    "product_type": "TEMPLATE_BUNDLE",
                    "product_title": "Professional Workflow Toolkit",
                    "product_summary": "A practical bundle of reusable workflow templates for planning and delivery.",
                    "buyer_problem": "Professionals need repeatable systems for planning and delivery.",
                    "solution_promise": "Help buyers save time with reusable workflow assets.",
                    "packaging_strategy": "Bundle a planning template, execution worksheet, and buyer guide.",
                    "artifact_plan": [
                        {
                            "artifact_type": "planning_template",
                            "file_name": "planning-template.md",
                            "file_format": "md",
                            "purpose": "Help the buyer define weekly priorities and milestones.",
                            "is_required": True,
                            "generation_instructions": "Create a concise planning template with headings and fillable prompts.",
                        },
                        {
                            "artifact_type": "execution_worksheet",
                            "file_name": "execution-worksheet.md",
                            "file_format": "md",
                            "purpose": "Support daily execution and tracking.",
                            "is_required": True,
                            "generation_instructions": "Create a worksheet with task sections, blockers, and review prompts.",
                        },
                        {
                            "artifact_type": "buyer_guide",
                            "file_name": "buyer-guide.md",
                            "file_format": "md",
                            "purpose": "Explain how to use the toolkit effectively.",
                            "is_required": True,
                            "generation_instructions": "Write a short usage guide with setup and workflow steps.",
                        },
                    ],
                }
            )
        elif request.stage_name == "product_creation":
            content = json.dumps(
                {
                    "created_artifacts": [
                        {
                            "artifact_type": "planning_template",
                            "file_name": "planning-template.md",
                            "content": "# Planning Template\n\n## Weekly Goals\n- Goal 1\n- Goal 2\n\n## Priorities\n- Priority A\n- Priority B\n",
                        },
                        {
                            "artifact_type": "execution_worksheet",
                            "file_name": "execution-worksheet.md",
                            "content": "# Execution Worksheet\n\n## Today's Focus\n-\n\n## Blockers\n-\n\n## End-of-Day Review\n- Wins\n- Improvements\n",
                        },
                        {
                            "artifact_type": "buyer_guide",
                            "file_name": "buyer-guide.md",
                            "content": "# Buyer Guide\n\nUse the planning template at the start of the week, the worksheet daily, and review progress at the end of each cycle.\n",
                        },
                    ]
                }
            )
        else:
            content = (
                f"[Placeholder AI response] Stage={request.stage_name}; "
                f"Model={request.model}; no OPENAI_API_KEY configured."
            )

        return LLMResponse(
            model=request.model,
            content=content,
            metadata={
                "provider": "openai",
                "mode": "placeholder",
                "stage_name": request.stage_name,
                "prompt_version": request.prompt_version,
                "cost_estimation": "none",
                "require_json": request.require_json,
            },
        )