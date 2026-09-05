from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel, Field


class LLMRequest(BaseModel):
    stage_name: str
    system_prompt: str
    user_prompt: str
    model: str
    temperature: float = 0.2
    require_json: bool = False
    prompt_version: str = "v1"


class LLMResponse(BaseModel):
    model: str
    content: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    estimated_cost: float = 0.0
    metadata: dict[str, Any] = Field(default_factory=dict)


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, request: LLMRequest) -> LLMResponse:
        raise NotImplementedError
