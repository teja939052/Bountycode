"""
Card Collection System — Collectible cards for every problem solved.
Gamification layer inspired by Pokemon TCG and Genshin Impact.
"""
from datetime import datetime, timezone, timedelta
import random
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import (
    curated_questions_collection, solved_problems_collection,
    cards_collection
)

router = APIRouter(prefix="/api/cards", tags=["cards"])

# Card rarity configuration
RARITY_CONFIG = {
    "common": {
        "name": "Common",
        "color": "#9CA3AF",
        "border": "border-gray-400",
        "bg": "bg-gray-900/30",
        "xp_base": 10,
        "drop_rate": 0.50,
        "emoji": "⬜",
        "stars": 1,
    },
    "uncommon": {
        "name": "Uncommon",
        "color": "#22C55E",
        "border": "border-green-400",
        "bg": "bg-green-900/20",
        "xp_base": 25,
        "drop_rate": 0.25,
        "emoji": "🟢",
        "stars": 2,
    },
    "rare": {
        "name": "Rare",
        "color": "#3B82F6",
        "border": "border-blue-400",
        "bg": "bg-blue-900/20",
        "xp_base": 50,
        "drop_rate": 0.15,
        "emoji": "🔵",
        "stars": 3,
    },
    "epic": {
        "name": "Epic",
        "color": "#A855F7",
        "border": "border-purple-400",
        "bg": "bg-purple-900/20",
        "xp_base": 100,
        "drop_rate": 0.07,
        "emoji": "🟣",
        "stars": 4,
    },
    "legendary": {
        "name": "Legendary",
        "color": "#EAB308",
        "border": "border-yellow-400",
        "bg": "bg-yellow-900/20",
        "xp_base": 250,
        "drop_rate": 0.025,
        "emoji": "🟡",
        "stars": 5,
    },
    "mythic": {
        "name": "Mythic",
        "color": "#F472B6",
        "border": "border-pink-400",
        "bg": "bg-pink-900/20",
        "xp_base": 500,
        "drop_rate": 0.005,
        "emoji": "🩷",
        "stars": 6,
    },
}

# Problem-to-card emoji mapping based on topic
TOPIC_EMOJIS = {
    "Arrays": ["📦", "🧮", "📊", "🔢", "📐"],
    "Linked Lists": ["🔗", "⛓️", "🪝", "🔗", "💍"],
    "Stacks & Queues": ["📚", "📥", "📤", "📚", "🏗️"],
    "Binary Trees": ["🌲", "🌳", "🌿", "🍀", "🎄"],
    "Graphs": ["🕸️", "🗺️", "🌐", "🕸️", "🧭"],
    "Dynamic Programming": ["🧩", "🎯", "⚡", "🔮", "💡"],
    "Binary Search": ["🎯", "🔍", "🏹", "🎯", "🧭"],
    "Sorting": ["📋", "🔢", "📊", "📈", "📉"],
    "Recursion": ["🔄", "🔁", "♻️", "🔄", "🪞"],
    "Bit Manipulation": ["💡", "⚡", "🔮", "✨", "🌟"],
    "Heaps": ["⛰️", "🏔️", "🌋", "⛰️", "🏔️"],
    "Greedy": ["💰", "🏆", "🥇", "💰", "🏆"],
    "BST": ["🌲", "🔍", "🎯", "🌲", "🔍"],
    "Tries": ["🔤", "📖", "📚", "🔤", "📖"],
    "Strings": ["📝", "✏️", "📖", "📝", "✏️"],
    "Sliding Window": ["🪟", "👀", "🔍", "🪟", "👀"],
}


def calculate_rarity(user_stats):
    """Determine card rarity based on user performance."""
    problems_solved = user_stats.get("total_solved", 0)
    streak = user_stats.get("streak", 0)
    avg_score = user_stats.get("avg_score", 0)

    # Weighted random based on rarity rates
    rand = random.random()
    cumulative = 0
    for rarity, config in RARITY_CONFIG.items():
        cumulative += config["drop_rate"]
        if rand <= cumulative:
            # Boost rarity based on user performance
            if problems_solved > 50 and rarity in ("common", "uncommon"):
                if random.random() < 0.3:
                    rarity = "rare"
            if streak > 7 and rarity in ("common", "uncommon", "rare"):
                if random.random() < 0.2:
                    rarity = "epic"
            return rarity
    return "common"


def get_card_emoji(topic):
    """Get a random emoji for a problem based on its topic."""
    emojis = TOPIC_EMOJIS.get(topic, ["❓"])
    return random.choice(emojis)


@router.get("/collection")
async def get_collection(
    rarity: Optional[str] = None,
    topic: Optional[str] = None,
    sort: Optional[str] = "obtained_at",
    user=Depends(get_current_user),
):
    """Get user's card collection with filtering and sorting."""
    collection = cards_collection()
    query = {"user_id": user["id"]}

    if rarity:
        query["rarity"] = rarity
    if topic:
        query["topic"] = topic

    cursor = collection.find(query).sort(sort, -1)
    cards = []
    async for card in cursor:
        card["id"] = str(card.pop("_id"))
        cards.append(card)

    # Calculate stats
    rarity_counts = {}
    topic_counts = {}
    for card in cards:
        r = card.get("rarity", "common")
        t = card.get("topic", "Unknown")
        rarity_counts[r] = rarity_counts.get(r, 0) + 1
        topic_counts[t] = topic_counts.get(t, 0) + 1

    total_problems = await curated_questions_collection().count_documents({})

    return {
        "cards": cards,
        "total_collected": len(cards),
        "total_available": total_problems,
        "completion_percentage": round(len(cards) / max(total_problems, 1) * 100, 1),
        "rarity_counts": rarity_counts,
        "topic_counts": topic_counts,
        "rarity_config": RARITY_CONFIG,
    }


@router.get("/daily-draw")
async def daily_draw(user=Depends(get_current_user)):
    """Get today's daily card draw."""
    collection = cards_collection()
    today = datetime.now(timezone.utc).date().isoformat()

    # Check if already drawn today
    existing = await collection.find_one({
        "user_id": user["id"],
        "daily_draw_date": today,
    })
    if existing:
        return {
            "already_drawn": True,
            "card": existing,
            "message": "You've already drawn today's card!",
        }

    # Get user stats for rarity calculation
    solved_col = solved_problems_collection()
    total_solved = await solved_col.count_documents({"user_id": user["id"]})

    # Get weakest topic for the draw
    pipeline = [
        {"$match": {"user_id": user["id"]}},
        {"$lookup": {
            "from": "curated_questions",
            "localField": "question_id",
            "foreignField": "_id",
            "as": "question"
        }},
        {"$unwind": "$question"},
        {"$group": {"_id": "$question.topic", "count": {"$sum": 1}}}
    ]
    topic_solved = {}
    async for doc in solved_col.aggregate(pipeline):
        topic_solved[doc["_id"]] = doc["count"]

    # Find least solved topic
    all_topics = ["Arrays", "Linked Lists", "Stacks & Queues", "Binary Trees",
                   "Graphs", "Dynamic Programming", "Binary Search", "Sorting",
                   "Recursion", "Bit Manipulation", "Heaps", "Greedy", "BST", "Tries"]
    weakest_topic = min(all_topics, key=lambda t: topic_solved.get(t, 0))

    # Get a random unsolved problem from weakest topic
    questions_col = curated_questions_collection()
    solved_ids = []
    async for doc in solved_col.find({"user_id": user["id"]}, {"question_id": 1}):
        solved_ids.append(doc["question_id"])

    query = {"topic": weakest_topic, "type": "coding"}
    if solved_ids:
        query["_id"] = {"$nin": [ObjectId(sid) for sid in solved_ids if ObjectId.is_valid(sid)]}

    problem = await questions_col.find_one(query)
    if not problem:
        # Fallback: any random problem
        problem = await questions_col.find_one({"type": "coding"})

    if not problem:
        return {"already_drawn": False, "card": None, "message": "No problems available for draw."}

    # Determine rarity
    rarity = calculate_rarity({"total_solved": total_solved})

    # Create card
    card = {
        "user_id": user["id"],
        "problem_id": str(problem["_id"]),
        "problem_title": problem.get("question_title", "Unknown"),
        "topic": problem.get("topic", "Unknown"),
        "difficulty": problem.get("difficulty", "medium"),
        "rarity": rarity,
        "emoji": get_card_emoji(problem.get("topic", "")),
        "obtained_at": datetime.now(timezone.utc),
        "daily_draw_date": today,
        "is_favorite": False,
        "evolution_level": 0,
        "stats": {
            "solve_time": None,
            "success_rate": None,
            "attempts": 0,
        },
    }

    result = await collection.insert_one(card)
    card["id"] = str(result.inserted_id)

    rarity_config = RARITY_CONFIG[rarity]

    return {
        "already_drawn": False,
        "card": card,
        "rarity_info": rarity_config,
        "xp_gained": rarity_config["xp_base"],
        "message": f"You drew a {rarity_config['name']} card! {rarity_config['emoji']}",
    }


@router.post("/favorite/{card_id}")
async def toggle_favorite(card_id: str, user=Depends(get_current_user)):
    """Toggle card favorite status."""
    collection = cards_collection()
    try:
        c_oid = ObjectId(card_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid card ID")

    card = await collection.find_one({"_id": c_oid, "user_id": user["id"]})
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    new_status = not card.get("is_favorite", False)
    await collection.update_one(
        {"_id": c_oid},
        {"$set": {"is_favorite": new_status}}
    )

    return {"card_id": card_id, "is_favorite": new_status}


@router.post("/fuse")
async def fuse_cards(card_ids: list, user=Depends(get_current_user)):
    """Fuse 3 cards of same rarity into 1 higher rarity card."""
    collection = cards_collection()

    if len(card_ids) != 3:
        raise HTTPException(status_code=400, detail="Must provide exactly 3 card IDs")

    # Get all three cards
    cards = []
    for cid in card_ids:
        try:
            card = await collection.find_one({"_id": ObjectId(cid), "user_id": user["id"]})
            if not card:
                raise HTTPException(status_code=404, detail=f"Card {cid} not found")
            cards.append(card)
        except Exception:
            raise HTTPException(status_code=400, detail=f"Invalid card ID: {cid}")

    # Check same rarity
    rarities = [c.get("rarity") for c in cards]
    if len(set(rarities)) != 1:
        raise HTTPException(status_code=400, detail="All cards must be same rarity for fusion")

    current_rarity = rarities[0]
    rarity_order = ["common", "uncommon", "rare", "epic", "legendary", "mythic"]
    current_idx = rarity_order.index(current_rarity)

    if current_idx >= len(rarity_order) - 1:
        raise HTTPException(status_code=400, detail="Cannot fuse Mythic cards")

    new_rarity = rarity_order[current_idx + 1]
    new_rarity_config = RARITY_CONFIG[new_rarity]

    # Delete the three fused cards
    for cid in card_ids:
        await collection.delete_one({"_id": ObjectId(cid), "user_id": user["id"]})

    # Create new fused card (pick the best problem from the three)
    best_card = max(cards, key=lambda c: c.get("stats", {}).get("success_rate", 0) or 0)

    new_card = {
        "user_id": user["id"],
        "problem_id": best_card["problem_id"],
        "problem_title": best_card["problem_title"],
        "topic": best_card["topic"],
        "difficulty": best_card["difficulty"],
        "rarity": new_rarity,
        "emoji": get_card_emoji(best_card.get("topic", "")),
        "obtained_at": datetime.now(timezone.utc),
        "is_favorite": False,
        "evolution_level": 0,
        "fused_from": card_ids,
        "stats": {
            "solve_time": None,
            "success_rate": None,
            "attempts": 0,
        },
    }

    result = await collection.insert_one(new_card)
    new_card["id"] = str(result.inserted_id)

    return {
        "card": new_card,
        "old_rarity": current_rarity,
        "new_rarity": new_rarity,
        "rarity_info": new_rarity_config,
        "xp_gained": new_rarity_config["xp_base"] * 2,
        "message": f"Cards fused! {new_rarity_config['emoji']} {new_rarity_config['name']} card created!",
    }


@router.get("/stats")
async def get_card_stats(user=Depends(get_current_user)):
    """Get comprehensive card collection stats."""
    collection = cards_collection()

    total_cards = await collection.count_documents({"user_id": user["id"]})
    total_problems = await curated_questions_collection().count_documents({})

    # Rarity breakdown
    pipeline = [
        {"$match": {"user_id": user["id"]}},
        {"$group": {"_id": "$rarity", "count": {"$sum": 1}}}
    ]
    rarity_stats = {}
    async for doc in collection.aggregate(pipeline):
        rarity_stats[doc["_id"]] = doc["count"]

    # Topic breakdown
    topic_pipeline = [
        {"$match": {"user_id": user["id"]}},
        {"$group": {"_id": "$topic", "count": {"$sum": 1}}}
    ]
    topic_stats = {}
    async for doc in collection.aggregate(topic_pipeline):
        topic_stats[doc["_id"]] = doc["count"]

    # Favorites count
    favorites = await collection.count_documents({"user_id": user["id"], "is_favorite": True})

    # Recent cards (last 7 days)
    week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    recent_count = await collection.count_documents({
        "user_id": user["id"],
        "obtained_at": {"$gte": week_ago}
    })

    return {
        "total_collected": total_cards,
        "total_available": total_problems,
        "completion_percentage": round(total_cards / max(total_problems, 1) * 100, 1),
        "rarity_breakdown": rarity_stats,
        "topic_breakdown": topic_stats,
        "favorites_count": favorites,
        "recent_week": recent_count,
        "rarity_config": RARITY_CONFIG,
    }


@router.get("/missing")
async def get_missing_cards(user=Depends(get_current_user)):
    """Get problems the user hasn't collected cards for yet."""
    collection = cards_collection()
    questions_col = curated_questions_collection()

    # Get all collected problem IDs
    collected_ids = set()
    async for doc in collection.find({"user_id": user["id"]}, {"problem_id": 1}):
        collected_ids.add(doc["problem_id"])

    # Get all problems
    all_problems = []
    async for doc in questions_col.find({}, {"question_title": 1, "topic": 1, "difficulty": 1}):
        pid = str(doc["_id"])
        if pid not in collected_ids:
            all_problems.append({
                "problem_id": pid,
                "problem_title": doc.get("question_title", "Unknown"),
                "topic": doc.get("topic", "Unknown"),
                "difficulty": doc.get("difficulty", "medium"),
                "collected": False,
            })

    return {
        "missing": all_problems[:50],  # Return first 50 missing
        "total_missing": len(all_problems),
    }
