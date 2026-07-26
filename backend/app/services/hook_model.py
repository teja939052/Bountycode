import random
from datetime import datetime, timezone, timedelta
from app.database import gamification_collection


# Mystery Box rewards pool
MYSTERY_BOX_REWARDS = [
    {"type": "xp_bonus", "value": 10, "weight": 30, "name": "10 XP Bonus", "icon": "✨"},
    {"type": "xp_bonus", "value": 25, "weight": 20, "name": "25 XP Bonus", "icon": "⭐"},
    {"type": "xp_bonus", "value": 50, "weight": 10, "name": "50 XP Bonus", "icon": "💫"},
    {"type": "xp_bonus", "value": 100, "weight": 3, "name": "100 XP Jackpot!", "icon": "🎰"},
    {"type": "streak_freeze", "value": 1, "weight": 15, "name": "Streak Freeze", "icon": "🧊"},
    {"type": "double_xp_next", "value": 1, "weight": 12, "name": "2x XP Next Session", "icon": "🔥"},
    {"type": "badge_hint", "value": 1, "weight": 5, "name": "Secret Badge Hint", "icon": "🔍"},
    {"type": "level_skip", "value": 1, "weight": 2, "name": "Level Skip Token", "icon": "🚀"},
    {"type": "nothing", "value": 0, "weight": 3, "name": "Better luck next time!", "icon": "🎲"},
]

# Double XP triggers (variable reward)
DOUBLE_XP_TRIGGERS = [
    {"condition": "perfect_score", "description": "Perfect Score Bonus!", "multiplier": 2},
    {"condition": "streak_5", "description": "5-Day Streak Bonus!", "multiplier": 2},
    {"condition": "first_today", "description": "Early Bird Bonus!", "multiplier": 1.5},
    {"condition": "speed_demon", "description": "Speed Demon Bonus!", "multiplier": 1.5},
    {"condition": "comeback", "description": "Welcome Back Bonus!", "multiplier": 2},
]

# Savage feedback messages (engaging, memorable)
SAVAGE_FEEDBACK = {
    "excellent": [
        "Absolute fire! You're built different. 🔥",
        "That answer was chef's kiss. The hiring manager is shaking. 👨‍🍳",
        "You didn't just answer that—you dominated it. 💪",
        "Google called. They want to hire you yesterday. 📞",
    ],
    "good": [
        "Solid answer! A few tweaks and you're unstoppable. 💯",
        "You're getting there! One more push and you'll crush it. 🎯",
        "Not bad at all! Your future boss would be impressed. 👔",
        "Keep this energy and you're landing that offer. 🚀",
    ],
    "average": [
        "It's giving... mid. But we can fix that. 🛠️",
        "You survived, but let's aim for thriving next time. 📈",
        "The interviewer is thinking... 'interesting choice.' Let's level up. 🎮",
        "Not your best work, but hey, practice makes perfect. 🔄",
    ],
    "poor": [
        "That answer was... a choice. Let's pretend that didn't happen. 🫣",
        "The interviewer is politely nodding but internally screaming. 😅",
        "We've all been there. The key is to never be there again. 📚",
        "Plot twist: you're the main character, so let's write a better script. 📝",
    ],
}


def roll_mystery_box() -> dict:
    """Roll for a mystery box reward using weighted random."""
    total_weight = sum(r["weight"] for r in MYSTERY_BOX_REWARDS)
    random_value = random.randint(1, total_weight)
    
    cumulative = 0
    for reward in MYSTERY_BOX_REWARDS:
        cumulative += reward["weight"]
        if random_value <= cumulative:
            return {
                "type": reward["type"],
                "value": reward["value"],
                "name": reward["name"],
                "icon": reward["icon"],
                "is_rare": reward["type"] in ["level_skip", "xp_bonus"] and reward["value"] >= 50,
            }
    
    return MYSTERY_BOX_REWARDS[0]


def check_double_xp_trigger(profile: dict, activity_type: str, score: float) -> dict:
    """Check if any double XP trigger is met."""
    triggers = []
    
    # Perfect score
    if score >= 10:
        triggers.append({
            "type": "perfect_score",
            "description": "Perfect Score Bonus!",
            "multiplier": 2,
            "icon": "💯",
        })
    
    # Streak milestone
    streak = profile.get("streak", 0)
    if streak in [5, 10, 15, 20, 25, 30]:
        triggers.append({
            "type": "streak_milestone",
            "description": f"{streak}-Day Streak Bonus!",
            "multiplier": 2,
            "icon": "🔥",
        })
    
    # First practice today
    last_date = profile.get("last_practice_date")
    if last_date:
        last_date = last_date.date() if isinstance(last_date, datetime) else last_date
        if last_date < datetime.now(timezone.utc).date():
            triggers.append({
                "type": "comeback",
                "description": "Welcome Back Bonus!",
                "multiplier": 2,
                "icon": "👋",
            })
    
    # Speed demon (scored high quickly)
    if score >= 8 and activity_type in ["interview", "coding"]:
        triggers.append({
            "type": "speed_demon",
            "description": "Quick Learner Bonus!",
            "multiplier": 1.5,
            "icon": "⚡",
        })
    
    # Return random trigger if multiple (variable reward!)
    if triggers:
        return random.choice(triggers)
    
    return None


def get_savage_feedback(score: float) -> str:
    """Get engaging, memorable feedback based on score."""
    if score >= 9:
        category = "excellent"
    elif score >= 7:
        category = "good"
    elif score >= 5:
        category = "average"
    else:
        category = "poor"
    
    return random.choice(SAVAGE_FEEDBACK[category])


async def use_streak_freeze(user_id: str) -> dict:
    """Use a streak freeze to protect today's streak."""
    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        return {"success": False, "message": "Profile not found"}
    
    freezes = profile.get("streak_freezes", 0)
    if freezes <= 0:
        return {"success": False, "message": "No streak freezes available"}
    
    # Check if streak was broken today
    last_date = profile.get("last_practice_date")
    if last_date:
        last_date = last_date.date() if isinstance(last_date, datetime) else last_date
        days_diff = (datetime.now(timezone.utc).date() - last_date).days
        
        if days_diff <= 1:
            return {"success": False, "message": "Streak is still active, no need to freeze!"}
        
        # Use freeze and maintain streak
        await gamification_collection.update_one(
            {"user_id": user_id},
            {
                "$inc": {"streak_freezes": -1},
                "$set": {"last_practice_date": datetime.now(timezone.utc)},
            },
        )
        return {
            "success": True,
            "message": f"Streak freeze used! Your {profile.get('streak', 0)}-day streak is saved!",
            "streak": profile.get("streak", 0),
            "freezes_remaining": freezes - 1,
        }
    
    return {"success": False, "message": "No streak to freeze"}


async def apply_mystery_box_reward(user_id: str, reward: dict) -> dict:
    """Apply a mystery box reward to the user."""
    if reward["type"] == "xp_bonus":
        await gamification_collection.update_one(
            {"user_id": user_id},
            {"$inc": {"xp": reward["value"]}},
        )
        return {"applied": True, "message": f"+{reward['value']} XP added!"}
    
    elif reward["type"] == "streak_freeze":
        await gamification_collection.update_one(
            {"user_id": user_id},
            {"$inc": {"streak_freezes": 1}},
        )
        return {"applied": True, "message": "Streak freeze added to inventory!"}
    
    elif reward["type"] == "double_xp_next":
        await gamification_collection.update_one(
            {"user_id": user_id},
            {"$set": {"double_xp_active": True}},
        )
        return {"applied": True, "message": "2x XP active for next session!"}
    
    elif reward["type"] == "badge_hint":
        return {"applied": True, "message": "Hint: Complete 5 system design sessions to unlock a secret badge!"}
    
    elif reward["type"] == "level_skip":
        profile = await gamification_collection.find_one({"user_id": user_id})
        current_level = profile.get("level", 1)
        await gamification_collection.update_one(
            {"user_id": user_id},
            {"$set": {"level": current_level + 1}},
        )
        return {"applied": True, "message": f"Level up! You're now Level {current_level + 1}!"}
    
    return {"applied": False, "message": "Better luck next time!"}


async def check_daily_bonus(user_id: str) -> dict:
    """Check if user qualifies for daily bonus."""
    profile = await gamification_collection.find_one({"user_id": user_id})
    if not profile:
        return {"qualifies": False}
    
    last_date = profile.get("last_practice_date")
    if not last_date:
        return {"qualifies": True, "reason": "first_day"}
    
    last_date = last_date.date() if isinstance(last_date, datetime) else last_date
    today = datetime.now(timezone.utc).date()
    days_diff = (today - last_date).days
    
    if days_diff >= 2:
        return {"qualifies": True, "reason": "comeback", "days_away": days_diff}
    
    return {"qualifies": False}
