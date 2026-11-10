"""Known broken Cognizant items are quarantined from trusted serving."""
from __future__ import annotations

import json
from pathlib import Path

from app.services.question_store import _is_servable


BANK = Path(__file__).resolve().parents[1] / "app" / "data" / "cognizant_genc_verified.json"
QUARANTINED_IDS = {
    "cognizant_coding_001",
    "cognizant_coding_002",
    "cognizant_coding_003",
}


def test_defective_cognizant_items_are_marked_unverified_and_non_servable():
    bank = json.loads(BANK.read_text(encoding="utf-8"))
    items = {item["id"]: item for item in bank if item.get("id") in QUARANTINED_IDS}

    assert set(items) == QUARANTINED_IDS
    for item_id, item in items.items():
        assert item["trust_status"] == "unverified", item_id
        assert item["content_review_status"] == "quarantined", item_id
        assert item["content_review_reason"], item_id
        assert _is_servable(item) is False, item_id
