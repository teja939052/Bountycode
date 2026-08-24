"""
Grand Line Assessment — cross-fleet readiness deltas.

Compares the user against the mass-recruiter fleet (TCS/Infosys/Wipro) and an
optional product-company target in a single pass: one data gather, N cheap
scoring runs. Produces gap-to-cutoff per category with estimated focus hours
and a prioritized voyage plan.
"""
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.middleware.auth import get_current_user
from app.routes.readiness import (
    _gather_aptitude_data,
    _gather_coding_data,
    _gather_cs_fundamentals_data,
    _gather_dsa_data,
    _gather_interview_data,
    _gather_project_data,
    _gather_resume_data,
)
from app.services.readiness_engine import (
    COMPANY_PROFILES,
    calculate_readiness,
    predict_readiness_date,
)

router = APIRouter(prefix="/api/v1/grand-line", tags=["grand-line"])

PRODUCT_FLEET_KEYS = ["tcs", "infosys", "wipro"]

CATEGORY_LABELS = {
    "dsa": "DSA",
    "aptitude": "Aptitude",
    "cs_fundamentals": "CS Fundamentals",
    "coding": "Coding",
    "interview": "Interview",
    "resume": "Resume",
    "projects": "Projects",
}

# Deterministic heuristic: points missing -> estimated focused practice hours.
HOURS_PER_POINT = {"dsa": 1.2, "coding": 1.0, "aptitude": 0.5,
                   "cs_fundamentals": 0.6, "interview": 0.4, "resume": 0.2,
                   "projects": 0.8}
MAX_HOURS_PER_CATEGORY = 80


def _gap_categories(categories: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Weakest-first category gaps with estimated focus hours."""
    gaps = []
    for key, cat in categories.items():
        missing = max(0.0, 100.0 - float(cat.get("score", 0)))
        hours = min(
            int(missing * HOURS_PER_POINT.get(key, 0.8)),
            MAX_HOURS_PER_CATEGORY,
        )
        gaps.append({
            "key": key,
            "label": CATEGORY_LABELS.get(key, key.replace("_", " ").title()),
            "score": round(float(cat.get("score", 0)), 1),
            "missing_points": round(missing, 1),
            "est_hours": hours,
        })
    gaps.sort(key=lambda g: (-g["missing_points"], g["label"]))
    return gaps


def _match_label(score: float) -> str:
    if score >= 75:
        return "Set sail"
    if score >= 55:
        return "Nearly there"
    if score >= 35:
        return "Provisions needed"
    return "Stay in port"


def _verdict(name: str, score: float) -> str:
    if score >= 75:
        return f"You'd clear {name}'s bar today."
    if score >= 55:
        return f"A focused week or two puts you past {name}'s bar."
    if score >= 35:
        return f"{name} is within reach — close the big gaps first."
    return f"Build your sea legs before challenging {name}."


def _assess_company(name: str, result, gather_stats: Dict[str, Any]) -> Dict[str, Any]:
    prediction = predict_readiness_date(result.company_score or result.overall, name)
    gaps = _gap_categories(result.categories)
    return {
        "company": name,
        "display_name": name.upper() if len(name) <= 4 else name.title(),
        "overall_score": result.overall,
        "company_score": result.company_score,
        "match_label": _match_label(result.company_score),
        "weeks_remaining": prediction.get("weeks_remaining"),
        "estimated_date": prediction.get("estimated_date"),
        "confidence": prediction.get("confidence"),
        "requirements": {
            "min_problems": gather_stats.get("min_problems"),
            "interview_rounds": gather_stats.get("interview_rounds"),
            "typical_timeline_weeks": gather_stats.get("typical_timeline_weeks"),
        },
        "top_gaps": [
            {"label": g["label"], "score": g["score"], "est_hours": g["est_hours"]}
            for g in gaps[:3]
        ],
        "verdict": _verdict(name.title(), result.company_score),
    }


@router.get("/assess")
async def assess(
    target: Optional[str] = Query(
        None, description="Optional product-company target key (e.g. amazon)"
    ),
    user=Depends(get_current_user),
):
    """Cross-fleet assessment: mass recruiters + optional product target."""
    uid = user["id"]

    # One gather pass, reused across every scoring run.
    dsa_data = await _gather_dsa_data(uid)
    aptitude_data = await _gather_aptitude_data(uid)
    cs_data = await _gather_cs_fundamentals_data(uid)
    coding_data = await _gather_coding_data(uid)
    interview_data = await _gather_interview_data(uid)
    resume_data = await _gather_resume_data(uid)
    project_data = await _gather_project_data(uid)

    def _run(company: Optional[str]):
        return calculate_readiness(
            dsa_data=dsa_data,
            aptitude_data=aptitude_data,
            cs_data=cs_data,
            coding_data=coding_data,
            interview_data=interview_data,
            resume_data=resume_data,
            project_data=project_data,
            company=company,
        )

    general_result = _run(None)
    general_prediction = predict_readiness_date(general_result.overall)

    fleet = []
    for key in PRODUCT_FLEET_KEYS:
        profile = COMPANY_PROFILES[key]
        res = _run(key)
        entry = _assess_company(
            key,
            res,
            {
                "min_problems": profile.get("min_solved"),
                "interview_rounds": profile.get("interview_rounds"),
                "typical_timeline_weeks": profile.get("typical_timeline_weeks"),
            },
        )
        fleet.append(entry)

    target_entry = None
    if target:
        t_key = target.lower().strip()
        profile = COMPANY_PROFILES.get(t_key)
        if not profile:
            raise HTTPException(
                status_code=404,
                detail=f"Unknown target company: {target}. Available: "
                + ", ".join(k for k in COMPANY_PROFILES if k not in PRODUCT_FLEET_KEYS),
            )
        res = _run(t_key)
        target_entry = _assess_company(
            t_key,
            res,
            {
                "min_problems": profile.get("min_solved"),
                "interview_rounds": profile.get("interview_rounds"),
                "typical_timeline_weeks": profile.get("typical_timeline_weeks"),
            },
        )

    # Voyage plan: merge top gaps across fleet + target, dedupe by label,
    # keep highest hours per label, sort desc.
    merged: Dict[str, Dict[str, Any]] = {}
    sources = [e["top_gaps"] for e in fleet] + (
        [target_entry["top_gaps"]] if target_entry else []
    )
    for gaps in sources:
        for g in gaps:
            cur = merged.get(g["label"])
            if cur is None or g["est_hours"] > cur["est_hours"]:
                merged[g["label"]] = dict(g)
    voyage_plan = sorted(merged.values(), key=lambda g: -g["est_hours"])[:4]

    best_fleet = max(fleet, key=lambda e: e["company_score"])

    summary_bits = []
    if best_fleet["company_score"] >= 55:
        summary_bits.append(f"{best_fleet['display_name']} is yours to take")
    if target_entry:
        if target_entry["company_score"] < best_fleet["company_score"] - 15:
            summary_bits.append(
                f"{target_entry['display_name']} is a longer voyage — bank the fleet wins first"
            )
        elif target_entry["company_score"] >= 55:
            summary_bits.append(f"{target_entry['display_name']} is also in range")
    if not summary_bits:
        summary_bits.append("Focus on fundamentals before chasing any specific ship")

    return {
        "general": {
            "overall": general_result.overall,
            "categories": {
                name: {"score": cat.score, "weight": cat.weight}
                for name, cat in general_result.categories.items()
            },
            "prediction": general_prediction,
        },
        "fleet": fleet,
        "target": target_entry,
        "voyage_plan": voyage_plan,
        "summary": ". ".join(summary_bits) + ".",
        "your_stats": {
            "total_problems": dsa_data.get("total_solved", 0),
            "medium": dsa_data.get("medium", 0),
            "hard": dsa_data.get("hard", 0),
            "aptitude_tests": aptitude_data.get("test_count", 0),
            "interviews_completed": interview_data.get("completed_count", 0),
        },
    }


@router.get("/companies")
async def list_target_companies():
    """Product-company targets available for the Grand Line Assessment."""
    targets = []
    for key, p in COMPANY_PROFILES.items():
        if key in PRODUCT_FLEET_KEYS:
            continue
        targets.append({
            "key": key,
            "name": key.title(),
            "focus_topics": p.get("focus_topics", []),
            "typical_timeline_weeks": p.get("typical_timeline_weeks"),
        })
    return {"targets": targets}
