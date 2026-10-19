"""Explicit, grounded TF-IDF evidence search — no fabricated LLM answers."""
from __future__ import annotations
from functools import lru_cache
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DOCS = Path(__file__).resolve().parent.parent / "knowledge"

@lru_cache(maxsize=1)
def index():
    docs = sorted(DOCS.glob("*.md"))
    texts = [p.read_text(encoding="utf-8") for p in docs]
    if not texts:
        raise RuntimeError("Knowledge documents are missing")
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
    vectors = vectorizer.fit_transform(texts)
    return docs, texts, vectorizer, vectors

def search(query: str, limit: int = 3) -> list[dict]:
    if not query.strip():
        return []
    docs, texts, vectorizer, vectors = index()
    scores = cosine_similarity(vectorizer.transform([query]), vectors).ravel()
    ranking = scores.argsort()[::-1][:limit]
    matches = []
    for i in ranking:
        if scores[i] <= 0:
            continue
        text = texts[i]
        lines = [s.strip() for s in text.splitlines() if s.strip()]
        matches.append({
            "document_id": docs[i].stem,
            "title": lines[0].removeprefix("# "),
            "citation": lines[1].removeprefix("Source: ") if len(lines) > 1 else docs[i].name,
            "score": round(float(scores[i]), 4),
            "excerpt": " ".join(lines[2:])[:560],
            "source_path": str(Path("knowledge") / docs[i].name),
        })
    return matches
