import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.analyzer import analyze_cv

CV = (
    "Python developer with machine learning experience using TensorFlow, "
    "Pandas, NumPy, FastAPI, SQL, Git and GitHub. Built REST API services "
    "and data analysis pipelines with strong communication and teamwork."
)
JOB = (
    "We need a Python engineer with machine learning, TensorFlow, FastAPI, "
    "SQL, Docker and REST API experience. Pandas and Git are required."
)
JOB_UNRELATED = (
    "We need a professional chef for a French restaurant kitchen with "
    "five years of culinary experience in baking and pastry arts."
)


def test_matching_cv_scores_higher_than_unrelated():
    matched = analyze_cv(CV, JOB)
    unrelated = analyze_cv(CV, JOB_UNRELATED)
    assert matched["ats_score"] > unrelated["ats_score"]


def test_detects_matched_and_missing_skills():
    result = analyze_cv(CV, JOB)
    assert "python" in result["matched_skills"]
    assert "docker" in result["missing_skills"]


def test_score_is_within_range():
    result = analyze_cv(CV, JOB)
    assert 0 <= result["ats_score"] <= 100


def test_empty_input_raises():
    try:
        analyze_cv("", JOB)
        assert False, "expected ValueError"
    except ValueError:
        pass
