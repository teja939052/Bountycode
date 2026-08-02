from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth import get_current_user
from app.services.energy import get_energy, consume_energy, add_daily_energy

router = APIRouter(prefix="/api/v1/energy", tags=["energy"])


@router.get("")
async def energy_status(user=Depends(get_current_user)):
    return await get_energy(user)


@router.post("/consume")
async def consume(body: dict, user=Depends(get_current_user)):
    amount = body.get("amount", 1)
    success = await consume_energy(user, amount)
    if not success:
        raise HTTPException(status_code=402, detail="No energy remaining. Wait for recharge or upgrade to Pro.")
    energy = await get_energy(user)
    return {"success": True, "energy": energy}


@router.post("/daily-bonus")
async def daily_bonus(user=Depends(get_current_user)):
    result = await add_daily_energy(user)
    energy = await get_energy(user)
    return {**result, "energy": energy}
