"""Role content API endpoints.

Serves exercises, quizzes, coding challenges, and practice sets
for each role.
"""
from fastapi import APIRouter, Depends, HTTPException

from app.middleware.auth import get_current_user
from app.content.role_packages import get_role_package, all_roles
from app.content.role_content import (
    get_exercises_for_role,
    get_quizzes_for_role,
    get_challenges_for_role,
    get_practice_sets_for_role,
    get_exercise_by_id,
    get_challenge_by_id,
    get_quiz_by_id,
    get_all_role_content,
)

router = APIRouter(prefix="/api/v1/roles", tags=["roles"])


@router.get("/")
async def list_roles():
    """List all available roles."""
    return {"roles": [r.model_dump() for r in all_roles()]}


@router.get("/{role_id}")
async def get_role(role_id: str):
    """Get a role's full package."""
    package = get_role_package(role_id)
    if not package:
        raise HTTPException(status_code=404, detail="Role not found")
    return package.model_dump()


@router.get("/{role_id}/content")
async def get_role_content(role_id: str, user=Depends(get_current_user)):
    """Get all content for a role."""
    package = get_role_package(role_id)
    if not package:
        raise HTTPException(status_code=404, detail="Role not found")
    return get_all_role_content(role_id)


@router.get("/{role_id}/exercises")
async def get_role_exercises(role_id: str, user=Depends(get_current_user)):
    """Get exercises for a role."""
    exercises = get_exercises_for_role(role_id)
    return {"exercises": [e.model_dump() for e in exercises]}


@router.get("/{role_id}/quizzes")
async def get_role_quizzes(role_id: str, user=Depends(get_current_user)):
    """Get quizzes for a role."""
    quizzes = get_quizzes_for_role(role_id)
    return {"quizzes": [q.model_dump() for q in quizzes]}


@router.get("/{role_id}/challenges")
async def get_role_challenges(role_id: str, user=Depends(get_current_user)):
    """Get coding challenges for a role."""
    challenges = get_challenges_for_role(role_id)
    return {"challenges": [c.model_dump() for c in challenges]}


@router.get("/{role_id}/practice-sets")
async def get_role_practice_sets(role_id: str, user=Depends(get_current_user)):
    """Get practice sets for a role."""
    practice_sets = get_practice_sets_for_role(role_id)
    return {"practice_sets": [ps.model_dump() for ps in practice_sets]}


@router.get("/exercise/{exercise_id}")
async def get_exercise(exercise_id: str, user=Depends(get_current_user)):
    """Get a specific exercise."""
    exercise = get_exercise_by_id(exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise.model_dump()


@router.get("/challenge/{challenge_id}")
async def get_challenge(challenge_id: str, user=Depends(get_current_user)):
    """Get a specific coding challenge."""
    challenge = get_challenge_by_id(challenge_id)
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    return challenge.model_dump()


@router.get("/quiz/{quiz_id}")
async def get_quiz(quiz_id: str, user=Depends(get_current_user)):
    """Get a specific quiz."""
    quiz = get_quiz_by_id(quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz.model_dump()
