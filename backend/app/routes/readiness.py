from fastapi import APIRouter, Depends, HTTPException

from app.middleware.auth import get_current_user
from app.database import get_collection
from app.services.readiness import compute_readiness as _compute_basic_readiness
from app.services.observability import record_event

router = APIRouter(prefix="/api/v1/readiness", tags=["readiness"])


@router.get("/score")
async def score(user=Depends(get_current_user)):
    """Return the learner's readiness score with components, drivers, and
    evidence-backed blockers + next action from the deterministic readiness
    engine."""
    result = _compute_basic_readiness(user["id"])

    # Enhance with readiness_engine blockers / next_action when available.
    try:
        from app.services.readiness_engine import (
            calculate_target_readiness,
            collect_target_evidence,
        )
        from app.database import academy_learner_profiles

        profile_doc = await get_collection("academy_learner_profiles").find_one({"user_id": user["id"]})
        if profile_doc:
            profile = {
                "role": profile_doc.get("target_role", "sde"),
                "company": profile_doc.get("target_company", "tcs"),
                "skills": profile_doc.get("skills", []),
            }
            evidence = await collect_target_evidence(user["id"], profile)
            target = calculate_target_readiness(profile, evidence)
            result["blockers"] = target.get("blockers", [])
            result["strengths"] = target.get("strengths", [])
            result["gaps"] = target.get("gaps", [])
            result["next_action"] = target.get("next_action")
            result["coverage"] = target.get("coverage")
            result["readiness_status"] = target.get("status")
            result["evidence_counts"] = target.get("evidence", {})
            result["freshness_pct"] = target.get("freshness_pct")
    except Exception:
        # Readiness engine enhancement is best-effort; basic score still works.
        pass

    # Record readiness view for funnel observability.
    try:
        await record_event(user["id"], "readiness_viewed", {"overall_readiness": result.get("readiness_score") or result.get("overall_readiness")})
    except Exception:
        pass
    return result
