from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.middleware.auth import get_current_user
from app.services.coupon import create_coupon, validate_coupon, apply_coupon as apply_coupon_service

router = APIRouter(prefix="/api/v1/coupon", tags=["coupon"])


class CreateCouponRequest(BaseModel):
    code: str
    discount_type: str
    discount_value: float
    max_uses: Optional[int] = 1000
    expiry_days: Optional[int] = 90
    applicable_plans: Optional[list] = None


class ApplyCouponRequest(BaseModel):
    code: str
    plan: str
    amount: float
    billing_cycle: str


@router.post("/apply")
async def apply_coupon_endpoint(req: ApplyCouponRequest, user=Depends(get_current_user)):
    result = await apply_coupon_service(user["id"], req.code, req.plan, req.amount, req.billing_cycle)
    return result


@router.post("/admin/create")
async def create_coupon_admin(req: CreateCouponRequest, user=Depends(get_current_user)):
    result = await create_coupon(
        code=req.code,
        discount_type=req.discount_type,
        discount_value=req.discount_value,
        max_uses=req.max_uses,
        expiry_date=None,
        applicable_plans=req.applicable_plans,
        active=True,
    )
    return result


@router.get("/validate/{code}")
async def validate_coupon_endpoint(code: str, plan: str = "pro"):
    return await validate_coupon(code, plan)