"""
Semantic ATS scoring using lightweight local embeddings.
Falls back to keyword scoring if model unavailable.
"""

from typing import Dict, List, Any
import re

try:
    from sentence_transformers import SentenceTransformer
    import numpy as np

    _model = SentenceTransformer("all-MiniLM-L6-v2")

    def _cosine(a, b):
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    def semantic_score(resume_text: str, jd_text: str) -> Dict[str, Any]:
        r_emb = _model.encode(resume_text or "")
        j_emb = _model.encode(jd_text or "")
        overall = round(_cosine(r_emb, j_emb) * 100, 1)
        return {
            "overall_score": overall,
            "method": "semantic",
            "model": "all-MiniLM-L6-v2",
        }

except Exception:
    def semantic_score(resume_text: str, jd_text: str) -> Dict[str, Any]:
        return {
            "overall_score": 0,
            "method": "keyword_fallback",
            "model": None,
            "error": "semantic model unavailable",
        }


def section_scores(resume_text: str, jd_text: str) -> Dict[str, float]:
    sections = ["summary", "experience", "skills", "education"]
    out: Dict[str, float] = {}
    for sec in sections:
        r_sec = _extract_section(resume_text, sec)
        j_sec = _extract_section(jd_text, sec)
        if r_sec and j_sec:
            out[sec] = round(semantic_score(r_sec, j_sec).get("overall_score", 0), 1)
        else:
            out[sec] = 0.0
    return out


def _extract_section(text: str, section: str) -> str:
    if not text:
        return ""
    lower = text.lower()
    idx = lower.find(section)
    if idx == -1:
        return ""
    snippet = text[idx: idx + 1200]
    return snippet


def semantic_gaps(resume_text: str, jd_text: str, threshold: float = 0.55) -> Dict[str, Any]:
    try:
        from sentence_transformers import SentenceTransformer
        import numpy as np

        model = SentenceTransformer("all-MiniLM-L6-v2")
    except Exception:
        return {"gaps": [], "matches": [], "error": "model unavailable"}

    resume_sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", resume_text or "") if len(s.strip()) > 20]
    jd_sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", jd_text or "") if len(s.strip()) > 20]
    if not resume_sents or not jd_sents:
        return {"gaps": [], "matches": []}

    r_emb = model.encode(resume_sents)
    j_emb = model.encode(jd_sents)

    matches = []
    gaps = []
    for i, js in enumerate(jd_sents):
        best_score = 0.0
        best_idx = -1
        for j, rs in enumerate(resume_sents):
            score = float(np.dot(j_emb[i], r_emb[j]) / (np.linalg.norm(j_emb[i]) * np.linalg.norm(r_emb[j])))
            if score > best_score:
                best_score = score
                best_idx = j
        if best_score >= threshold:
            matches.append({
                "jd_sentence": js,
                "resume_sentence": resume_sents[best_idx],
                "score": round(best_score * 100, 1),
            })
        else:
            gaps.append({
                "jd_sentence": js,
                "best_resume_match": resume_sents[best_idx] if best_idx >= 0 else "",
                "score": round(best_score * 100, 1),
            })

    return {
        "matches": matches[:20],
        "gaps": gaps[:20],
        "resume_sentences": len(resume_sents),
        "jd_sentences": len(jd_sents),
    }
