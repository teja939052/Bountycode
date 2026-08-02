from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth import get_current_user
from app.services.hook_model import (
    roll_mystery_box,
    check_double_xp_trigger,
    get_savage_feedback,
    use_streak_freeze,
    apply_mystery_box_reward,
    check_daily_bonus,
)
from app.services.gamification import get_gamification_profile, record_practice
from app.services.ats_enhanced import calculate_ats_score
from app.services.social import (
    create_study_group,
    join_study_group,
    get_study_groups,
    get_active_contests,
    enter_contest,
    get_contest_leaderboard,
)

router = APIRouter(prefix="/api/v1/hook", tags=["hook-model"])


# Mystery Box endpoints
@router.post("/mystery-box")
async def open_mystery_box(user=Depends(get_current_user)):
    """Open a mystery box for a random reward."""
    reward = roll_mystery_box()
    result = await apply_mystery_box_reward(user["id"], reward)
    return {
        "reward": reward,
        "result": result,
    }


@router.post("/double-xp-check")
async def check_double_xp(activity_type: str, score: float, user=Depends(get_current_user)):
    """Check if double XP is triggered."""
    profile = await get_gamification_profile(user["id"])
    trigger = check_double_xp_trigger(profile, activity_type, score)
    return {"trigger": trigger}


@router.get("/savage-feedback")
async def get_feedback(score: float):
    """Get engaging, memorable feedback."""
    return {"feedback": get_savage_feedback(score)}


# Streak endpoints
@router.post("/streak-freeze")
async def freeze_streak(user=Depends(get_current_user)):
    """Use a streak freeze."""
    return await use_streak_freeze(user["id"])


@router.get("/daily-bonus")
async def daily_bonus(user=Depends(get_current_user)):
    """Check for daily bonus."""
    return await check_daily_bonus(user["id"])


# Enhanced ATS
@router.post("/ats-analyze")
async def analyze_ats(resume_text: str, job_description: str = None, user=Depends(get_current_user)):
    """Enhanced ATS analysis with semantic scoring."""
    return calculate_ats_score(resume_text, job_description)


# Social - Study Groups
@router.post("/study-groups/create")
async def create_group(name: str, description: str = "", user=Depends(get_current_user)):
    """Create a study group."""
    return await create_study_group(name, user["id"], description)


@router.post("/study-groups/{group_id}/join")
async def join_group(group_id: str, user=Depends(get_current_user)):
    """Join a study group."""
    return await join_study_group(group_id, user["id"])


@router.get("/study-groups")
async def list_groups(user=Depends(get_current_user)):
    """List study groups."""
    return await get_study_groups(user["id"])


# Social - Contests
@router.get("/contests")
async def list_contests():
    """Get active contests."""
    return await get_active_contests()


@router.post("/contests/{contest_id}/enter")
async def enter(contest_id: str, score: float, user=Depends(get_current_user)):
    """Enter a contest."""
    return await enter_contest(contest_id, user["id"], score)


@router.get("/contests/{contest_id}/leaderboard")
async def contest_leaderboard(contest_id: str):
    """Get contest leaderboard."""
    return await get_contest_leaderboard(contest_id)
