"""Single source of truth for all company-related data.

This module does not replace the underlying data files. It provides a
unified lookup surface so callers do not need to know whether interview
rubrics, mock blueprints, readiness thresholds, or overlay profiles live
in which module.

Available registries:
    - interview_profiles   — ai_interview.COMPANY_PROFILES
    - mock_blueprints      — company_conversion.MOCK_BLUEPRINTS
    - readiness_profiles   — readiness_engine.COMPANY_PROFILES
    - overlays             — company_overlays.get_company_overlay()
    - blueprints_json      — company_blueprints.py loaded from disk
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


def _safe_import(module_path: str, attr: str) -> Any:
    try:
        import importlib
        mod = importlib.import_module(module_path)
        return getattr(mod, attr)
    except Exception:
        return {}


def get_interview_profiles() -> Dict[str, Dict[str, Any]]:
    """Return COMPANY_PROFILES from ai_interview (interview rubrics)."""
    return _safe_import("app.services.ai_interview", "COMPANY_PROFILES")


def get_mock_blueprints() -> Dict[str, Dict[str, Any]]:
    """Return MOCK_BLUEPRINTS from company_conversion (mock test structure)."""
    return _safe_import("app.services.company_conversion", "MOCK_BLUEPRINTS")


def get_readiness_profiles() -> Dict[str, Dict[str, Any]]:
    """Return COMPANY_PROFILES from readiness_engine (placement thresholds)."""
    return _safe_import("app.services.readiness_engine", "COMPANY_PROFILES")


def get_overlay(company_id: str) -> Optional[Dict[str, Any]]:
    """Return a single company overlay from company_overlays."""
    try:
        from app.content.company_overlays import get_company_overlay
        return get_company_overlay(company_id)
    except Exception:
        return None


def get_overlays() -> Dict[str, Any]:
    """Return all company overlays."""
    try:
        from app.content.company_overlays import get_all_overlays
        return get_all_overlays()
    except Exception:
        return {}


def get_blueprint_json(company_id: str) -> Optional[Dict[str, Any]]:
    """Return a single company blueprint from the JSON data file."""
    try:
        from app.data.company_blueprints import get_blueprint
        return get_blueprint(company_id)
    except Exception:
        return None


def list_supported_companies() -> List[str]:
    """Return all known company IDs across every registry."""
    seen = set()
    for registry in (
        get_interview_profiles(),
        get_mock_blueprints(),
        get_readiness_profiles(),
        get_overlays(),
    ):
        seen.update(registry.keys())
    return sorted(seen)


def get_company(company_id: str) -> Dict[str, Any]:
    """Return a merged company record from every available registry.

    The returned dict contains keys:
        - id
        - interview: from interview_profiles
        - mock: from mock_blueprints
        - readiness: from readiness_profiles
        - overlay: from overlays
        - blueprint: from blueprints_json
    """
    cid = company_id.lower().strip().replace(" ", "_").replace("-", "_")
    return {
        "id": cid,
        "interview": get_interview_profiles().get(cid),
        "mock": get_mock_blueprints().get(cid),
        "readiness": get_readiness_profiles().get(cid),
        "overlay": get_overlay(cid),
        "blueprint": get_blueprint_json(cid),
    }
