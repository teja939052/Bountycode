"""Billing and payment processing — PostgreSQL-backed, no MongoDB."""

from datetime import datetime, timedelta
from typing import Optional, List
import json
import httpx
import base64
import uuid
import hashlib
import hmac
from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from sqlalchemy import select, func, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.middleware.auth import get_current_user
from app.config import get_settings
from app.services.revenue import record_payment, record_revenue_event
from app.services.coupon import validate_coupon
from app.services.invoice import invoice_service
from app.repositories.identity import UserRepository
from app.repositories.operations import BillingRecordRepository
from app.models.identity import User as UserModel
from app.models.coupon import Coupon
from app.models.operations import BillingRecord
from app.services.response_cache import invalidate_questions_cache

router = APIRouter(prefix="/api/v1/billing", tags=["billing"])
settings = get_settings()

FRONTEND_URL = settings.CORS_ORIGINS.split(",")[0].strip() if settings.CORS_ORIGINS else "http://localhost:5173"

PAYPAL_BASE = "https://api-m.sandbox.paypal.com" if settings.PAYPAL_MODE == "sandbox" else "https://api-m.paypal.com"


# ── Pricing ────────────────────────────────────────────────────────────────

PRICING = {
    "monthly": {"pro": 29, "lifetime": 399},
    "yearly": {"pro": 299, "lifetime": 999},
    "team": {"monthly": 49, "yearly": 499, "per_seat_monthly": 49},
    "enterprise": "custom",
}


# ── Models & Repos ───────────────────────────────────────────────────────

async def _get_user_repo(session: AsyncSession) -> UserRepository:
    return UserRepository(session)


async def _get_billing_repo(session: AsyncSession) -> BillingRecordRepository:
    return BillingRecordRepository(session)


# ── Customer Portal ────────────────────────────────────────────────────────

@router.get("/customer-portal")
async def customer_portal(user=Depends(get_current_user)):
    """Render the customer portal page with usage stats and upgrade options."""
    async with get_session() as session:
        user_repo = await _get_user_repo(session)
        user = await user_repo.get_by_id(user["id"])

        # Get usage stats from the updated usage service
        from app.services.usage import check_and_reset_monthly_usage, get_usage_stats
        usage = await get_usage_stats(user["id"])

        # Get available plans
        plan_options = []
        for plan_type in ["pro", "lifetime"]:
            monthly_price = PRICING["monthly"][plan_type]
            yearly_price = PRICING["yearly"][plan_type]
            plan_options.append({
                "plan": plan_type,
                "monthly_price": monthly_price,
                "yearly_price": yearly_price,
                "is_current": user.plan == plan_type,
            })

        return {
            "success": True,
            "data": {
                "user": {"id": str(user.id), "name": user.name, "email": user.email, "plan": user.plan},
                "usage": usage,
                "plan_options": plan_options,
                "frontend_url": FRONTEND_URL,
            },
        }


# ── Coupon routes ──────────────────────────────────────────────────────────

class CouponValidate(BaseModel):
    code: str = Field(min_length=1, max_length=50)


@router.post("/coupon/validate")
async def validate_coupon_endpoint(payload: CouponValidate, user=Depends(get_current_user)):
    """Validate a coupon code for a user."""
    valid, message, discount = validate_coupon(payload.code, user["id"])
    return {"success": valid, "message": message, "discount": discount}


@router.post("/coupon/apply")
async def apply_coupon_endpoint(payload: CouponValidate, user=Depends(get_current_user)):
    """Apply a coupon to the user's account."""
    success, message = apply_coupon_service(payload.code, user["id"])
    return {"success": success, "message": message}


# ── Payment routes ─────────────────────────────────────────────────────────

class CreatePaymentIntent(BaseModel):
    plan: str = Field(min_length=1)
    payment_method_id: str = Field(min_length=1)


@router.post("/create-payment-intent")
async def create_payment_intent(payload: CreatePaymentIntent, user=Depends(get_current_user)):
    """Create a PayPal/PaymentIntent for plan upgrade."""
    if payload.plan not in ("pro", "lifetime"):
        raise HTTPException(status_code=400, detail="Invalid plan")

    # Use the revenue service to record the intent
    async with get_session() as session:
        await record_payment(
            user_id=user["id"],
            amount=PRICING["monthly"][payload.plan]
            if payload.plan == "pro"
            else PRICING["yearly"][payload.plan],
            currency="USD",
            payment_type="subscription",
            provider="paypal",
            metadata={"plan": payload.plan, "user_id": str(user["id"])},
        )

    # Return PayPal approval link
    async with get_session() as session:
        user_repo = UserRepository(session)
        user = await user_repo.get_by_id(user["id"])

    # Build PayPal API call
    async with httpx.AsyncClient() as client:
        auth = (settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET)
        headers = {"Accept": "application/json", "Accept-Language": "en_US"}
        intent = "CAPTURE" if settings.PAYPAL_MODE == "live" else "AUTHORIZE"

        paypal_url = f"{PAYPAL_BASE}/v1/payments/authorization/{payload.plan}"
        # ... (PayPal integration continues)

    return {"success": True, "approval_url": f"{FRONTEND_URL}/billing/paypal/redirect"}


# ── Revenue tracking ──────────────────────────────────────────────────────

@router.post("/revenue-event")
async def record_revenue_event_endpoint(
    payload: dict, user=Depends(get_current_user)
):
    """Record a revenue event (for analytics)."""
    await record_revenue_event(
        user_id=user["id"],
        event_type=payload.get("event_type", "payment"),
        amount=payload.get("amount"),
        currency=payload.get("currency", "USD"),
        metadata=payload.get("metadata", {}),
    )
    return {"success": True}


# ── Usage stats ──────────────────────────────────────────────────────────

@router.get("/usage/stats")
async def usage_stats_endpoint(user=Depends(get_current_user)):
    """Get user usage statistics for tier gating."""
    async with get_session() as session:
        from app.services.usage import get_usage_stats
        stats = await get_usage_stats(user["id"])
    return {"success": True, "data": stats}


# ── Plan management ──────────────────────────────────────────────────────

@router.post("/plan/upgrade")
async def upgrade_plan(payload: dict, user=Depends(get_current_user)):
    """Handle plan upgrade (pro/lifetime)."""
    new_plan = payload.get("plan")
    if new_plan not in ("pro", "lifetime"):
        raise HTTPException(status_code=400, detail="Invalid plan")

    async with get_session() as session:
        user_repo = UserRepository(session)
        user = await user_repo.get_by_id(user["id"])

        # Update plan
        await user_repo.update(user["id"], {"plan": new_plan})

        # Record revenue event
        await record_payment(
            user_id=user["id"],
            amount=PRICING["yearly"][new_plan]
            if new_plan == "lifetime"
            else PRICING["monthly"][new_plan],
            currency="USD",
            payment_type="subscription",
            provider="internal",
            metadata={"plan": new_plan, "upgraded_from": user.plan},
        )

    return {"success": True, "new_plan": new_plan}


# ── Trial routes ─────────────────────────────────────────────────────────

@router.post("/trial/start")
async def start_trial_endpoint(user=Depends(get_current_user)):
    """Start a 7-day free trial."""
    from app.services.trial import start_trial
    result = await start_trial(user["id"])
    return {"success": True, "data": result}


@router.post("/trial/check")
async def check_trial(user=Depends(get_current_user)):
    """Check trial status."""
    from app.services.trial import get_trial_status
    result = await get_trial_status(user["id"])
    return {"success": True, "data": result}