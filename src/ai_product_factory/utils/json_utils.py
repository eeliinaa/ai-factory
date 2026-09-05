import json
from typing import Any


def extract_json_object(raw_text: str) -> dict[str, Any]:
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        start = raw_text.find("{")
        end = raw_text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise ValueError("No JSON object found in model response.")
        snippet = raw_text[start : end + 1]
        return json.loads(snippet)
