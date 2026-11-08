"""Placement API endpoints.

Gap analysis, offer probability, dashboard insights, alumni experiences,
and placement drives — all backed by PlacementEngine for deterministic,
zero-AI-cost calculations.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from app.database import users_collection
from app.middleware.auth import get_current_user
from app.services.placement_engine import PlacementEngine

router = APIRouter(prefix="/api/v1/placement", tags=["placement"])
engine = PlacementEngine()


class GapAnalysisRequest(BaseModel):
    company: str
    target_probability: float = 75.0


@router.post("/gap-analysis")
async def gap_analysis(req: GapAnalysisRequest, user=Depends(get_current_user)):
    """Identify skill gaps between current readiness and target company.

    Returns per-skill gaps, weighted contribution, and prioritized
    improvement actions to reach the target probability.
    """
    try:
        company = req.company.lower().strip()
        if company not in engine.COMPANY_PROFILES:
            matches = [c for c in engine.COMPANY_PROFILES if company in c or c in company]
            if matches:
                company = matches[0]
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Company '{req.company}' not found",
                )

        profile = engine.COMPANY_PROFILES[company]
        weights = engine._effective_weights(profile["tier"], "SDE")
        student_scores = await engine._get_user_scores(user["id"])
        experience = await engine._get_experience_data(user["id"])

        target_score = req.target_probability
        min_bar = profile["min_score"] * 10

        gaps = []
        for skill, weight in weights.items():
            current = student_scores.get(skill, 0)
            gap = max(0.0, min_bar - current)
            weighted_gap = gap * weight
            if gap > 0:
                gaps.append({
                    "skill": skill,
                    "label": engine._humanize_skill(skill),
                    "current_score": round(current, 1),
                    "target_score": round(min_bar, 1),
                    "gap": round(gap, 1),
                    "weight": round(weight, 2),
                    "weighted_gap": round(weighted_gap, 2),
                    "priority": "high" if weighted_gap > 5 else ("medium" if weighted_gap > 2 else "low"),
                })

        gaps.sort(key=lambda g: g["weighted_gap"], reverse=True)

        total_gap = sum(g["weighted_gap"] for g in gaps)
        total_weight = sum(weights.values())
        estimated_weeks = round(total_gap / 4.0, 1) if total_gap > 0 else 0

        return {
            "company": req.company.title(),
            "company_tier": profile["tier"],
            "target_probability": req.target_probability,
            "current_readiness": round(
                sum(student_scores.get(s, 0) * w for s, w in weights.items()) / total_weight,
                1,
            ),
            "min_bar": min_bar,
            "total_gap": round(total_gap, 1),
            "estimated_prep_weeks": estimated_weeks,
            "gaps": gaps[:10],
            "top_priority": gaps[0] if gaps else None,
            "ready": len(gaps) == 0,
        }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Gap analysis failed")


@router.get("/probability/{company}")
async def company_probability(
    company: str,
    target: float = Query(75.0, description="Target probability percentage"),
    user=Depends(get_current_user),
):
    """Get offer probability and gap analysis for a specific company."""
    try:
        result = await engine.calculate_probability(
            user_id=user["id"],
            company_name=company,
            role="SDE",
        )
        return {
            "company": company.title(),
            "current_probability": result["current_probability"],
            "target_probability": target,
            "probability_band": result["probability_band"],
            "breakdown": result["breakdown"],
            "skill_scores": result["skill_scores"],
            "skill_weights": result["skill_weights"],
            "what_if_scenarios": result["what_if_scenarios"],
            "improvement_roadmap": result["improvement_roadmap"],
            "next_best_moves": result["next_best_moves"],
            "what_it_means": result["what_it_means"],
            "meets_target": result["current_probability"] >= target,
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Probability calculation failed")


@router.get("/dashboard-insights")
async def dashboard_insights(user=Depends(get_current_user)):
    """Get placement dashboard insights — overall readiness, top targets,
    and recommended next actions.
    """
    import logging
    logger = logging.getLogger(__name__)
    try:
        user_id = user["id"]
        logger.info(f"Dashboard insights for user {user_id}")
        student_scores = await engine._get_user_scores(user_id)
        experience = await engine._get_experience_data(user_id)

        total_practice = (
            experience["total_interviews"]
            + experience["total_coding"]
            + experience["total_aptitude"]
        )

        # Average readiness across all skill categories
        total_weight = sum(engine.TIER_WEIGHTS["Services"].values())
        avg_readiness = round(
            sum(student_scores.get(s, 0) * w for s, w in engine.TIER_WEIGHTS["Services"].items()) / total_weight,
            1,
        )

        # Simple response without per-company probability (too many DB calls)
        all_companies = engine.get_all_companies()
        top_targets = [
            {
                "company": c["id"],
                "name": c["name"],
                "tier": c["tier"],
                "color": c["color"],
                "acceptance_rate": c["acceptance_rate"],
            }
            for c in all_companies[:5]
        ]

        return {
            "overall_readiness": avg_readiness,
            "total_practice_sessions": total_practice,
            "streak": experience["streak"],
            "top_targets": top_targets,
            "companies_assessed": len(all_companies),
            "next_best_move": top_targets[0] if top_targets else None,
        }
    except Exception as exc:
        logger.exception(f"Dashboard insights failed: {exc}")
        raise HTTPException(status_code=500, detail=f"Failed to load dashboard insights: {str(exc)}")


@router.get("/alumni")
async def alumni_experiences(
    company: Optional[str] = Query(None, description="Filter by company"),
    role: Optional[str] = Query(None, description="Filter by role"),
    limit: int = Query(20, description="Maximum results"),
):
    """Get alumni placement experiences and outcomes."""
    try:
        # Return curated alumni data — in production this comes from a
        # alumni collection with real user-submitted experiences.
        alumni_data = [
            {
                "id": "alumni_001",
                "name": "Rahul Sharma",
                "role": "SDE",
                "company": "Google",
                "package": "45 LPA",
                "status": "placed",
                "prep_months": 6,
                "key_skills": ["DSA", "System Design", "Behavioral"],
                "testimonial": "Consistent practice on BountyCode helped me crack Google.",
            },
            {
                "id": "alumni_002",
                "name": "Priya Patel",
                "role": "SDE",
                "company": "Amazon",
                "package": "38 LPA",
                "status": "placed",
                "prep_months": 4,
                "key_skills": ["DSA", "Java", "Leadership Principles"],
                "testimonial": "The mock interviews were spot-on for Amazon rounds.",
            },
            {
                "id": "alumni_003",
                "name": "Arjun Reddy",
                "role": "SDE",
                "company": "Microsoft",
                "package": "42 LPA",
                "status": "placed",
                "prep_months": 5,
                "key_skills": ["DSA", "System Design", "OS/DBMS"],
                "testimonial": "Company-specific prep made all the difference.",
            },
            {
                "id": "alumni_004",
                "name": "Sneha Gupta",
                "role": "SDE",
                "company": "TCS",
                "package": "7 LPA",
                "status": "placed",
                "prep_months": 2,
                "key_skills": ["Aptitude", "Coding", "HR"],
                "testimonial": "Great for TCS NQT and services companies.",
            },
            {
                "id": "alumni_005",
                "name": "Vikram Singh",
                "role": "SDE",
                "company": "Flipkart",
                "package": "32 LPA",
                "status": "placed",
                "prep_months": 4,
                "key_skills": ["DSA", "System Design", "React"],
                "testimonial": "Flipkart rounds were exactly as practiced.",
            },
        ]

        filtered = alumni_data
        if company:
            filtered = [a for a in filtered if a["company"].lower() == company.lower()]
        if role:
            filtered = [a for a in filtered if a["role"].lower() == role.lower()]

        return {
            "alumni": filtered[:limit],
            "total": len(filtered),
            "filters": {"company": company, "role": role},
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Failed to load alumni experiences")


@router.get("/drives")
async def placement_drives(limit: int = Query(10, description="Maximum results")):
    """Get upcoming placement drives and campus recruitment events."""
    try:
        return {
            "drives": [
                {
                    "id": "d1",
                    "company": "TCS",
                    "title": "TCS NQT 2026",
                    "type": "Campus Drive",
                    "tier": "Services",
                    "apply_by": "2026-12-15",
                    "drive_date": "2027-01-10",
                    "eligibility": "BE/BTech/MCA 2025-2027",
                    "locations": ["Pan India"],
                    "status": "upcoming",
                }
            ],
            "total": 1,
            "upcoming": 1,
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
