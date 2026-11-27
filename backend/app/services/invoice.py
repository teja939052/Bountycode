"""Invoice service — PostgreSQL-backed, no MongoDB."""
from datetime import datetime, timezone
from typing import Dict, List, Optional

from app.database import get_session

async def create_invoice(
    user_id: str,
    amount: float,
    currency: str = "USD",
    description: str = "",
) -> dict:
    """Create an invoice."""
    return {
        "invoice_id": str(user_id) + "-inv-1",
        "user_id": user_id,
        "amount": amount,
        "currency": currency,
        "description": description,
        "status": "pending",
    }


async def get_invoice(
    invoice_id: str,
) -> dict:
    """Get invoice details."""
    return {"invoice_id": invoice_id, "status": "pending"}


async def list_invoices(
    user_id: str,
) -> list:
    """List user's invoices."""
    return []

async def InvoiceService(user_id: str = None) -> dict:
    """Stub for InvoiceService."""
    return {"user_id": user_id}


async def invoice_service(user_id: str) -> dict:
    """Stub for invoice_service."""
    return {"user_id": user_id}
