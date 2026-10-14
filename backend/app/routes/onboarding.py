from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from app.middleware.auth import get_current_user
from app.database import users_collection, gamification_collection
from app.services.onboarding_launch import (
    get_beginner_go,
    get_dev_launch,
    run_beginner_go,
    run_dev_launch,
)
from app.services.role_engine.profiles import door_roles
from app.services.job_diagnostic import get_diagnostic_questions, run_job_diagnostic
from bson import ObjectId

logger = __import__("logging").getLogger(__name__)

router = APIRouter(prefix="/api/v1/onboarding", tags=["onboarding"])

QUEST_STEPS = [
    {
        "id": "step-1",
        "title": "Choose Your Language",
        "description": "Pick the language you want to learn. C, C++, Java, or Python — all paths lead to placement success.",
        "type": "navigation",
        "action": "Select a language from the learning hub",
        "target": "/learn/c",
        "icon": "\U0001f3af",
    },
    {
        "id": "step-2",
        "title": "Write Your First Code",
        "description": "Open the first lesson and run your first program. You will have code running in under 30 seconds.",
        "type": "action",
        "action": "Open any lesson and click Run",
        "target": "/free-trial",
        "icon": "\u2328\ufe0f",
    },
    {
        "id": "step-3",
        "title": "Earn Your First Diamonds",
        "description": "Complete the lesson and watch your progress climb. Gamification keeps you hooked.",
        "type": "action",
        "action": "Complete a lesson to earn Diamonds",
        "target": "/learn/c",
        "icon": "\u2b50",
    },
    {
        "id": "step-4",
        "title": "Track Your Streak",
        "description": "Keep learning daily to build your streak multiplier. Consistency beats intensity.",
        "type": "info",
        "action": "Check your streak in the dashboard",
        "target": "/dashboard",
        "icon": "\U0001f525",
    },
    {
        "id": "step-5",
        "title": "Go Pro for Unlimited Access",
        "description": "Free users get 3 lessons per month. Pro unlocks everything for ₹99/mo or ₹899/yr.",
        "type": "conversion",
        "action": "Upgrade to Pro",
        "target": "/pricing",
        "icon": "\U0001f680",
    },
]


class CompleteStepRequest(BaseModel):
    model_config = {"extra": "allow"}

    step_id: str
    completed: bool = True
    xp_earned: int = 10


# ============================================
# DOORS (migrated from onboarding_doors.py)
# ============================================

DOORS = [
    {
        "key": "job",
        "emoji": "\U0001f4bc",
        "title": "I NEED A JOB",
        "subtitle": "Graduate, job seeker, career switcher or working professional.",
        "tagline": "Find your gaps, train for the role, get ready.",
    },
    {
        "key": "dev",
        "emoji": "\U0001f393",
        "title": "I WANT TO BECOME A DEVELOPER",
        "subtitle": "Student or learner building coding and CS skills.",
        "tagline": "One mission at a time. We'll turn learning into engineering ability.",
    },
    {
        "key": "beginner",
        "emoji": "\U0001f331",
        "title": "I'M NEW TO TECH",
        "subtitle": "Coding, AI and technology feel confusing. Start from zero.",
        "tagline": "You don't need to know anything yet. We'll teach you from zero.",
    },
]

CAREER_STAGES = [
    {"key": "nothing", "label": "I know nothing / very little"},
    {"key": "code", "label": "I can code"},
    {"key": "degree", "label": "I have a degree"},
    {"key": "experience", "label": "I have experience"},
    {"key": "projects", "label": "I have projects"},
    {"key": "interviewed", "label": "I've interviewed before"},
]

DOOR_REDIRECTS = {
    "job": "/diagnostic",
    "dev": "/dev-launch",
    "beginner": "/beginner-launch",
}

VALID_DEV_TRACKS = {"programming", "cs", "algorithms", "backend", "ai"}


class DoorCompleteRequest(BaseModel):
    door: str = Field(..., description="Door key: job | dev | beginner")
    role: Optional[str] = Field(None, description="Target role key (job door)")
    stage: Optional[str] = Field(None, description="Career-stage key (job door)")
    track: Optional[str] = Field(None, description="Adventure track key (dev door)")


@router.get("/doors")
async def get_doors(user=Depends(get_current_user)):
    return {
        "doors": DOORS,
        "job_roles": door_roles(),
        "career_stages": CAREER_STAGES,
        "dev_tracks": [
            {"key": "programming", "label": "Programming Village"},
            {"key": "cs", "label": "Computer Science Castle"},
            {"key": "algorithms", "label": "Algorithm Arena"},
            {"key": "backend", "label": "Backend Harbor"},
            {"key": "ai", "label": "AI Lab"},
        ],
    }


@router.post("/doors/complete")
async def complete_door(req: DoorCompleteRequest, user=Depends(get_current_user)):
    door = next((d for d in DOORS if d["key"] == req.door), None)
    if not door:
        raise HTTPException(status_code=400, detail="Unknown door")

    if req.door == "job":
        if req.role and not any(r["key"] == req.role for r in door_roles()):
            raise HTTPException(status_code=400, detail="Unknown target role")
        if req.stage and not any(s["key"] == req.stage for s in CAREER_STAGES):
            raise HTTPException(status_code=400, detail="Unknown career stage")
    elif req.door == "dev":
        if req.track and req.track not in VALID_DEV_TRACKS:
            raise HTTPException(status_code=400, detail="Unknown dev track")

    onboarding = {
        "completed": True,
        "door": req.door,
        "role": req.role,
        "stage": req.stage,
        "track": req.track,
        "completed_at": datetime.now(timezone.utc),
    }

    await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {
            "$set": {
                "onboarding": onboarding,
                "career_goal.door": req.door,
                "career_goal.role": req.role,
                "career_goal.stage": req.stage,
                "career_goal.track": req.track,
            }
        },
    )

    if req.door == "dev":
        redirect = f"{DOOR_REDIRECTS['dev']}?track={req.track or 'programming'}"
    elif req.door == "job":
        redirect = f"{DOOR_REDIRECTS['job']}?role={req.role or 'sde'}"
    else:
        redirect = DOOR_REDIRECTS.get(req.door, "/dashboard")

    return {
        "status": "ok",
        "redirect": redirect,
        "onboarding": onboarding,
    }


# ============================================
# LAUNCH (migrated from onboarding_launch.py)
# ============================================

VALID_TRACKS = {"programming", "cs", "algorithms", "backend", "ai"}


@router.get("/dev/start")
async def dev_start(track: Optional[str] = "programming", user=Depends(get_current_user)):
    if track not in VALID_TRACKS:
        track = "programming"
    return get_dev_launch(track)


@router.post("/dev/complete")
async def dev_complete(payload: Dict[str, Any], user=Depends(get_current_user)):
    track = payload.get("track", "programming")
    answers = payload.get("answers") or {}
    if track not in VALID_TRACKS:
        raise HTTPException(status_code=400, detail="Unknown track")
    uid = user.get("id") or user.get("_id")
    return await run_dev_launch(uid, track, answers)


@router.get("/beginner/start")
async def beginner_start(user=Depends(get_current_user)):
    return get_beginner_go()


@router.post("/beginner/complete")
async def beginner_complete(user=Depends(get_current_user)):
    uid = user.get("id") or user.get("_id")
    return await run_beginner_go(uid)


# ============================================
# DIAGNOSTIC (migrated from onboarding_diagnostic.py)
# ============================================

VALID_ROLES = {r["key"] for r in door_roles()}


class DiagnosticCompleteRequest(BaseModel):
    role: str = Field(..., description="Door-1 target role key")
    answers: Dict[str, Any] = Field(default_factory=dict, description="question_id -> answer")


@router.get("/diagnostic/start")
async def start_diagnostic(role: str, user=Depends(get_current_user)):
    """Return the role's real interactive mini-diagnostic (gradable MCQ steps)."""
    if role not in VALID_ROLES:
        raise HTTPException(status_code=400, detail="Unknown target role")
    return get_diagnostic_questions(role)


@router.post("/diagnostic/complete")
async def complete_diagnostic(req: DiagnosticCompleteRequest, user=Depends(get_current_user)):
    """Grade answers, seed the skill graph, compute readiness, build the path,
    and return first 3 missions."""
    if req.role not in VALID_ROLES:
        raise HTTPException(status_code=400, detail="Unknown target role")
    result = await run_job_diagnostic(user["id"], req.role, req.answers)
    return result


@router.get("/quest")
async def get_quest(user=Depends(get_current_user)):
    return {
        "quest": {
            "id": "onboarding-quest",
            "title": "Welcome Aboard! Your First Steps",
            "description": "Get started in 5 minutes and see the platform shine",
            "steps": QUEST_STEPS,
        }
    }


@router.get("/diagnostic/status")
async def diagnostic_status(user=Depends(get_current_user)):
    try:
        from bson import ObjectId
        from app.database import users_collection
        doc = await users_collection.find_one({"_id": ObjectId(user["id"])}, {"career_goal.diagnostic": 1})
        diagnostic = (((doc or {}).get("career_goal") or {}).get("diagnostic") or {})
        if not diagnostic or not diagnostic.get("completed"):
            return {"completed": False}
        return {
            "completed": True,
            "readiness": diagnostic.get("readiness"),
            "baseline_categories": diagnostic.get("baseline_categories"),
            "first_missions": diagnostic.get("first_missions"),
            "path": diagnostic.get("path"),
            "completed_at": diagnostic.get("completed_at"),
        }
    except Exception:
        return {"completed": False}


# Client-side V3 target selections persisted without a QUEST_STEPS entry.
# Stored into users.onboarding so the study engine can personalize;
# never blocks onboarding when payloads are partial.
V3_TARGET_STEPS = {"v3-target"}


def _normalize_company(raw: str) -> str:
    """Map display names ("TCS NQT") to canonical ids ("tcs")."""
    t = (raw or "").strip().lower()
    aliases = {
        "tcs nqt": "tcs",
        "tcs": "tcs",
        "infosys": "infosys",
        "infytq": "infosys",
        "wipro": "wipro",
        "cognizant": "cognizant",
        "genc": "cognizant",
        "capgemini": "capgemini",
        "accenture": "accenture",
        "hcl": "hcl",
        "amazon": "amazon",
        "google": "google",
    }
    if t in aliases:
        return aliases[t]
    for key, canon in aliases.items():
        if key in t or t in key:
            return canon
    return t


@router.post("/complete")
async def complete_step(req: CompleteStepRequest, user=Depends(get_current_user)):
    step = next((s for s in QUEST_STEPS if s["id"] == req.step_id), None)
    if not step and req.step_id not in V3_TARGET_STEPS:
        raise HTTPException(status_code=404, detail="Step not found")
    if not step:
        body = req.model_dump() if hasattr(req, "model_dump") else {}
        patch = {"onboarding.completed": True}
        for key in (
            "goal", "role", "company", "language", "college", "branch",
            "grad_year", "placement_date", "daily_minutes", "target_role",
            "target_company", "prep_level", "learning_style",
        ):
            if body.get(key) not in (None, ""):
                patch[f"onboarding.{key}"] = body[key]
        await users_collection.update_one(
            {"_id": ObjectId(user["id"])},
            {"$addToSet": {"onboarding_quest.completed_steps": req.step_id}, "$set": patch},
            upsert=True,
        )
        _tc = _normalize_company(
            str(body.get("target_company") or body.get("company") or "")
        )
        if _tc:
            try:
                await gamification_collection.update_one(
                    {"user_id": user["id"]},
                    {"$set": {"target_company": _tc}},
                    upsert=True,
                )
            except Exception:
                pass
        return {"step_id": req.step_id, "completed": True, "xp_earned": 0}

    await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {
            "$addToSet": {"onboarding_quest.completed_steps": req.step_id},
            "$set": {
                "onboarding_quest.last_active": datetime.now(timezone.utc),
                # Unlock the app once the user engages with the quest — the
                # OnboardingGuard reads this legacy flag.
                "onboarding.completed": True,
            },
        },
        upsert=True,
    )

    return {
        "step_id": req.step_id,
        "completed": req.completed,
        "xp_earned": req.xp_earned,
    }


@router.get("/status")
async def onboarding_status(user=Depends(get_current_user)):
    db_user = await users_collection.find_one({"_id": ObjectId(user["id"])})
    quest_data = db_user.get("onboarding_quest", {}) if db_user else {}
    completed_steps = quest_data.get("completed_steps", [])
    total_steps = len(QUEST_STEPS)
    overall_progress = int((len(completed_steps) / total_steps) * 100) if total_steps > 0 else 0
    is_complete = len(completed_steps) >= total_steps

    # Backfill for users who completed quest steps before the legacy flag was
    # synced — keeps the OnboardingGuard from trapping them in a redirect loop.
    legacy_completed = (db_user or {}).get("onboarding", {}).get("completed", False)
    if completed_steps and not legacy_completed:
        await users_collection.update_one(
            {"_id": ObjectId(user["id"])},
            {"$set": {"onboarding.completed": True}},
        )

    return {
        "completed_steps": completed_steps,
        "overall_progress": overall_progress,
        "is_complete": is_complete,
    }