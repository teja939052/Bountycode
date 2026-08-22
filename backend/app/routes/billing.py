import httpx
import base64
import uuid
import json
import hashlib
import hmac
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, List
from app.database import users_collection, payments_collection, coupons_collection
from app.middleware.auth import get_current_user
from app.config import get_settings
from app.services.revenue import record_payment, record_revenue_event
from app.services.coupon import validate_coupon, apply_coupon as apply_coupon_service
from bson import ObjectId
from datetime import datetime, timezone

router = APIRouter(prefix="/api/v1/billing", tags=["billing"])
settings = get_settings()

FRONTEND_URL = settings.CORS_ORIGINS.split(",")[0].strip() if settings.CORS_ORIGINS else "http://localhost:5173"

PAYPAL_BASE = "https://api-m.sandbox.paypal.com" if settings.PAYPAL_MODE == "sandbox" else "https://api-m.paypal.com"

# Pricing ladder (recurring must always be < lifetime, and yearly < 12x monthly):
#   monthly < yearly(≈5-6x monthly) < lifetime(≈8-12x monthly)
#   team/enterprise priced per seat/month with yearly ≈ 10x monthly.
PRICING = {
    "pro_monthly": {"INR": {"amount": "99.00", "currency": "INR"}, "USD": {"amount": "19.00", "currency": "USD"}},
    "lifetime": {"INR": {"amount": "1499.00", "currency": "INR"}, "USD": {"amount": "149.00", "currency": "USD"}},
    "pro_yearly": {"INR": {"amount": "499.00", "currency": "INR"}, "USD": {"amount": "99.00", "currency": "USD"}},
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


class StripeCheckoutRequest(BaseModel):
    country: str = "US"
    coupon_code: Optional[str] = None
    seats: int = 1


async def get_paypal_access_token() -> str:
    credentials = base64.b64encode(
        f"{settings.PAYPAL_CLIENT_ID}:{settings.PAYPAL_CLIENT_SECRET}".encode()
    ).decode()

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{PAYPAL_BASE}/v1/oauth2/token",
            headers={
                "Authorization": f"Basic {credentials}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={"grant_type": "client_credentials"},
        )
        resp.raise_for_status()
        return resp.json()["access_token"]


def _get_pricing(plan_key: str, country: str) -> dict:
    pricing = PRICING.get(plan_key)
    if not pricing:
        raise HTTPException(status_code=400, detail=f"Unknown plan: {plan_key}")
    return pricing["INR"] if country == "IN" else pricing["USD"]


async def _create_paypal_order(access_token: str, price_key: dict, final_amount: float, description: str, custom_id: str, seats: int = 1) -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{PAYPAL_BASE}/v2/checkout/orders",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
            json={
                "intent": "CAPTURE",
                "purchase_units": [
                    {
                        "amount": {
                            "currency_code": price_key["currency"],
                            "value": f"{final_amount:.2f}",
                        },
                        "description": description,
                        "custom_id": custom_id,
                    }
                ],
                "application_context": {
                    "return_url": f"{FRONTEND_URL}/dashboard?upgraded=true",
                    "cancel_url": f"{FRONTEND_URL}/pricing",
                },
            },
        )
        resp.raise_for_status()
        return resp.json()


def _verify_paypal_webhook_signature(body: bytes, headers: dict) -> bool:
    if not settings.PAYPAL_WEBHOOK_ID or not settings.PAYPAL_CLIENT_SECRET:
        return False
    transmission_id = headers.get("paypal-transmission-id", "")
    transmission_time = headers.get("paypal-transmission-time", "")
    webhook_id = settings.PAYPAL_WEBHOOK_ID

    expected_sig = hmac.new(
        settings.PAYPAL_CLIENT_SECRET.encode(),
        f"{transmission_id}|{transmission_time}|{webhook_id}|{body.decode()}".encode(),
        hashlib.sha256,
    ).hexdigest()

    transmission_sig = headers.get("paypal-transmission-sig", "")
    return hmac.compare_digest(expected_sig, transmission_sig)


@router.post("/checkout")
async def create_checkout(request: Request, user=Depends(get_current_user)):
    if not settings.PAYPAL_CLIENT_ID:
        raise HTTPException(status_code=500, detail="PayPal not configured")

    body = await request.json() if request.headers.get("content-type", "").startswith("application/json") else {}
    checkout_req = CheckoutRequest(**body) if isinstance(body, dict) else CheckoutRequest()
    country = checkout_req.country.upper() if isinstance(body, dict) else "US"
    coupon_code = checkout_req.coupon_code if isinstance(body, dict) else None
    seats = checkout_req.seats if isinstance(body, dict) and checkout_req.seats > 0 else 1

    price_key = _get_pricing("pro_monthly", country)
    final_amount = float(price_key["amount"]) * seats

    if coupon_code:
        coupon_result = await apply_coupon_service(user["id"], coupon_code, "pro", final_amount, "monthly")
        if coupon_result.get("valid"):
            final_amount = coupon_result["final_amount"]

    access_token = await get_paypal_access_token()
    data = await _create_paypal_order(
        access_token, price_key, final_amount,
        f"PlacementPro Pro Monthly x{seats} ({price_key['currency']} {price_key['amount']}/seat)",
        user["id"], seats
    )

    approval_url = next(
        (link["href"] for link in data.get("links", []) if link.get("rel") == "approve"),
        None,
    )

    if not approval_url:
        raise HTTPException(status_code=500, detail="Failed to create PayPal order")

    await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {
            "$set": {
                "paypal_order_id": data["id"],
                "plan_pending": "pro",
                "checkout_seats": seats,
            }
        },
    )

    await record_payment(
        user_id=user["id"],
        amount=final_amount,
        currency=price_key["currency"],
        plan="pro",
        billing_cycle="monthly",
        payment_method="paypal",
        payment_id=data["id"],
        status="pending",
        metadata={"seats": seats, "coupon_code": coupon_code},
    )

    return {"checkout_url": approval_url, "order_id": f"PO-{uuid.uuid4().hex[:12].upper()}", "amount": final_amount}


@router.post("/checkout/lifetime")
async def create_lifetime_checkout(request: Request, user=Depends(get_current_user)):
    if not settings.PAYPAL_CLIENT_ID:
        raise HTTPException(status_code=500, detail="PayPal not configured")

    body = await request.json() if request.headers.get("content-type", "").startswith("application/json") else {}
    checkout_req = CheckoutRequest(**body) if isinstance(body, dict) else CheckoutRequest()
    country = checkout_req.country.upper() if isinstance(body, dict) else "US"
    coupon_code = checkout_req.coupon_code if isinstance(body, dict) else None

    price_key = _get_pricing("lifetime", country)
    final_amount = float(price_key["amount"])

    if coupon_code:
        coupon_result = await apply_coupon_service(user["id"], coupon_code, "lifetime", final_amount, "lifetime")
        if coupon_result.get("valid"):
            final_amount = coupon_result["final_amount"]

    access_token = await get_paypal_access_token()
    data = await _create_paypal_order(
        access_token, price_key, final_amount,
        f"PlacementPro Lifetime ({price_key['currency']} {price_key['amount']})",
        user["id"]
    )

    approval_url = next(
        (link["href"] for link in data.get("links", []) if link.get("rel") == "approve"),
        None,
    )

    if not approval_url:
        raise HTTPException(status_code=500, detail="Failed to create PayPal order")

    await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {
            "$set": {
                "paypal_order_id": data["id"],
                "plan_pending": "lifetime",
            }
        },
    )

    await record_payment(
        user_id=user["id"],
        amount=final_amount,
        currency=price_key["currency"],
        plan="lifetime",
        billing_cycle="lifetime",
        payment_method="paypal",
        payment_id=data["id"],
        status="pending",
        metadata={"coupon_code": coupon_code},
    )

    return {"checkout_url": approval_url, "amount": final_amount}


@router.post("/checkout/yearly")
async def create_yearly_checkout(request: Request, user=Depends(get_current_user)):
    if not settings.PAYPAL_CLIENT_ID:
        raise HTTPException(status_code=500, detail="PayPal not configured")

    body = await request.json() if request.headers.get("content-type", "").startswith("application/json") else {}
    checkout_req = CheckoutRequest(**body) if isinstance(body, dict) else CheckoutRequest()
    country = checkout_req.country.upper() if isinstance(body, dict) else "US"
    coupon_code = checkout_req.coupon_code if isinstance(body, dict) else None

    price_key = _get_pricing("pro_yearly", country)
    final_amount = float(price_key["amount"])

    if coupon_code:
        coupon_result = await apply_coupon_service(user["id"], coupon_code, "pro", final_amount, "yearly")
        if coupon_result.get("valid"):
            final_amount = coupon_result["final_amount"]

    access_token = await get_paypal_access_token()
    data = await _create_paypal_order(
        access_token, price_key, final_amount,
        f"PlacementPro Pro Yearly ({price_key['currency']} {price_key['amount']})",
        user["id"]
    )

    approval_url = next(
        (link["href"] for link in data.get("links", []) if link.get("rel") == "approve"),
        None,
    )

    if not approval_url:
        raise HTTPException(status_code=500, detail="Failed to create PayPal order")

    await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {
            "$set": {
                "paypal_order_id": data["id"],
                "plan_pending": "pro_yearly",
            }
        },
    )

    await record_payment(
        user_id=user["id"],
        amount=final_amount,
        currency=price_key["currency"],
        plan="pro",
        billing_cycle="yearly",
        payment_method="paypal",
        payment_id=data["id"],
        status="pending",
        metadata={"coupon_code": coupon_code},
    )

    return {"checkout_url": approval_url, "amount": final_amount}


@router.post("/checkout/team")
async def create_team_checkout(request: Request, user=Depends(get_current_user)):
    if not settings.PAYPAL_CLIENT_ID:
        raise HTTPException(status_code=500, detail="PayPal not configured")

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

    if is_yearly:
        price_key = _get_pricing("team_yearly", country)
    else:
        price_key = _get_pricing("team", country)

    final_amount = float(price_key["amount"]) * seats

    if coupon_code:
        coupon_result = await apply_coupon_service(user["id"], coupon_code, "team", final_amount, "monthly")
        if coupon_result.get("valid"):
            final_amount = coupon_result["final_amount"]

    access_token = await get_paypal_access_token()
    data = await _create_paypal_order(
        access_token, price_key, final_amount,
        f"PlacementPro Team ({seats} seats, {price_key['currency']} {price_key['amount']}/seat/mo)",
        user["id"], seats
    )

    approval_url = next(
        (link["href"] for link in data.get("links", []) if link.get("rel") == "approve"),
        None,
    )

    if not approval_url:
        raise HTTPException(status_code=500, detail="Failed to create PayPal order")

    await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {
            "$set": {
                "paypal_order_id": data["id"],
                "plan_pending": "team",
                "checkout_seats": seats,
                "checkout_billing_cycle": "yearly" if is_yearly else "monthly",
            }
        },
    )

    await record_payment(
        user_id=user["id"],
        amount=final_amount,
        currency=price_key["currency"],
        plan="team",
        billing_cycle="yearly" if is_yearly else "monthly",
        payment_method="paypal",
        payment_id=data["id"],
        status="pending",
        metadata={"seats": seats, "coupon_code": coupon_code},
    )

    return {"checkout_url": approval_url, "amount": final_amount, "seats": seats}


@router.post("/checkout/enterprise")
async def create_enterprise_checkout(request: Request, user=Depends(get_current_user)):
    if not settings.PAYPAL_CLIENT_ID:
        raise HTTPException(status_code=500, detail="PayPal not configured")

    body = await request.json() if request.headers.get("content-type", "").startswith("application/json") else {}
    checkout_req = CheckoutRequest(**body) if isinstance(body, dict) else CheckoutRequest()
    country = checkout_req.country.upper() if isinstance(body, dict) else "US"
    coupon_code = checkout_req.coupon_code if isinstance(body, dict) else None
    seats = checkout_req.seats if isinstance(body, dict) and checkout_req.seats > 0 else 10

    if seats < 10:
        raise HTTPException(status_code=400, detail="Enterprise plan requires minimum 10 seats")

    is_yearly = body.get("billing_cycle", "monthly") == "yearly" if isinstance(body, dict) else False

    if is_yearly:
        price_key = _get_pricing("enterprise_yearly", country)
    else:
        price_key = _get_pricing("enterprise_monthly", country)

    final_amount = float(price_key["amount"]) * seats

    if coupon_code:
        coupon_result = await apply_coupon_service(user["id"], coupon_code, "enterprise", final_amount, "monthly")
        if coupon_result.get("valid"):
            final_amount = coupon_result["final_amount"]

    access_token = await get_paypal_access_token()
    data = await _create_paypal_order(
        access_token, price_key, final_amount,
        f"PlacementPro Enterprise ({seats} seats, {price_key['currency']} {price_key['amount']}/seat/mo)",
        user["id"], seats
    )

    approval_url = next(
        (link["href"] for link in data.get("links", []) if link.get("rel") == "approve"),
        None,
    )

    if not approval_url:
        raise HTTPException(status_code=500, detail="Failed to create PayPal order")

    await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {
            "$set": {
                "paypal_order_id": data["id"],
                "plan_pending": "enterprise",
                "checkout_seats": seats,
                "checkout_billing_cycle": "yearly" if is_yearly else "monthly",
            }
        },
    )

    await record_payment(
        user_id=user["id"],
        amount=final_amount,
        currency=price_key["currency"],
        plan="enterprise",
        billing_cycle="yearly" if is_yearly else "monthly",
        payment_method="paypal",
        payment_id=data["id"],
        status="pending",
        metadata={"seats": seats, "coupon_code": coupon_code},
    )

    return {"checkout_url": approval_url, "amount": final_amount, "seats": seats}


@router.post("/checkout/stripe")
async def create_stripe_checkout(request: Request, user=Depends(get_current_user)):
    if not settings.STRIPE_SECRET_KEY:
        raise HTTPException(status_code=500, detail="Stripe not configured")

    body = await request.json() if request.headers.get("content-type", "").startswith("application/json") else {}
    checkout_req = StripeCheckoutRequest(**body) if isinstance(body, dict) else StripeCheckoutRequest()
    plan = body.get("plan", "pro_monthly") if isinstance(body, dict) else "pro_monthly"
    country = checkout_req.country.upper() if isinstance(body, dict) else "US"
    seats = checkout_req.seats if isinstance(body, dict) and checkout_req.seats > 0 else 1
    coupon_code = checkout_req.coupon_code if isinstance(body, dict) else None

    price_key = _get_pricing(f"{plan}", country)

    import stripe
    stripe.api_key = settings.STRIPE_SECRET_KEY

    line_items = [
        {
            "price_data": {
                "currency": price_key["currency"].lower(),
                "unit_amount": int(float(price_key["amount"]) * 100),
                "product_data": {
                    "name": f"PlacementPro {plan}",
                    "description": f"Plan: {plan}, Seats: {seats}",
                },
            },
            "quantity": seats,
        }
    ]

    session_data = {
        "payment_method_types": ["card", "paypal", "blik"],
        "line_items": line_items,
        "mode": "payment",
        "success_url": f"{FRONTEND_URL}/dashboard?upgraded=true",
        "cancel_url": f"{FRONTEND_URL}/pricing",
        "metadata": {
            "user_id": user["id"],
            "plan": plan,
            "seats": str(seats),
            "coupon_code": coupon_code or "",
        },
    }

    session = stripe.checkout.Session.create(**session_data)

    await record_payment(
        user_id=user["id"],
        amount=float(price_key["amount"]) * seats,
        currency=price_key["currency"],
        plan=plan,
        billing_cycle="monthly",
        payment_method="stripe",
        payment_id=session.id,
        status="pending",
        metadata={"seats": seats, "coupon_code": coupon_code},
    )

    return {"checkout_url": session.url, "session_id": session.id}


@router.post("/capture")
async def capture_paypal_order(request: Request, user=Depends(get_current_user)):
    if not settings.PAYPAL_CLIENT_ID:
        raise HTTPException(status_code=500, detail="PayPal not configured")

    body = await request.json()
    order_id = body.get("order_id")
    if not order_id:
        raise HTTPException(status_code=400, detail="Missing order_id")

    pending_plan = user.get("plan_pending", "pro")
    new_plan = "lifetime" if pending_plan == "lifetime" else ("pro_yearly" if pending_plan == "pro_yearly" else pending_plan if pending_plan in ("team", "enterprise") else "pro")

    access_token = await get_paypal_access_token()

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{PAYPAL_BASE}/v2/checkout/orders/{order_id}/capture",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
        )
        resp.raise_for_status()
        data = resp.json()

    if data.get("status") == "COMPLETED":
        await users_collection.update_one(
            {"_id": ObjectId(user["id"])},
            {
                "$set": {
                    "plan": new_plan,
                    "plan_updated_at": datetime.now(timezone.utc),
                },
                "$unset": {"paypal_order_id": "", "plan_pending": "", "checkout_seats": "", "checkout_billing_cycle": ""},
            },
        )

        payment_docs = await payments_collection.find(
            {"payment_id": order_id, "user_id": user["id"]}
        ).to_list(length=1)
        if payment_docs:
            await payments_collection.update_one(
                {"_id": payment_docs[0]["_id"]},
                {"$set": {"status": "completed", "captured_at": datetime.now(timezone.utc)}},
            )

        return {"status": "success", "plan": new_plan}

    raise HTTPException(status_code=400, detail=f"Payment not completed: {data.get('status')}")


@router.post("/webhook")
async def paypal_webhook(request: Request):
    body = await request.body()
    headers = dict(request.headers)

    if not _verify_paypal_webhook_signature(body, headers):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")

    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    event_type = payload.get("event_type")

    if event_type == "PAYMENT.CAPTURE.COMPLETED":
        resource = payload.get("resource", {})
        custom_id = resource.get("custom_id")
        amount = resource.get("amount", {}).get("value")
        currency = resource.get("amount", {}).get("currency_code", "USD")

        if custom_id:
            if not ObjectId.is_valid(custom_id):
                return {"status": "ok"}
            user = await users_collection.find_one({"_id": ObjectId(custom_id)})
            if user:
                pending = user.get("plan_pending")
                if pending == "lifetime":
                    new_plan = "lifetime"
                elif pending == "pro_yearly":
                    new_plan = "pro_yearly"
                elif pending in ("team", "enterprise"):
                    new_plan = pending
                else:
                    new_plan = "pro"
                await users_collection.update_one(
                    {"_id": ObjectId(custom_id)},
                    {
                        "$set": {"plan": new_plan, "plan_updated_at": datetime.now(timezone.utc)},
                        "$unset": {"plan_pending": "", "paypal_order_id": "", "checkout_seats": "", "checkout_billing_cycle": ""},
                    },
                )
                from app.services.trial import mark_trial_converted
                await mark_trial_converted(custom_id)
                try:
                    paid_amount = float(amount)
                except (TypeError, ValueError):
                    paid_amount = 0.0
                await record_payment(
                    user_id=custom_id,
                    amount=paid_amount,
                    currency=currency,
                    plan=new_plan,
                    billing_cycle="monthly",
                    payment_method="paypal_webhook",
                    payment_id=f"wh-{custom_id}",
                    status="completed",
                )

    elif event_type == "PAYMENT.CAPTURE.DENIED":
        resource = payload.get("resource", {})
        custom_id = resource.get("custom_id")
        if custom_id and ObjectId.is_valid(custom_id):
            await users_collection.update_one(
                {"_id": ObjectId(custom_id)},
                {"$set": {"plan": "free"}},
            )

    return {"status": "ok"}


@router.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    if not settings.STRIPE_SECRET_KEY:
        raise HTTPException(status_code=500, detail="Stripe not configured")

    body = await request.body()
    sig_header = request.headers.get("stripe-signature", "")

    try:
        import stripe
        stripe.api_key = settings.STRIPE_SECRET_KEY
        event = stripe.Webhook.construct_event(
            body, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ImportError:
        raise HTTPException(status_code=500, detail="Stripe SDK not installed")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Webhook verification failed: {str(e)}")

    event_type = event.get("type")
    session = event.get("data", {}).get("object", {})

    if event_type == "checkout.session.completed":
        metadata = session.get("metadata", {})
        user_id = metadata.get("user_id")
        plan = metadata.get("plan", "pro")
        amount = session.get("amount_total", 0) / 100.0
        currency = session.get("currency", "USD").upper()

        if user_id:
            new_plan = "enterprise" if "enterprise" in plan else "team" if "team" in plan else "pro"
            billing_cycle = "yearly" if "yearly" in plan else "monthly"
            await users_collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"plan": new_plan, "plan_updated_at": datetime.now(timezone.utc)}},
            )
            from app.services.trial import mark_trial_converted
            await mark_trial_converted(user_id)
            await record_payment(
                user_id=user_id,
                amount=amount,
                currency=currency,
                plan=new_plan,
                billing_cycle=billing_cycle,
                payment_method="stripe",
                payment_id=session.get("id"),
                status="completed",
            )

    return {"status": "ok"}


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


# Single source of truth for prices. Frontend renders from this so prices can
# never drift from what PayPal/Stripe actually charges at checkout.
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
