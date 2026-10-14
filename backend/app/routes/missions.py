"""Mission API — read-only serving of the mission layer.

Serves mission structure (brief, stages, reward, consequence) and track
layouts. NEVER serves question content: stages carry bank_refs (IDs) that
the existing question endpoints resolve behind the trust gate.

A mission with failing validate_mission() returns 404 with the errors —
unvalid missions are not servable, same rule as unservable questions.
"""
from fastapi import APIRouter, Depends, HTTPException

from app.content import service_tracks
from app.content.curriculum.missions import MISSIONS
from app.content.mission_definitions import mission_index, validate_mission
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/v1/missions", tags=["missions"])


@router.get("/tracks")
async def list_tracks(user=Depends(get_current_user)):
    """Service-company tracks with stage layouts."""
    return {
        "tracks": [
            {**service_tracks.SERVICE_TRACKS[tid].model_dump(),
             "mission_ids": service_tracks.track_mission_ids(tid)}
            for tid in service_tracks.list_tracks()
        ]
    }


@router.get("/tracks/{track_id}")
async def track_detail(track_id: str, user=Depends(get_current_user)):
    """One track: stages, mission briefs, bank-filter fallbacks."""
    track = service_tracks.get_track(track_id)
    if track is None:
        raise HTTPException(status_code=404, detail=f"Unknown track: {track_id}")
    out = track.model_dump()
    briefs = {}
    for mid in service_tracks.track_mission_ids(track_id):
        m = MISSIONS.get(mid)
        if m is None:
            continue
        briefs[mid] = {
            "brief": m.brief.model_dump(),
            "domain": m.domain,
            "mentor_skill": m.mentor_skill,
            "reward": m.reward.model_dump(),
            "consequence": m.consequence.model_dump(),
            "frontend_slug": m.frontend_slug,
            "status": m.status,
        }
    out["mission_briefs"] = briefs
    return out


@router.get("/index")
async def index(user=Depends(get_current_user)):
    """Journey planner view: mission_id -> routing refs (no content)."""
    return {"missions": mission_index(list(MISSIONS.values()))}


@router.get("/{mission_id}")
async def mission_detail(mission_id: str, user=Depends(get_current_user)):
    """Full mission structure. Invalid missions 404 with errors."""
    m = MISSIONS.get(mission_id)
    if m is None:
        raise HTTPException(status_code=404, detail=f"Unknown mission: {mission_id}")
    errors = validate_mission(m)
    if errors:
        raise HTTPException(status_code=404, detail={"mission": mission_id, "errors": errors})
    from app.content.curriculum.captain_byte.missions import mission_line

    data = m.model_dump()
    data["mentor"] = {
        "brief": mission_line(m.domain, "brief"),
        "consequence_mastery": mission_line(m.domain, "consequence_mastery"),
        "consequence_repair": mission_line(m.domain, "consequence_repair"),
    }
    return data
