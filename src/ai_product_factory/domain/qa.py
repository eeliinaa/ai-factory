from pydantic import BaseModel, Field


class QaResult(BaseModel):
    passed: bool
    findings: list[str] = Field(default_factory=list)
    ai_findings: list[str] = Field(default_factory=list)
    technical_findings: list[str] = Field(default_factory=list)
