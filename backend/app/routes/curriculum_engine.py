"""Capability Curriculum routes — simulation-based learning engine.

GET  /api/v1/curriculum/worlds
GET  /api/v1/curriculum/world/{id}
GET  /api/v1/curriculum/mission/{world}/{competency}
POST /api/v1/curriculum/complete-step
GET  /api/v1/curriculum/daily
GET  /api/v1/curriculum/progress
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone

from app.middleware.auth import get_current_user
from app.database import gamification_collection, skill_graph_collection
from app.data.capability_curriculum import (
    ALL_WORLDS, get_worlds, get_world, get_competency,
    get_daily_plan,
)
from app.services.job_readiness import get_personalized_gaps
from app.services.skill_assessment import SKILL_CATEGORIES

router = APIRouter(prefix="/api/v1/curriculum", tags=["Capability Curriculum"])


class StepCompleteRequest(BaseModel):
    world_id: str
    competency_id: str
    step_index: int
    score: float = Field(0, ge=0, le=100)
    time_spent_seconds: int = 0


@router.get("/worlds")
async def list_worlds(user=Depends(get_current_user)):
    worlds = get_worlds()
    return {"worlds": [{**w, "unlocked": True} for w in worlds]}


@router.get("/world/{world_id}")
async def world_detail(world_id: str, user=Depends(get_current_user)):
    world = get_world(world_id)
    if not world:
        raise HTTPException(status_code=404, detail=f"Unknown world: {world_id}")

    gamification = await gamification_collection.find_one({"user_id": user["id"]}) or {}
    completed = gamification.get("completed_competencies", {})

    competencies = []
    for comp in world.get("competencies", []):
        key = f"{world['id']}:{comp['id']}"
        progress = completed.get(key, {})
        competencies.append({
            "id": comp["id"],
            "title": comp["title"],
            "skills_taught": comp["skills_taught"],
            "scenario": comp["scenario"],
            "goal": comp.get("goal", ""),
            "step_count": len(comp.get("steps", [])),
            "mastery_xp": comp.get("mastery_xp", 100),
            "completed": progress.get("completed", False),
            "score": progress.get("score", 0),
            "best_score": progress.get("best_score", 0),
        })

    return {
        "world": {
            "id": world["id"],
            "title": world["title"],
            "icon": world["icon"],
            "description": world["description"],
            "order": world["order"],
        },
        "competencies": competencies,
    }


@router.get("/mission/{world_id}/{competency_id}")
async def mission_detail(world_id: str, competency_id: str, user=Depends(get_current_user)):
    result = get_competency(world_id, competency_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Mission not found: {world_id}/{competency_id}")

    return {
        "world_id": world_id,
        "world_title": result["world"]["title"],
        "competency": result["competency"],
        "total_steps": len(result["competency"].get("steps", [])),
    }


@router.post("/complete-step")
async def complete_step(req: StepCompleteRequest, user=Depends(get_current_user)):
    uid = user["id"]
    now = datetime.now(timezone.utc)

    gamification = await gamification_collection.find_one({"user_id": uid}) or {}
    completed = gamification.get("completed_competencies", {})
    comp_key = f"{req.world_id}:{req.competency_id}"

    if comp_key not in completed:
        completed[comp_key] = {"steps": {}, "completed": False, "score": 0, "best_score": 0}

    comp_progress = completed[comp_key]
    comp_progress["steps"][str(req.step_index)] = {
        "score": req.score,
        "time_spent": req.time_spent_seconds,
        "completed_at": now.isoformat(),
    }

    scores = [s["score"] for s in comp_progress["steps"].values()]
    avg_score = sum(scores) / len(scores) if scores else 0
    comp_progress["score"] = round(avg_score, 1)
    comp_progress["best_score"] = max(comp_progress.get("best_score", 0), avg_score)

    result = get_competency(req.world_id, req.competency_id)
    xp_awarded = 0
    if result:
        total_steps = len(result["competency"].get("steps", []))
        steps_done = len(comp_progress["steps"])

        if steps_done >= total_steps and not comp_progress.get("completed"):
            comp_progress["completed"] = True
            xp_awarded = result["competency"].get("mastery_xp", 100)
            gamification["xp"] = gamification.get("xp", 0) + xp_awarded

        for skill in result["competency"].get("skills_taught", []):
            for cat_id, cat_info in SKILL_CATEGORIES.items():
                if skill in cat_info.get("skills", []):
                    from app.services.skill_assessment import update_skill_score
                    await update_skill_score(uid, cat_id, skill, req.score, req.score >= 70)

    completed[comp_key] = comp_progress
    gamification["completed_competencies"] = completed
    gamification["updated_at"] = now

    await gamification_collection.update_one(
        {"user_id": uid}, {"$set": gamification}, upsert=True,
    )

    # ── Readiness reassessment ────────────────────────────────────────
    # Skill graph is already updated; recompute the readiness score so
    # the frontend can show progress toward job-readiness immediately.
    readiness_score = None
    try:
        from app.routes.readiness import get_readiness_score
        readiness = await get_readiness_score(None, user)
        readiness_score = readiness.get("readiness_score")
        await gamification_collection.update_one(
            {"user_id": uid},
            {"$set": {
                "readiness_snapshot": {
                    "score": readiness_score,
                    "updated_at": now,
                },
            }},
        )
    except Exception:
        pass  # readiness recalc is best-effort; never block step completion

    return {
        "status": "recorded",
        "competency_score": comp_progress["score"],
        "completed": comp_progress["completed"],
        "xp_awarded": xp_awarded,
        "readiness_score": readiness_score,
    }


@router.get("/daily")
async def daily_plan(user=Depends(get_current_user)):
    now = datetime.now(timezone.utc)
    day_name = now.strftime("%A")

    gaps = await get_personalized_gaps(user["id"], "sde")
    top_gaps = gaps.get("critical_gaps", [])[:2] + gaps.get("close_gaps", [])[:1]

    plan = get_daily_plan(day_name, {
        "critical": [{"category": g["category"], "name": g["name"], "gap": g["gap"]} for g in top_gaps],
    })

    recommendation = None
    if plan["type"] in ("learn", "practice") and top_gaps:
        rec_gap = top_gaps[0]
        for world in ALL_WORLDS.values():
            for comp in world.get("competencies", []):
                for skill in comp.get("skills_taught", []):
                    if skill in rec_gap.get("critical_topics", []):
                        recommendation = {
                            "world_id": world["id"],
                            "competency_id": comp["id"],
                            "title": comp["title"],
                            "scenario": comp["scenario"],
                        }
                        break
                if recommendation:
                    break
            if recommendation:
                break

    return {
        "day": plan["day"],
        "type": plan["type"],
        "icon": plan["icon"],
        "label": plan["label"],
        "description": plan["description"],
        "recommendation": recommendation,
    }


@router.get("/progress")
async def curriculum_progress(user=Depends(get_current_user)):
    gamification = await gamification_collection.find_one({"user_id": user["id"]}) or {}
    completed = gamification.get("completed_competencies", {})

    world_progress = []
    for world in sorted(ALL_WORLDS.values(), key=lambda x: x["order"]):
        comps = world.get("competencies", [])
        done = sum(1 for c in comps if completed.get(f"{world['id']}:{c['id']}", {}).get("completed", False))
        total = len(comps)
        scores = [completed.get(f"{world['id']}:{c['id']}", {}).get("score", 0) for c in comps]
        avg = sum(scores) / len(scores) if scores else 0

        world_progress.append({
            "id": world["id"],
            "title": world["title"],
            "icon": world["icon"],
            "completed": done,
            "total": total,
            "avg_score": round(avg, 1),
            "progress_pct": round(done / total * 100) if total > 0 else 0,
        })

    total_done = sum(w["completed"] for w in world_progress)
    total_all = sum(w["total"] for w in world_progress)

    return {
        "worlds": world_progress,
        "total_completed": total_done,
        "total_competencies": total_all,
        "overall_progress_pct": round(total_done / total_all * 100) if total_all > 0 else 0,
    }
