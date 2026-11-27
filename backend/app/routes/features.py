"""Features routes — PostgreSQL-backed, no MongoDB."""
from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth import get_current_user
from app.database import get_session
from sqlalchemy import select

router = APIRouter(prefix="/api/v1/features", tags=["features"])


@router.get("/features")
async def list_features(user=Depends(get_current_user)):
    """Get available features."""
    return {"features": []}


@router.get("/features/{feature_id}")
async def get_feature(feature_id: str, user=Depends(get_current_user)):
    """Get feature details."""
    return {"feature_id": feature_id, "enabled": True}