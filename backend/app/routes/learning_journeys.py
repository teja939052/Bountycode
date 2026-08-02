"""
Learning Journeys — Curated learning paths inspired by codedex.io.
Guides learners through a structured sequence of languages and levels based on their goals.
"""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import gamification_collection, users_collection, solved_problems_collection
from app.data.curriculum import get_all_languages, LANGUAGES
import app.data.curriculum_enrichment  # noqa: F401

router = APIRouter(prefix="/api/v1/learning/journeys", tags=["learning-journeys"])

JOURNEYS = [
    {
        "id": "web-dev",
        "title": "Web Development",
        "subtitle": "Build websites and web apps from scratch",
        "icon": "🌐",
        "color": "#3B82F6",
        "gradient": "from-blue-500 to-cyan-500",
        "description": "Master HTML, CSS, JavaScript, and React to build modern web applications.",
        "estimated_hours": 120,
        "difficulty": "Beginner to Advanced",
        "languages": ["html", "css", "javascript"],
        "total_lessons": 0,  # computed at runtime
    },
    {
        "id": "data-science",
        "title": "Data Science",
        "subtitle": "Analyze data and build ML models",
        "icon": "📊",
        "color": "#22C55E",
        "gradient": "from-green-500 to-emerald-500",
        "description": "Learn Python, SQL, and data analysis to extract insights from data.",
        "estimated_hours": 100,
        "difficulty": "Beginner to Intermediate",
        "languages": ["python"],
        "total_lessons": 0,
    },
    {
        "id": "ai-machine-learning",
        "title": "Artificial Intelligence",
        "subtitle": "Build intelligent systems and LLMs",
        "icon": "🤖",
        "color": "#A855F7",
        "gradient": "from-purple-500 to-pink-500",
        "description": "Explore machine learning, neural networks, and generative AI with Python.",
        "estimated_hours": 80,
        "difficulty": "Intermediate",
        "languages": ["python"],
        "total_lessons": 0,
    },
    {
        "id": "computer-science",
        "title": "Computer Science",
        "subtitle": "Master the fundamentals of computing",
        "icon": "💻",
        "color": "#F59E0B",
        "gradient": "from-amber-500 to-orange-500",
        "description": "Learn C, C++, Java, and Rust — from memory management to systems programming.",
        "estimated_hours": 200,
        "difficulty": "Beginner to Expert",
        "languages": ["c", "cpp", "java", "rust"],
        "total_lessons": 0,
    },
    {
        "id": "game-development",
        "title": "Game Development",
        "subtitle": "Create 2D and 3D games",
        "icon": "🕹️",
        "color": "#EC4899",
        "gradient": "from-pink-500 to-rose-500",
        "description": "Build games with JavaScript, C++, and Python — from concept to deployment.",
        "estimated_hours": 90,
        "difficulty": "Intermediate",
        "languages": ["javascript", "cpp", "python"],
        "total_lessons": 0,
    },
    {
        "id": "placement-prep",
        "title": "Placement Preparation",
        "subtitle": "Crack your dream company interview",
        "icon": "🎯",
        "color": "#EF4444",
        "gradient": "from-red-500 to-rose-500",
        "description": "Master DSA, system design, aptitude, and company-specific interview patterns for campus placements.",
        "estimated_hours": 150,
        "difficulty": "Intermediate to Advanced",
        "languages": ["python", "java", "cpp"],
        "total_lessons": 0,
    },
    {
        "id": "interview-prep",
        "title": "Interview Preparation",
        "subtitle": "FAANG and top-tier company prep",
        "icon": "👑",
        "color": "#6366F1",
        "gradient": "from-indigo-500 to-violet-500",
        "description": "System design, behavioral interviews, and DSA patterns for FAANG-level interviews.",
        "estimated_hours": 120,
        "difficulty": "Advanced",
        "languages": ["python", "java", "cpp"],
        "total_lessons": 0,
    },
    {
        "id": "backend-development",
        "title": "Backend Development",
        "subtitle": "Build APIs and server-side systems",
        "icon": "⚙️",
        "color": "#14B8A6",
        "gradient": "from-teal-500 to-cyan-500",
        "description": "Go, Python, and JavaScript for building scalable backend systems and APIs.",
        "estimated_hours": 100,
        "difficulty": "Intermediate to Advanced",
        "languages": ["go", "python", "javascript"],
        "total_lessons": 0,
    },
]

LANGUAGE_ID_MAP = {
    "html": "html",
    "css": "css",
    "javascript": "javascript",
    "python": "python",
    "java": "java",
    "cpp": "c++",
    "c": "c",
    "go": "go",
    "rust": "rust",
}


def compute_journey_lessons():
    """Compute total lessons per journey from curriculum data."""
    all_langs = get_all_languages()
    lang_map = {lang["id"]: lang for lang in all_langs}
    for journey in JOURNEYS:
        total = 0
        for lang_id in journey["languages"]:
            curriculum_id = LANGUAGE_ID_MAP.get(lang_id, lang_id)
            lang = lang_map.get(curriculum_id)
            if lang:
                total += lang.get("total_lessons", 0)
        journey["total_lessons"] = total


compute_journey_lessons()


@router.get("")
async def list_journeys(user=Depends(get_current_user)):
    """List all learning journeys with user progress."""
    compute_journey_lessons()
    gam_col = gamification_collection()
    uid = user["id"]

    gam_doc = await gam_col.find_one({"user_id": uid})
    journey_progress = gam_doc.get("journey_progress", {}) if gam_doc else {}

    result = []
    for journey in JOURNEYS:
        jp = journey_progress.get(journey["id"], {})
        completed = jp.get("completed_lessons", 0)
        total = journey["total_lessons"]
        result.append({
            **journey,
            "lessons_completed": completed,
            "progress_pct": round(completed / total * 100) if total > 0 else 0,
        })

    return {"journeys": result, "total": len(result)}


@router.get("/{journey_id}")
async def get_journey_detail(journey_id: str, user=Depends(get_current_user)):
    """Get detailed info about a specific journey including language breakdown."""
    compute_journey_lessons()
    journey = next((j for j in JOURNEYS if j["id"] == journey_id), None)
    if not journey:
        raise HTTPException(status_code=404, detail=f"Journey '{journey_id}' not found")

    all_langs = get_all_languages()
    lang_map = {lang["id"]: lang for lang in all_langs}
    gam_col = gamification_collection()
    uid = user["id"]

    gam_doc = await gam_col.find_one({"user_id": uid})
    journey_progress = gam_doc.get("journey_progress", {}) if gam_doc else {}
    jp = journey_progress.get(journey_id, {})
    completed = jp.get("completed_lessons", 0)
    total = journey["total_lessons"]

    languages_detail = []
    for lang_id in journey["languages"]:
        curriculum_id = LANGUAGE_ID_MAP.get(lang_id, lang_id)
        lang = lang_map.get(curriculum_id)
        if lang:
            lang_jp = jp.get("languages", {}).get(lang_id, {})
            lang_completed = lang_jp.get("completed", 0)
            lang_total = lang.get("total_lessons", 0)
            languages_detail.append({
                "id": lang_id,
                "name": lang.get("name", lang_id),
                "icon": lang.get("icon", "📘"),
                "color": lang.get("color", "#6366F1"),
                "total_lessons": lang_total,
                "completed_lessons": lang_completed,
                "progress_pct": round(lang_completed / lang_total * 100) if lang_total > 0 else 0,
            })

    return {
        **journey,
        "lessons_completed": completed,
        "progress_pct": round(completed / total * 100) if total > 0 else 0,
        "languages": languages_detail,
    }


@router.post("/{journey_id}/enroll")
async def enroll_journey(journey_id: str, user=Depends(get_current_user)):
    """Enroll the user in a learning journey."""
    journey = next((j for j in JOURNEYS if j["id"] == journey_id), None)
    if not journey:
        raise HTTPException(status_code=404, detail=f"Journey '{journey_id}' not found")

    gam_col = gamification_collection()
    uid = user["id"]

    await gam_col.update_one(
        {"user_id": uid},
        {"$set": {f"journey_progress.{journey_id}.enrolled_at": datetime.now(timezone.utc).isoformat()}},
        upsert=True,
    )

    return {"status": "enrolled", "journey_id": journey_id}


@router.post("/{journey_id}/progress")
async def update_journey_progress(
    journey_id: str,
    language_id: str = Query(...),
    lessons_completed: int = Query(default=0),
    user=Depends(get_current_user),
):
    """Update user progress within a learning journey."""
    journey = next((j for j in JOURNEYS if j["id"] == journey_id), None)
    if not journey:
        raise HTTPException(status_code=404, detail=f"Journey '{journey_id}' not found")

    gam_col = gamification_collection()
    uid = user["id"]

    await gam_col.update_one(
        {"user_id": uid},
        {
            "$set": {
                f"journey_progress.{journey_id}.languages.{language_id}.completed": lessons_completed,
                f"journey_progress.{journey_id}.last_updated": datetime.now(timezone.utc).isoformat(),
            },
            "$inc": {
                f"journey_progress.{journey_id}.completed_lessons": lessons_completed,
            },
        },
        upsert=True,
    )

    return {"status": "updated", "journey_id": journey_id, "language_id": language_id}
