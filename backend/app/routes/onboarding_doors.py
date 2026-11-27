"""Onboarding doors — PostgreSQL-backed, no MongoDB."""

from datetime import datetime, timezone
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.middleware.auth import get_current_user

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


class DoorCompleteRequest:
    """Request to complete a door selection."""
    def __init__(self, door: str):
        self.door = door


router = APIRouter(prefix="/api/v1/onboarding/doors", tags=["onboarding-doors"])


@router.post("/complete")
async def complete_door(door: str):
    """Record user's door selection and redirect."""
    if door not in {"job", "dev", "beginner"}:
        raise HTTPException(status_code=400, detail="Invalid door key")
    
    # Record the door selection (in a full implementation, this would save to user profile)
    redirect = DOOR_REDIRECTS.get(door, "/diagnostic")
    
    return {"door": door, "redirect": redirect}


@router.get("/redirects")
async def door_redirects():
    """Get door redirect mappings."""
    return {"redirects": DOOR_REDIRECTS}


@router.get("/career-stages")
async def career_stages():
    """Get career stage options for job door."""
    return {"stages": CAREER_STAGES}


@router.get("/valid-dev-tracks")
async def valid_dev_tracks():
    """Get valid development tracks."""
    return {"tracks": list(VALID_DEV_TRACKS)}