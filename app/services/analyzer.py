"""CV versus job description analysis.

Scoring model (transparent and explainable):
- 50 percent from TF-IDF cosine similarity between CV and job text
- 50 percent from the share of job skills that also appear in the CV

The result is an ATS style score from 0 to 100.
"""
import math
from collections import Counter

from .preprocessing import tokenize
from .skills import detect_skills, flatten_skills


def tfidf_vectors(doc_a: list[str], doc_b: list[str]) -> tuple[dict, dict]:
    """Build TF-IDF vectors for two documents using only the stdlib."""
    docs = [doc_a, doc_b]
    counters = [Counter(d) for d in docs]
    vocab = set(doc_a) | set(doc_b)
    vectors: list[dict[str, float]] = []
    for counter in counters:
        total = sum(counter.values()) or 1
        vector: dict[str, float] = {}
        for term in vocab:
            tf = counter.get(term, 0) / total
            if tf == 0:
                vector[term] = 0.0
                continue
            doc_freq = sum(1 for c in counters if c.get(term, 0) > 0)
            idf = math.log((len(docs) + 1) / (doc_freq + 1)) + 1.0
            vector[term] = tf * idf
        vectors.append(vector)
    return vectors[0], vectors[1]


def cosine_similarity(vec_a: dict[str, float], vec_b: dict[str, float]) -> float:
    """Compute cosine similarity between two sparse vectors."""
    dot = sum(vec_a[k] * vec_b[k] for k in vec_a)
    norm_a = math.sqrt(sum(v * v for v in vec_a.values()))
    norm_b = math.sqrt(sum(v * v for v in vec_b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def analyze_cv(cv_text: str, job_text: str) -> dict:
    """Analyze a CV against a job description.

    Returns the score, similarity, matched and missing skills, and
    concrete recommendations that a candidate can act on.
    """
    if not cv_text.strip() or not job_text.strip():
        raise ValueError("cv_text and job_text must not be empty")

    cv_tokens = tokenize(cv_text)
    job_tokens = tokenize(job_text)
    vec_cv, vec_job = tfidf_vectors(cv_tokens, job_tokens)
    similarity = cosine_similarity(vec_cv, vec_job)

    cv_skills = flatten_skills(detect_skills(cv_text))
    job_skills = flatten_skills(detect_skills(job_text))
    matched = sorted(set(cv_skills) & set(job_skills))
    missing = sorted(set(job_skills) - set(cv_skills))
    skill_ratio = (len(matched) / len(job_skills)) if job_skills else 0.0

    score = round(((similarity * 0.5) + (skill_ratio * 0.5)) * 100, 2)
    score = max(0.0, min(100.0, score))

    recommendations: list[str] = []
    if missing:
        recommendations.append(
            "Pelajari atau tampilkan skill yang belum ada di CV ini: "
            + ", ".join(missing[:5])
            + "."
        )
    if similarity < 0.25:
        recommendations.append(
            "Sesuaikan kata kunci di CV dengan bahasa yang dipakai "
            "pada deskripsi pekerjaan, terutama pada bagian pengalaman."
        )
    if len(cv_tokens) < 80:
        recommendations.append(
            "CV terdeteksi cukup singkat. Tambahkan pencapaian terukur "
            "pada setiap pengalaman, bukan hanya daftar tugas."
        )
    if not recommendations:
        recommendations.append(
            "CV sudah selaras dengan deskripsi pekerjaan. Pertahankan "
            "struktur ini dan sesuaikan hanya pada detail peran."
        )

    if score >= 75:
        verdict = "Sangat selaras"
    elif score >= 50:
        verdict = "Cukup selaras, masih bisa ditingkatkan"
    elif score >= 30:
        verdict = "Kurang selaras, perlu penyesuaian"
    else:
        verdict = "Belum selaras, perlu revisi besar"

    return {
        "ats_score": score,
        "verdict": verdict,
        "text_similarity": round(similarity, 4),
        "skill_match_ratio": round(skill_ratio, 4),
        "cv_skills": cv_skills,
        "job_skills": job_skills,
        "matched_skills": matched,
        "missing_skills": missing,
        "recommendations": recommendations,
    }
