from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from app.database import get_db
from app.middleware.auth import get_current_user
from app.services.gamification import get_gamification_profile

router = APIRouter(prefix="/api/v1/career", tags=["career"])

ALL_COMPANIES = ["infosys", "tcs", "wipro", "amazon", "google", "meta", "microsoft", "netflix", "apple"]
ALL_STYLES = ["technical", "behavioral", "system_design", "coding", "aptitude"]

ROLES = [
    {
        "index": 1,
        "title": "Intern",
        "level": 1,
        "xp_required": 0,
        "emoji": "🎓",
        "unlocks": ["journey", "world"],
        "companies": ["infosys", "tcs", "wipro"],
        "interview_styles": ["aptitude"],
        "cosmetic": "#34d399",
        "title_perk": "Begin your journey and unlock the world.",
    },
    {
        "index": 2,
        "title": "Junior Developer",
        "level": 2,
        "xp_required": 1000,
        "emoji": "🧑‍💻",
        "unlocks": ["merchant"],
        "companies": ["infosys", "tcs", "wipro", "amazon"],
        "interview_styles": ["aptitude", "technical"],
        "cosmetic": "#38bdf8",
        "title_perk": "Trade with the merchant for power-ups and gear.",
    },
    {
        "index": 3,
        "title": "Software Engineer",
        "level": 3,
        "xp_required": 4000,
        "emoji": "👨‍💻",
        "unlocks": ["dungeons", "collection"],
        "companies": ["infosys", "tcs", "wipro", "amazon", "google"],
        "interview_styles": ["aptitude", "technical", "coding"],
        "cosmetic": "#a78bfa",
        "title_perk": "Enter dungeons and collect mastery cards.",
    },
    {
        "index": 4,
        "title": "Senior Engineer",
        "level": 4,
        "xp_required": 12000,
        "emoji": "🧙",
        "unlocks": ["guilds", "battles"],
        "companies": ["infosys", "tcs", "wipro", "amazon", "google", "meta"],
        "interview_styles": ["aptitude", "technical", "coding", "behavioral"],
        "cosmetic": "#f472b6",
        "title_perk": "Form guilds and challenge rivals in battles.",
    },
    {
        "index": 5,
        "title": "Tech Lead",
        "level": 5,
        "xp_required": 30000,
        "emoji": "🛠️",
        "unlocks": ["economy"],
        "companies": ["infosys", "tcs", "wipro", "amazon", "google", "meta", "microsoft"],
        "interview_styles": ["aptitude", "technical", "coding", "behavioral", "system_design"],
        "cosmetic": "#fb923c",
        "title_perk": "Command a player economy of coins and trading.",
    },
    {
        "index": 6,
        "title": "Staff Engineer",
        "level": 6,
        "xp_required": 70000,
        "emoji": "🚀",
        "unlocks": ["showcase"],
        "companies": ["infosys", "tcs", "wipro", "amazon", "google", "meta", "microsoft", "netflix"],
        "interview_styles": ["aptitude", "technical", "coding", "behavioral", "system_design"],
        "cosmetic": "#f43f5e",
        "title_perk": "Showcase your builds to the community.",
    },
    {
        "index": 7,
        "title": "Principal Engineer",
        "level": 7,
        "xp_required": 150000,
        "emoji": "🏛️",
        "unlocks": ["prestige"],
        "companies": ["infosys", "tcs", "wipro", "amazon", "google", "meta", "microsoft", "netflix", "apple"],
        "interview_styles": ["aptitude", "technical", "coding", "behavioral", "system_design"],
        "cosmetic": "#a855f7",
        "title_perk": "Unlock prestige and begin endgame progression.",
    },
    {
        "index": 8,
        "title": "Founder",
        "level": 8,
        "xp_required": 300000,
        "emoji": "👑",
        "unlocks": ["campus"],
        "companies": ALL_COMPANIES,
        "interview_styles": ALL_STYLES,
        "cosmetic": "#fbbf24",
        "title_perk": "Rule the campus and stand at the top of the Legend Hall.",
    },
]


def _derive_role_index(current_xp: int) -> int:
    role_index = 1
    for role in ROLES:
        if current_xp >= role["xp_required"]:
            role_index = role["index"]
    return role_index


def _build_response(current_xp: int, role_index: int) -> dict:
    role = ROLES[role_index - 1]
    next_role = ROLES[role_index] if role_index < len(ROLES) else None
    if next_role:
        span = next_role["xp_required"] - role["xp_required"]
        pct = round(min(100.0, max(0.0, (current_xp - role["xp_required"]) / span * 100)), 1)
    else:
        pct = 100.0

    unlocks = []
    for r in ROLES[:role_index]:
        for key in r["unlocks"]:
            if key not in unlocks:
                unlocks.append(key)

    return {
        "role_index": role_index,
        "role": role,
        "all_roles": ROLES,
        "progress_pct_to_next": pct,
        "next_role": next_role,
        "unlocks": unlocks,
        "current_xp": current_xp,
    }


async def _persist_role(user_id: str, current_xp: int, role_index: int):
    db = get_db()
    doc = await db["career_rpg"].find_one({"user_id": user_id})
    now = datetime.now(timezone.utc)
    if not doc:
        await db["career_rpg"].insert_one({
            "user_id": user_id,
            "role_index": role_index,
            "current_xp": current_xp,
            "role_history": [{
                "role_index": role_index,
                "title": ROLES[role_index - 1]["title"],
                "emoji": ROLES[role_index - 1]["emoji"],
                "promoted_at": now,
            }],
            "updated_at": now,
        })
        return

    if doc.get("role_index") != role_index:
        history = list(doc.get("role_history") or [])
        if role_index > doc.get("role_index", 1):
            history.append({
                "role_index": role_index,
                "title": ROLES[role_index - 1]["title"],
                "emoji": ROLES[role_index - 1]["emoji"],
                "promoted_at": now,
            })
        await db["career_rpg"].update_one(
            {"user_id": user_id},
            {"$set": {
                "role_index": role_index,
                "current_xp": current_xp,
                "role_history": history,
                "updated_at": now,
            }},
        )
    else:
        await db["career_rpg"].update_one(
            {"user_id": user_id},
            {"$set": {"current_xp": current_xp, "updated_at": now}},
        )


async def _current_state(user) -> dict:
    gam = await get_gamification_profile(user["id"])
    current_xp = int(gam.get("xp") or 0)
    role_index = _derive_role_index(current_xp)
    await _persist_role(user["id"], current_xp, role_index)
    return _build_response(current_xp, role_index)


@router.get("")
async def get_career(user=Depends(get_current_user)):
    return await _current_state(user)


@router.post("/refresh")
async def refresh_career(user=Depends(get_current_user)):
    return await _current_state(user)


@router.get("/hall")
async def get_hall():
    return {"roles": [
        {
            "title": r["title"],
            "level": r["level"],
            "emoji": r["emoji"],
            "xp_required": r["xp_required"],
            "title_perk": r["title_perk"],
            "cosmetic": r["cosmetic"],
        }
        for r in ROLES
    ]}
