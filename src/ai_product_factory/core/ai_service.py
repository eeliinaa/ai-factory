from ..agents import PromptBuilder
from ..core.errors import ProviderError
from ..domain import ArtifactPlanItem, WorkflowStage
from ..providers import LLMRequest, LLMResponse, LLMProvider, ModelPolicy


class AIService:
    def __init__(self, provider: LLMProvider, model_policy: ModelPolicy, structured_output_retries: int = 1) -> None:
        self.provider = provider
        self.model_policy = model_policy
        self.prompt_builder = PromptBuilder()
        self.structured_output_retries = structured_output_retries

    def generate_for_stage(
        self,
        stage: WorkflowStage,
        topic: str,
        context_text: str,
        objective: str,
        require_json: bool = False,
        prompt_version: str = "v1",
        attempt: int = 1,
        supplemental_context: str | None = None,
    ) -> LLMResponse:
        attempt_objective = objective
        if supplemental_context:
            attempt_objective = f"{attempt_objective}\n\nUse this product-specific context to ground the response:\n{supplemental_context}"
        if require_json and attempt > 1:
            attempt_objective = f"{attempt_objective} Return only valid JSON matching the required schema exactly."

        if stage == WorkflowStage.RESEARCH:
            system_prompt, user_prompt = self.prompt_builder.build_research_prompt(topic, context_text, attempt=attempt)
        elif stage == WorkflowStage.EVALUATION:
            system_prompt, user_prompt = self.prompt_builder.build_evaluation_prompt(
                topic,
                context_text,
                candidates_payload=[],
                attempt=attempt,
            )
        elif stage == WorkflowStage.PRODUCT_ARCHITECTURE:
            system_prompt, user_prompt = self.prompt_builder.build_product_architecture_prompt(
                topic,
                context_text,
                selected_candidate={},
                attempt=attempt,
            )
        elif stage == WorkflowStage.PRODUCT_CREATION:
            system_prompt, user_prompt = self.prompt_builder.build_product_creation_prompt(
                topic,
                context_text,
                artifact_plan=[],
                attempt=attempt,
            )
        else:
            system_prompt = f"You are supporting the {stage.value} stage."
            user_prompt = (
                f"Topic: {topic}\n"
                f"Objective: {attempt_objective}\n\n"
                f"Context:\n{context_text}"
            )

        request = LLMRequest(
            stage_name=stage.value,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model=self.model_policy.for_stage(stage),
            require_json=require_json,
            prompt_version=prompt_version,
        )
        try:
            response = self.provider.generate(request)
            response.metadata["attempt"] = attempt
            return response
        except Exception as exc:
            raise ProviderError(str(exc)) from exc

    def generate_research(self, topic: str, context_text: str, attempt: int = 1) -> LLMResponse:
        system_prompt, user_prompt = self.prompt_builder.build_research_prompt(topic, context_text, attempt=attempt)
        request = LLMRequest(
            stage_name=WorkflowStage.RESEARCH.value,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model=self.model_policy.for_stage(WorkflowStage.RESEARCH),
            require_json=True,
            prompt_version="research-v1",
        )
        try:
            response = self.provider.generate(request)
            response.metadata["attempt"] = attempt
            return response
        except Exception as exc:
            raise ProviderError(str(exc)) from exc

    def generate_evaluation(
        self,
        topic: str,
        context_text: str,
        candidates: list[dict],
        attempt: int = 1,
    ) -> LLMResponse:
        system_prompt, user_prompt = self.prompt_builder.build_evaluation_prompt(
            topic,
            context_text,
            candidates_payload=candidates,
            attempt=attempt,
        )
        request = LLMRequest(
            stage_name=WorkflowStage.EVALUATION.value,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model=self.model_policy.for_stage(WorkflowStage.EVALUATION),
            require_json=True,
            prompt_version="evaluation-v1",
        )
        try:
            response = self.provider.generate(request)
            response.metadata["attempt"] = attempt
            return response
        except Exception as exc:
            raise ProviderError(str(exc)) from exc

    def generate_product_architecture(
        self,
        topic: str,
        context_text: str,
        selected_candidate: dict,
        attempt: int = 1,
    ) -> LLMResponse:
        system_prompt, user_prompt = self.prompt_builder.build_product_architecture_prompt(
            topic,
            context_text,
            selected_candidate,
            attempt=attempt,
        )
        request = LLMRequest(
            stage_name=WorkflowStage.PRODUCT_ARCHITECTURE.value,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model=self.model_policy.for_stage(WorkflowStage.PRODUCT_ARCHITECTURE),
            require_json=True,
            prompt_version="product-architecture-v1",
        )
        try:
            response = self.provider.generate(request)
            response.metadata["attempt"] = attempt
            return response
        except Exception as exc:
            raise ProviderError(str(exc)) from exc

    def generate_product_creation(
        self,
        topic: str,
        context_text: str,
        artifact_plan: list[ArtifactPlanItem],
        attempt: int = 1,
    ) -> LLMResponse:
        system_prompt, user_prompt = self.prompt_builder.build_product_creation_prompt(
            topic,
            context_text,
            artifact_plan,
            attempt=attempt,
        )
        request = LLMRequest(
            stage_name=WorkflowStage.PRODUCT_CREATION.value,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model=self.model_policy.for_stage(WorkflowStage.PRODUCT_CREATION),
            require_json=True,
            prompt_version="product-creation-v1",
        )
        try:
            response = self.provider.generate(request)
            response.metadata["attempt"] = attempt
            return response
        except Exception as exc:
            raise ProviderError(str(exc)) from exc