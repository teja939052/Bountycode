"""Invoice generation — PostgreSQL-backed, no MongoDB."""

from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.middleware.auth import get_current_user
from app.services.invoice import InvoiceService
from app.services.email import send_email, limit_reached_email
from app.config import get_settings

router = APIRouter(prefix="/api/v1/invoices", tags=["invoices"])
invoice_service = InvoiceService()


class GenerateInvoiceRequest(BaseModel):
    plan: str
    amount: float
    currency: str = "USD"
    transaction_id: Optional[str] = None


@router.post("/generate")
async def generate_invoice(req: GenerateInvoiceRequest, user=Depends(get_current_user)):
    """Generate an invoice for a payment."""
    # Use the PostgreSQL-backed invoice service
    result = await invoice_service.generate_invoice(
        user_id=user["id"],
        plan=req.plan,
        amount=req.amount,
        currency=req.currency,
        transaction_id=req.transaction_id,
    )
    return result


@router.post("/usage/stats")
async def usage_stats_endpoint(user=Depends(get_current_user)):
    """Get user usage statistics for tier gating."""
    async with get_session() as session:
        from app.services.usage import get_usage_stats
        stats = await get_usage_stats(user["id"])
    return {"success": True, "data": stats}


@router.post("/plan/upgrade")
async def upgrade_plan(payload: dict, user=Depends(get_current_user)):
    """Handle plan upgrade (pro/lifetime)."""
    new_plan = payload.get("plan")
    if new_plan not in ("pro", "lifetime"):
        raise HTTPException(status_code=400, detail="Invalid plan")

    async with get_session() as session:
        from app.repositories.identity import UserRepository
        user_repo = UserRepository(session)
        user = await user_repo.get_by_id(user["id"])

        # Update plan
        await user_repo.update(user["id"], {"plan": new_plan})

        # Record revenue event
        await invoice_service.record_revenue_event(
            user_id=user["id"],
            event_type="plan_upgrade",
            amount=29.0 if new_plan == "pro" else 399.0,
            currency="USD",
            metadata={"plan": new_plan, "upgraded_from": user.plan},
        )

    return {"success": True, "new_plan": new_plan}