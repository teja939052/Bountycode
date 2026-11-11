"""Service-company OA mock generator.

Builds timed, section-weighted mocks from:
  - app/data/company_exam_ontology.json
  - app/data/service_oa_problem_bank_part*.json

Questions are original exam-style items tagged by company and topic.
"""

from __future__ import annotations

import glob
import json
import os
import random
import uuid
from functools import lru_cache
from typing import Any, Dict, List, Optional

_DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

COMPANY_ALIASES = {
    "tcs": "tcs_nqt",
    "tcs_nqt": "tcs_nqt",
    "nqt": "tcs_nqt",
    "infosys": "infosys",
    "infy": "infosys",
    "wipro": "wipro_nlth",
    "wipro_nlth": "wipro_nlth",
    "nlth": "wipro_nlth",
    "cognizant": "cognizant_genc",
    "cognizant_genc": "cognizant_genc",
    "genc": "cognizant_genc",
    "accenture": "accenture",
}

BANK_TAG = {
    "tcs_nqt": "tcs",
    "infosys": "infosys",
    "wipro_nlth": "wipro",
    "cognizant_genc": "cognizant",
    "accenture": "accenture",
}

SECTION_LABELS = {
    "numerical_ability": "Numerical Ability",
    "reasoning_ability": "Reasoning Ability",
    "verbal_ability": "Verbal Ability",
    "programming_logic": "Programming Logic",
}


@lru_cache(maxsize=1)
def load_ontology() -> Dict[str, Any]:
    path = os.path.join(_DATA, "company_exam_ontology.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def load_problem_bank() -> List[Dict[str, Any]]:
    """Load all curated service OA parts (part1, part2, part3, …)."""
    problems: List[Dict[str, Any]] = []
    paths = sorted(glob.glob(os.path.join(_DATA, "service_oa_problem_bank_part*.json")))
    for path in paths:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        problems.extend(data.get("problems") or [])
    seen = set()
    out = []
    for p in problems:
        pid = p.get("id")
        if not pid or pid in seen:
            continue
        if not p.get("options") or p.get("correct_index") is None:
            continue
        if not (p.get("explanation") or "").strip():
            continue
        seen.add(pid)
        out.append(p)
    return out


def resolve_company(key: str) -> str:
    k = (key or "").strip().lower().replace(" ", "_").replace("-", "_")
    if k not in COMPANY_ALIASES:
        raise ValueError(f"Unknown company '{key}'. Use: tcs, infosys, wipro, cognizant, accenture")
    return COMPANY_ALIASES[k]


def list_companies() -> List[Dict[str, Any]]:
    ont = load_ontology()
    rows = []
    for cid, meta in (ont.get("companies") or {}).items():
        rows.append({
            "id": cid,
            "api_keys": [k for k, v in COMPANY_ALIASES.items() if v == cid],
            "name": meta.get("name", cid),
            "tracks": meta.get("tracks") or [],
            "high_weight_topics": meta.get("high_weight_topics") or {},
        })
    return rows


def _section_quota(company_id: str, total: int) -> Dict[str, int]:
    if company_id == "tcs_nqt":
        raw = {"numerical_ability": 8, "reasoning_ability": 7, "verbal_ability": 5, "programming_logic": 5}
    elif company_id == "infosys":
        raw = {"numerical_ability": 6, "reasoning_ability": 8, "verbal_ability": 5, "programming_logic": 6}
    elif company_id == "wipro_nlth":
        raw = {"numerical_ability": 7, "reasoning_ability": 7, "verbal_ability": 6, "programming_logic": 5}
    elif company_id == "cognizant_genc":
        raw = {"numerical_ability": 6, "reasoning_ability": 6, "verbal_ability": 8, "programming_logic": 5}
    else:
        raw = {"numerical_ability": 6, "reasoning_ability": 6, "verbal_ability": 6, "programming_logic": 7}

    base_sum = sum(raw.values())
    scaled = {s: max(1, int(round(total * c / base_sum))) for s, c in raw.items()}
    while sum(scaled.values()) > total:
        k = max(scaled, key=scaled.get)
        if scaled[k] > 1:
            scaled[k] -= 1
        else:
            break
    while sum(scaled.values()) < total:
        k = max(scaled, key=scaled.get)
        scaled[k] += 1
    return scaled


def _weight_for(problem: Dict[str, Any], company_id: str) -> float:
    ont = load_ontology()
    meta = (ont.get("companies") or {}).get(company_id) or {}
    hw = meta.get("high_weight_topics") or {}
    topic = problem.get("topic") or ""
    section = problem.get("section") or ""
    w = 1.0
    for topics in hw.values():
        if isinstance(topics, list) and topic in topics:
            w += 2.0
            break
    tag = BANK_TAG.get(company_id, company_id)
    if tag in (problem.get("companies") or []):
        w += 1.5
    if problem.get("difficulty") == "medium":
        w += 0.3
    if section in ("numerical_ability", "reasoning_ability"):
        w += 0.2
    if "high_freq" in (problem.get("tags") or []):
        w += 0.5
    return w


def _sample_section(
    pool: List[Dict[str, Any]],
    section: str,
    n: int,
    company_id: str,
    rng: random.Random,
) -> List[Dict[str, Any]]:
    candidates = [p for p in pool if p.get("section") == section]
    if not candidates:
        candidates = list(pool)
    if not candidates:
        return []
    weights = [_weight_for(p, company_id) for p in candidates]
    chosen: List[Dict[str, Any]] = []
    items = list(zip(candidates, weights))
    for _ in range(min(n, len(items))):
        total_w = sum(w for _, w in items)
        r = rng.uniform(0, total_w)
        acc = 0.0
        idx = 0
        for i, (_, w) in enumerate(items):
            acc += w
            if acc >= r:
                idx = i
                break
        chosen.append(items[idx][0])
        items.pop(idx)
        if not items:
            break
    return chosen


def _public_question(p: Dict[str, Any], order: int) -> Dict[str, Any]:
    return {
        "id": p["id"],
        "order": order,
        "section": p.get("section"),
        "section_label": SECTION_LABELS.get(p.get("section") or "", p.get("section")),
        "topic": p.get("topic"),
        "difficulty": p.get("difficulty"),
        "prompt": p.get("prompt"),
        "options": p.get("options") or [],
        "time_sec_target": p.get("time_sec_target") or 75,
    }


def generate_mock(
    company: str,
    *,
    question_count: int = 25,
    seed: Optional[int] = None,
    sections: Optional[List[str]] = None,
) -> Dict[str, Any]:
    company_id = resolve_company(company)
    ont = load_ontology()
    meta = (ont.get("companies") or {}).get(company_id) or {}
    bank = load_problem_bank()
    if not bank:
        raise RuntimeError("Problem bank empty — missing service_oa_problem_bank_part*.json")

    qcount = max(5, min(40, int(question_count)))
    quota = _section_quota(company_id, qcount)
    if sections:
        wanted = set(sections)
        quota = {s: c for s, c in quota.items() if s in wanted}
        if not quota:
            quota = {sections[0]: qcount}

    rng = random.Random(seed if seed is not None else uuid.uuid4().int & 0xFFFFFFFF)
    picked: List[Dict[str, Any]] = []
    used_ids = set()
    for section, n in quota.items():
        batch = _sample_section(bank, section, n, company_id, rng)
        for p in batch:
            if p["id"] not in used_ids:
                picked.append(p)
                used_ids.add(p["id"])

    if len(picked) < qcount:
        rest = [p for p in bank if p["id"] not in used_ids]
        rng.shuffle(rest)
        for p in rest:
            if len(picked) >= qcount:
                break
            picked.append(p)
            used_ids.add(p["id"])

    rng.shuffle(picked)
    picked = picked[:qcount]

    duration_sec = sum(int(p.get("time_sec_target") or 75) for p in picked)
    duration_sec = min(duration_sec, 75 * 60)
    duration_sec = max(duration_sec, qcount * 45)

    session_id = f"soa_{company_id}_{uuid.uuid4().hex[:10]}"
    answer_key = {p["id"]: int(p.get("correct_index", 0)) for p in picked}

    return {
        "session_id": session_id,
        "company_id": company_id,
        "company_name": meta.get("name", company_id),
        "tracks": meta.get("tracks") or [],
        "question_count": len(picked),
        "duration_sec": duration_sec,
        "duration_min": max(1, duration_sec // 60),
        "section_quota": quota,
        "sections_present": sorted({p.get("section") for p in picked}),
        "bank_size": len(bank),
        "questions": [_public_question(p, i + 1) for i, p in enumerate(picked)],
        "_answer_key": answer_key,
        "_explanations": {p["id"]: p.get("explanation") or "" for p in picked},
        "_topics": {p["id"]: p.get("topic") for p in picked},
        "_sections": {p["id"]: p.get("section") for p in picked},
    }


def grade_mock(
    *,
    answer_key: Dict[str, int],
    explanations: Dict[str, str],
    topics: Dict[str, str],
    sections: Dict[str, str],
    answers: Dict[str, int],
    company_id: str,
    duration_sec: int,
    time_spent_sec: Optional[int] = None,
) -> Dict[str, Any]:
    total = len(answer_key)
    correct = 0
    by_section: Dict[str, Dict[str, int]] = {}
    by_topic: Dict[str, Dict[str, int]] = {}
    detail = []

    for qid, correct_idx in answer_key.items():
        chosen = answers.get(qid)
        if chosen is None:
            chosen = answers.get(str(qid))
        try:
            chosen_i = int(chosen) if chosen is not None else None
        except (TypeError, ValueError):
            chosen_i = None
        is_ok = chosen_i is not None and chosen_i == int(correct_idx)
        if is_ok:
            correct += 1
        sec = sections.get(qid) or "unknown"
        top = topics.get(qid) or "unknown"
        by_section.setdefault(sec, {"correct": 0, "total": 0})
        by_section[sec]["total"] += 1
        if is_ok:
            by_section[sec]["correct"] += 1
        by_topic.setdefault(top, {"correct": 0, "total": 0})
        by_topic[top]["total"] += 1
        if is_ok:
            by_topic[top]["correct"] += 1
        detail.append({
            "id": qid,
            "section": sec,
            "topic": top,
            "correct": is_ok,
            "chosen": chosen_i,
            "correct_index": int(correct_idx),
            "explanation": explanations.get(qid) or "",
        })

    score_pct = round(100.0 * correct / total, 1) if total else 0.0
    section_scores = {
        s: {
            "correct": v["correct"],
            "total": v["total"],
            "score_pct": round(100.0 * v["correct"] / v["total"], 1) if v["total"] else 0.0,
            "label": SECTION_LABELS.get(s, s),
        }
        for s, v in by_section.items()
    }
    weak_topics = sorted(
        [
            {"topic": t, "score_pct": round(100.0 * v["correct"] / v["total"], 1), **v}
            for t, v in by_topic.items()
            if v["total"] > 0 and (v["correct"] / v["total"]) < 0.7
        ],
        key=lambda x: x["score_pct"],
    )

    if score_pct >= 80:
        band = "strong"
        message = "Strong service-OA readiness on this mix. Push advanced coding next."
    elif score_pct >= 65:
        band = "borderline"
        message = "Near typical cutoffs. Drill weak topics below, then re-mock."
    else:
        band = "needs_work"
        message = "Below safe cutoff. Follow Academy scrims for weak topics before the next mock."

    return {
        "company_id": company_id,
        "correct": correct,
        "total": total,
        "score_pct": score_pct,
        "band": band,
        "message": message,
        "section_scores": section_scores,
        "weak_topics": weak_topics[:8],
        "time_spent_sec": time_spent_sec,
        "duration_sec": duration_sec,
        "detail": detail,
    }
