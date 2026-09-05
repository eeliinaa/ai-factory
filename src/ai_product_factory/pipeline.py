from .config import AppSettings
from .core import (
    AIProductFactoryError,
    AIService,
    BudgetExceededError,
    BudgetSnapshot,
    PipelineState,
    QaValidationError,
    QaValidator,
    ResponseParser,
    StructuredOutputError,
    StructuredStageExecutor,
    extract_refinement_targets,
    should_continue_refinement,
)
from .domain import (
    EvaluationResponsePayload,
    EvaluationResult,
    ListingDraft,
    ListingResult,
    PackagingResult,
    ProductArchitectureResponsePayload,
    ProductArchitectureResult,
    ProductCreationResponsePayload,
    ProductCreationResult,
    ProductPlan,
    ProductType,
    QaResult,
    ResearchResponsePayload,
    ResearchResult,
    RunContext,
    RunStatus,
    SelectedProduct,
    WorkflowStage,
)
from .fs import ensure_directory
from .outputs import build_output_package, render_artifacts, write_run_report
from .utils import slugify_topic


class PipelineRunner:
    def __init__(self, settings: AppSettings, context_text: str, ai_service: AIService) -> None:
        self.settings = settings
        self.context_text = context_text
        self.ai_service = ai_service
        self.response_parser = ResponseParser()
        self.qa_validator = QaValidator()
        self.stage_executor = StructuredStageExecutor(max_retries=settings.ai_structured_output_retries)

    def create_run(self, topic: str) -> RunContext:
        safe_topic = slugify_topic(topic)
        run_output_dir = self.settings.runs_dir / f"run_{safe_topic}"
        ensure_directory(run_output_dir)
        return RunContext.create(topic=topic, output_dir=run_output_dir)

    def create_state(self, topic: str, run_context: RunContext) -> PipelineState:
        return PipelineState(
            topic=topic,
            context_text=self.context_text,
            budget=BudgetSnapshot(
                total_limit=self.settings.max_total_cost,
                research_limit=self.settings.max_research_cost,
                product_creation_limit=self.settings.max_product_creation_cost,
                listing_preview_limit=self.settings.max_listing_preview_cost,
            ),
            output_root=run_context.run.output_path,
        )

    def register_stage_cost(self, stage: WorkflowStage, estimated_cost: float, state: PipelineState) -> None:
        try:
            state.budget.register_spend(stage, estimated_cost)
            state.budget.assert_within_limits(stage)
        except ValueError as exc:
            raise BudgetExceededError(str(exc)) from exc

    def build_product_specific_context(self, selected_product: SelectedProduct, artifact_plan, artifacts) -> str:
        artifact_plan_lines = [
            f"- {item.artifact_type}: {item.file_name} ({item.file_format}, required={item.is_required})"
            for item in artifact_plan
        ]
        artifact_output_lines = [
            f"- {artifact.artifact_type}: {artifact.file_path} ({artifact.file_format}, required={artifact.is_required})"
            for artifact in artifacts
        ]
        return "\n".join(
            [
                f"Selected product title: {selected_product.product_title}",
                f"Selected product type: {selected_product.product_type}",
                f"Product summary: {selected_product.product_summary}",
                f"Buyer problem: {selected_product.buyer_problem}",
                f"Solution promise: {selected_product.solution_promise}",
                f"Packaging strategy: {selected_product.packaging_strategy}",
                "Planned artifacts:",
                *artifact_plan_lines,
                "Generated artifacts:",
                *artifact_output_lines,
            ]
        )

    def run_research_stage(self, topic: str, state: PipelineState, stage_metadata: dict[str, dict]) -> ResearchResult:
        state.advance(WorkflowStage.RESEARCH)
        payload = self.stage_executor.execute(
            WorkflowStage.RESEARCH,
            generator=lambda attempt: self.ai_service.generate_research(topic=topic, context_text=state.context_text, attempt=attempt),
            parser=self.response_parser.parse_research_response,
            stage_metadata=stage_metadata,
        )
        self.register_stage_cost(
            WorkflowStage.RESEARCH,
            stage_metadata[WorkflowStage.RESEARCH.value]["estimated_cost"],
            state,
        )
        research_payload = ResearchResponsePayload.model_validate(payload)
        if len(research_payload.candidates) < 2:
            raise StructuredOutputError("Research stage returned fewer than 2 viable candidates.")

        return ResearchResult(
            evidence_summary=research_payload.evidence_summary,
            candidates=research_payload.candidates,
        )

    def run_evaluation_stage(
        self,
        research: ResearchResult,
        state: PipelineState,
        stage_metadata: dict[str, dict],
    ) -> EvaluationResult:
        state.advance(WorkflowStage.EVALUATION)
        payload = self.stage_executor.execute(
            WorkflowStage.EVALUATION,
            generator=lambda attempt: self.ai_service.generate_evaluation(
                topic=state.topic,
                context_text=state.context_text,
                candidates=[candidate.model_dump() for candidate in research.candidates],
                attempt=attempt,
            ),
            parser=self.response_parser.parse_evaluation_response,
            stage_metadata=stage_metadata,
        )
        self.register_stage_cost(
            WorkflowStage.EVALUATION,
            stage_metadata[WorkflowStage.EVALUATION.value]["estimated_cost"],
            state,
        )
        evaluation_payload = EvaluationResponsePayload.model_validate(payload)
        selected_candidate = self.response_parser.select_candidate_by_id(
            research.candidates,
            evaluation_payload.selected_candidate_id,
        )
        if selected_candidate is None:
            raise StructuredOutputError("Evaluation stage did not return a valid selected candidate.")

        top_score = next(
            (score for score in evaluation_payload.scores if score.candidate_id == selected_candidate.id),
            None,
        )
        if top_score is None or top_score.weighted_final_score < 6.5:
            raise StructuredOutputError("Selected candidate did not pass the viability threshold.")

        backup_candidates = self.response_parser.select_candidates_by_ids(
            research.candidates,
            evaluation_payload.backup_candidate_ids,
        )
        rejected_candidates = self.response_parser.select_candidates_by_ids(
            research.candidates,
            evaluation_payload.rejected_candidate_ids,
        )

        return EvaluationResult(
            selected_candidate=selected_candidate,
            backup_candidates=backup_candidates,
            rejected_candidates=rejected_candidates,
            scores=evaluation_payload.scores,
            failure_reason=evaluation_payload.failure_reason,
        )

    def run_product_architecture_stage(
        self,
        evaluation: EvaluationResult,
        state: PipelineState,
        stage_metadata: dict[str, dict],
    ) -> ProductArchitectureResult:
        state.advance(WorkflowStage.PRODUCT_ARCHITECTURE)
        candidate = evaluation.selected_candidate
        if candidate is None:
            raise StructuredOutputError("No selected candidate available for product architecture.")

        payload = self.stage_executor.execute(
            WorkflowStage.PRODUCT_ARCHITECTURE,
            generator=lambda attempt: self.ai_service.generate_product_architecture(
                topic=state.topic,
                context_text=state.context_text,
                selected_candidate=candidate.model_dump(),
                attempt=attempt,
            ),
            parser=self.response_parser.parse_product_architecture_response,
            stage_metadata=stage_metadata,
        )
        self.register_stage_cost(
            WorkflowStage.PRODUCT_ARCHITECTURE,
            stage_metadata[WorkflowStage.PRODUCT_ARCHITECTURE.value]["estimated_cost"],
            state,
        )
        architecture_payload = ProductArchitectureResponsePayload.model_validate(payload)
        plan = ProductPlan(
            product_type=ProductType(architecture_payload.product_type),
            product_title=architecture_payload.product_title,
            product_summary=architecture_payload.product_summary,
            buyer_problem=architecture_payload.buyer_problem,
            solution_promise=architecture_payload.solution_promise,
            packaging_strategy=architecture_payload.packaging_strategy,
        )
        return ProductArchitectureResult(plan=plan, artifact_plan=architecture_payload.artifact_plan)

    def run_product_creation_stage(
        self,
        architecture: ProductArchitectureResult,
        selected_candidate_id: str,
        state: PipelineState,
        stage_metadata: dict[str, dict],
        attempt: int = 1,
    ) -> tuple[ProductCreationResult, SelectedProduct, list]:
        state.advance(WorkflowStage.PRODUCT_CREATION)
        payload = self.stage_executor.execute(
            WorkflowStage.PRODUCT_CREATION,
            generator=lambda generator_attempt: self.ai_service.generate_product_creation(
                topic=state.topic,
                context_text=state.context_text,
                artifact_plan=architecture.artifact_plan,
                attempt=generator_attempt + attempt - 1,
            ),
            parser=self.response_parser.parse_product_creation_response,
            stage_metadata=stage_metadata,
        )
        self.register_stage_cost(
            WorkflowStage.PRODUCT_CREATION,
            stage_metadata[WorkflowStage.PRODUCT_CREATION.value]["estimated_cost"],
            state,
        )
        creation_payload = ProductCreationResponsePayload.model_validate(payload)
        artifacts = render_artifacts(
            state.output_root,
            [artifact.model_dump() for artifact in creation_payload.created_artifacts],
        )
        selected_product = SelectedProduct(
            candidate_id=selected_candidate_id,
            product_type=architecture.plan.product_type,
            product_title=architecture.plan.product_title,
            product_summary=architecture.plan.product_summary,
            buyer_problem=architecture.plan.buyer_problem,
            solution_promise=architecture.plan.solution_promise,
            packaging_strategy=architecture.plan.packaging_strategy,
        )
        return (
            ProductCreationResult(
                plan=architecture.plan,
                created_artifacts=[str(artifact.file_path) for artifact in artifacts],
            ),
            selected_product,
            artifacts,
        )

    def run_qa_stage(
        self,
        state: PipelineState,
        selected_product: SelectedProduct,
        artifact_plan,
        artifacts,
        stage_metadata: dict[str, dict],
    ) -> QaResult:
        state.advance(WorkflowStage.AI_QA)
        supplemental_context = self.build_product_specific_context(selected_product, artifact_plan, artifacts)
        ai_result = self.ai_service.generate_for_stage(
            stage=WorkflowStage.AI_QA,
            topic=state.topic,
            context_text=state.context_text,
            objective="Review the generated product for completeness and quality risks. Validate the response against the selected product and generated artifacts; do not invent a different product concept.",
            prompt_version="qa-v2",
            supplemental_context=supplemental_context,
        )
        stage_metadata[WorkflowStage.AI_QA.value] = {
            "model": ai_result.model,
            "mode": ai_result.metadata.get("mode"),
            "prompt_version": ai_result.metadata.get("prompt_version"),
            "attempt": ai_result.metadata.get("attempt", 1),
            "prompt_tokens": ai_result.prompt_tokens,
            "completion_tokens": ai_result.completion_tokens,
            "estimated_cost": ai_result.estimated_cost,
            "parsed_successfully": True,
            "error": None,
        }
        self.register_stage_cost(WorkflowStage.AI_QA, ai_result.estimated_cost, state)
        state.advance(WorkflowStage.TECHNICAL_QA)
        technical_result = self.qa_validator.validate_artifact_outputs(artifact_plan, artifacts)
        stage_metadata[WorkflowStage.TECHNICAL_QA.value] = {
            "parsed_successfully": technical_result.passed,
            "error": None if technical_result.passed else "Technical QA validation failed.",
            "findings_count": len(technical_result.technical_findings),
        }
        if not technical_result.passed:
            raise QaValidationError("Technical QA validation failed.")
        findings = [ai_result.content] + technical_result.findings
        return QaResult(
            passed=True,
            findings=findings,
            ai_findings=[ai_result.content],
            technical_findings=technical_result.technical_findings,
        )

    def run_listing_stage(
        self,
        selected_product: SelectedProduct,
        artifact_plan,
        artifacts,
        state: PipelineState,
        stage_metadata: dict[str, dict],
    ) -> ListingResult:
        state.advance(WorkflowStage.LISTING)
        supplemental_context = self.build_product_specific_context(selected_product, artifact_plan, artifacts)
        ai_result = self.ai_service.generate_for_stage(
            stage=WorkflowStage.LISTING,
            topic=state.topic,
            context_text=state.context_text,
            objective=(
                "Draft Etsy listing copy for the selected product. Keep the listing tightly aligned to the selected product title, summary, buyer problem, solution promise, and generated artifacts. "
                "Do not switch to a generic wedding planning bundle or mention deliverables that are not in the generated artifact list."
            ),
            prompt_version="listing-v2",
            supplemental_context=supplemental_context,
        )
        stage_metadata[WorkflowStage.LISTING.value] = {
            "model": ai_result.model,
            "mode": ai_result.metadata.get("mode"),
            "prompt_version": ai_result.metadata.get("prompt_version"),
            "attempt": ai_result.metadata.get("attempt", 1),
            "prompt_tokens": ai_result.prompt_tokens,
            "completion_tokens": ai_result.completion_tokens,
            "estimated_cost": ai_result.estimated_cost,
            "parsed_successfully": True,
            "error": None,
        }
        self.register_stage_cost(WorkflowStage.LISTING, ai_result.estimated_cost, state)
        return ListingResult(
            title=selected_product.product_title,
            description=ai_result.content,
            tags=["wedding emergency kit", "day of checklist", "printable wedding", "digital download"],
        )

    def run_packaging_stage(
        self,
        state: PipelineState,
        artifacts,
        artifact_plan,
        stage_metadata: dict[str, dict],
    ) -> PackagingResult:
        state.advance(WorkflowStage.FINAL_PACKAGE)
        package_path, manifest_path = build_output_package(state.output_root, artifacts, artifact_plan)
        stage_metadata[WorkflowStage.FINAL_PACKAGE.value] = {
            "parsed_successfully": True,
            "error": None,
            "manifest_path": str(manifest_path),
            "package_path": str(package_path),
        }
        return PackagingResult(
            package_path=str(package_path),
            manifest_path=str(manifest_path),
        )

    def run(self, topic: str) -> dict:
        run_context = self.create_run(topic)
        state = self.create_state(topic, run_context)
        stage_metadata: dict[str, dict] = {}
        selected_product = None
        listing_draft = None
        qa_result = None
        packaging = None
        artifacts = []
        artifact_plan = []
        final_outcome_reason = "completed"
        refinement_cycles_used = 0
        refinement_stop_reason = "not_needed"
        refinement_history: list[dict] = []

        try:
            research = self.run_research_stage(topic, state, stage_metadata)
            evaluation = self.run_evaluation_stage(research, state, stage_metadata)
            architecture = self.run_product_architecture_stage(evaluation, state, stage_metadata)
            artifact_plan = architecture.artifact_plan

            previous_findings: list[str] = []
            qa_passed = False
            for cycle in range(self.settings.max_refinement_cycles + 1):
                product_creation, selected_product, artifacts = self.run_product_creation_stage(
                    architecture,
                    evaluation.selected_candidate.id,
                    state,
                    stage_metadata,
                    attempt=cycle + 1,
                )
                refinement_cycles_used = cycle
                try:
                    qa_result = self.run_qa_stage(state, selected_product, architecture.artifact_plan, artifacts, stage_metadata)
                    refinement_history.append(
                        {
                            "cycle": cycle,
                            "targeted_artifacts": [],
                            "qa_outcome": "passed",
                            "findings": [],
                            "decision": "stop",
                            "stop_reason": "qa_passed",
                        }
                    )
                    qa_passed = True
                    refinement_stop_reason = "qa_passed"
                    break
                except QaValidationError as exc:
                    current_findings = list(state.failures[-1:]) if state.failures else [str(exc)]
                    targets = extract_refinement_targets(current_findings)
                    decision = should_continue_refinement(
                        previous_findings=previous_findings,
                        current_findings=current_findings,
                        cycle=cycle,
                        max_cycles=self.settings.max_refinement_cycles,
                    )
                    refinement_history.append(
                        {
                            "cycle": cycle,
                            "targeted_artifacts": [target.__dict__ for target in targets],
                            "qa_outcome": "failed",
                            "findings": current_findings,
                            "decision": "continue" if decision.should_continue else "stop",
                            "stop_reason": decision.stop_reason,
                        }
                    )
                    previous_findings = current_findings
                    refinement_stop_reason = decision.stop_reason
                    if not decision.should_continue:
                        raise

            if not qa_passed:
                raise QaValidationError("Technical QA validation failed after refinement attempts.")

            packaging = self.run_packaging_stage(state, artifacts, architecture.artifact_plan, stage_metadata)
            listing = self.run_listing_stage(selected_product, architecture.artifact_plan, artifacts, state, stage_metadata)
            listing_draft = ListingDraft(
                title=listing.title,
                description=listing.description,
                tags=listing.tags,
            )

            run_context.run.status = RunStatus.COMPLETED
            run_context.run.selected_product_type = selected_product.product_type
            run_context.run.total_cost = state.budget.spent_total
        except AIProductFactoryError as exc:
            final_outcome_reason = str(exc)
            state.fail(str(exc))
            run_context.run.status = RunStatus.FAILED
            run_context.run.total_cost = state.budget.spent_total
        except Exception as exc:
            final_outcome_reason = f"Unexpected error: {exc}"
            state.fail(final_outcome_reason)
            run_context.run.status = RunStatus.FAILED
            run_context.run.total_cost = state.budget.spent_total
            research = None
            evaluation = None
            architecture = None
            product_creation = None
        else:
            final_outcome_reason = "completed"

        report_path = write_run_report(
            state.output_root,
            run_context,
            state,
            selected_product,
            listing_draft,
            qa_result,
            packaging,
            artifacts,
            artifact_plan,
            stage_metadata=stage_metadata,
            final_outcome_reason=final_outcome_reason,
            environment=self.settings.app_env,
            refinement_cycles_used=refinement_cycles_used,
            refinement_stop_reason=refinement_stop_reason,
            refinement_history=refinement_history,
        )

        return {
            "run_context": run_context,
            "state": state,
            "research": locals().get("research"),
            "evaluation": locals().get("evaluation"),
            "architecture": locals().get("architecture"),
            "product_creation": locals().get("product_creation"),
            "selected_product": selected_product,
            "qa": qa_result,
            "listing": listing_draft,
            "packaging": packaging,
            "artifacts": artifacts,
            "report_path": report_path,
            "stage_metadata": stage_metadata,
            "refinement_cycles_used": refinement_cycles_used,
            "refinement_stop_reason": refinement_stop_reason,
            "refinement_history": refinement_history,
        }