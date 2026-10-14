"""Mission Pack routes — canonical content API.

Endpoints:
  GET  /api/v1/mission-packs              → list all packs
  GET  /api/v1/mission-packs/domain/{d}  → list by domain
  GET  /api/v1/mission-packs/tag/{t}     → list by tag
  GET  /api/v1/mission-packs/skill/{s}   → get by skill_id
  GET  /api/v1/mission-packs/{pack_id}   → get one pack
  POST  /api/v1/mission-packs            → create/update pack (admin only)
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.middleware.auth import get_current_user
from app.models.mission_pack import MissionPack
from app.services.mission_pack_service import (
    get_pack,
    get_pack_by_skill,
    list_by_domain,
    list_by_tag,
    list_all,
    save_pack,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/mission-packs", tags=["mission-packs"])


class PackCreate(BaseModel):
    pack: Dict[str, Any]


def _admin_only(user: Dict[str, Any]) -> None:
    if not (user.get("is_admin") or user.get("role") == "admin"):
        raise HTTPException(status_code=403, detail="Admin only")


@router.get("")
async def list_packs(
    domain: Optional[str] = None,
    tag: Optional[str] = None,
    skill: Optional[str] = None,
):
    if skill:
        pack = get_pack_by_skill(skill)
        if not pack:
            raise HTTPException(status_code=404, detail="Pack not found")
        return {"packs": [pack.model_dump()]}

    if domain:
        packs = list_by_domain(domain)
        return {"packs": [p.model_dump() for p in packs]}

    if tag:
        packs = list_by_tag(tag)
        return {"packs": [p.model_dump() for p in packs]}

    packs = list_all()
    return {"packs": [p.model_dump() for p in packs]}


@router.get("/domain/{domain}")
async def list_by_domain_route(domain: str):
    packs = list_by_domain(domain)
    return {"domain": domain, "packs": [p.model_dump() for p in packs]}


@router.get("/tag/{tag}")
async def list_by_tag_route(tag: str):
    packs = list_by_tag(tag)
    return {"tag": tag, "packs": [p.model_dump() for p in packs]}


@router.get("/skill/{skill_id}")
async def get_by_skill(skill_id: str):
    pack = get_pack_by_skill(skill_id)
    if not pack:
        raise HTTPException(status_code=404, detail="Pack not found")
    return {"pack": pack.model_dump()}


@router.get("/{pack_id}")
async def get_pack_route(pack_id: str):
    pack = get_pack(pack_id)
    if not pack:
        raise HTTPException(status_code=404, detail="Pack not found")
    return {"pack": pack.model_dump()}


@router.post("")
async def create_or_update_pack(req: PackCreate, user=Depends(get_current_user)):
    _admin_only(user)
    try:
        pack = MissionPack(**req.pack)
        save_pack(pack)
        return {"pack": pack.model_dump(), "saved": True}
    except Exception as exc:
        logger.exception("mission_pack.save_failed")
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/quality-report")
async def quality_report(user=Depends(get_current_user)):
    from app.services.lesson_depth import audit_all_mission_packs
    report = audit_all_mission_packs()
    return report


@router.get("/{pack_id}/quality")
async def pack_quality(pack_id: str, user=Depends(get_current_user)):
    from app.services.lesson_depth import diagnose_mission_pack
    report = diagnose_mission_pack(pack_id)
    if "error" in report:
        raise HTTPException(status_code=404, detail=report["error"])
    return report


@router.post("/validate")
async def validate_pack(req: PackCreate, user=Depends(get_current_user)):
    _admin_only(user)
    from app.services.lesson_depth import audit_mission_pack
    try:
        pack = MissionPack(**req.pack)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    report = audit_mission_pack(pack)
    return {"valid": report["is_complete"], "quality": report["quality"], "report": report}
