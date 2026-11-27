"""Placement packs routes — PostgreSQL-backed, no MongoDB."""
from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth import get_current_user
from app.database import get_session

router = APIRouter(prefix="/api/v1/placement-packs", tags=["placement-packs"])


@router.get("/packs")
async def list_placement_packs(user=Depends(get_current_user)):
    """List placement preparation packs."""
    return {
        "packs": [
            {"id": "tcs_nqt", "name": "TCS NQT Preparation Pack", "levels": 10},
            {"id": "infosys_infytq", "name": "Infosys InfyTQ Pack", "levels": 8},
            {"id": "wipro_nlth", "name": "Wipro NLTH Pack", "levels": 6},
        ]
    }


@router.get("/packs/{pack_id}")
async def get_placement_pack(pack_id: str, user=Depends(get_current_user)):
    """Get placement pack details."""
    return {"pack_id": pack_id, "name": pack_id, "levels": [], "total_levels": 0}