"""Skill taxonomy and skill detection.

The taxonomy is intentionally editable. Add or remove skills in
SKILL_TAXONOMY to adapt the tool to a new domain.
"""
import re

SKILL_TAXONOMY: dict[str, list[str]] = {
    "programming": [
        "python", "javascript", "typescript", "java", "c++", "c#", "go",
        "rust", "php", "sql", "html", "css", "kotlin", "swift", "r",
    ],
    "data_and_ai": [
        "machine learning", "deep learning", "data science", "tensorflow",
        "keras", "pytorch", "scikit-learn", "pandas", "numpy", "nlp",
        "computer vision", "data analysis", "data visualization",
        "statistics", "excel", "tableau", "power bi",
    ],
    "backend_and_api": [
        "fastapi", "flask", "django", "node.js", "express", "rest api",
        "graphql", "postgresql", "mysql", "mongodb", "redis", "docker",
        "git", "github", "linux", "ci/cd",
    ],
    "frontend_and_mobile": [
        "react", "vue", "angular", "next.js", "tailwind", "flutter",
        "react native", "figma", "ui/ux",
    ],
    "soft_skills": [
        "communication", "teamwork", "leadership", "problem solving",
        "project management", "time management", "presentation",
    ],
}

ALL_SKILLS: list[str] = sorted(
    {skill for skills in SKILL_TAXONOMY.values() for skill in skills}
)


def detect_skills(text: str) -> dict[str, list[str]]:
    """Detect taxonomy skills mentioned in text, grouped by category."""
    lowered = f" {text.lower()} "
    found: dict[str, list[str]] = {}
    for category, skills in SKILL_TAXONOMY.items():
        matched = []
        for skill in skills:
            pattern = r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])"
            if re.search(pattern, lowered):
                matched.append(skill)
        if matched:
            found[category] = sorted(matched)
    return found


def flatten_skills(grouped: dict[str, list[str]]) -> list[str]:
    """Flatten grouped skills into one sorted list."""
    return sorted({s for skills in grouped.values() for s in skills})
