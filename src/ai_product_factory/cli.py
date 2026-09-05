import argparse
from pathlib import Path

from .config import AppSettings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the AI Product Factory pipeline")
    parser.add_argument("--topic", action="append", help="Topic to generate product ideas for")
    parser.add_argument("--topic-file", help="Path to a file with one topic per line")
    parser.add_argument("--output-dir", help="Optional output directory override for this run")
    parser.add_argument(
        "--allow-placeholder-fallback",
        choices=["true", "false"],
        help="Override placeholder fallback behavior for this run",
    )
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("--live", action="store_true", help="Force live mode without placeholder fallback")
    mode_group.add_argument("--placeholder", action="store_true", help="Force placeholder fallback mode")

    parser.add_argument("--list-runs", action="store_true", help="List previously saved runs")
    parser.add_argument("--run-id", help="Show detailed information for a specific run id")
    parser.add_argument("--compare-run", action="append", help="Compare one or more run ids")
    parser.add_argument("--best-runs", action="store_true", help="Show best successful runs")
    parser.add_argument("--limit", type=int, default=10, help="Limit for history queries")
    parser.add_argument("--status", help="Filter runs by status")
    parser.add_argument("--topic-contains", help="Filter runs whose topic contains this string")
    parser.add_argument("--sort-by", choices=["score", "cost", "newest"], default="newest", help="Sort mode for best runs")
    parser.add_argument("--json", action="store_true", help="Print history/detail output as JSON")
    return parser


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    return build_parser().parse_args(argv)


def load_topics_from_file(path: str) -> list[str]:
    topics: list[str] = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        normalized = line.strip()
        if not normalized or normalized.startswith("#"):
            continue
        topics.append(normalized)
    return topics


def resolve_topics(args: argparse.Namespace) -> list[str]:
    topics: list[str] = []
    if args.topic:
        topics.extend(topic.strip() for topic in args.topic if topic and topic.strip())
    if args.topic_file:
        topics.extend(load_topics_from_file(args.topic_file))

    deduped: list[str] = []
    seen: set[str] = set()
    for topic in topics:
        if topic not in seen:
            deduped.append(topic)
            seen.add(topic)

    if not deduped and not args.list_runs and not args.run_id and not args.compare_run and not args.best_runs:
        raise ValueError("At least one topic must be provided via --topic or --topic-file.")
    return deduped


def apply_cli_overrides(settings: AppSettings, args: argparse.Namespace) -> AppSettings:
    if args.output_dir:
        settings.runs_dir = Path(args.output_dir)
    if args.allow_placeholder_fallback is not None:
        settings.ai_allow_placeholder_fallback = args.allow_placeholder_fallback == "true"
    if args.live:
        settings.ai_allow_placeholder_fallback = False
    if args.placeholder:
        settings.ai_allow_placeholder_fallback = True
    return settings
