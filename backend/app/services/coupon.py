from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any
from bson import ObjectId
from app.database import coupons_collection, users_collection, payments_collection
from app.config import get_settings

settings = get_settings()


async def create_coupon(
    code: str,
    discount_type: str,
    discount_value: float,
    max_uses: int = settings.COUPON_MAX_USES,
    expiry_date: Optional[datetime] = None,
    applicable_plans: Optional[list] = None,
    active: bool = True,
) -> dict:
    now = datetime.now(timezone.utc)
    expiry = expiry_date or now + timedelta(days=90)

    doc = {
        "code": code.upper().strip(),
        "discount_type": discount_type,
        "discount_value": discount_value,
        "max_uses": max_uses,
        "used_count": 0,
        "expiry_date": expiry,
        "applicable_plans": applicable_plans or ["pro", "team", "enterprise", "lifetime"],
        "active": active,
        "created_at": now,
    }
    result = await coupons_collection.insert_one(doc)
    return {"coupon_id": str(result.inserted_id), "code": doc["code"], "status": "created"}


async def validate_coupon(code: str, plan: str = "pro") -> Dict[str, Any]:
    coupon = await coupons_collection.find_one({"code": code.upper().strip()})

    if not coupon:
        return {"valid": False, "error": "Invalid coupon code"}

    if not coupon.get("active", True):
        return {"valid": False, "error": "Coupon is no longer active"}

    if coupon.get("used_count", 0) >= coupon.get("max_uses", settings.COUPON_MAX_USES):
        return {"valid": False, "error": "Coupon usage limit reached"}

    expiry = coupon.get("expiry_date")
    if expiry and expiry < datetime.now(timezone.utc):
        return {"valid": False, "error": "Coupon has expired"}

    applicable = coupon.get("applicable_plans", [])
    if applicable and plan not in applicable:
        return {"valid": False, "error": f"Coupon not applicable to {plan} plan"}

    return {
        "valid": True,
        "coupon_id": str(coupon["_id"]),
        "discount_type": coupon["discount_type"],
        "discount_value": coupon["discount_value"],
        "applicable_plans": applicable,
    }


async def apply_coupon(
    user_id: str,
    code: str,
    plan: str,
    amount: float,
    billing_cycle: str,
) -> Dict[str, Any]:
    validation = await validate_coupon(code, plan)
    if not validation["valid"]:
        return validation

    coupon = await coupons_collection.find_one({"code": code.upper().strip()})
    discount_value = coupon["discount_value"]
    discount_type = coupon["discount_type"]

    if discount_type == "percent":
        discount_amount = round(amount * (discount_value / 100), 2)
    elif discount_type == "fixed":
        discount_amount = min(discount_value, amount)
    else:
        discount_amount = 0.0

    final_amount = round(amount - discount_amount, 2)

    await coupons_collection.update_one(
        {"_id": coupon["_id"]},
        {"$inc": {"used_count": 1}},
    )

    await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"coupon_used": code.upper().strip(), "coupon_applied_at": datetime.now(timezone.utc)}},
    )

    return {
        "valid": True,
        "original_amount": amount,
        "discount_amount": discount_amount,
        "discount_type": discount_type,
        "discount_value": discount_value,
        "final_amount": final_amount,
        "coupon_code": code.upper().strip(),
    }


async def get_coupon_stats(coupon_id: str) -> Dict[str, Any]:
    coupon = await coupons_collection.find_one({"_id": ObjectId(coupon_id)})
    if not coupon:
        return {"error": "Coupon not found"}

    return {
        "code": coupon.get("code"),
        "discount_type": coupon.get("discount_type"),
        "discount_value": coupon.get("discount_value"),
        "used_count": coupon.get("used_count", 0),
        "max_uses": coupon.get("max_uses"),
        "active": coupon.get("active", True),
        "expiry_date": coupon.get("expiry_date"),
        "applicable_plans": coupon.get("applicable_plans", []),
    }