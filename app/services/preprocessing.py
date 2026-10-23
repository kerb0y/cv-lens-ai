"""Text preprocessing utilities.

Pure standard library implementation so the core logic can run
anywhere without heavy dependencies.
"""
import re
from collections import Counter

STOPWORDS_ID = {
    "yang", "dan", "di", "ke", "dari", "untuk", "dengan", "pada", "adalah",
    "ini", "itu", "atau", "juga", "dalam", "sebagai", "telah", "akan",
    "oleh", "tidak", "ada", "saya", "kami", "anda", "mereka", "dapat",
    "secara", "agar", "karena", "saat", "sudah", "lebih", "sangat",
}

STOPWORDS_EN = {
    "the", "and", "of", "to", "in", "a", "is", "for", "with", "on",
    "as", "by", "an", "be", "this", "that", "or", "are", "was", "were",
    "will", "have", "has", "had", "at", "from", "it", "its", "you",
    "your", "we", "our", "they", "their", "i", "my", "me", "am",
}

STOPWORDS = STOPWORDS_ID | STOPWORDS_EN


def clean_text(text: str) -> str:
    """Lowercase text and keep only letters, numbers and a few symbols.

    The plus, hash and dot characters are kept so skills such as
    c++, c#, and node.js survive cleaning.
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#.\s-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def tokenize(text: str, remove_stopwords: bool = True) -> list[str]:
    """Split cleaned text into tokens, optionally removing stopwords."""
    cleaned = clean_text(text)
    tokens = [t.strip(".") for t in cleaned.split() if t.strip(".")]
    if remove_stopwords:
        tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 1]
    return tokens


def word_frequencies(text: str) -> Counter:
    """Return a Counter of token frequencies for the given text."""
    return Counter(tokenize(text))
