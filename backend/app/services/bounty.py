"""Bounty Card System - One Piece-inspired placement bounty cards."""
from app.database import (
    gamification_collection, skill_graph_collection, users_collection,
    solved_problems_collection,
)
from app.services.skill_assessment import get_readiness_score

BOUNTY_TIERS = [
    {"min": 0, "max": 100000, "title": "Rookie Pirate", "tier": "rookie", "color": "#9CA3AF", "stars": 1},
    {"min": 100000, "max": 500000, "title": "Apprentice Sword", "tier": "apprentice", "color": "#22C55E", "stars": 2},
    {"min": 500000, "max": 2000000, "title": "Skilled Navigator", "tier": "skilled", "color": "#3B82F6", "stars": 3},
    {"min": 2000000, "max": 10000000, "title": "Expert Marksman", "tier": "expert", "color": "#A855F7", "stars": 4},
    {"min": 10000000, "max": 100000000, "title": "Master Swordsman", "tier": "master", "color": "#F59E0B", "stars": 5},
    {"min": 100000000, "max": 1000000000, "title": "Yonko Commander", "tier": "yonko", "color": "#EF4444", "stars": 6},
    {"min": 1000000000, "max": 999999999999, "title": "Pirate King", "tier": "king", "color": "#FFD700", "stars": 7},
]


def get_bounty_tier(bounty):
    for tier in BOUNTY_TIERS:
        if tier["min"] <= bounty < tier["max"]:
            progress = (bounty - tier["min"]) / max(1, tier["max"] - tier["min"])
            nxt = next((t for t in BOUNTY_TIERS if t["min"] == tier["max"]), None)
            return {
                **tier,
                "progress": round(progress, 3),
                "next_tier": {"title": nxt["title"], "min": nxt["min"]} if nxt else None,
                "gap_to_next": max(0, tier["max"] - bounty) if nxt else 0,
            }
    return {**BOUNTY_TIERS[0], "progress": 0, "next_tier": None, "gap_to_next": 0}


def format_bounty(n):
    if n >= 1000000000:
        return f"{n / 1000000000:.1f}B"
    if n >= 1000000:
        return f"{n / 1000000:.1f}M"
    if n >= 1000:
        return f"{n / 1000:.1f}K"
    return str(n)


def calculate_bounty(level=1, xp=0, streak=0, longest_streak=0, badges_count=0,
                     problems_solved=0, interviews_done=0, resume_score=0,
                     readiness=0, aptitude_done=0, coding_done=0,
                     system_design_done=0, bosses_defeated=0, dungeons_cleared=0):
    b = 0
    b += level * 50000
    b += xp * 2
    b += streak * 10000
    b += longest_streak * 5000
    b += badges_count * 25000
    b += problems_solved * 15000
    b += interviews_done * 75000
    b += int(resume_score * 10000)
    b += int(readiness * 50000)
    b += aptitude_done * 30000
    b += coding_done * 25000
    b += system_design_done * 50000
    b += bosses_defeated * 100000
    b += dungeons_cleared * 150000
    m = 1.0
    if readiness >= 80: m *= 1.3
    elif readiness >= 60: m *= 1.15
    elif readiness >= 40: m *= 1.05
    if streak >= 30: m *= 1.2
    elif streak >= 7: m *= 1.1
    if level >= 50: m *= 1.25
    elif level >= 30: m *= 1.15
    elif level >= 10: m *= 1.05
    return int(b * m)


def get_display_title(bounty, level, badges):
    earned = []
    if level >= 10: earned.append("Code Apprentice")
    if level >= 30: earned.append("Algorithm Adept")
    if level >= 50: earned.append("Software Builder")
    if level >= 80: earned.append("Elite Candidate")
    if "binary_search_master" in badges: earned.append("Binary Hunter")
    if "graph_guardian" in badges: earned.append("Graph Walker")
    if "dp_slayer" in badges: earned.append("DP Slayer")
    if "interview_champion" in badges: earned.append("Interview Champion")
    if "google_challenger" in badges: earned.append("Google Slayer")
    return earned[-1] if earned else get_bounty_tier(bounty)["title"]


async def generate_bounty_card(user_id):
    gam = await gamification_collection.find_one({"user_id": user_id}) or {}
    user = await users_collection.find_one({"uid": user_id}) or {}

    level = gam.get("level", 1)
    xp = gam.get("xp", 0)
    streak = gam.get("streak", 0)
    longest = gam.get("longest_streak", 0)
    badges = gam.get("badges", [])
    bosses = gam.get("bosses_defeated", [])
    dungeons = gam.get("dungeons_cleared", [])
    interviews = gam.get("total_interviews", 0)
    aptitude = gam.get("total_aptitude", 0)
    coding = gam.get("total_coding", 0)
    sysdesign = gam.get("total_system_design", 0)

    solved = await solved_problems_collection.count_documents({"user_id": user_id})
    rd = await get_readiness_score(user_id)
    readiness = rd.get("overall", 0)
    cats = rd.get("categories", {})

    bounty = calculate_bounty(
        level=level, xp=xp, streak=streak, longest_streak=longest,
        badges_count=len(badges), problems_solved=solved,
        interviews_done=interviews, resume_score=cats.get("resume", 0),
        readiness=readiness, aptitude_done=aptitude, coding_done=coding,
        system_design_done=sysdesign, bosses_defeated=len(bosses),
        dungeons_cleared=len(dungeons),
    )

    tier = get_bounty_tier(bounty)
    title = get_display_title(bounty, level, badges)
    status = "legendary" if bounty >= 100000000 else ("active" if streak > 0 else "inactive")

    return {
        "user_id": user_id,
        "name": user.get("name", "Unknown"),
        "avatar_url": user.get("avatar_url", ""),
        "bounty": bounty,
        "bounty_formatted": format_bounty(bounty),
        "tier": tier,
        "display_title": title,
        "level": level,
        "xp": xp,
        "streak": streak,
        "longest_streak": longest,
        "badges_count": len(badges),
        "problems_solved": solved,
        "readiness": round(readiness, 1),
        "categories": {k: round(v, 1) for k, v in cats.items()},
        "bosses_defeated": len(bosses),
        "dungeons_cleared": len(dungeons),
        "status": status,
    }


async def generate_leaderboard(limit=20):
    gam_docs = await gamification_collection.find({}).sort("xp", -1).limit(limit).to_list(length=limit)
    cards = []
    for gam in gam_docs:
        uid = gam.get("user_id")
        if not uid:
            continue
        card = await generate_bounty_card(uid)
        cards.append(card)
    cards.sort(key=lambda c: c["bounty"], reverse=True)
    for i, c in enumerate(cards):
        c["rank"] = i + 1
    return cards
