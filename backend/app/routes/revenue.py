from fastapi import APIRouter, Depends, Query
from typing import Optional
from app.middleware.auth import get_current_user
from app.services.revenue import get_monthly_recurring_revenue, get_revenue_analytics, get_revenue_metrics

router = APIRouter(prefix="/api/v1/revenue", tags=["revenue"])


@router.get("/metrics")
async def revenue_metrics(user=Depends(get_current_user)):
    return await get_revenue_metrics()


@router.get("/mrr")
async def monthly_recurring_revenue(user=Depends(get_current_user)):
    return await get_monthly_recurring_revenue()


@router.get("/analytics")
async def revenue_analytics(days: Optional[int] = Query(30, ge=1, le=365)):
    return await get_revenue_analytics(days)