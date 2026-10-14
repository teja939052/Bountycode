"""Mission Pack service — canonical loader and registry for all packs.

Packs are authored as data files under:
  backend/app/content/mission_packs/

Each pack is a JSON file named by its id, e.g.:
  aptitude.percentages.json
  coding.variables.json
  cs_core.sql_joins.json
  tcs.nqt.json

This service loads them at startup and serves them by id/skill_id/domain/tag.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.models.mission_pack import MissionPack

logger = logging.getLogger(__name__)

_PACKS_DIR = Path(__file__).resolve().parent.parent / "content" / "mission_packs"
_pack_cache: Dict[str, MissionPack] = {}
_index_by_skill: Dict[str, List[str]] = {}
_index_by_domain: Dict[str, List[str]] = {}
_index_by_tag: Dict[str, List[str]] = {}


def _ensure_dirs() -> None:
    _PACKS_DIR.mkdir(parents=True, exist_ok=True)


def _load_pack(path: Path) -> Optional[MissionPack]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        return MissionPack(**raw)
    except Exception as exc:
        logger.warning("mission_pack.load_failed path=%s err=%s", path, exc)
        return None


def load_all_packs(force: bool = False) -> Dict[str, MissionPack]:
    global _pack_cache, _index_by_skill, _index_by_domain, _index_by_tag
    if _pack_cache and not force:
        return _pack_cache

    _ensure_dirs()
    _pack_cache = {}
    _index_by_skill = {}
    _index_by_domain = {}
    _index_by_tag = {}

    if not _PACKS_DIR.exists():
        return _pack_cache

    for path in _PACKS_DIR.glob("*.json"):
        pack = _load_pack(path)
        if pack is None:
            continue
        _pack_cache[pack.id] = pack
        _index_by_skill.setdefault(pack.skill_id, []).append(pack.id)
        _index_by_domain.setdefault(pack.domain, []).append(pack.id)
        for tag in pack.tags:
            _index_by_tag.setdefault(tag, []).append(pack.id)

    logger.info("mission_pack.loaded count=%d", len(_pack_cache))
    return _pack_cache


def get_pack(pack_id: str) -> Optional[MissionPack]:
    return _pack_cache.get(pack_id)


def get_pack_by_skill(skill_id: str) -> Optional[MissionPack]:
    ids = _index_by_skill.get(skill_id)
    if not ids:
        return None
    return _pack_cache.get(ids[0])


def list_by_domain(domain: str) -> List[MissionPack]:
    ids = _index_by_domain.get(domain, [])
    return [_pack_cache[i] for i in ids if i in _pack_cache]


def list_by_tag(tag: str) -> List[MissionPack]:
    ids = _index_by_tag.get(tag, [])
    return [_pack_cache[i] for i in ids if i in _pack_cache]


def list_all() -> List[MissionPack]:
    return list(_pack_cache.values())


def save_pack(pack: MissionPack) -> None:
    _ensure_dirs()
    path = _PACKS_DIR / f"{pack.id}.json"
    path.write_text(json.dumps(pack.model_dump(), indent=2, ensure_ascii=False), encoding="utf-8")
    load_all_packs(force=True)


def pack_to_dict(pack: MissionPack) -> Dict[str, Any]:
    return pack.model_dump()
