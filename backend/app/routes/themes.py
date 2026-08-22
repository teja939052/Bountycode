"""Custom gamification themes — server-authoritative gating + persistence.

Non-AI feature: 10 color themes (3 free, 7 Pro-exclusive). The backend is the
single source of truth for which themes a user may use (Pro plan gate) and
persists the user's current selection. Theme *display variants* (CSS vars plus
the free "transparent"/"blue"/"emerald" variants) live on the frontend.
"""
from fastapi import APIRouter, Depends, HTTPException, Body
from app.middleware.auth import get_current_user
from app.database import users_collection
from bson import ObjectId

router = APIRouter(prefix="/api/v1/themes", tags=["themes"])

# Pro-exclusive theme ids (everything else is free, including the built-in
# transparent/blue/emerald variants which are valid ThemeMode values).
PRO_THEMES = {"cyber", "aurora", "ember", "synthwave", "retro", "ocean", "lavender"}
FREE_THEMES = {"meadow", "dark", "sunset", "transparent", "blue", "emerald"}
ALL_THEMES = FREE_THEMES | PRO_THEMES


def _is_pro(user) -> bool:
    return user.get("plan") in ("pro", "lifetime") or user.get("is_admin")


@router.get("/")
async def list_themes(user=Depends(get_current_user)):
    is_pro = _is_pro(user)
    unlocked = list(FREE_THEMES)
    if is_pro:
        unlocked += list(PRO_THEMES)
    return {
        "is_pro": is_pro,
        "unlocked": unlocked,
        "current": user.get("selected_theme", "meadow"),
    }


@router.get("/current")
async def current_theme(user=Depends(get_current_user)):
    return {"theme": user.get("selected_theme", "meadow")}


@router.post("/select")
async def select_theme(body: dict = Body(...), user=Depends(get_current_user)):
    theme_id = (body.get("theme_id") or body.get("theme") or "").strip().lower()
    if theme_id not in ALL_THEMES:
        raise HTTPException(status_code=400, detail=f"Invalid theme id: {theme_id}")

    if theme_id in PRO_THEMES and not _is_pro(user):
        raise HTTPException(
            status_code=402,
            detail="Premium theme — upgrade to Pro to unlock.",
        )

    await users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"selected_theme": theme_id}},
    )
    return {"success": True, "theme": theme_id}
