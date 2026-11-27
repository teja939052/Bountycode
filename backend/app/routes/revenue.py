"""Revenue routes — PostgreSQL-backed, no MongoDB."""
from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth import get_current_user
from app.database import get_session

router = APIRouter(prefix="/api/v1/revenue", tags=["revenue"])


@router.get("/metrics")
async def get_revenue_metrics(user=Depends(get_current_user)):
    """Get revenue metrics."""
    return {"revenue": 0, "currency": "USD", "period": "monthly"}


@router.get("/transactions")
async def get_revenue_transactions(user=Depends(get_current_user)):
    """Get revenue transactions."""
    return {"transactions": []}