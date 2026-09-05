from pathlib import Path

import pytest

from ai_product_factory.cli import apply_cli_overrides, load_topics_from_file, parse_args, resolve_topics
from ai_product_factory.config import AppSettings


def test_parse_args_topic_required_shape() -> None:
    args = parse_args(["--topic", "etsy planners", "--topic", "wedding checklists"])
    assert args.topic == ["etsy planners", "wedding checklists"]


def test_apply_cli_overrides() -> None:
    settings = AppSettings()
    args = parse_args([
        "--topic",
        "etsy planners",
        "--output-dir",
        "custom-runs",
        "--allow-placeholder-fallback",
        "false",
    ])

    updated = apply_cli_overrides(settings, args)

    assert str(updated.runs_dir) == "custom-runs"
    assert updated.ai_allow_placeholder_fallback is False


def test_load_topics_from_file(tmp_path: Path) -> None:
    topic_file = tmp_path / "topics.txt"
    topic_file.write_text("etsy planners\n# ignore\n\nwedding checklists\n", encoding="utf-8")

    topics = load_topics_from_file(str(topic_file))

    assert topics == ["etsy planners", "wedding checklists"]


def test_resolve_topics_dedupes_file_and_args(tmp_path: Path) -> None:
    topic_file = tmp_path / "topics.txt"
    topic_file.write_text("etsy planners\nwedding checklists\n", encoding="utf-8")
    args = parse_args(["--topic", "etsy planners", "--topic-file", str(topic_file)])

    topics = resolve_topics(args)

    assert topics == ["etsy planners", "wedding checklists"]


def test_resolve_topics_requires_at_least_one() -> None:
    args = parse_args([])
    with pytest.raises(ValueError):
        resolve_topics(args)
