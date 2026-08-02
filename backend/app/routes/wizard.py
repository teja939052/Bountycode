"""
Code Wizard Character System — Your AI coding companion that grows with you.
Inspired by anime-style RPGs and Duolingo's mascot system.
"""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import (
    solved_problems_collection, gamification_collection,
    wizard_collection, cards_collection
)

router = APIRouter(prefix="/api/v1/wizard", tags=["wizard"])

# Wizard configuration
WIZARD_STYLES = {
    "fantasy": {
        "name": "Fantasy",
        "description": "Medieval mage with arcane powers",
        "base_emoji": "🧙",
        "outfits": {
            1: {"name": "Apprentice Robe", "emoji": "🧙", "description": "Basic apprentice clothing"},
            10: {"name": "Mage Robe", "emoji": "🧙‍♂️", "description": "Enchanted robes with glowing runes"},
            25: {"name": "Archmage Armor", "emoji": "🧝", "description": "Powerful magical armor"},
            50: {"name": "Sage Crown", "emoji": "👑", "description": "Legendary sage attire"},
            100: {"name": "Code God", "emoji": "⚡", "description": "Ultimate coding deity form"},
        },
    },
    "cyberpunk": {
        "name": "Cyberpunk",
        "description": "Futuristic hacker with neon abilities",
        "base_emoji": "🧑‍💻",
        "outfits": {
            1: {"name": "Street Coder", "emoji": "🧑‍💻", "description": "Basic cyberpunk outfit"},
            10: {"name": "Neon Hacker", "emoji": "🤖", "description": "Neon-lit hacker gear"},
            25: {"name": "Cyber Knight", "emoji": "🦾", "description": "Enhanced cybernetic armor"},
            50: {"name": "Net Runner", "emoji": "🌀", "description": "Master of the digital realm"},
            100: {"name": "Singularity", "emoji": "💎", "description": "Transcended human limits"},
        },
    },
    "steampunk": {
        "name": "Steampunk",
        "description": "Victorian-era inventor with clockwork tech",
        "base_emoji": "🔧",
        "outfits": {
            1: {"name": "Tinkerer", "emoji": "🔧", "description": "Basic workshop tools"},
            10: {"name": "Inventor", "emoji": "⚙️", "description": "Clockwork gadgets"},
            25: {"name": "Engineer", "emoji": "🛠️", "description": "Steam-powered gear"},
            50: {"name": "Artificer", "emoji": "🏭", "description": "Master of mechanisms"},
            100: {"name": "Time Lord", "emoji": "⏰", "description": "Controls time itself"},
        },
    },
    "modern": {
        "name": "Modern",
        "description": "Contemporary developer with sleek tech",
        "base_emoji": "👨‍💻",
        "outfits": {
            1: {"name": "Junior Dev", "emoji": "👨‍💻", "description": "Fresh out of bootcamp"},
            10: {"name": "Senior Dev", "emoji": "👩‍💻", "description": "Experienced developer"},
            25: {"name": "Tech Lead", "emoji": "🧑‍🏫", "description": "Team leader"},
            50: {"name": "CTO", "emoji": "🏢", "description": "Chief Technology Officer"},
            100: {"name": "Tech Legend", "emoji": "🌟", "description": "Industry icon"},
        },
    },
}

# Pet configuration
PETS = {
    "pixel": {"name": "Pixel", "emoji": "🦊", "description": "A clever fox that learns alongside you"},
    "cache": {"name": "Cache", "emoji": "🐱", "description": "A cat that remembers everything"},
    "bit": {"name": "Bit", "emoji": "🐕", "description": "A loyal dog that fetches solutions"},
    "node": {"name": "Node", "emoji": "🐰", "description": "A rabbit that hops through trees"},
    "stack": {"name": "Stack", "emoji": "🐢", "description": "A wise turtle that never forgets"},
    "loop": {"name": "Loop", "emoji": "🐦", "description": "A bird that circles back to help"},
}

# Wizard dialogue
DIALOGUES = {
    "greeting": [
        "Ready to code today? Let's tackle some problems!",
        "Welcome back, coder! Your wizard awaits.",
        "Time to level up! Let's solve some challenges.",
        "The code flows through you today. Let's begin!",
    ],
    "solve_easy": [
        "Nice work! That was a warm-up. Ready for harder ones?",
        "Easy peasy! You're getting faster each day.",
        "Clean solution! Keep that momentum going.",
    ],
    "solve_medium": [
        "Solid solve! Your algorithms are sharpening.",
        "Great problem-solving skills! The wizard is impressed.",
        "That's the spirit! Keep climbing the difficulty ladder.",
    ],
    "solve_hard": [
        "Incredible! You've conquered a tough challenge!",
        "The wizard bows to your mastery! That was epic!",
        "Legendary performance! You're becoming a code sage!",
    ],
    "fail": [
        "Don't worry, even the best wizards fail sometimes. Let's learn from this!",
        "Every failure is a lesson. Check the editorial and try again!",
        "The enemy was tough, but we'll come back stronger!",
    ],
    "streak": [
        "Your streak is on fire! Keep it going!",
        "Daily practice makes perfect. You're doing great!",
        "The wizard is proud of your consistency!",
    ],
    "level_up": [
        "LEVEL UP! Your power grows stronger!",
        "New level unlocked! The wizard evolves!",
        "You've reached a new level of mastery!",
    ],
}


def get_wizard_level(xp):
    """Calculate wizard level from XP."""
    import math
    return int(math.sqrt(xp / 100)) + 1


def get_outfit_for_level(level, style):
    """Get the best outfit unlocked for the current level."""
    style_config = WIZARD_STYLES.get(style, WIZARD_STYLES["modern"])
    outfits = style_config["outfits"]
    best_level = 1
    for lvl in sorted(outfits.keys()):
        if level >= lvl:
            best_level = lvl
    return outfits[best_level]


@router.get("/profile")
async def get_wizard_profile(user=Depends(get_current_user)):
    """Get user's wizard profile with level, outfit, and stats."""
    wizard_col = wizard_collection()
    gam_col = gamification_collection()
    cards_col = cards_collection()
    solved_col = solved_problems_collection()

    # Get or create wizard profile
    wizard = await wizard_col.find_one({"user_id": user["id"]})
    if not wizard:
        wizard = {
            "user_id": user["id"],
            "name": user.get("name", "Coder").split()[0],
            "style": "modern",
            "pet": "pixel",
            "created_at": datetime.now(timezone.utc),
        }
        result = await wizard_col.insert_one(wizard)
        wizard["_id"] = result.inserted_id

    # Get gamification stats
    gam_doc = await gam_col.find_one({"user_id": user["id"]})
    xp = gam_doc.get("xp", 0) if gam_doc else 0
    streak = gam_doc.get("streak", 0) if gam_doc else 0

    # Calculate level and outfit
    level = get_wizard_level(xp)
    style = wizard.get("style", "modern")
    outfit = get_outfit_for_level(level, style)
    style_config = WIZARD_STYLES.get(style, WIZARD_STYLES["modern"])

    # Get pet
    pet_key = wizard.get("pet", "pixel")
    pet = PETS.get(pet_key, PETS["pixel"])

    # Get stats
    total_solved = await solved_col.count_documents({"user_id": user["id"]})
    total_cards = await cards_col.count_documents({"user_id": user["id"]})

    # Get greeting
    import random
    greeting = random.choice(DIALOGUES["greeting"])

    return {
        "wizard_id": str(wizard["_id"]),
        "name": wizard.get("name", "Coder"),
        "style": style,
        "style_config": style_config,
        "level": level,
        "xp": xp,
        "xp_to_next": (level * level * 100) - xp,
        "outfit": outfit,
        "pet": pet,
        "streak": streak,
        "total_solved": total_solved,
        "total_cards": total_cards,
        "greeting": greeting,
    }


@router.put("/customize")
async def customize_wizard(
    name: Optional[str] = None,
    style: Optional[str] = None,
    pet: Optional[str] = None,
    user=Depends(get_current_user),
):
    """Customize wizard appearance."""
    wizard_col = wizard_collection()
    updates = {}

    if name and len(name) <= 20:
        updates["name"] = name
    if style and style in WIZARD_STYLES:
        updates["style"] = style
    if pet and pet in PETS:
        updates["pet"] = pet

    if not updates:
        raise HTTPException(status_code=400, detail="No valid updates provided")

    updates["updated_at"] = datetime.now(timezone.utc)

    await wizard_col.update_one(
        {"user_id": user["id"]},
        {"$set": updates},
        upsert=True
    )

    return {"message": "Wizard updated!", "updates": updates}


@router.get("/dialogue/{situation}")
async def get_dialogue(situation: str, user=Depends(get_current_user)):
    """Get wizard dialogue for a specific situation."""
    import random

    dialogues = DIALOGUES.get(situation, DIALOGUES["greeting"])
    dialogue = random.choice(dialogues)

    # Get wizard name
    wizard_col = wizard_collection()
    wizard = await wizard_col.find_one({"user_id": user["id"]})
    wizard_name = wizard.get("name", "Wizard") if wizard else "Wizard"

    # Get outfit emoji
    gam_col = gamification_collection()
    gam_doc = await gam_col.find_one({"user_id": user["id"]})
    xp = gam_doc.get("xp", 0) if gam_doc else 0
    level = get_wizard_level(xp)
    style = wizard.get("style", "modern") if wizard else "modern"
    outfit = get_outfit_for_level(level, style)

    return {
        "wizard_name": wizard_name,
        "outfit_emoji": outfit["emoji"],
        "dialogue": dialogue,
        "situation": situation,
    }


@router.get("/levels")
async def get_wizard_levels(user=Depends(get_current_user)):
    """Get all wizard level milestones and outfits."""
    gam_col = gamification_collection()
    gam_doc = await gam_col.find_one({"user_id": user["id"]})
    xp = gam_doc.get("xp", 0) if gam_doc else 0
    current_level = get_wizard_level(xp)

    levels = []
    for style_key, style_config in WIZARD_STYLES.items():
        style_levels = []
        for lvl, outfit in sorted(style_config["outfits"].items()):
            style_levels.append({
                "level": lvl,
                "outfit": outfit,
                "unlocked": current_level >= lvl,
            })
        levels.append({
            "style": style_key,
            "name": style_config["name"],
            "description": style_config["description"],
            "outfits": style_levels,
        })

    return {
        "current_level": current_level,
        "current_xp": xp,
        "styles": levels,
    }
