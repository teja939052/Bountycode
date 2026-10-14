import httpx
import json
import hashlib
import hmac
import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
from app.database import users_collection, processed_webhook_events_collection
from app.middleware.auth import get_current_user
from app.config import get_settings
from app.services.revenue import record_payment
from app.services.coupon import validate_coupon, apply_coupon as apply_coupon_service
from app.services.invoice import invoice_service
from bson import ObjectId
from datetime import datetime, timezone

router = APIRouter(prefix="/api/v1/billing", tags=["billing"])
settings = get_settings()
logger = logging.getLogger(__name__)

# Pricing ladder (yearly < 12x monthly):
#   monthly < yearly < lifetime
#   team/enterprise priced per seat/month with yearly ≈ 10x monthly.
PRICING = {
    "pro_monthly": {"INR": {"amount": "99.00", "currency": "INR"}, "USD": {"amount": "19.00", "currency": "USD"}},
    "lifetime": {"INR": {"amount": "1499.00", "currency": "INR"}, "USD": {"amount": "149.00", "currency": "USD"}},
    "pro_yearly": {"INR": {"amount": "899.00", "currency": "INR"}, "USD": {"amount": "99.00", "currency": "USD"}},
    "team": {"INR": {"amount": "12250.00", "currency": "INR"}, "USD": {"amount": "145.00", "currency": "USD"}},
    "team_yearly": {"INR": {"amount": "119900.00", "currency": "INR"}, "USD": {"amount": "1499.00", "currency": "USD"}},
    "enterprise_monthly": {"INR": {"amount": "66392.00", "currency": "INR"}, "USD": {"amount": "99.00", "currency": "USD"}},
    "enterprise_yearly": {"INR": {"amount": "663920.00", "currency": "INR"}, "USD": {"amount": "999.00", "currency": "USD"}},
}


class CheckoutRequest(BaseModel):
    country: str = "US"
    coupon_code: Optional[str] = None
    seats: int = 1


class CouponRequest(BaseModel):
    code: str


async def _record_processed_webhook(provider: str, event_id: str) -> bool:
    """Atomically mark a webhook event as processed.

    Returns True if this is the first time we've seen the event,
    False if it was already processed (idempotent duplicate).
    """
    if not event_id:
        return True
    doc = await processed_webhook_events_collection.find_one_and_update(
        {"provider": provider, "event_id": event_id},
        {"$setOnInsert": {
            "provider": provider,
            "event_id": event_id,
            "created_at": datetime.now(timezone.utc),
        }},
        upsert=True,
        return_document=False,
    )
    return doc is None


def _get_pricing(plan_key: str, country: str) -> dict:
    pricing = PRICING.get(plan_key)
    if not pricing:
        raise HTTPException(status_code=400, detail=f"Unknown plan: {plan_key}")
    return pricing["INR"] if country == "IN" else pricing["USD"]


def _require_verified_email(user: dict) -> None:
    """Money requires a verified email. Learning stays open to grow the funnel."""
    if not user.get("email_verified"):
        raise HTTPException(
            status_code=403,
            detail="Verify your email before checkout. Check your inbox for the verification link.",
        )


async def _create_razorpay_order(plan_key: str, seats: int, country: str, coupon_code: Optional[str], user: dict) -> dict:
    """Create a Razorpay order and persist pending state + payment row."""
    if not settings.RAZORPAY_KEY_ID or not settings.RAZORPAY_KEY_SECRET:
        raise HTTPException(status_code=500, detail="Razorpay not configured")

    price_key = _get_pricing(plan_key, country)
    final_amount = float(price_key["amount"]) * seats

    if coupon_code:
        base_plan = plan_key.replace("_monthly", "").replace("_yearly", "").replace("_lifetime", "")
        coupon_result = await apply_coupon_service(user["id"], coupon_code, base_plan, final_amount, "monthly")
        if coupon_result.get("valid"):
            final_amount = coupon_result["final_amount"]

    order_data = {
        "amount": int(final_amount * 100),
        "currency": price_key["currency"],
        "receipt": f"rc_{user['id']}_{plan_key}",
        "notes": {
            "user_id": str(user["id"]),
            "plan": plan_key,
            "seats": str(seats),
        },
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://api.razorpay.com/v1/orders",
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET),
            headers={"Content-Type": "application/json"},
            json=order_data,
        )
        resp.raise_for_status()
        order = resp.json()

    await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {
            "$set": {
                "razorpay_order_id": order["id"],
                "plan_pending": plan_key,
                "checkout_seats": seats,
                "checkout_billing_cycle": "yearly" if "yearly" in plan_key else "lifetime" if "lifetime" in plan_key else "monthly",
            },
        },
    )

    await record_payment(
        user_id=user["id"],
        amount=final_amount,
        currency=price_key["currency"],
        plan=plan_key.replace("_monthly", "").replace("_yearly", "").replace("_lifetime", ""),
        billing_cycle="yearly" if "yearly" in plan_key else "lifetime" if "lifetime" in plan_key else "monthly",
        payment_method="razorpay",
        payment_id=order["id"],
        status="pending",
        metadata={"seats": seats, "coupon_code": coupon_code},
    )

    return {
        "order_id": order["id"],
        "amount": order["amount"],
        "currency": order["currency"],
        "key_id": settings.RAZORPAY_KEY_ID,
    }


@router.post("/checkout")
async def create_checkout(request: Request, user=Depends(get_current_user)):
    _require_verified_email(user)
    body = await request.json() if request.headers.get("content-type", "").startswith("application/json") else {}
    checkout_req = CheckoutRequest(**body) if isinstance(body, dict) else CheckoutRequest()
    country = checkout_req.country.upper() if isinstance(body, dict) else "US"
    coupon_code = checkout_req.coupon_code if isinstance(body, dict) else None
    seats = checkout_req.seats if isinstance(body, dict) and checkout_req.seats > 0 else 1
    return await _create_razorpay_order("pro_monthly", seats, country, coupon_code, user)


@router.post("/checkout/lifetime")
async def create_lifetime_checkout(request: Request, user=Depends(get_current_user)):
    _require_verified_email(user)
    body = await request.json() if request.headers.get("content-type", "").startswith("application/json") else {}
    checkout_req = CheckoutRequest(**body) if isinstance(body, dict) else CheckoutRequest()
    country = checkout_req.country.upper() if isinstance(body, dict) else "US"
    coupon_code = checkout_req.coupon_code if isinstance(body, dict) else None
    return await _create_razorpay_order("lifetime", 1, country, coupon_code, user)


@router.post("/checkout/yearly")
async def create_yearly_checkout(request: Request, user=Depends(get_current_user)):
    _require_verified_email(user)
    body = await request.json() if request.headers.get("content-type", "").startswith("application/json") else {}
    checkout_req = CheckoutRequest(**body) if isinstance(body, dict) else CheckoutRequest()
    country = checkout_req.country.upper() if isinstance(body, dict) else "US"
    coupon_code = checkout_req.coupon_code if isinstance(body, dict) else None
    return await _create_razorpay_order("pro_yearly", 1, country, coupon_code, user)


@router.post("/checkout/team")
async def create_team_checkout(request: Request, user=Depends(get_current_user)):
    _require_verified_email(user)
    body = await request.json() if request.headers.get("content-type", "").startswith("application/json") else {}
    checkout_req = CheckoutRequest(**body) if isinstance(body, dict) else CheckoutRequest()
    country = checkout_req.country.upper() if isinstance(body, dict) else "US"
    coupon_code = checkout_req.coupon_code if isinstance(body, dict) else None
    seats = checkout_req.seats if isinstance(body, dict) and checkout_req.seats > 0 else 5
    if seats < 5:
        raise HTTPException(status_code=400, detail="Team plan requires minimum 5 seats")
    if seats > 50:
        raise HTTPException(status_code=400, detail="Team plan supports maximum 50 seats")
    is_yearly = body.get("billing_cycle", "monthly") == "yearly" if isinstance(body, dict) else False
    plan_key = "team_yearly" if is_yearly else "team"
    return await _create_razorpay_order(plan_key, seats, country, coupon_code, user)


@router.post("/checkout/enterprise")
async def create_enterprise_checkout(request: Request, user=Depends(get_current_user)):
    _require_verified_email(user)
    body = await request.json() if request.headers.get("content-type", "").startswith("application/json") else {}
    checkout_req = CheckoutRequest(**body) if isinstance(body, dict) else CheckoutRequest()
    country = checkout_req.country.upper() if isinstance(body, dict) else "US"
    coupon_code = checkout_req.coupon_code if isinstance(body, dict) else None
    seats = checkout_req.seats if isinstance(body, dict) and checkout_req.seats > 0 else 10
    if seats < 10:
        raise HTTPException(status_code=400, detail="Enterprise plan requires minimum 10 seats")
    is_yearly = body.get("billing_cycle", "monthly") == "yearly" if isinstance(body, dict) else False
    plan_key = "enterprise_yearly" if is_yearly else "enterprise_monthly"
    return await _create_razorpay_order(plan_key, seats, country, coupon_code, user)


@router.post("/coupon/validate")
async def validate_coupon_endpoint(req: CouponRequest):
    return await validate_coupon(req.code)


@router.post("/coupon/apply")
async def apply_coupon_endpoint(request: Request, user=Depends(get_current_user)):
    body = await request.json() if request.headers.get("content-type", "").startswith("application/json") else {}
    code = body.get("code", "")
    plan = body.get("plan", "pro")
    amount = float(body.get("amount", 0))
    billing_cycle = body.get("billing_cycle", "monthly")

    result = await apply_coupon_service(user["id"], code, plan, amount, billing_cycle)
    return result


@router.get("/status")
async def billing_status(user=Depends(get_current_user)):
    return {
        "plan": user.get("plan", "free"),
        "interviews_used": user.get("interviews_used", 0),
        "resumes_used": user.get("resumes_used", 0),
    }


@router.get("/invoices")
async def list_invoices(user=Depends(get_current_user)):
    """List the current user's invoices (metadata only)."""
    return {"invoices": await invoice_service.get_user_invoices(user["id"])}


@router.get("/invoices/{invoice_id}")
async def get_invoice(invoice_id: str, request: Request, user=Depends(get_current_user)):
    """Fetch a single invoice as JSON, or HTML with ?format=html."""
    invoice = await invoice_service.get_invoice(invoice_id)
    if not invoice or invoice.get("customer", {}).get("user_id") != str(user["id"]):
        raise HTTPException(status_code=404, detail="Invoice not found")
    if request.query_params.get("format") == "html":
        return HTMLResponse(content=invoice_service.generate_invoice_html(invoice))
    return invoice


# Single source of truth for prices. Frontend renders from this so prices can
# never drift from what Razorpay actually charges at checkout.
_PLAN_META = {
    "pro_monthly": {"id": "pro", "name": "Commander", "period": "/month", "desc": "Cancel anytime. Instant access."},
    "pro_yearly": {"id": "yearly", "name": "Strategist", "period": "/year", "desc": "Save vs monthly. Best value."},
    "lifetime": {"id": "lifetime", "name": "Admiral", "period": "one-time", "desc": "Pay once. Use forever."},
    "team": {"id": "team", "name": "Command Squad", "period": "/month per seat", "desc": "5–50 seats. Perfect for teams."},
    "enterprise_monthly": {"id": "enterprise", "name": "Executive Suite", "period": "/month per seat", "desc": "Unlimited seats. White-label. API access."},
}


@router.get("/plans")
async def get_plans():
    out = []
    for key, meta in _PLAN_META.items():
        pricing = PRICING.get(key, {})
        usd = pricing.get("USD", {})
        inr = pricing.get("INR", {})
        out.append({
            "id": meta["id"],
            "key": key,
            "name": meta["name"],
            "period": meta["period"],
            "desc": meta["desc"],
            "usd": usd.get("amount"),
            "inr": inr.get("amount"),
            "currency_usd": usd.get("currency"),
            "currency_inr": inr.get("currency"),
        })
    return {"plans": out, "seat_min": {"team": 5, "enterprise": 10}, "seat_max": {"team": 50}}


def _verify_razorpay_signature(body: bytes, headers: dict) -> bool:
    """Verify Razorpay webhook signature."""
    if not settings.RAZORPAY_WEBHOOK_SECRET:
        return False

    signature = headers.get("x-razorpay-signature", "")
    if not signature:
        return False

    secret = settings.RAZORPAY_WEBHOOK_SECRET.encode()
    computed = hmac.new(secret, body, hashlib.sha256).hexdigest()

    try:
        return hmac.compare_digest(signature, computed)
    except Exception as exc:
        logger.warning("Razorpay webhook signature compare failed: %s", exc)
        return False


@router.post("/webhook/razorpay")
async def razorpay_webhook(request: Request):
    """Handle Razorpay payment webhook events (UPI, cards, netbanking)."""
    body = await request.body()
    headers = dict(request.headers)

    if not _verify_razorpay_signature(body, headers):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")

    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    event_type = payload.get("event", "")

    if event_type == "payment.captured":
        payment = payload.get("payload", {}).get("payment", {}).get("entity", {})
        order_id = payment.get("order_id", "")
        notes = payment.get("notes", {})

        user_id = notes.get("user_id", "")
        plan_key = notes.get("plan", "pro")

        if not user_id or not ObjectId.is_valid(user_id):
            logger.warning("Razorpay webhook: payment.captured with missing/invalid user_id for order=%s", order_id)
            return {"status": "ok"}

        new_plan = "pro" if plan_key in ("pro_monthly",) else plan_key
        billing_cycle = "lifetime" if "lifetime" in plan_key else "yearly" if "yearly" in plan_key else "monthly"

        amount = float(payment.get("amount", 0)) / 100.0
        currency = payment.get("currency", "INR").upper()

        await users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "plan": new_plan,
                    "plan_updated_at": datetime.now(timezone.utc),
                },
                "$unset": {"razorpay_order_id": "", "plan_pending": ""},
            },
        )

        from app.services.trial import mark_trial_converted
        await mark_trial_converted(user_id)

        logger.info(
            "Razorpay webhook: user=%s upgraded to plan=%s order=%s amount=%s %s",
            user_id, new_plan, order_id, amount, currency,
        )

        await record_payment(
            user_id=user_id,
            amount=amount,
            currency=currency,
            plan=new_plan,
            billing_cycle=billing_cycle,
            payment_method="razorpay_webhook",
            payment_id=order_id,
            status="completed",
        )

        user = await users_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            try:
                await invoice_service.generate_invoice(
                    user=user,
                    plan=new_plan,
                    amount=amount,
                    currency=currency,
                    transaction_id=order_id,
                    billing_cycle="one-time" if "lifetime" in plan_key else billing_cycle,
                )
            except Exception as exc:
                # Invoice generation must never break the upgrade flow,
                # but the failure is revenue-visible: log it loudly.
                logger.error(
                    "Razorpay webhook: invoice generation failed for user=%s order=%s amount=%s %s: %s",
                    user_id, order_id, amount, currency, exc,
                )

    elif event_type == "payment.failed":
        payment = payload.get("payload", {}).get("payment", {}).get("entity", {})
        order_id = payment.get("order_id", "")
        notes = payment.get("notes", {})
        user_id = notes.get("user_id", "")

        if user_id and ObjectId.is_valid(user_id):
            await users_collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"plan": "free", "plan_pending": ""}},
            )

    return {"status": "ok"}
