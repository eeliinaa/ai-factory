from pydantic import BaseModel, Field


class ListingDraft(BaseModel):
    title: str
    description: str
    tags: list[str] = Field(default_factory=list)
    listing_version: int = 1
