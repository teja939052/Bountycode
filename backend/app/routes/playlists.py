"""
Curated Playlists — Guided learning paths for placement preparation.
Pre-built playlists for different goals and skill levels.
"""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from app.middleware.auth import get_current_user
from app.database import (
    solved_problems_collection,
    playlists_collection,
    get_db,
)

router = APIRouter(prefix="/api/v1/playlists", tags=["playlists"])

# Pre-defined curated playlists
CURATED_PLAYLISTS = [
    {
        "id": "dsa-foundation",
        "title": "DSA Foundation",
        "description": "Master the basics of Data Structures and Algorithms",
        "difficulty": "easy",
        "duration_weeks": 2,
        "problems_count": 30,
        "topics": ["Arrays", "Linked Lists", "Stacks & Queues"],
        "icon": "🏗️",
        "color": "blue",
        "tags": ["beginner", "foundation", "basics"],
    },
    {
        "id": "tree-master",
        "title": "Binary Tree Mastery",
        "description": "Complete guide to binary trees and BSTs",
        "difficulty": "medium",
        "duration_weeks": 1,
        "problems_count": 20,
        "topics": ["Binary Trees", "Binary Search Trees"],
        "icon": "🌳",
        "color": "green",
        "tags": ["trees", "dfs", "bfs"],
    },
    {
        "id": "dp-crack",
        "title": "DP Crash Course",
        "description": "Conquer Dynamic Programming with pattern-based learning",
        "difficulty": "medium",
        "duration_weeks": 2,
        "problems_count": 25,
        "topics": ["Dynamic Programming"],
        "icon": "🧠",
        "color": "purple",
        "tags": ["dp", "patterns", "optimization"],
    },
    {
        "id": "graph-pro",
        "title": "Graph Algorithms Pro",
        "description": "Master graphs from BFS/DFS to advanced algorithms",
        "difficulty": "hard",
        "duration_weeks": 2,
        "problems_count": 20,
        "topics": ["Graphs"],
        "icon": "🕸️",
        "color": "indigo",
        "tags": ["graphs", "bfs", "dfs", "dijkstra"],
    },
    {
        "id": "google-prep",
        "title": "Google SDE Prep",
        "description": "30 curated problems for Google interviews",
        "difficulty": "hard",
        "duration_weeks": 4,
        "problems_count": 30,
        "topics": ["Arrays", "Dynamic Programming", "Graphs", "Trees", "System Design"],
        "icon": "🔍",
        "color": "red",
        "tags": ["google", "faang", "interview"],
        "company": "Google",
    },
    {
        "id": "amazon-prep",
        "title": "Amazon SDE Prep",
        "description": "30 pattern-relevant problems for Amazon preparation (pattern alignment, never historically-asked claims)",
        "difficulty": "medium",
        "duration_weeks": 4,
        "problems_count": 30,
        "topics": ["Arrays", "Linked Lists", "Trees", "Dynamic Programming"],
        "icon": "📦",
        "color": "orange",
        "tags": ["amazon", "faang", "interview"],
        "company": "Amazon",
    },
    {
        "id": "placement-crash",
        "title": "Placement Crash Course",
        "description": "50 problems covering all topics in 4 weeks",
        "difficulty": "medium",
        "duration_weeks": 4,
        "problems_count": 50,
        "topics": ["Arrays", "Strings", "Trees", "Dynamic Programming", "Graphs"],
        "icon": "🚀",
        "color": "cyan",
        "tags": ["placement", "crash-course", "all-topics"],
    },
    {
        "id": "tcs-nqt",
        "title": "TCS NQT Ready",
        "description": "Prepare for TCS National Qualifier Test",
        "difficulty": "easy",
        "duration_weeks": 2,
        "problems_count": 25,
        "topics": ["Arrays", "Strings", "Basic Algorithms"],
        "icon": "🎯",
        "color": "teal",
        "tags": ["tcs", "nqt", "campus"],
        "company": "TCS",
    },
]


def _playlist_pool(playlist: dict) -> list:
    """In-memory problem pool for a playlist (Residency Rule): topic-scoped
    verified-leaning selection from the canonical store, optionally narrowed
    by the playlist's company tag. Never MongoDB."""
    from app.services import question_store
    pool = question_store.find(
        {"topic": {"$in": playlist["topics"]}, "type": "coding"}
    ).prefer_verified().to_list()
    if playlist.get("company"):
        co = str(playlist["company"]).lower()
        pool = [q for q in pool if co in {str(c).lower() for c in (q.get("companies") or [])}]
    # Legacy order semantics: difficulty string ascending, then topic/problem order.
    pool.sort(key=lambda q: (
        str(q.get("difficulty", "medium")),
        str(q.get("topic_order", "")),
        str(q.get("problem_order", "")),
    ))
    return pool


@router.get("")
async def list_playlists(
    difficulty: Optional[str] = None,
    company: Optional[str] = None,
    user=Depends(get_current_user),
):
    """List all curated playlists with optional filters."""
    playlists = CURATED_PLAYLISTS

    if difficulty:
        playlists = [p for p in playlists if p["difficulty"] == difficulty]
    if company:
        playlists = [p for p in playlists if p.get("company", "").lower() == company.lower()]

    # Get user's progress for each playlist (in-memory only, Residency Rule)
    solved_col = solved_problems_collection()
    solved_ids = set()
    async for doc in solved_col.find({"user_id": user["id"]}, {"question_id": 1}):
        solved_ids.add(str(doc["question_id"]))

    result = []
    for playlist in playlists:
        # Get problems in this playlist's topics
        pool = _playlist_pool(playlist)
        total_problems = len(pool)

        # Solved count within the same pool (string id compare)
        solved_count = sum(1 for q in pool if str(q.get("id")) in solved_ids)

        result.append({
            **playlist,
            "total_problems": total_problems,
            "solved_count": solved_count,
            "progress": round(solved_count / max(total_problems, 1) * 100, 1),
        })

    return {"playlists": result}


@router.get("/{playlist_id}")
async def get_playlist(playlist_id: str, user=Depends(get_current_user)):
    """Get a specific playlist with its problems."""
    # Find playlist
    playlist = next((p for p in CURATED_PLAYLISTS if p["id"] == playlist_id), None)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")

    # Get problems for this playlist (in-memory only, Residency Rule)
    solved_col = solved_problems_collection()

    pool = _playlist_pool(playlist)[:playlist["problems_count"]]

    problems = []
    solved_ids = set()
    async for doc in solved_col.find({"user_id": user["id"]}, {"question_id": 1}):
        solved_ids.add(str(doc["question_id"]))

    for q in pool:
        doc = dict(q)
        doc["id"] = str(q.get("id", ""))
        doc["solved"] = doc["id"] in solved_ids
        problems.append(doc)

    # Get solved count
    solved_count = sum(1 for p in problems if p.get("solved"))

    return {
        **playlist,
        "problems": problems,
        "solved_count": solved_count,
        "progress": round(solved_count / max(len(problems), 1) * 100, 1),
    }


@router.get("/{playlist_id}/next")
async def get_next_problem(playlist_id: str, user=Depends(get_current_user)):
    """Get the next unsolved problem in a playlist."""
    playlist = next((p for p in CURATED_PLAYLISTS if p["id"] == playlist_id), None)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")

    solved_col = solved_problems_collection()

    # Get solved problem IDs
    solved_ids = set()
    async for doc in solved_col.find({"user_id": user["id"]}, {"question_id": 1}):
        solved_ids.add(str(doc["question_id"]))

    # Get problems in order, find first unsolved (in-memory, Residency Rule)
    for q in _playlist_pool(playlist):
        qid = str(q.get("id", ""))
        if qid not in solved_ids:
            doc = dict(q)
            doc["id"] = qid
            return {"next_problem": doc, "playlist": playlist}

    return {"next_problem": None, "message": "Playlist complete! All problems solved."}


@router.post("/custom")
async def create_custom_playlist(
    title: str,
    description: str,
    problem_ids: List[str],
    user=Depends(get_current_user),
):
    """Create a custom playlist with selected problems."""
    db = get_db()

    # Verify all problems exist in the in-memory canonical store
    # (Residency Rule): never MongoDB.
    from app.services import question_store
    valid_ids = []
    for pid in problem_ids:
        if question_store.get_question_for_serving(pid):
            valid_ids.append(pid)

    if not valid_ids:
        raise HTTPException(status_code=400, detail="No valid problem IDs provided")

    playlist = {
        "user_id": user["id"],
        "title": title,
        "description": description,
        "problem_ids": valid_ids,
        "problems_count": len(valid_ids),
        "created_at": datetime.now(timezone.utc),
        "is_custom": True,
    }

    result = await db["playlists"].insert_one(playlist)
    playlist["id"] = str(result.inserted_id)

    return playlist


@router.get("/my/custom")
async def get_my_custom_playlists(user=Depends(get_current_user)):
    """Get user's custom playlists."""
    db = get_db()

    cursor = db["playlists"].find({"user_id": user["id"]}).sort("created_at", -1)
    playlists = []
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        playlists.append(doc)

    return {"playlists": playlists}
