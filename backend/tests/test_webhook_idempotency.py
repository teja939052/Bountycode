"""Tests for webhook idempotency and concurrency safety."""

import pytest
import asyncio
import json
from datetime import datetime, timezone
from bson import ObjectId
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import users_collection, processed_webhook_events_collection
from app.routes.billing import _record_processed_webhook
from app.config import get_settings

settings = get_settings()


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest.fixture
async def clean_db():
    await users_collection().delete_many({"email": "webhook_test@example.com"})
    await processed_webhook_events_collection.delete_many({"provider": {"$in": ["stripe", "paypal"]}})
    yield
    await users_collection().delete_many({"email": "webhook_test@example.com"})
    await processed_webhook_events_collection.delete_many({"provider": {"$in": ["stripe", "paypal"]}})


@pytest.mark.asyncio
async def test_stripe_webhook_idempotency_duplicate_event(client, clean_db):
    """Same Stripe event sent twice must not create duplicate plan changes."""
    if not settings.STRIPE_SECRET_KEY:
        pytest.skip("Stripe not configured")

    user_id = None
    email = "webhook_test@example.com"
    await users_collection().insert_one({
        "email": email,
        "name": "Webhook Test",
        "password_hash": "fake",
        "plan": "free",
        "created_at": datetime.now(timezone.utc),
    })
    user = await users_collection().find_one({"email": email})
    user_id = str(user["_id"])

    event_id = "evt_test_duplicate_123"
    payload = {
        "id": event_id,
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "id": "cs_test_123",
                "metadata": {"user_id": user_id, "plan": "pro"},
                "amount_total": 1900,
                "currency": "USD",
            }
        },
    }

    headers = {"stripe-signature": "fake_sig"}

    # First request
    r1 = await client.post("/api/v1/billing/webhook/stripe", json=payload, headers=headers)
    assert r1.status_code == 200

    # Second request (duplicate)
    r2 = await client.post("/api/v1/billing/webhook/stripe", json=payload, headers=headers)
    assert r2.status_code == 200

    doc = await users_collection().find_one({"_id": ObjectId(user_id)})
    assert doc["plan"] == "pro"

    processed = await processed_webhook_events_collection.count_documents({"provider": "stripe", "event_id": event_id})
    assert processed == 1


@pytest.mark.asyncio
async def test_stripe_webhook_concurrent_duplicates(client, clean_db):
    """Concurrent duplicate webhooks must not race into double processing."""
    if not settings.STRIPE_SECRET_KEY:
        pytest.skip("Stripe not configured")

    user_id = None
    email = "webhook_concurrent@example.com"
    await users_collection().insert_one({
        "email": email,
        "name": "Concurrent Test",
        "password_hash": "fake",
        "plan": "free",
        "created_at": datetime.now(timezone.utc),
    })
    user = await users_collection().find_one({"email": email})
    user_id = str(user["_id"])

    event_id = "evt_test_concurrent_456"
    payload = {
        "id": event_id,
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "id": "cs_test_456",
                "metadata": {"user_id": user_id, "plan": "pro"},
                "amount_total": 1900,
                "currency": "USD",
            }
        },
    }
    headers = {"stripe-signature": "fake_sig"}

    async def send_webhook():
        return await client.post("/api/v1/billing/webhook/stripe", json=payload, headers=headers)

    responses = await asyncio.gather(*[send_webhook() for _ in range(5)])
    for resp in responses:
        assert resp.status_code == 200

    doc = await users_collection().find_one({"_id": ObjectId(user_id)})
    assert doc["plan"] == "pro"

    processed = await processed_webhook_events_collection.count_documents({"provider": "stripe", "event_id": event_id})
    assert processed == 1


@pytest.mark.asyncio
async def test_paypal_webhook_idempotency(client, clean_db):
    """Duplicate PayPal webhook events must not double-apply plan changes."""
    user_id = None
    email = "paypal_webhook_test@example.com"
    await users_collection().insert_one({
        "email": email,
        "name": "PayPal Test",
        "password_hash": "fake",
        "plan": "free",
        "created_at": datetime.now(timezone.utc),
    })
    user = await users_collection().find_one({"email": email})
    user_id = str(user["_id"])

    event_id = "wh_paypal_duplicate_789"
    payload = {
        "id": event_id,
        "event_type": "PAYMENT.CAPTURE.COMPLETED",
        "resource": {
            "custom_id": user_id,
            "amount": {"value": "19.00", "currency_code": "USD"},
        },
    }

    # Patch signature verification so the test doesn't depend on PayPal secrets
    import app.routes.billing as billing_module
    original_verify = billing_module._verify_paypal_webhook_signature
    billing_module._verify_paypal_webhook_signature = lambda body, headers: True
    try:
        # First request
        r1 = await client.post("/api/v1/billing/webhook", json=payload)
        assert r1.status_code == 200, f"First webhook failed: {r1.status_code} {r1.text}"

        # Second request (duplicate)
        r2 = await client.post("/api/v1/billing/webhook", json=payload)
        assert r2.status_code == 200, f"Duplicate webhook failed: {r2.status_code} {r2.text}"
    finally:
        billing_module._verify_paypal_webhook_signature = original_verify

    doc = await users_collection().find_one({"_id": ObjectId(user_id)})
    assert doc["plan"] == "pro"

    processed = await processed_webhook_events_collection.count_documents({"provider": "paypal", "event_id": event_id})
    assert processed == 1


@pytest.mark.asyncio
async def test_processed_webhook_events_helper():
    """Unit test for the _record_processed_webhook idempotency helper."""
    provider = "test_provider"
    event_id = "test_event_999"

    # First call should return True (not processed before)
    result1 = await _record_processed_webhook(provider, event_id)
    assert result1 is True

    # Second call should return False (already processed)
    result2 = await _record_processed_webhook(provider, event_id)
    assert result2 is False

    # Empty event_id should always return True (no dedup possible)
    result3 = await _record_processed_webhook(provider, "")
    assert result3 is True

    await processed_webhook_events_collection.delete_many({"provider": provider, "event_id": event_id})
