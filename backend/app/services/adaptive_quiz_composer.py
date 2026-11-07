"""Deterministic, evidence-driven quiz composition.

The composer deliberately contains no randomness. The same learner evidence,
question pool and seed produce the same form, which makes assessment results
reproducible and auditable while still allowing equivalent forms by changing the
seed per attempt.
"""
from __future__ import annotations

import hashlib
from collections import Counter, defaultdict
from typing import Any, Iterable


def _text(value: Any) -> str:
    return str(value or "").strip()


def question_skills(question: dict[str, Any]) -> list[str]:
    """Return stable skill labels from mixed legacy question schemas."""
    raw: list[Any] = []
    for key in ("canonical_skills", "skills", "skill_ids", "skill", "sub_topic", "topic", "pattern"):
        value = question.get(key)
        if isinstance(value, (list, tuple, set)):
            raw.extend(value)
        elif value:
            raw.append(value)
    seen: set[str] = set()
    result: list[str] = []
    for value in raw:
        label = _text(value).lower().replace("-", "_").replace(" ", "_")
        if label and label not in seen:
            seen.add(label)
            result.append(label)
    return result or ["unmapped"]


def _stable_rank(seed: str, question_id: str) -> str:
    return hashlib.sha256(f"{seed}:{question_id}".encode("utf-8")).hexdigest()


def _normalise_company(value: str | None) -> str:
    return _text(value).lower().replace(" ", "_")


def compose_quiz(
    questions: Iterable[dict[str, Any]],
    *,
    num_questions: int,
    seed: str,
    evidence: dict[str, Any] | None = None,
    company: str | None = None,
    difficulty: str | None = None,
    target_skills: list[str] | None = None,
) -> dict[str, Any]:
    """Select a reproducible, weakness-first, diverse assessment form.

    Evidence accepts either ``skill_scores`` (0..1), ``weak_skills`` and
    ``due_skills``. Unknown skills receive a small exploration bonus. The
    algorithm is intentionally explainable: every selected item exposes the
    signals that caused it to rank highly.
    """
    evidence = evidence or {}
    requested = max(1, int(num_questions))
    company_key = _normalise_company(company)
    wanted = {
        _text(skill).lower().replace("-", "_").replace(" ", "_")
        for skill in (target_skills or []) if _text(skill)
    }
    raw_scores = evidence.get("skill_scores") or {}
    skill_scores = {
        _text(key).lower().replace("-", "_").replace(" ", "_"): float(value)
        for key, value in raw_scores.items()
        if _text(key)
    }
    weak = {
        _text(value).lower().replace("-", "_").replace(" ", "_")
        for value in (evidence.get("weak_skills") or []) if _text(value)
    }
    due = {
        _text(value).lower().replace("-", "_").replace(" ", "_")
        for value in (evidence.get("due_skills") or []) if _text(value)
    }
    seen_ids = {str(value) for value in (evidence.get("seen_question_ids") or [])}
    target_difficulty = _text(difficulty).lower() or _text(evidence.get("recommended_difficulty")).lower()
    if target_difficulty not in {"easy", "medium", "hard"}:
        target_difficulty = "medium"

    candidates: list[tuple[float, str, dict[str, Any], dict[str, Any]]] = []
    for question in questions:
        question_id = _text(question.get("id"))
        if not question_id:
            continue
        skills = question_skills(question)
        skill_score = max((skill_scores.get(skill, 0.5) for skill in skills), default=0.5)
        weakness = max((1.0 - skill_scores.get(skill, 0.5) for skill in skills), default=0.5)
        if any(skill in weak for skill in skills):
            weakness = max(weakness, 0.9)
        due_bonus = 0.35 if any(skill in due for skill in skills) else 0.0
        target_bonus = 0.45 if wanted.intersection(skills) else 0.0
        q_companies = question.get("companies") or question.get("company") or []
        if isinstance(q_companies, str):
            q_companies = [q_companies]
        # A company-targeted form must contain company-relevant evidence when
        # the pool has it; this outweighs a small generic weakness difference.
        company_bonus = 1.6 if company_key and any(_normalise_company(str(item)) == company_key for item in q_companies) else 0.0
        unseen_bonus = 0.18 if question_id not in seen_ids else -0.08
        q_difficulty = _text(question.get("difficulty")).lower() or "medium"
        difficulty_bonus = 0.25 if q_difficulty == target_difficulty else 0.0
        score = (weakness * 1.6) + due_bonus + target_bonus + company_bonus + unseen_bonus + difficulty_bonus
        reason = {
            "weakness": round(weakness, 3),
            "skill_score": round(skill_score, 3),
            "due_review": bool(due_bonus),
            "company_match": bool(company_bonus),
            "unseen": question_id not in seen_ids,
            "target_skill": bool(target_bonus),
        }
        candidates.append((score, _stable_rank(seed, question_id), question, reason))

    candidates.sort(key=lambda item: (-item[0], item[1]))
    selected: list[dict[str, Any]] = []
    skill_counts: Counter[str] = Counter()
    for base_score, rank, question, reason in candidates:
        skills = question_skills(question)
        # Greedy diversity: do not exhaust one concept while another viable
        # concept has not appeared in the form.
        dominant = max(skills, key=lambda skill: (skill_scores.get(skill, 0.5), skill))
        diversity_penalty = skill_counts[dominant] * 0.28
        effective_score = base_score - diversity_penalty
        if len(selected) < requested:
            selected.append({"question": question, "score": effective_score, "reason": reason, "rank": rank})
            skill_counts[dominant] += 1
        else:
            weakest_index = min(range(len(selected)), key=lambda index: (selected[index]["score"], selected[index]["rank"]))
            if effective_score > selected[weakest_index]["score"]:
                replaced = selected[weakest_index]
                old_skill = max(question_skills(replaced["question"]), key=lambda skill: (skill_scores.get(skill, 0.5), skill))
                skill_counts[old_skill] -= 1
                selected[weakest_index] = {"question": question, "score": effective_score, "reason": reason, "rank": rank}
                skill_counts[dominant] += 1

    selected.sort(key=lambda item: item["rank"])
    return {
        "questions": [item["question"] for item in selected],
        "selection_evidence": [
            {"question_id": item["question"].get("id"), **item["reason"]}
            for item in selected
        ],
        "skill_distribution": dict(skill_counts),
        "strategy": "evidence_first_deterministic_v1",
        "seed": seed,
        "evidence_summary": {
            "weak_skills": sorted(weak),
            "due_skills": sorted(due),
            "seen_question_count": len(seen_ids),
            "company": company,
            "target_difficulty": target_difficulty,
        },
    }
