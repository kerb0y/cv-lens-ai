"""Keyword extraction based on word frequency after preprocessing."""
from .preprocessing import word_frequencies


def extract_keywords(text: str, top_n: int = 10) -> list[dict]:
    """Return the top keywords with their frequencies."""
    frequencies = word_frequencies(text)
    return [
        {"keyword": word, "count": count}
        for word, count in frequencies.most_common(top_n)
    ]
