import httpx
import base64
from fastapi import APIRouter, Depends, HTTPException, Request
from app.database import users_collection
from app.middleware.auth import get_current_user
from app.config import get_settings
from bson import ObjectId
from datetime import datetime, timezone

router = APIRouter(prefix="/api/billing", tags=["billing"])
settings = get_settings()

FRONTEND_URL = settings.CORS_ORIGINS.split(",")[0].strip() if settings.CORS_ORIGINS else "http://localhost:5173"

PAYPAL_BASE = "https://api-m.sandbox.paypal.com" if settings.PAYPAL_MODE == "sandbox" else "https://api-m.paypal.com"

PRICING = {
    "pro_monthly": {"INR": {"amount": "99.00", "currency": "INR"}, "USD": {"amount": "19.00", "currency": "USD"}},
    "lifetime": {"INR": {"amount": "499.00", "currency": "INR"}, "USD": {"amount": "49.00", "currency": "USD"}},
    "pro_yearly": {"INR": {"amount": "499.00", "currency": "INR"}, "USD": {"amount": "49.00", "currency": "USD"}},
}


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


@router.post("/checkout")
async def create_checkout(request: Request, user=Depends(get_current_user)):
    if not settings.PAYPAL_CLIENT_ID:
        raise HTTPException(status_code=500, detail="PayPal not configured")

    body = await request.json() if request.headers.get("content-type", "").startswith("application/json") else {}
    country = body.get("country", "US").upper()
    price_key = PRICING["pro_monthly"]["INR"] if country == "IN" else PRICING["pro_monthly"]["USD"]

    access_token = await get_paypal_access_token()

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
                            "value": price_key["amount"],
                        },
                        "description": f"PlacementPro Pro Monthly ({price_key['currency']} {price_key['amount']})",
                        "custom_id": user["id"],
                    }
                ],
                "application_context": {
                    "return_url": f"{FRONTEND_URL}/dashboard?upgraded=true",
                    "cancel_url": f"{FRONTEND_URL}/pricing",
                },
            },
        )
        resp.raise_for_status()
        data = resp.json()

    approval_url = next(
        (link["href"] for link in data.get("links", []) if link.get("rel") == "approve"),
        None,
    )

    if not approval_url:
        raise HTTPException(status_code=500, detail="Failed to create PayPal order")

    await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {"$set": {"paypal_order_id": data["id"], "plan_pending": "pro"}},
    )

    return {"checkout_url": approval_url}


@router.post("/checkout/lifetime")
async def create_lifetime_checkout(request: Request, user=Depends(get_current_user)):
    if not settings.PAYPAL_CLIENT_ID:
        raise HTTPException(status_code=500, detail="PayPal not configured")

    body = await request.json() if request.headers.get("content-type", "").startswith("application/json") else {}
    country = body.get("country", "US").upper()
    price_key = PRICING["lifetime"]["INR"] if country == "IN" else PRICING["lifetime"]["USD"]

    access_token = await get_paypal_access_token()

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
                            "value": price_key["amount"],
                        },
                        "description": f"PlacementPro Lifetime ({price_key['currency']} {price_key['amount']})",
                        "custom_id": user["id"],
                    }
                ],
                "application_context": {
                    "return_url": f"{FRONTEND_URL}/dashboard?upgraded=true",
                    "cancel_url": f"{FRONTEND_URL}/pricing",
                },
            },
        )
        resp.raise_for_status()
        data = resp.json()

    approval_url = next(
        (link["href"] for link in data.get("links", []) if link.get("rel") == "approve"),
        None,
    )

    if not approval_url:
        raise HTTPException(status_code=500, detail="Failed to create PayPal order")

    await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {"$set": {"paypal_order_id": data["id"], "plan_pending": "lifetime"}},
    )

    return {"checkout_url": approval_url}


@router.post("/checkout/yearly")
async def create_yearly_checkout(request: Request, user=Depends(get_current_user)):
    if not settings.PAYPAL_CLIENT_ID:
        raise HTTPException(status_code=500, detail="PayPal not configured")

    body = await request.json() if request.headers.get("content-type", "").startswith("application/json") else {}
    country = body.get("country", "US").upper()
    price_key = PRICING["pro_yearly"]["INR"] if country == "IN" else PRICING["pro_yearly"]["USD"]

    access_token = await get_paypal_access_token()

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
                            "value": price_key["amount"],
                        },
                        "description": f"PlacementPro Pro Yearly ({price_key['currency']} {price_key['amount']})",
                        "custom_id": user["id"],
                    }
                ],
                "application_context": {
                    "return_url": f"{FRONTEND_URL}/dashboard?upgraded=true",
                    "cancel_url": f"{FRONTEND_URL}/pricing",
                },
            },
        )
        resp.raise_for_status()
        data = resp.json()

    approval_url = next(
        (link["href"] for link in data.get("links", []) if link.get("rel") == "approve"),
        None,
    )

    if not approval_url:
        raise HTTPException(status_code=500, detail="Failed to create PayPal order")

    await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {"$set": {"paypal_order_id": data["id"], "plan_pending": "pro_yearly"}},
    )

    return {"checkout_url": approval_url}


@router.post("/capture")
async def capture_paypal_order(request: Request, user=Depends(get_current_user)):
    if not settings.PAYPAL_CLIENT_ID:
        raise HTTPException(status_code=500, detail="PayPal not configured")

    body = await request.json()
    order_id = body.get("order_id")
    if not order_id:
        raise HTTPException(status_code=400, detail="Missing order_id")

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
        pending_plan = user.get("plan_pending", "pro")
        new_plan = "lifetime" if pending_plan == "lifetime" else "pro"

        await users_collection.update_one(
            {"_id": ObjectId(user["id"])},
            {
                "$set": {
                    "plan": new_plan,
                    "plan_updated_at": datetime.now(timezone.utc),
                },
                "$unset": {"paypal_order_id": "", "plan_pending": ""},
            },
        )
        return {"status": "success", "plan": new_plan}

    raise HTTPException(status_code=400, detail=f"Payment not completed: {data.get('status')}")


@router.post("/webhook")
async def paypal_webhook(request: Request):
    body = await request.json()
    event_type = body.get("event_type")

    if event_type == "PAYMENT.CAPTURE.COMPLETED":
        resource = body.get("resource", {})
        custom_id = resource.get("custom_id")
        amount = resource.get("amount", {}).get("value")
        currency = resource.get("amount", {}).get("currency_code", "USD")

        if custom_id:
            user = await users_collection.find_one({"_id": ObjectId(custom_id)})
            if user:
                if currency == "INR":
                    new_plan = "lifetime" if float(amount) >= 499 else "pro"
                else:
                    new_plan = "lifetime" if float(amount) >= 49 else "pro"
                await users_collection.update_one(
                    {"_id": ObjectId(custom_id)},
                    {"$set": {"plan": new_plan, "plan_updated_at": datetime.now(timezone.utc)}},
                )

    elif event_type == "PAYMENT.CAPTURE.DENIED":
        resource = body.get("resource", {})
        custom_id = resource.get("custom_id")
        if custom_id:
            await users_collection.update_one(
                {"_id": ObjectId(custom_id)},
                {"$set": {"plan": "free"}},
            )

    return {"status": "ok"}


@router.get("/status")
async def billing_status(user=Depends(get_current_user)):
    return {
        "plan": user.get("plan", "free"),
        "interviews_used": user.get("interviews_used", 0),
        "resumes_used": user.get("resumes_used", 0),
    }
