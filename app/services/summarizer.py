"""Extractive summarization.

Sentences are scored by the average frequency of their meaningful
words. The highest scoring sentences are returned in original order.
"""
import re

from .preprocessing import tokenize, word_frequencies


def split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p.strip() for p in parts if len(p.strip()) > 15]


def summarize(text: str, max_sentences: int = 3) -> dict:
    """Summarize text into its most informative sentences."""
    sentences = split_sentences(text)
    if not sentences:
        return {"summary": "", "sentence_count": 0, "sentences": []}
    if len(sentences) <= max_sentences:
        return {
            "summary": " ".join(sentences),
            "sentence_count": len(sentences),
            "sentences": sentences,
        }

    frequencies = word_frequencies(text)
    max_freq = max(frequencies.values()) if frequencies else 1

    scored: list[tuple[int, float, str]] = []
    for index, sentence in enumerate(sentences):
        tokens = tokenize(sentence)
        if not tokens:
            continue
        score = sum(frequencies.get(t, 0) / max_freq for t in tokens) / len(tokens)
        scored.append((index, score, sentence))

    top = sorted(scored, key=lambda item: item[1], reverse=True)[:max_sentences]
    chosen = [sentence for _, _, sentence in sorted(top, key=lambda item: item[0])]
    return {
        "summary": " ".join(chosen),
        "sentence_count": len(chosen),
        "sentences": chosen,
    }
