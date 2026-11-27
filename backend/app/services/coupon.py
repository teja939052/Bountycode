"""Coupon service — PostgreSQL-backed, no MongoDB."""

from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.middleware.auth import get_current_user
from app.models.coupon import Coupon, CouponUsage

router = APIRouter(prefix="/api/v1/coupon", tags=["coupon"])


@router.post("/")
async def create_coupon(
    code: str,
    discount_type: str,
    discount_value: float,
    max_uses: int,
    expiry_date: Optional[str] = None,
    applicable_plans: Optional[List[str]] = None,
    active: bool = True,
    user=Depends(get_current_user),
):
    """Create a new coupon code."""
    now = datetime.now(timezone.utc)
    expiry = datetime.fromisoformat(expiry_date).replace(tzinfo=timezone.utc) if expiry_date else now + timedelta(days=90)
    
    coupon_id = str(user["id"]) + "-" + str(datetime.now().timestamp())
    
    # Insert coupon
    await get_session().execute(
        """INSERT INTO coupons (id, code, discount_type, discount_value, max_uses, used_count, expiry_date, applicable_plans, active, created_at)
           VALUES (:id, :code, :discount_type, :discount_value, :max_uses, 0, :expiry_date, :applicable_plans, :active, :created_at)""",
        {
            "id": coupon_id,
            "code": code.upper().strip(),
            "discount_type": discount_type,
            "discount_value": discount_value,
            "max_uses": max_uses,
            "expiry_date": expiry,
            "applicable_plans": applicable_plans or ["pro", "team", "enterprise", "lifetime"],
            "active": active,
            "created_at": now,
        },
    )
    await get_session().commit()
    
    return {"coupon_id": coupon_id, "code": code.upper().strip(), "status": "created"}


@router.post("/validate")
async def validate_coupon(code: str, plan: str = "pro", user=Depends(get_current_user)):
    """Validate a coupon code for a user plan."""
    code = code.upper().strip()
    
    # Check if coupon exists
    result = await get_session().execute(
        select(Coupon).where(Coupon.code == code)
    )
    coupon = result.scalar_one_or_none()
    
    if not coupon:
        return {"valid": False, "error": "Invalid coupon code"}
    
    if not coupon.active:
        return {"valid": False, "error": "Coupon is no longer active"}
    
    if coupon.used_count >= coupon.max_uses:
        return {"valid": False, "error": "Coupon usage limit reached"}
    
    expiry = coupon.expiry_date
    if expiry and expiry < datetime.now(timezone.utc):
        return {"valid": False, "error": "Coupon has expired"}
    
    if coupon.applicable_plans and plan not in coupon.applicable_plans:
        return {"valid": False, "error": f"Coupon not applicable for {plan} plan"}
    
    # Increment use count
    await get_session().execute(
        CouponUsage.__table__.insert().values(
            coupon_id=Coupon.id,
            user_id=user["id"],
            used_at=datetime.now(timezone.utc),
        )
    )
    await get_session().execute(
        Coupon.__table__.update()
        .where(Coupon.id == coupon.id)
        .values(used_count=Coupon.used_count + 1)
    )
    await get_session().commit()
    
    return {"valid": True, "coupon": {"id": str(coupon.id), "code": coupon.code}}


@router.post("/list")
async def list_coupons(user=Depends(get_current_user)):
    """List all coupons (admin only)."""
    result = await get_session().execute(select(Coupon).order_by(Coupon.created_at.desc()))
    coupons = result.scalars().all()
    return {"coupons": [
        {"id": str(c.id), "code": c.code, "discount_type": c.discount_type, 
         "max_uses": c.max_uses, "used_count": c.used_count, "active": c.active}
        for c in coupons
    ]}


@router.post("/{coupon_id}/redeem")
async def redeem_coupon(coupon_id: str, user=Depends(get_current_user)):
    """Redeem a coupon for a user."""
    result = await get_session().execute(select(Coupon).where(Coupon.id == coupon_id))
    coupon = result.scalar_one_or_none()
    
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")
    
    if not coupon.active:
        raise HTTPException(status_code=400, detail="Coupon is no longer active")
    
    if coupon.used_count >= coupon.max_uses:
        raise HTTPException(status_code=400, detail="Coupon usage limit reached")
    
    if coupon.applicable_plans and user.get("plan", "") not in coupon.applicable_plans:
        raise HTTPException(status_code=400, detail="Coupon not applicable for your plan")
    
    # Record usage
    await get_session().execute(
        CouponUsage.__table__.insert().values(
            coupon_id=coupon.id,
            user_id=user["id"],
            used_at=datetime.now(timezone.utc),
        )
    )
    await get_session().execute(
        Coupon.__table__.update()
        .where(Coupon.id == coupon.id)
        .values(used_count=Coupon.used_count + 1)
    )
    await get_session().commit()
    
    return {"coupon_id": coupon_id, "status": "redeemed", "discount_applied": True}