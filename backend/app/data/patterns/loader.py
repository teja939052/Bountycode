"""Pattern Pack loader.

Discovers and loads all ``.py`` files under ``app/data/patterns/``.
Each module must define a ``pack`` dict conforming to ``schema.py``.

The loader is imported once at startup by ``main.py`` and the resulting
registry is served through the campaign API.
"""
from __future__ import annotations

import importlib.util
import logging
import os
from pathlib import Path
from typing import Dict, List

from app.data.patterns.schema import empty_pack

logger = logging.getLogger(__name__)

_PACKS: Dict[str, Dict[str, Any]] = {}

_BACKEND_ROOT = Path(__file__).resolve().parents[3]
_PATTERNS_DIR = _BACKEND_ROOT / "app" / "data" / "patterns"


def _module_name(path: Path) -> str:
    return path.stem


def _is_valid_pack(obj: object) -> bool:
    if not isinstance(obj, dict):
        return False
    return "pattern_id" in obj and "name" in obj and "teaching" in obj


def load_all() -> List[str]:
    """Load every pattern-pack module under ``app/data/patterns/``.

    Returns the list of loaded pattern IDs.
    """
    loaded: List[str] = []
    if not _PATTERNS_DIR.exists():
        logger.warning("Patterns directory not found: %s", _PATTERNS_DIR)
        return loaded

    for path in sorted(_PATTERNS_DIR.glob("*.py")):
        if path.name.startswith("_") or path.name == "schema.py":
            continue
        try:
            spec = importlib.util.spec_from_file_location(
                f"app.data.patterns.{path.stem}", path
            )
            mod = importlib.util.module_from_spec(spec)
            assert spec.loader is not None
            spec.loader.exec_module(mod)  # type: ignore[union-attr]
            pack = getattr(mod, "pack", None)
            if _is_valid_pack(pack):
                _PACKS[pack["pattern_id"]] = pack
                loaded.append(pack["pattern_id"])
            else:
                logger.warning("Invalid pattern pack skipped: %s", path.name)
        except Exception as exc:
            logger.warning("Failed to load pattern pack %s: %s", path.name, exc)

    logger.info("Loaded %d pattern packs: %s", len(loaded), ", ".join(loaded))
    return loaded


def get_pack(pattern_id: str) -> Optional[Dict[str, Any]]:
    """Return a loaded pattern pack by ID, or ``None``."""
    return _PACKS.get(pattern_id)


def all_packs() -> Dict[str, Dict[str, Any]]:
    """Return the full registry (read-only copy)."""
    return dict(_PACKS)


def reset() -> None:
    """Clear loaded packs (test helper)."""
    _PACKS.clear()
