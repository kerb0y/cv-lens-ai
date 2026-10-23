"""CV Lens AI, FastAPI application.

Run locally:
    uvicorn app.main:app --reload
Then open http://127.0.0.1:8000/docs for the interactive API docs.
"""
from fastapi import FastAPI, HTTPException

from .schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    SummarizeRequest,
    TextRequest,
)
from .services.analyzer import analyze_cv
from .services.keywords import extract_keywords
from .services.summarizer import summarize

app = FastAPI(
    title="CV Lens AI",
    description=(
        "AI toolkit for CV analysis, ATS style scoring, and skill gap "
        "analysis. Built with Python and FastAPI. No external API key "
        "required and CV data never leaves the server."
    ),
    version="1.0.0",
)


@app.get("/")
def root() -> dict:
    return {
        "name": "CV Lens AI",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": ["/analyze", "/keywords", "/summarize", "/health"],
    }


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(payload: AnalyzeRequest) -> dict:
    try:
        return analyze_cv(payload.cv_text, payload.job_text)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/keywords")
def keywords(payload: TextRequest) -> dict:
    return {"keywords": extract_keywords(payload.text, top_n=payload.top_n)}


@app.post("/summarize")
def summarize_text(payload: SummarizeRequest) -> dict:
    return summarize(payload.text, max_sentences=payload.max_sentences)
