"""Company track overviews — one deterministic reader over the canonical
verified question store + existing OA exam structures. No new content systems:
Foundation sections drill the verified question bank per topic; Advanced lists
verified coding problems with the student's live solved/attempted status.
Pure read aggregation. All questions are TRUSTED and carry their own
provenance (pattern-relevant where no company tag exists)."""

from typing import Optional, Dict, List, Any
from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth import get_current_user
from app.database import solved_problems_collection, question_answers_collection
from app.services import question_store
from app.routes.oa import _EXAM_STRUCTURE_FOR, _VERIFIED_TYPE_FOR_SECTION

router = APIRouter(prefix="/api/v1/tracks", tags=["company-tracks"])

_SECTION_TITLES = {
    "aptitude": "Numerical Ability",
    "logical": "Reasoning Ability",
    "verbal": "Verbal Ability",
    "cs_fundamentals": "Programming (MCQ)",
    "coding": "Coding",
}


def _display_topic(topic) -> str:
    return question_store._display_topic(topic or "General")


def _spread_by_topic(pool, qtype, cap: int) -> list:
    """Pick up to `cap` samples round-robin across topics (diverse practice)."""
    by_topic: Dict[str, list] = {}
    for q in pool:
        if q.get("type") != qtype:
            continue
        by_topic.setdefault(q.get("topic") or "General", []).append(q)
    samples = []
    while len(samples) < cap:
        added = False
        for t in by_topic:
            if len(samples) >= cap:
                break
            if by_topic[t]:
                samples.append(by_topic[t].pop(0))
                added = True
        if not added:
            break
    return samples


async def _status_map(uid: str, ids: List[str]) -> Dict[str, Dict[str, Any]]:
    """Return {question_id: {status, best_score}} from canonical student state."""
    out: Dict[str, Dict[str, Any]] = {}
    solved = set()
    if ids:
        docs = await solved_problems_collection.find(
            {"user_id": uid, "question_id": {"$in": ids}}, {"question_id": 1}
        ).to_list(10000)
        solved = {d.get("question_id") for d in docs}
    best: Dict[str, float] = {}
    if ids:
        cursor = question_answers_collection.find(
            {"user_id": uid, "question_id": {"$in": ids}}, {"question_id": 1, "score": 1}
        )
        async for a in cursor:
            qid = a.get("question_id")
            sc = a.get("score") or 0
            if qid not in best or sc > best[qid]:
                best[qid] = sc
    for qid in ids:
        if qid in solved:
            out[qid] = {"status": "solved", "best_score": None}
        elif qid in best:
            out[qid] = {"status": "attempted", "best_score": round(best[qid], 1)}
        else:
            out[qid] = {"status": "not_started", "best_score": None}
    return out


def _brief(q: dict, st: Dict[str, Any]) -> dict:
    guide = q.get("dsa_guide") or {}
    title = q.get("title") or q.get("question_title") or ""
    if not title:
        snippet = (q.get("question") or "").strip()
        title = (snippet[:72] + "…") if len(snippet) > 72 else snippet or ""
    return {
        "id": q.get("id"),
        "title": title,
        "difficulty": q.get("difficulty") or "medium",
        "status": st["status"],
        "best_score": st["best_score"],
        "topic": _display_topic(q.get("topic")),
        "companies": q.get("companies") or [],
        "provenance": q.get("provenance") or "",
        "statement": (q.get("question") or "")[:220],
        "approach": guide.get("approach") or "",
        "complexity": guide.get("complexity") or {},
        "testcase_count": len(q.get("testcases") or (q.get("solution") or {}).get("testcases") or []),
    }


@router.get("/{company}/overview")
async def company_track_overview(
    company: str,
    user=Depends(get_current_user),
    foundation_cap: int = 8,
    coding_cap: int = 25,
):
    canon = question_store.canonical_company_key(company)
    if canon not in _EXAM_STRUCTURE_FOR and canon not in question_store._COMPANY_TAG_ALIASES:
        raise HTTPException(status_code=404, detail=f"No track for company: {company}")
    structure = _EXAM_STRUCTURE_FOR.get(canon)
    bank = question_store.company_verified_bank(canon)
    sections: List[dict] = []
    section_status: List[dict] = []

    def section_ready(sec: str, title: str, ids: List[str], meta: Dict[str, Dict[str, Any]]) -> None:
        solved_n = sum(1 for qid in ids if meta.get(qid, {}).get("status") == "solved")
        total_n = len(ids)
        section_status.append({
            "section": sec,
            "title": title,
            "solved": solved_n,
            "total": total_n,
            "percent": round((solved_n / total_n) * 100, 1) if total_n else 0,
        })

    if structure:
        # foundation: per-section per-topic verified counts + practice samples
        seen_sections = set()
        for stage in structure["stages"]:
            for sec in stage.get("sections", []):
                if sec in seen_sections:
                    continue
                seen_sections.add(sec)
                qtype = _VERIFIED_TYPE_FOR_SECTION.get(sec)
                if not qtype:
                    continue
                topical = {}
                pool = bank["items"] + question_store.find({"type": qtype}).prefer_verified().to_list(600)
                for q in pool:
                    if q.get("type") != qtype:
                        continue
                    topical.setdefault(_display_topic(q.get("topic")), []).append(q)
                samples = _spread_by_topic(pool, qtype, foundation_cap)
                meta = await _status_map(user["id"], [q.get("id") for q in samples]) if samples else {}
                section_ready(sec, _SECTION_TITLES.get(sec, sec), [q.get("id") for q in samples], meta)
                sections.append({
                    "section": sec,
                    "title": _SECTION_TITLES.get(sec, sec),
                    "topics": [{"topic": t, "count": len(v)} for t, v in topical.items()],
                    "practice_count": len(samples),
                    "practice": [_brief(q, meta.get(q.get("id"), {"status": "not_started", "best_score": None})) for q in samples],
                })
    else:
        # product/DSA-style track: top verified coding patterns drive the curriculum
        patterns = question_store.get_pattern_stats()
        verified_by_pattern = {}
        for q in question_store.find({}).prefer_verified().to_list(3000):
            if q.get("type") != "coding":
                continue
            pat = q.get("pattern")
            if pat:
                verified_by_pattern.setdefault(pat, []).append(q)
        pattern_order = {"easy": 0, "medium": 1, "hard": 2}
        ranked = []
        for p in patterns:
            rows = verified_by_pattern.get(p["pattern"], [])
            if rows:
                ranked.append((p["pattern"], rows))
        ranked.sort(key=lambda r: -len(r[1]))
        for pname, rows in ranked[:6]:
            samples = _spread_by_topic(rows, "coding", foundation_cap)
            row_meta = await _status_map(user["id"], [q.get("id") for q in samples])
            section_ready("pattern", pname, [q.get("id") for q in samples], row_meta)
            sections.append({
                "section": "pattern",
                "title": pname,
                "topics": [{"topic": _display_topic(q.get("topic")), "count": 0} for q in samples],
                "practice_count": min(len(samples), foundation_cap),
                "practice": [_brief(q, row_meta.get(q.get("id"), {"status": "not_started", "best_score": None})) for q in samples],
            })

    # advanced coding: verified coding problems, company-first, Easy->Hard
    coding = []
    seen_ids = set()
    for q in bank["items"]:
        if q.get("type") == "coding" and q.get("id") not in seen_ids:
            coding.append(q)
            seen_ids.add(q.get("id"))
    for q in question_store.find({"type": "coding"}).only_verified().to_list(600):
        if q.get("id") not in seen_ids:
            coding.append(q)
            seen_ids.add(q.get("id"))
    coding = coding[:coding_cap]
    order = {"easy": 0, "medium": 1, "hard": 2}
    coding.sort(key=lambda q: (order.get(q.get("difficulty", "medium"), 3), (q.get("title") or "")))
    cm = await _status_map(user["id"], [q.get("id") for q in coding]) if coding else {}
    coding_solved = sum(1 for q in coding if cm.get(q.get("id"), {}).get("status") == "solved")
    advanced = {
        "total": len(coding),
        "solved": coding_solved,
        "problems": [_brief(q, cm.get(q.get("id"), {"status": "not_started", "best_score": None})) for q in coding],
    }

    # readiness: honest solved/total over the problems actually served in this track
    foundation_total = sum(s["total"] for s in section_status)
    foundation_solved = sum(s["solved"] for s in section_status)
    overall_total = foundation_total + advanced["total"]
    overall_solved = foundation_solved + coding_solved
    all_problems = []
    for s in sections:
        all_problems.extend(
            {"id": p["id"], "status": p["status"], "order": len(all_problems)} for p in s["practice"]
        )
    all_problems.extend(
        {"id": p["id"], "status": p["status"], "order": len(all_problems)} for p in advanced["problems"]
    )
    next_up = next((p for p in all_problems if p["status"] == "not_started"), None)
    weakest = min(section_status, key=lambda s: (s["percent"] if s["total"] else 0, -s["total"])) if section_status else None

    return {
        "company": canon,
        "structure": structure,
        "track": f"{canon}-track",
        "verified_only": True,
        "provenance_note": "Every question is TRUSTED; company tags are explicit provenance, "
                           "otherwise pattern-relevant.",
        "foundation": {"sections": sections},
        "advanced_coding": advanced,
        "readiness": {
            "foundation": {"solved": foundation_solved, "total": foundation_total},
            "coding": {"solved": coding_solved, "total": advanced["total"]},
            "overall_percent": round((overall_solved / overall_total) * 100, 1) if overall_total else 0,
            "sections": section_status,
            "next_up_id": next_up["id"] if next_up else None,
            "weakest_section": weakest["section"] if weakest else None,
            "weakest_title": weakest["title"] if weakest else None,
        },
    }