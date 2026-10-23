import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.keywords import extract_keywords
from app.services.preprocessing import clean_text, tokenize
from app.services.skills import detect_skills
from app.services.summarizer import summarize

TEXT = (
    "Python is a popular language for data science. "
    "Many data scientists use Python with Pandas every day. "
    "Data science combines statistics, programming and domain knowledge. "
    "Cooking dinner at home is a relaxing evening activity for families."
)


def test_clean_text_lowercases():
    assert clean_text("Hello, WORLD!") == "hello world"


def test_tokenize_removes_stopwords():
    tokens = tokenize("the python and the data")
    assert "the" not in tokens
    assert "python" in tokens


def test_detect_skills_groups_by_category():
    found = detect_skills("I use Python, FastAPI and React daily.")
    flat = [s for group in found.values() for s in group]
    assert "python" in flat
    assert "fastapi" in flat


def test_extract_keywords_returns_top_items():
    keywords = extract_keywords(TEXT, top_n=3)
    assert len(keywords) == 3
    assert keywords[0]["count"] >= keywords[-1]["count"]


def test_summarize_picks_fewer_sentences():
    result = summarize(TEXT, max_sentences=2)
    assert result["sentence_count"] == 2
    assert "Python" in result["summary"] or "Data" in result["summary"]
