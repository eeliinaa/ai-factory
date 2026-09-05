from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from pydantic import BaseModel, Field

from .enums import ProductType, RunStatus


class Run(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    topic: str
    status: RunStatus = RunStatus.PENDING
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    output_path: Path
    total_cost: float = 0.0
    selected_product_type: ProductType | None = None


class RunContext(BaseModel):
    run: Run

    @classmethod
    def create(cls, topic: str, output_dir: Path) -> "RunContext":
        return cls(run=Run(topic=topic, output_path=output_dir))
