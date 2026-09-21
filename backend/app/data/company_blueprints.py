"""Company blueprints — file-backed, loaded once at import time.

The JSON file is the single source of truth. This module exposes
``company_blueprints`` as a dict with the same shape as the JSON root.

No LLM. No MongoDB writes for question content.
"""

from __future__ import annotations

import json
import os
from typing import Dict, Any

_PATH = os.path.join(os.path.dirname(__file__), "company_blueprints.json")

try:
    with open(_PATH, "r", encoding="utf-8") as _f:
        company_blueprints: Dict[str, Any] = json.load(_f)
except Exception:
    company_blueprints = {"company_blueprints": {}}


def get_blueprint(company: str) -> Dict[str, Any] | None:
    """Return a blueprint by company key, or None."""
    return company_blueprints.get("company_blueprints", {}).get(company.lower())
