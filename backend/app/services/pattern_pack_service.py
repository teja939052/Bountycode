"""Pattern Pack service — load and serve authored pattern packs.

Reuses the data-layer loader; adds lightweight caching and validation.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

from app.data.patterns.loader import load_all, get_pack, all_packs
from app.data.patterns.schema import empty_pack

logger = logging.getLogger(__name__)

# Load packs once at import time. In production this is called from
# main.py lifespan so packs are in memory before the first request.
_packs_loaded = False

_BACKEND_ROOT = Path(__file__).resolve().parents[2]
_BLUEPRINTS_PATH = _BACKEND_ROOT / "app" / "data" / "company_blueprints.json"


def _load_blueprints() -> Dict[str, Any]:
    try:
        with open(_BLUEPRINTS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("company_blueprints", {})
    except Exception as exc:
        logger.warning("Failed to load company blueprints: %s", exc)
        return {}


def ensure_loaded() -> None:
    global _packs_loaded
    if not _packs_loaded:
        load_all()
        _packs_loaded = True


def get_pattern_pack(pattern_id: str) -> Dict[str, Any]:
    """Return a pattern pack by ID, or an empty skeleton if missing."""
    ensure_loaded()
    pack = get_pack(pattern_id)
    if pack is None:
        logger.debug("No pattern pack for '%s' — returning empty skeleton", pattern_id)
        return empty_pack(pattern_id)
    return dict(pack)


def list_pattern_packs() -> Dict[str, Dict[str, Any]]:
    """Return the full registry of loaded packs."""
    ensure_loaded()
    return all_packs()


def get_company_blueprint(company_id: str) -> Optional[Dict[str, Any]]:
    """Return a company blueprint by ID, or None if not found."""
    blueprints = _load_blueprints()
    blueprint = blueprints.get(company_id)
    if blueprint is None:
        # Try alias lookup
        alias_map = {
            "tcs": "tcs_nqt",
            "infosys": "infosys",
            "wipro": "wipro_nlth",
            "accenture": "accenture",
            "capgemini": "capgemini",
            "ibm": "ibm",
            "tech_mahindra": "tech_mahindra",
            "ltimindtree": "ltimindtree",
            "hcl": "hcl",
            "cognizant": "cognizant_genc",
        }
        alias_id = alias_map.get(company_id)
        if alias_id:
            blueprint = blueprints.get(alias_id)
    return dict(blueprint) if blueprint else None

