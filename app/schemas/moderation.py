from pydantic import BaseModel, Field


class ModerationRequest(BaseModel):
    text: str = Field(..., min_length=2,max_length=500,description="The text to be analyzed")

class ModerationResponse(BaseModel):
    text: str
    is_flagged: bool
    toxicity_score: float
    category: str  # e.g., "toxic", "spam", "clean"