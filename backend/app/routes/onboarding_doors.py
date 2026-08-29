from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from app.middleware.auth import get_current_user
from app.database import users_collection
from bson import ObjectId

logger = __import__("logging").getLogger(__name__)

router = APIRouter(prefix="/api/v1/onboarding/doors", tags=["onboarding-doors"])

# The three "doors" a new user picks from. Everything else is revealed
# progressively after this single decision.
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

# Career-stage options for the job door (Door 1).
CAREER_STAGES = [
    {"key": "nothing", "label": "I know nothing / very little"},
    {"key": "code", "label": "I can code"},
    {"key": "degree", "label": "I have a degree"},
    {"key": "experience", "label": "I have experience"},
    {"key": "projects", "label": "I have projects"},
    {"key": "interviewed", "label": "I've interviewed before"},
]

# Where each door sends the learner right after they pick it.
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


@router.get("")
async def get_doors(user=Depends(get_current_user)):
    from app.services.role_engine.profiles import door_roles

    # Door 2 offers the adventure track progression; Door 3 offers reassurance.
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


@router.post("/complete")
async def complete_door(req: DoorCompleteRequest, user=Depends(get_current_user)):
    door = next((d for d in DOORS if d["key"] == req.door), None)
    if not door:
        raise HTTPException(status_code=400, detail="Unknown door")

    # Validate role/stage only when the job door is chosen.
    if req.door == "job":
        from app.services.role_engine.profiles import door_roles

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
