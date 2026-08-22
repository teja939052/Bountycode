"""
Placement Season Predictor + Company Visit Countdown routes.

Provides a personalized campus recruitment calendar with:
  - Predicted company visit dates based on historical patterns
  - Countdown timers to upcoming drives
  - Boss battle triggers 7 days before each major company visit
  - Preparation timeline with milestone tracking
"""
from datetime import datetime, timezone, date, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from app.middleware.auth import get_current_user
from app.services.placement_calendar import (
    get_user_placement_calendar,
    get_countdown,
    get_company_timeline,
    get_all_supported_companies,
    predict_drive_dates,
    COMPANY_SEASON_PATTERNS,
)

router = APIRouter(prefix="/api/v1/placement-calendar", tags=["Placement Calendar"])


class CalendarPreferences(BaseModel):
    graduation_year: Optional[int] = None
    college: Optional[str] = None
    branch: Optional[str] = None
    target_companies: Optional[List[str]] = None


@router.get("/companies")
async def list_companies():
    """List all companies with predicted visit patterns."""
    return {"companies": get_all_supported_companies()}


@router.get("/calendar")
async def get_calendar(user=Depends(get_current_user)):
    """Get the user's full placement calendar with predicted drive dates."""
    try:
        calendar = await get_user_placement_calendar(user["id"])
        return calendar
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/countdown")
async def get_countdown(user=Depends(get_current_user)):
    """Get countdown to the next approaching drives and active boss battles."""
    return await get_countdown(user["id"])


@router.get("/company/{company_slug}")
async def company_timeline(
    company_slug: str,
    user=Depends(get_current_user),
):
    """Get detailed preparation timeline for a specific company."""
    try:
        return await get_company_timeline(company_slug, user["id"])
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/boss-battles")
async def boss_battles(user=Depends(get_current_user)):
    """Get all upcoming and available boss battles."""
    calendar = await get_user_placement_calendar(user["id"])
    
    today = datetime.now(timezone.utc).date()
    battles = []
    
    for drive in calendar["predicted_drives"]:
        boss_start_str = drive.get("boss_battle_start")
        if not boss_start_str or drive["boss_level"] < 10:
            continue
        
        boss_date = date.fromisoformat(boss_start_str)
        days_to_boss = (boss_date - today).days
        
        # Check if boss has been fought
        already_fought = drive["slug"] in calendar.get("_fought_bosses", set())
        for ab in calendar["upcoming_boss_battles"]:
            if ab["slug"] == drive["slug"]:
                already_fought = ab.get("already_fought", False)
                break
        
        status = "available"
        if days_to_boss < 0:
            if already_fought:
                status = "completed"
            else:
                status = "missed"
        elif days_to_boss == 0:
            status = "active"
        else:
            status = "upcoming"
        
        battles.append({
            "company": drive["company"],
            "slug": drive["slug"],
            "boss_level": drive["boss_level"],
            "boss_battle_start": boss_start_str,
            "days_to_battle": days_to_boss,
            "status": status,
            "color": drive["color"],
            "tier": drive["tier"],
            "already_fought": already_fought,
            "visit_dates": drive["primary_visit_dates"],
        })
    
    battles.sort(key=lambda b: b["days_to_battle"])
    
    return {
        "battles": battles,
        "active_count": len([b for b in battles if b["status"] == "active"]),
        "upcoming_count": len([b for b in battles if b["status"] == "upcoming"]),
        "completed_count": len([b for b in battles if b["status"] == "completed"]),
    }


@router.get("/timeline/{company_slug}")
async def timeline_view(
    company_slug: str,
    user=Depends(get_current_user),
):
    """Get preparation timeline for a company (alias for company_timeline)."""
    try:
        return await get_company_timeline(company_slug, user["id"])
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
