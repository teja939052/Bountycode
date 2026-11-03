from fastapi import APIRouter, Depends, HTTPException

from app.middleware.auth import get_current_user
from app.services.readiness import compute_readiness

router = APIRouter(prefix="/api/v1/readiness", tags=["readiness"])


@router.get("/score")
async def score(user=Depends(get_current_user)):
    return compute_readiness(user["id"])
