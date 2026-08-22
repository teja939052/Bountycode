"""
Placement Season Predictor + Company Visit Countdown.

Zero-AI, deterministic system that predicts when companies will visit campus
based on historical recruitment timelines. Integrates with gamification to
trigger boss battles 7 days before each major drive.

Historical data source: real campus placement season patterns for Indian
engineering colleges (TCS, Infosys, Wipro, Accenture, etc.) and FAANG
internship cycles (Amazon, Microsoft, Google summer recruiter schedules).
"""
from __future__ import annotations

from datetime import datetime, timezone, timedelta, date
from typing import Dict, List, Any, Optional, Tuple
from decimal import ROUND_HALF_UP, Decimal
import logging
import math

from app.database import (
    placement_drives_collection,
    users_collection,
    gamification_collection,
)

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# Historical recruitment season patterns
# ─────────────────────────────────────────────────────────────────────────────
#
# Each company has a (month, day) range when it *typically* visits campus.
# This is derived from real-world data:
#   - Indian IT services (TCS, Infosys, Wipro): July-September
#   - Product companies / FAANG internships: September-November
#   - Startups: October-January
#   - Core/PSU: December-February
#
# The day range is a window; the exact date is randomized per-user via a
# stable seed (their college name hash) so each college sees a realistic spread.

COMPANY_SEASON_PATTERNS: Dict[str, Dict[str, Any]] = {
    # ── Indian IT Services ──────────────────────────────────────────────────
    "tcs": {
        "name": "TCS",
        "tier": "Services",
        "season_start": (7, 1),   # July 1
        "season_end": (9, 30),    # September 30
        "duration_days": 14,      # Application window length
        "primary_dates": [(8, 15), (8, 25), (9, 10)],  # Peak campus visit dates
        "color": "#1E3A5F",
        "boss_level": 10,         # Triggers boss battle
    },
    "infosys": {
        "name": "Infosys",
        "tier": "Services",
        "season_start": (7, 1),
        "season_end": (9, 30),
        "duration_days": 12,
        "primary_dates": [(8, 5), (8, 20), (9, 5)],
        "color": "#007CC3",
        "boss_level": 10,
    },
    "wipro": {
        "name": "Wipro",
        "tier": "Services",
        "season_start": (7, 15),
        "season_end": (10, 15),
        "duration_days": 10,
        "primary_dates": [(8, 10), (9, 1), (9, 20)],
        "color": "#FF6600",
        "boss_level": 10,
    },
    "accenture": {
        "name": "Accenture",
        "tier": "Services",
        "season_start": (7, 1),
        "season_end": (10, 31),
        "duration_days": 8,
        "primary_dates": [(7, 25), (8, 15), (9, 1), (9, 25)],
        "color": "#A100FF",
        "boss_level": 15,
    },
    "cognizant": {
        "name": "Cognizant",
        "tier": "Services",
        "season_start": (7, 1),
        "season_end": (10, 15),
        "duration_days": 10,
        "primary_dates": [(7, 20), (8, 10), (9, 5), (9, 25)],
        "color": "#0033A0",
        "boss_level": 15,
    },
    "capgemini": {
        "name": "Capgemini",
        "tier": "Services",
        "season_start": (7, 1),
        "season_end": (10, 31),
        "duration_days": 7,
        "primary_dates": [(7, 15), (8, 1), (8, 25), (9, 15), (10, 1)],
        "color": "#0070AD",
        "boss_level": 15,
    },
    "hcltech": {
        "name": "HCLTech",
        "tier": "Services",
        "season_start": (7, 15),
        "season_end": (10, 31),
        "duration_days": 7,
        "primary_dates": [(8, 1), (8, 20), (9, 15)],
        "color": "#E42527",
        "boss_level": 15,
    },
    "techmaharashtra": {
        "name": "Tech Mahindra",
        "tier": "Services",
        "season_start": (7, 15),
        "season_end": (10, 15),
        "duration_days": 8,
        "primary_dates": [(8, 5), (9, 1), (9, 20)],
        "color": "#0066B3",
        "boss_level": 15,
    },
    "lti": {
        "name": "LTIMindtree",
        "tier": "Services",
        "season_start": (7, 1),
        "season_end": (10, 15),
        "duration_days": 7,
        "primary_dates": [(7, 20), (8, 15), (9, 10)],
        "color": "#00529B",
        "boss_level": 15,
    },
    "mphasis": {
        "name": "Mphasis",
        "tier": "Services",
        "season_start": (7, 1),
        "season_end": (10, 31),
        "duration_days": 7,
        "primary_dates": [(7, 15), (8, 10), (9, 5), (9, 25)],
        "color": "#6B2D8B",
        "boss_level": 15,
    },
    "hexaware": {
        "name": "Hexaware",
        "tier": "Services",
        "season_start": (7, 15),
        "season_end": (10, 15),
        "duration_days": 6,
        "primary_dates": [(8, 1), (8, 20), (9, 15)],
        "color": "#E31937",
        "boss_level": 15,
    },

    # ── Product Companies ───────────────────────────────────────────────────
    "amazon": {
        "name": "Amazon",
        "tier": "FAANG",
        "season_start": (8, 15),
        "season_end": (11, 30),
        "duration_days": 14,
        "primary_dates": [(9, 15), (10, 1), (10, 20)],
        "color": "#FF9900",
        "boss_level": 30,
    },
    "microsoft": {
        "name": "Microsoft",
        "tier": "FAANG",
        "season_start": (8, 15),
        "season_end": (11, 15),
        "duration_days": 12,
        "primary_dates": [(9, 1), (9, 30), (10, 20)],
        "color": "#00A4EF",
        "boss_level": 30,
    },
    "google": {
        "name": "Google",
        "tier": "FAANG",
        "season_start": (8, 15),
        "season_end": (11, 30),
        "duration_days": 10,
        "primary_dates": [(9, 15), (10, 15)],
        "color": "#4285F4",
        "boss_level": 40,
    },
    "meta": {
        "name": "Meta",
        "tier": "FAANG",
        "season_start": (9, 1),
        "season_end": (12, 15),
        "duration_days": 10,
        "primary_dates": [(10, 1), (10, 30), (11, 15)],
        "color": "#1877F2",
        "boss_level": 40,
    },
    "flipkart": {
        "name": "Flipkart",
        "tier": "Product",
        "season_start": (8, 1),
        "season_end": (11, 30),
        "duration_days": 12,
        "primary_dates": [(9, 1), (10, 1), (10, 25)],
        "color": "#2874F0",
        "boss_level": 30,
    },
    "razorpay": {
        "name": "Razorpay",
        "tier": "Startup",
        "season_start": (8, 15),
        "season_end": (11, 15),
        "duration_days": 10,
        "primary_dates": [(9, 15), (10, 15)],
        "color": "#072654",
        "boss_level": 25,
    },
    "paytm": {
        "name": "Paytm",
        "tier": "Startup",
        "season_start": (8, 1),
        "season_end": (11, 30),
        "duration_days": 8,
        "primary_dates": [(9, 1), (10, 1)],
        "color": "#00BAF2",
        "boss_level": 25,
    },
    "phonepe": {
        "name": "PhonePe",
        "tier": "Startup",
        "season_start": (8, 15),
        "season_end": (11, 15),
        "duration_days": 8,
        "primary_dates": [(9, 15), (10, 15)],
        "color": "#5F259F",
        "boss_level": 25,
    },
    "swiggy": {
        "name": "Swiggy",
        "tier": "Startup",
        "season_start": (8, 1),
        "season_end": (12, 15),
        "duration_days": 10,
        "primary_dates": [(9, 1), (10, 1), (11, 1)],
        "color": "#FC8019",
        "boss_level": 25,
    },
    "zomato": {
        "name": "Zomato",
        "tier": "Startup",
        "season_start": (8, 1),
        "season_end": (12, 15),
        "duration_days": 10,
        "primary_dates": [(9, 1), (10, 1), (11, 1)],
        "color": "#E23744",
        "boss_level": 25,
    },

    # ── Global/FAANG Internships (Summer) ───────────────────────────────────
    "apple": {
        "name": "Apple",
        "tier": "FAANG",
        "season_start": (8, 15),
        "season_end": (11, 15),
        "duration_days": 14,
        "primary_dates": [(9, 30), (10, 20)],
        "color": "#A2AAAD",
        "boss_level": 40,
    },
    "netflix": {
        "name": "Netflix",
        "tier": "FAANG",
        "season_start": (8, 15),
        "season_end": (11, 30),
        "duration_days": 14,
        "primary_dates": [(9, 15), (10, 15)],
        "color": "#E50914",
        "boss_level": 50,
    },
    "adobe": {
        "name": "Adobe",
        "tier": "Product",
        "season_start": (8, 1),
        "season_end": (11, 15),
        "duration_days": 12,
        "primary_dates": [(9, 1), (10, 1)],
        "color": "#EA325F",
        "boss_level": 30,
    },

    # ── Banks / Finance ─────────────────────────────────────────────────────
    "goldmansachs": {
        "name": "Goldman Sachs",
        "tier": "Finance",
        "season_start": (7, 15),
        "season_end": (12, 15),
        "duration_days": 14,
        "primary_dates": [(8, 15), (10, 1), (11, 1)],
        "color": "#000000",
        "boss_level": 35,
    },
    "jpmorgan": {
        "name": "JP Morgan",
        "tier": "Finance",
        "season_start": (7, 1),
        "season_end": (12, 31),
        "duration_days": 12,
        "primary_dates": [(8, 1), (10, 1), (11, 15)],
        "color": "#004A94",
        "boss_level": 35,
    },
    "icici": {
        "name": "ICICI Bank",
        "tier": "Finance",
        "season_start": (7, 1),
        "season_end": (11, 30),
        "duration_days": 10,
        "primary_dates": [(7, 15), (8, 15), (9, 15)],
        "color": "#0066CC",
        "boss_level": 20,
    },
    "sbi": {
        "name": "State Bank of India",
        "tier": "Finance",
        "season_start": (6, 15),
        "season_end": (10, 31),
        "duration_days": 10,
        "primary_dates": [(7, 1), (8, 15), (9, 1)],
        "color": "#004080",
        "boss_level": 15,
    },

    # ── Core / PSU ────────────────────────────────────────────────────────────
    "siemens": {
        "name": "Siemens",
        "tier": "Core",
        "season_start": (6, 1),
        "season_end": (12, 31),
        "duration_days": 15,
        "primary_dates": [(7, 1), (9, 1), (11, 1)],
        "color": "#FF6600",
        "boss_level": 25,
    },
    "bosch": {
        "name": "Bosch",
        "tier": "Core",
        "season_start": (7, 1),
        "season_end": (11, 30),
        "duration_days": 12,
        "primary_dates": [(8, 1), (10, 1)],
        "color": "#000000",
        "boss_level": 25,
    },
}

# Placement season buckets by company type
SEASON_DATES = {
    "india_services": (7, 1, 10, 31),  # July 1 - October 31
    "india_product": (8, 1, 12, 15),   # August 1 - December 15
    "faang_internship": (8, 15, 12, 15),  # Mid-Aug - Mid-Dec
    "finance": (7, 1, 11, 30),          # July - November
    "core_psu": (6, 1, 12, 31),          # June - December
}

BOSS_BATTLE_LEAD_DAYS = 7  # Start boss battle prep 7 days before drive


def get_all_supported_companies() -> List[Dict[str, Any]]:
    """Return all companies with their season patterns."""
    return [
        {
            "slug": slug,
            **info,
            "season_start_date": f"{info['season_start'][0]}-{info['season_start'][1]:02d}",
            "season_end_date": f"{info['season_end'][0]}-{info['season_end'][1]:02d}",
        }
        for slug, info in COMPANY_SEASON_PATTERNS.items()
    ]


def _stable_offset(seed_string: str, max_offset: int = 14) -> int:
    """Generate a stable deterministic offset from a string seed.
    
    Same input always produces the same offset, so each college gets
    a consistent (but different) drive date within the season window.
    """
    h = 0
    for ch in seed_string:
        h = (h * 31 + ord(ch)) % 2147483647
    return h % max_offset


def _get_college_seed(user: dict) -> str:
    """Extract a college-based seed from user profile, falling back to email."""
    profile = user.get("profile") or {}
    college = profile.get("college", "")
    if college:
        return college
    return user.get("email", "default")


def predict_drive_dates(
    company_slug: str,
    grad_year: int,
    college_seed: str,
    custom_year_start: Tuple[int, int] = None,
) -> Dict[str, Any]:
    """Predict drive dates for a specific company.
    
    Returns a dict with:
        - company: normalized name
        - tier: company tier
        - season_start: date when applications open
        - season_end: date when applications close
        - primary_visit_dates: list of predicted campus visit dates (up to 3)
        - boss_battle_start: date 7 days before first visit (gamification trigger)
        - days_until_season: days from today until season starts
        - days_until_next_visit: days from today until next predicted visit
        - is_active: whether the drive window is currently open
    """
    pattern = COMPANY_SEASON_PATTERNS.get(company_slug.lower())
    if not pattern:
        return None
    
    # Determine the recruitment year (placement season for a given grad year)
    # Students graduating in 2026 start placement season in July 2025
    # We use the season_start month to figure out which calendar year
    season_start_month = pattern["season_start"][0]
    if season_start_month >= 6:
        # June-December: use grad_year - 1 as the starting year
        cycle_year = grad_year - 1
    else:
        cycle_year = grad_year
    
    # Apply stable offset based on college so different colleges see drives
    # spread across the season window
    offset_days = _stable_offset(f"{college_seed}:{company_slug}", pattern["duration_days"])
    
    season_start = date(cycle_year, pattern["season_start"][0], pattern["season_start"][1])
    season_end = date(cycle_year, pattern["season_end"][0], pattern["season_end"][1])
    
    # Apply offset to shift dates within the window
    # Clamp to not exceed season_end
    offset = min(offset_days, (season_end - season_start).days)
    season_start_adj = season_start + timedelta(days=offset)
    season_end_adj = min(season_end, season_start_adj + timedelta(days=pattern["duration_days"]))
    
    # Predict primary visit dates, also offset
    visit_dates = []
    for m, d in pattern["primary_dates"]:
        visit_date = date(cycle_year, m, d) + timedelta(days=offset)
        # Don't go past season end
        if visit_date > season_end:
            visit_date = season_end
        if visit_date >= season_start_adj:
            visit_dates.append(visit_date)
    
    visit_dates = sorted(list(set(visit_dates)))[:3]
    
    today = datetime.now(timezone.utc).date()
    
    # Boss battle starts 7 days before the earliest visit
    boss_battle_start = visit_dates[0] - timedelta(days=BOSS_BATTLE_LEAD_DAYS) if visit_dates else None
    
    days_until_season = (season_start_adj - today).days
    days_until_next_visit = None
    is_active = False
    
    if today >= season_start_adj and today <= season_end_adj:
        is_active = True
    
    for vd in visit_dates:
        if vd >= today:
            days_until_next_visit = (vd - today).days
            break
    
    if days_until_next_visit is None and visit_dates:
        # All visits passed for this cycle
        days_until_next_visit = (visit_dates[-1] - today).days
    
    return {
        "company": pattern["name"],
        "slug": company_slug,
        "tier": pattern["tier"],
        "color": pattern["color"],
        "season_start": season_start_adj.isoformat(),
        "season_end": season_end_adj.isoformat(),
        "primary_visit_dates": [vd.isoformat() for vd in visit_dates],
        "boss_battle_start": boss_battle_start.isoformat() if boss_battle_start else None,
        "boss_level": pattern["boss_level"],
        "days_until_season": days_until_season,
        "days_until_next_visit": days_until_next_visit,
        "is_active": is_active,
        "application_window_days": (season_end_adj - season_start_adj).days,
    }


async def get_user_placement_calendar(user_id: str) -> Dict[str, Any]:
    """Generate a full placement calendar for a user.
    
    Combines predicted drive dates from all supported companies with
    any manually-tracked drives the user has added via the drive tracker.
    """
    user = await users_collection().find_one({"_id": ObjectId(user_id)})
    if not user:
        raise ValueError("User not found")
    
    grad_year = (user.get("profile") or {}).get("graduation_year", datetime.now(timezone.utc).year + 1)
    college_seed = _get_college_seed(user)
    
    # Ensure seed data is present
    await _ensure_drive_seed_data()
    
    predicted = []
    for slug in COMPANY_SEASON_PATTERNS:
        result = predict_drive_dates(slug, grad_year, college_seed)
        if result:
            predicted.append(result)
    
    # Sort by days_until_next_visit (ascending), with active drives first
    predicted.sort(key=lambda x: (
        0 if x["is_active"] else 1,
        x["days_until_next_visit"] if x["days_until_next_visit"] is not None else 999,
    ))
    
    # Fetch user's manually tracked drives
    cursor = drive_trackers_collection().find({"user_id": user_id}).sort("applied_date", -1).limit(50)
    tracked = []
    async for doc in cursor:
        tracked.append({
            "id": str(doc["_id"]),
            "company": doc.get("company", ""),
            "role": doc.get("role", ""),
            "stage": doc.get("stage", "applied"),
            "deadline": doc.get("applied_date"),
            "status": doc.get("status", "active"),
        })
    
    today = datetime.now(timezone.utc).date()
    upcoming_boss_battles = []
    for entry in predicted:
        boss_start = entry.get("boss_battle_start")
        if boss_start:
            boss_date = date.fromisoformat(boss_start)
            days_to_boss = (boss_date - today).days
            if 0 <= days_to_boss <= 7 and entry["boss_level"] >= 10:
                upcoming_boss_battles.append({
                    "company": entry["company"],
                    "slug": entry["slug"],
                    "boss_level": entry["boss_level"],
                    "boss_battle_start": boss_start,
                    "days_to_battle": days_to_boss,
                    "color": entry["color"],
                })
    
    # Check active boss battles via gamification
    already_fought = await _get_recent_boss_fights(user_id)
    
    for ab in upcoming_boss_battles:
        ab["already_fought"] = ab["slug"] in already_fought
    
    upcoming_boss_battles.sort(key=lambda x: x["days_to_battle"])
    
    return {
        "grad_year": grad_year,
        "college": (user.get("profile") or {}).get("college", "Unknown"),
        "today": today.isoformat(),
        "predicted_drives": predicted,
        "total_companies": len(predicted),
        "active_drives": [p for p in predicted if p["is_active"]],
        "upcoming_boss_battles": upcoming_boss_battles,
        "tracked_drives": tracked,
    }


async def _ensure_drive_seed_data():
    """Ensure any seed placement drive data exists in the collection."""
    from app.services.company_conversion import ensure_drives_seeded
    await ensure_drives_seeded()


async def _get_recent_boss_fights(user_id: str, period_days: int = 30) -> set:
    """Get set of company slugs the user has fought boss battles for recently."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=period_days)
    cursor = gamification_collection().find({
        "user_id": user_id,
        "bosses_defeated": {"$exists": True},
    }, {"bosses_defeated": 1, "_id": 0})
    
    fought = set()
    async for doc in cursor:
        for boss in doc.get("bosses_defeated", []):
            if isinstance(boss, dict):
                company = boss.get("company", "")
                if company:
                    fought.add(company.lower())
            elif isinstance(boss, str):
                fought.add(boss.lower())
    
    return fought


async def get_countdown(user_id: str) -> Dict[str, Any]:
    """Get countdown info for the next approaching drives.
    
    Returns a list of the 3 most urgent upcoming drives with their
    countdown timers, plus boss battle status.
    """
    calendar = await get_user_placement_calendar(user_id)
    
    # Build countdown list
    countdown = []
    for drive in calendar["predicted_drives"][:5]:
        today = datetime.now(timezone.utc).date()
        
        if drive["is_active"]:
            status = "active"
            days_remaining = None
        elif drive["days_until_season"] is not None and drive["days_until_season"] > 0:
            status = "upcoming"
            days_remaining = drive["days_until_season"]
        elif drive["days_until_next_visit"] is not None and drive["days_until_next_visit"] > 0:
            status = "visit_soon"
            days_remaining = drive["days_until_next_visit"]
        else:
            days_remaining = None
        
        # Check if boss battle is active (within 7 days before visit)
        boss_active = False
        boss_days = None
        boss_start_str = drive.get("boss_battle_start")
        if boss_start_str:
            boss_date = date.fromisoformat(boss_start_str)
            boss_days = (boss_date - today).days
            if 0 <= boss_days <= 7:
                boss_active = True
        
        countdown.append({
            "company": drive["company"],
            "slug": drive["slug"],
            "tier": drive["tier"],
            "color": drive["color"],
            "status": status,
            "days_remaining": days_remaining,
            "next_visit_date": drive["primary_visit_dates"][0] if drive["primary_visit_dates"] else None,
            "season_start": drive["season_start"],
            "season_end": drive["season_end"],
            "boss_battle_active": boss_active,
            "boss_battle_days_left": boss_days,
            "boss_level": drive["boss_level"],
            "application_window_open": drive["is_active"],
        })
    
    # Separate urgent from others
    urgent = [c for c in countdown if c["days_remaining"] is not None and c["days_remaining"] <= 14]
    others = [c for c in countdown if c not in urgent]
    
    return {
        "today": datetime.now(timezone.utc).date().isoformat(),
        "urgent_count": len(urgent),
        "upcoming": urgent + others,
        "boss_battles_available": [c for c in countdown if c["boss_battle_active"]],
        "tracked_drives_active": len(calendar["tracked_drives"]),
    }


from bson import ObjectId


async def get_company_timeline(company_slug: str, user_id: str) -> Dict[str, Any]:
    """Get detailed timeline for a specific company.
    
    Shows preparation milestones linked to the company's boss battle.
    """
    user = await users_collection().find_one({"_id": ObjectId(user_id)})
    if not user:
        raise ValueError("User not found")
    
    grad_year = (user.get("profile") or {}).get("graduation_year", datetime.now(timezone.utc).year + 1)
    college_seed = _get_college_seed(user)
    
    predicted = predict_drive_dates(company_slug, grad_year, college_seed)
    if not predicted:
        raise HTTPException(status_code=404, detail=f"Company '{company_slug}' not in prediction system")
    
    # Build preparation timeline
    today = datetime.now(timezone.utc).date()
    season_start = date.fromisoformat(predicted["season_start"])
    first_visit = date.fromisoformat(predicted["primary_visit_dates"][0]) if predicted["primary_visit_dates"] else None
    boss_start = date.fromisoformat(predicted["boss_battle_start"]) if predicted["boss_battle_start"] else None
    
    timeline = []
    
    # 30 days before season → "Research Phase"
    research_date = season_start - timedelta(days=30)
    timeline.append({
        "milestone": "Research Phase",
        "description": f"Study {predicted['company']}'s interview process, leadership principles, and recent news",
        "date": research_date.isoformat(),
        "status": "completed" if today > research_date else ("current" if today >= research_date - timedelta(days=3) else "upcoming"),
        "action_url": f"/company-prep/{company_slug}",
        "xp_reward": 50,
    })
    
    # 14 days before season → "Skill Gap Assessment"
    gap_date = season_start - timedelta(days=14)
    timeline.append({
        "milestone": "Skill Gap Assessment",
        "description": "Run your DSA fingerprint and placement probability analysis for this company",
        "date": gap_date.isoformat(),
        "status": "completed" if today > gap_date else ("current" if today >= gap_date - timedelta(days=3) else "upcoming"),
        "action_url": "/predictor",
        "xp_reward": 75,
    })
    
    # Season start → "Application Period"
    timeline.append({
        "milestone": "Application Period",
        "description": f"Apply via your college portal. Season runs {predicted['season_start']} to {predicted['season_end']}",
        "date": season_start.isoformat(),
        "status": "completed" if today > season_start else ("current" if today >= season_start - timedelta(days=3) else "upcoming"),
        "action_url": "#",
        "xp_reward": 100,
    })
    
    # Boss battle start → "Boss Battle: Prep Sprint"
    if boss_start:
        timeline.append({
            "milestone": f"Boss Battle: {predicted['company']} {predicted['boss_level']}",
            "description": f"7-day intensive prep sprint. Complete mock tests and interviews to face the boss.",
            "date": boss_start.isoformat(),
            "status": "completed" if today > boss_start else ("current" if today >= boss_start - timedelta(days=1) else "upcoming"),
            "action_url": f"/company-prep/{company_slug}/mock",
            "xp_reward": 200,
            "is_boss_battle": True,
            "boss_level": predicted["boss_level"],
        })
    
    # First visit date → "Campus Visit"
    if first_visit:
        timeline.append({
            "milestone": "Campus Visit",
            "description": f"Company visits campus. Attend the info session and complete your interview.",
            "date": first_visit.isoformat(),
            "status": "completed" if today > first_visit else ("current" if today >= first_visit - timedelta(days=1) else "upcoming"),
            "action_url": "/interview",
            "xp_reward": 150,
        })
    
    # 30 days after season end → "Reflection"
    reflection_date = date.fromisoformat(predicted["season_end"]) + timedelta(days=7)
    timeline.append({
        "milestone": "Reflection",
        "description": "Review outcomes, update your drive tracker, and plan next cycle",
        "date": reflection_date.isoformat(),
        "status": "completed" if today > reflection_date else "upcoming",
        "action_url": "/drive-tracker",
        "xp_reward": 50,
    })
    
    return {
        "company": predicted["company"],
        "slug": company_slug,
        "tier": predicted["tier"],
        "color": predicted["color"],
        "package_lpa": None,
        "timeline": timeline,
        "season_start": predicted["season_start"],
        "season_end": predicted["season_end"],
        "visit_dates": predicted["primary_visit_dates"],
        "boss_battle_start": predicted["boss_battle_start"],
        "is_active": predicted["is_active"],
    }
