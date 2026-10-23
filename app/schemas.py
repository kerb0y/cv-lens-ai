"""Request and response schemas for the API."""
from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    cv_text: str = Field(..., min_length=20, description="Full CV text")
    job_text: str = Field(..., min_length=20, description="Job description text")


class AnalyzeResponse(BaseModel):
    ats_score: float
    verdict: str
    text_similarity: float
    skill_match_ratio: float
    cv_skills: list[str]
    job_skills: list[str]
    matched_skills: list[str]
    missing_skills: list[str]
    recommendations: list[str]


class TextRequest(BaseModel):
    text: str = Field(..., min_length=20)
    top_n: int = Field(default=10, ge=1, le=50)


class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=40)
    max_sentences: int = Field(default=3, ge=1, le=10)
