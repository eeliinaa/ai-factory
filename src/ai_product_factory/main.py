from pathlib import Path

from .cli import apply_cli_overrides, parse_args, resolve_topics
from .config import AppSettings
from .context_loader import load_context_text
from .core import AIService
from .db import initialize_database
from .history import format_best_runs, format_json, format_run_comparison, format_run_detail, format_runs_list
from .logging_setup import configure_logging
from .outputs import write_batch_summary
from .pipeline import PipelineRunner
from .providers import ModelPolicy, OpenAIProvider
from .storage import SQLiteRepository


def main(argv: list[str] | None = None) -> None:
    configure_logging()
    args = parse_args(argv)
    settings = apply_cli_overrides(AppSettings(), args)
    settings.validate_runtime_configuration()
    initialize_database(settings.db_path)
    Path(settings.runs_dir).mkdir(parents=True, exist_ok=True)

    repository = SQLiteRepository(settings.db_path)

    if args.list_runs:
        runs = repository.list_runs(limit=args.limit, status=args.status, topic_contains=args.topic_contains)
        print(format_json(runs) if args.json else format_runs_list(runs))
        return

    if args.run_id:
        details = repository.get_run_details(args.run_id)
        if details is None:
            raise ValueError(f"Run not found: {args.run_id}")
        print(format_json(details) if args.json else format_run_detail(details))
        return

    if args.compare_run:
        comparison = repository.compare_runs(args.compare_run)
        print(format_json(comparison) if args.json else format_run_comparison(comparison))
        return

    if args.best_runs:
        best_runs = repository.list_best_runs(limit=args.limit, sort_by=args.sort_by)
        print(format_json(best_runs) if args.json else format_best_runs(best_runs))
        return

    topics = resolve_topics(args)
    project_root = Path(__file__).resolve().parents[2]
    context_text = load_context_text(project_root, settings)
    provider = OpenAIProvider(
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url,
        timeout_seconds=settings.openai_timeout_seconds,
        allow_placeholder_fallback=settings.ai_allow_placeholder_fallback,
    )
    model_policy = ModelPolicy(settings)
    ai_service = AIService(
        provider=provider,
        model_policy=model_policy,
        structured_output_retries=settings.ai_structured_output_retries,
    )

    runner = PipelineRunner(settings, context_text=context_text, ai_service=ai_service)
    batch_results: list[dict] = []

    for topic in topics:
        result = runner.run(topic=topic)
        run_context = result["run_context"]
        repository.save_run(run_context)
        if result["research"] is not None:
            repository.save_candidates(run_context.run.id, result["research"].candidates)
        if result["evaluation"] is not None:
            repository.save_scores(run_context.run.id, result["evaluation"].scores)
        if result["selected_product"] is not None:
            repository.save_selected_product(run_context.run.id, result["selected_product"])
        if result["artifacts"]:
            repository.save_artifacts(run_context.run.id, result["artifacts"])
        if result["listing"] is not None:
            repository.save_listing(run_context.run.id, result["listing"])

        batch_results.append(
            {
                "topic": topic,
                "status": run_context.run.status.value,
                "selected_product": (
                    result["selected_product"].product_title if result["selected_product"] is not None else None
                ),
                "selected_product_type": (
                    result["selected_product"].product_type.value if result["selected_product"] is not None else None
                ),
                "total_cost": run_context.run.total_cost,
                "output_path": str(run_context.run.output_path),
                "report_path": str(result["report_path"]),
                "failure_reason": result["state"].failures[-1] if result["state"].failures else None,
            }
        )

    summary_path = write_batch_summary(Path(settings.runs_dir), batch_results)

    print("Batch run summary")
    print("=================")
    for item in batch_results:
        print(
            f"- Topic: {item['topic']} | Status: {item['status']} | "
            f"Selected: {item['selected_product'] or 'N/A'} | Cost: {item['total_cost']}"
        )
    print(f"Total runs: {len(batch_results)}")
    print(f"Completed: {sum(1 for item in batch_results if item['status'] == 'completed')}")
    print(f"Failed: {sum(1 for item in batch_results if item['status'] == 'failed')}")
    print(f"Batch summary: {summary_path}")


if __name__ == "__main__":
    main()
