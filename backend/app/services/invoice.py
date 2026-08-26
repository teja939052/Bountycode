# backend/app/services/invoice.py
import json
import os
import uuid
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any

INVOICE_DIR = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "data", "invoices")
)


def _resolve_user(user) -> Dict[str, Any]:
    """Extract id/name/email from a dict (DB document) or object (model)."""
    if isinstance(user, dict):
        return {
            "id": str(user.get("id") or user.get("_id") or ""),
            "name": user.get("name") or "Valued Customer",
            "email": user.get("email") or "",
        }
    uid = getattr(user, "id", None) or getattr(user, "_id", None)
    return {
        "id": str(uid) if uid is not None else "",
        "name": getattr(user, "name", None) or "Valued Customer",
        "email": getattr(user, "email", None) or "",
    }


class InvoiceService:
    def __init__(self):
        self.invoice_dir = INVOICE_DIR
        os.makedirs(self.invoice_dir, exist_ok=True)

    def _period_end(self, start: datetime, billing_cycle: str) -> Optional[str]:
        if billing_cycle == "monthly":
            return (start + timedelta(days=30)).isoformat()
        if billing_cycle == "yearly":
            return (start + timedelta(days=365)).isoformat()
        return None  # lifetime / one-time

    def generate_invoice(
        self,
        user,
        plan: str,
        amount: float,
        currency: str = "USD",
        transaction_id: Optional[str] = None,
        billing_cycle: str = "one-time",
    ) -> dict:
        """Generate a legally compliant invoice."""
        u = _resolve_user(user)
        now = datetime.now(timezone.utc)
        invoice_id = f"INV-{now.strftime('%Y%m')}-{uuid.uuid4().hex[:8].upper()}"

        invoice = {
            "invoice_id": invoice_id,
            "company": {
                "name": "PlacementPro",
                "address": "[Your Business Address]",
                "email": "support@placementpro.com",
                "gst": "[Your GST Number]",
            },
            "customer": {
                "name": u["name"],
                "email": u["email"],
                "user_id": u["id"],
            },
            "items": [
                {
                    "description": f"{plan} Subscription",
                    "quantity": 1,
                    "unit_price": round(float(amount), 2),
                    "total": round(float(amount), 2),
                }
            ],
            "subtotal": round(float(amount), 2),
            "tax": 0.0,
            "total": round(float(amount), 2),
            "currency": currency,
            "transaction_id": transaction_id,
            "status": "paid",
            "payment_method": "PayPal",
            "billing_cycle": billing_cycle,
            "created_at": now.isoformat(),
            "period_start": now.isoformat(),
            "period_end": self._period_end(now, billing_cycle),
        }

        file_path = os.path.join(self.invoice_dir, f"{invoice_id}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(invoice, f, indent=2)

        return invoice

    def get_invoice(self, invoice_id: str) -> Optional[dict]:
        """Get an invoice by ID."""
        file_path = os.path.join(self.invoice_dir, f"{invoice_id}.json")
        if not os.path.exists(file_path):
            return None
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_user_invoices(self, user_id: str) -> List[dict]:
        """Get all invoices for a user (metadata only, sorted newest first)."""
        user_id = str(user_id)
        invoices = []
        if not os.path.isdir(self.invoice_dir):
            return invoices
        for filename in os.listdir(self.invoice_dir):
            if not filename.endswith(".json"):
                continue
            with open(os.path.join(self.invoice_dir, filename), "r", encoding="utf-8") as f:
                invoice = json.load(f)
                if invoice.get("customer", {}).get("user_id") == user_id:
                    invoices.append(invoice)
        return sorted(
            invoices, key=lambda x: x.get("created_at", ""), reverse=True
        )

    def generate_invoice_html(self, invoice: dict) -> str:
        """Generate an HTML version of the invoice."""
        items_html = "".join(
            f"<tr><td>{item['description']}</td><td>{item['quantity']}</td>"
            f"<td>{invoice['currency']} {item['unit_price']:.2f}</td>"
            f"<td>{invoice['currency']} {item['total']:.2f}</td></tr>"
            for item in invoice["items"]
        )
        period = ""
        if invoice.get("period_start") and invoice.get("period_end"):
            period = (
                f"<p style='font-size: 14px; font-weight: normal;'>"
                f"Period: {invoice['period_start'][:10]} to {invoice['period_end'][:10]}</p>"
            )
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Invoice {invoice['invoice_id']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; }}
                .header {{ display: flex; justify-content: space-between; border-bottom: 2px solid #22C55E; padding-bottom: 20px; }}
                .title {{ color: #22C55E; }}
                .details {{ margin: 20px 0; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                .total {{ font-size: 20px; font-weight: bold; text-align: right; }}
                .footer {{ margin-top: 40px; text-align: center; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <div>
                    <h1 class="title">Invoice</h1>
                    <p><strong>PlacementPro</strong></p>
                    <p>[Your Business Address]</p>
                </div>
                <div>
                    <p><strong>Invoice #:</strong> {invoice['invoice_id']}</p>
                    <p><strong>Date:</strong> {invoice['created_at'][:10]}</p>
                </div>
            </div>

            <div class="details">
                <p><strong>Bill To:</strong></p>
                <p>{invoice['customer']['name']}</p>
                <p>{invoice['customer']['email']}</p>
            </div>

            <table>
                <thead>
                    <tr>
                        <th>Description</th>
                        <th>Qty</th>
                        <th>Price</th>
                        <th>Total</th>
                    </tr>
                </thead>
                <tbody>
                    {items_html}
                </tbody>
            </table>

            <div class="total">
                <p>Total: {invoice['currency']} {invoice['total']:.2f}</p>
                <p style="font-size: 14px; font-weight: normal;">Payment Method: {invoice['payment_method']}</p>
                <p style="font-size: 14px; font-weight: normal;">Transaction ID: {invoice.get('transaction_id', 'N/A')}</p>
                {period}
            </div>

            <div class="footer">
                <p>Thank you for choosing PlacementPro!</p>
                <p>For any questions, contact support@placementpro.com</p>
                <p>GST: [Your GST Number]</p>
            </div>
        </body>
        </html>
        """


invoice_service = InvoiceService()
