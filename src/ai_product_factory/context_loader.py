from pathlib import Path

from .config import AppSettings


def load_context_text(base_path: Path, settings: AppSettings) -> str:
    context_sources = [
        base_path / ".." / "AI_PRODUCT_FACTORY_PROJECT_SPEC.md",
        base_path / ".." / "IMPLEMENTATION_PLAN.md",
        base_path / ".." / "crew-ai-context",
    ]

    parts: list[str] = []
    for path in context_sources:
        resolved = path.resolve()
        if resolved.exists():
            parts.append(resolved.read_text(encoding="utf-8"))

    return "\n\n".join(parts)
