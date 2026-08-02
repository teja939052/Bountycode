"""Placement Times — a daily newspaper built from LIVE world data.

Pure MongoDB + FastAPI (no AI). Every /today request re-queries the real
collections so the world always feels alive: recent XP jumps, battles,
guilds, campus wars, badge unlocks, the daily boss and the mystery merchant.

Every section is defensive: if a collection is missing or empty the section
is simply skipped (present: false), never crashes.
"""
from datetime import datetime, timedelta, timezone
from bson import ObjectId
from fastapi import APIRouter, Depends
from app.middleware.auth import get_current_user
from app.database import (
    get_db,
    users_collection,
    gamification_collection,
    battles_collection,
    campus_leaderboard_collection,
    daily_boss_collection,
    daily_boss_damage_collection,
    newspaper_collection,
)

router = APIRouter(prefix="/api/v1/newspaper", tags=["Newspaper"])

MAX_ARCHIVE_ITEMS = 14


def _today() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def _iso(value):
    if isinstance(value, datetime):
        return value.isoformat()
    if value is None:
        return None
    return str(value)


def _title_case(text):
    if not text:
        return ""
    words = str(text).split()
    return " ".join(w.capitalize() if w.islower() else w for w in words)


async def _user_name(user_id) -> str:
    """Best-effort human-readable name for a user id (never raises)."""
    if not user_id:
        return "Unknown"
    try:
        raw = str(user_id)
        oid = ObjectId(raw) if ObjectId.is_valid(raw) else None
        if oid is not None:
            user = await users_collection().find_one({"_id": oid})
        else:
            user = await users_collection().find_one({"id": raw})
        if user:
            name = (user.get("name") or "").strip()
            if name:
                return name[:24]
            email = user.get("email") or ""
            return email.split("@")[0].title()[:24] or "Unknown"
    except Exception:
        pass
    return "Unknown"


# ─── Sections ────────────────────────────────────────────────────────────

async def _headline() -> dict:
    """Top story: the most recent big XP gain in the last 24h."""
    candidate = None
    try:
        since = datetime.now(timezone.utc) - timedelta(hours=24)
        profiles = []
        async for p in (
            gamification_collection()
            .find({"updated_at": {"$gte": since}})
            .sort("updated_at", -1)
            .limit(30)
        ):
            profiles.append(p)
        if not profiles:
            top = await gamification_collection().find_one(sort=[("xp", -1)])
            if top:
                profiles.append(top)
        if profiles:
            candidate = profiles[0]
    except Exception:
        candidate = None

    if not candidate:
        try:
            user = await users_collection().find_one(sort=[("xp_updated_at", -1)])
            if user:
                candidate = {
                    "user_id": str(user.get("_id")),
                    "level": user.get("level", 1),
                    "xp": user.get("xp", 0),
                    "updated_at": user.get("xp_updated_at"),
                }
        except Exception:
            candidate = None

    if not candidate:
        return {
            "title": "The Arena Holds Its Breath",
            "subtitle": "No adventurers have logged XP yet today — be the first story.",
            "name": None,
            "level": None,
            "xp": 0,
        }

    user_id = candidate.get("user_id")
    name = await _user_name(user_id)
    level = candidate.get("level") or 1
    xp = candidate.get("xp") or 0
    streak = candidate.get("streak") or 0

    if level and level > 1:
        title = f"{name} hit Level {level}"
    elif xp:
        title = f"{name} surged past {xp:,} XP"
    else:
        title = f"{name} stepped into the arena"

    subtitle = f"Level {level} · {xp:,} total XP"
    if streak:
        subtitle += f" · {streak}-day streak"

    return {"title": title, "subtitle": subtitle, "name": name, "level": level, "xp": xp}


async def _battles() -> list:
    """Latest completed battle results."""
    items = []
    try:
        async for b in battles_collection().find().sort("created_at", -1).limit(10):
            if b.get("status") != "completed":
                continue
            p1_id = str(b.get("player1_id") or "")
            p2_id = str(b.get("player2_id") or "")
            winner_id = str(b.get("winner_id")) if b.get("winner_id") else None
            name1 = await _user_name(p1_id)
            name2 = await _user_name(p2_id)
            s1 = b.get("player1_score")
            s2 = b.get("player2_score")
            winner = name1 if winner_id == p1_id else (name2 if winner_id == p2_id else None)
            items.append({
                "id": str(b["_id"]),
                "mode": _title_case(b.get("mode")) or "Battle",
                "difficulty": _title_case(b.get("difficulty")),
                "player1": name1,
                "player2": name2,
                "score1": s1,
                "score2": s2,
                "winner": winner,
                "draw": not winner,
                "created_at": _iso(b.get("created_at")),
            })
            if len(items) >= 5:
                break
    except Exception:
        items = []
    return items


async def _guilds() -> dict:
    """Top guilds by XP plus the most recently resolved war."""
    top = []
    war = None
    try:
        db = get_db()
        async for g in db["guilds"].find().sort("xp", -1).limit(3):
            top.append({
                "name": g.get("name"),
                "xp": g.get("xp", 0),
                "level": g.get("level") or 1,
                "title": g.get("level_title") or g.get("title"),
                "members": len(g.get("members", [])),
            })
    except Exception:
        top = []

    try:
        db = get_db()
        latest = await db["guilds_war"].find_one(sort=[("created_at", -1)])
        if latest and latest.get("status") == "resolved" and latest.get("winner_id"):
            winner_name = (
                latest.get("challenger_name")
                if latest.get("winner_id") == latest.get("challenger_id")
                else latest.get("defender_name")
            )
            loser_name = (
                latest.get("defender_name")
                if latest.get("winner_id") == latest.get("challenger_id")
                else latest.get("challenger_name")
            )
            if winner_name:
                war = {
                    "winner": winner_name,
                    "loser": loser_name,
                    "headline": f"{winner_name} won the guild war",
                }
    except Exception:
        war = None

    return {"top": top, "war": war}


async def _campus() -> dict:
    """Top colleges this month."""
    items = []
    try:
        month = datetime.now(timezone.utc).strftime("%Y-%m")
        rank = 1
        async for c in (
            campus_leaderboard_collection()
            .find({"month": month})
            .sort("points", -1)
            .limit(5)
        ):
            items.append({
                "rank": rank,
                "college": c.get("college"),
                "points": c.get("points", 0),
                "members": c.get("members", 0),
            })
            rank += 1
    except Exception:
        items = []
    return {"month": datetime.now(timezone.utc).strftime("%Y-%m"), "items": items}


async def _achievements() -> list:
    """Recent badge unlocks from gamification profiles."""
    items = []
    try:
        since = datetime.now(timezone.utc) - timedelta(hours=48)
        async for p in (
            gamification_collection()
            .find({"updated_at": {"$gte": since}})
            .sort("updated_at", -1)
            .limit(12)
        ):
            badges = p.get("badges") or []
            if not badges:
                continue
            name = await _user_name(p.get("user_id"))
            badge_name = None
            for b in reversed(badges):
                if isinstance(b, dict):
                    badge_name = (b.get("name") or b.get("id") or "").replace("_", " ").title()
                    if badge_name:
                        break
            if not badge_name and len(badges) == 1:
                badge_name = str(badges[0]).replace("_", " ").title()
            items.append({
                "name": name,
                "badge": badge_name,
                "level": p.get("level", 1),
                "count": len(badges),
            })
            if len(items) >= 5:
                break
    except Exception:
        items = []
    return items


async def _boss() -> dict:
    """Today's daily boss + top damage dealers."""
    try:
        boss = await daily_boss_collection().find_one({"date": _today()})
        if not boss:
            return None
        top_dealers = []
        pipeline = [
            {"$match": {"boss_id": str(boss["_id"])}},
            {"$group": {"_id": "$user_id", "damage": {"$sum": "$damage"}}},
            {"$sort": {"damage": -1}},
            {"$limit": 3},
        ]
        async for entry in daily_boss_damage_collection().aggregate(pipeline):
            top_dealers.append({
                "name": await _user_name(entry.get("_id")),
                "damage": entry.get("damage", 0),
            })
        hp_total = boss.get("hp_total") or 1
        return {
            "name": boss.get("name"),
            "hp_remaining": boss.get("hp_remaining", 0),
            "hp_total": hp_total,
            "defeated": bool(boss.get("defeated_at")),
            "percent": round(boss.get("hp_remaining", 0) / hp_total * 100, 1),
            "top_dealers": top_dealers,
        }
    except Exception:
        return None


async def _merchant() -> dict:
    """Mystery Merchant — how many trades happened today."""
    try:
        db = get_db()
        trades = await db["merchant_purchases"].count_documents({"date": _today()})
        if trades <= 0:
            return None
        return {"trades": trades, "date": _today()}
    except Exception:
        return None


# ─── Archive helpers ─────────────────────────────────────────────────────

async def _ensure_archive(today: str, headline_title: str) -> int:
    """Store today's edition if missing (single collection). Returns the edition number."""
    try:
        doc = await newspaper_collection().find_one({"date": today})
        if doc:
            return doc.get("edition", 0)
        count = await newspaper_collection().count_documents({})
        edition = count + 1
        await newspaper_collection().insert_one({
            "date": today,
            "edition": edition,
            "headline": headline_title,
            "kind": "edition",
            "created_at": datetime.now(timezone.utc),
        })
        return edition
    except Exception:
        return 0


async def _archive_list() -> list:
    """Past editions, newest first."""
    editions = []
    try:
        async for e in (
            newspaper_collection()
            .find({"kind": "edition"})
            .sort("date", -1)
            .limit(MAX_ARCHIVE_ITEMS)
        ):
            editions.append({
                "date": e.get("date"),
                "headline": e.get("headline", "The Realm Awakens"),
            })
    except Exception:
        editions = []
    return editions


async def _snapshot(edition: int, headline: dict, sections: dict) -> dict:
    """Persist the full edition snapshot for later reuse."""
    try:
        await newspaper_collection().update_one(
            {"date": _today(), "kind": "snapshot"},
            {
                "$set": {
                    "edition": edition,
                    "headline": headline,
                    "sections": sections,
                    "generated_at": datetime.now(timezone.utc),
                }
            },
            upsert=True,
        )
    except Exception:
        pass


# ─── Routes ──────────────────────────────────────────────────────────────

@router.get("/today")
async def today_newspaper(user=Depends(get_current_user)):
    """Build today's edition of the Placement Times from live world data."""
    today = _today()
    headline = await _headline()
    edition = await _ensure_archive(today, headline.get("title", "The Arena Holds Its Breath"))

    battles = await _battles()
    guilds = await _guilds()
    campus = await _campus()
    achievements = await _achievements()
    boss = await _boss()
    merchant = await _merchant()

    sections = {
        "battles": {"present": bool(battles), "items": battles},
        "guilds": {
            "present": bool(guilds.get("top")) or bool(guilds.get("war")),
            "top": guilds.get("top", []),
            "war": guilds.get("war"),
        },
        "campus": {"present": bool(campus.get("items")), "month": campus.get("month"), "items": campus.get("items", [])},
        "achievements": {"present": bool(achievements), "items": achievements},
    }
    if boss:
        sections["boss"] = {"present": True, **boss}
    if merchant:
        sections["merchant"] = {"present": True, **merchant}

    await _snapshot(edition, headline, sections)

    return {
        "date": today,
        "edition": edition,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "headline": headline,
        "sections": sections,
        "archive": await _archive_list(),
    }


@router.get("/daily")
async def daily_newspapers(user=Depends(get_current_user)):
    """Past editions of the Placement Times (archive)."""
    today = _today()
    try:
        existing = await newspaper_collection().find_one({"date": today, "kind": "edition"})
    except Exception:
        existing = None

    if not existing:
        headline = await _headline()
        await _ensure_archive(today, headline.get("title", "The Arena Holds Its Breath"))

    return {"date": today, "archive": await _archive_list()}
