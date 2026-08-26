from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.database import users_collection
from app.middleware.auth import get_current_user
from app.services.invoice import InvoiceService
from bson import ObjectId

router = APIRouter(prefix="/api/v1/invoices", tags=["invoices"])
invoice_service = InvoiceService()


class GenerateInvoiceRequest(BaseModel):
    plan: str
    amount: float
    currency: str = "USD"
    transaction_id: Optional[str] = None


@router.post("/generate")
async def generate_invoice(req: GenerateInvoiceRequest, user: dict = Depends(get_current_user)):
    """Generate an invoice for a payment."""
    try:
        user_obj = users_collection.find_one({"_id": ObjectId(user["id"])})
        if not user_obj:
            raise HTTPException(status_code=404, detail="User not found")

        class SimpleUser:
            def __init__(self, data):
                self.id = str(data["_id"])
                self.name = data.get("name", "")
                self.email = data.get("email", "")

        invoice = invoice_service.generate_invoice(
            user=SimpleUser(user_obj),
            plan=req.plan,
            amount=req.amount,
            currency=req.currency,
            transaction_id=req.transaction_id
        )
        return {"success": True, "invoice": invoice}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/my-invoices")
async def get_my_invoices(user: dict = Depends(get_current_user)):
    """Get all invoices for the current user."""
    try:
        invoices = invoice_service.get_user_invoices(user["id"])
        return {"success": True, "invoices": invoices}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{invoice_id}")
async def get_invoice(invoice_id: str, user: dict = Depends(get_current_user)):
    """Get a specific invoice by ID."""
    try:
        invoice = invoice_service.get_invoice(invoice_id)
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        if invoice.get("customer", {}).get("user_id") != str(user["id"]):
            raise HTTPException(status_code=403, detail="Access denied")
        return {"success": True, "invoice": invoice}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
