MODEL_PRICING = {
    "gpt-5-mini": {"input_per_1m": 0.25, "output_per_1m": 2.0},
    "gpt-4.1-mini": {"input_per_1m": 0.4, "output_per_1m": 1.6},
}


def estimate_cost(model: str, prompt_tokens: int, completion_tokens: int) -> tuple[float, str]:
    pricing = MODEL_PRICING.get(model)
    if pricing is None:
        return 0.0, "unknown"

    input_cost = (prompt_tokens / 1_000_000) * pricing["input_per_1m"]
    output_cost = (completion_tokens / 1_000_000) * pricing["output_per_1m"]
    return input_cost + output_cost, "estimated"
