import re


def slugify_topic(topic: str, max_length: int = 80) -> str:
    normalized = topic.strip().lower()
    normalized = re.sub(r"[^a-z0-9]+", "_", normalized)
    normalized = normalized.strip("_")
    if not normalized:
        raise ValueError("Topic must not be empty.")
    return normalized[:max_length]
