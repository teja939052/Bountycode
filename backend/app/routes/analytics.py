from fastapi import APIRouter, Depends
from app.middleware.auth import get_current_user
from app.services.analytics import (
    get_overview,
    get_funnel,
    get_skill_progression,
    get_company_stats,
    get_insights,
)

router = APIRouter(prefix="/api/v1/analytics", tags=["analytics"])


@router.get("/overview")
async def overview(user=Depends(get_current_user)):
    return await get_overview(user["id"])


@router.get("/funnel")
async def funnel(user=Depends(get_current_user)):
    return await get_funnel(user["id"])


@router.get("/skills")
async def skills(user=Depends(get_current_user)):
    return await get_skill_progression(user["id"])


@router.get("/companies")
async def companies(user=Depends(get_current_user)):
    return await get_company_stats(user["id"])


@router.get("/insights")
async def insights(user=Depends(get_current_user)):
    return await get_insights(user["id"])
