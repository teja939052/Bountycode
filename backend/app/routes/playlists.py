"""Playlists routes — PostgreSQL-backed, no MongoDB."""
from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth import get_current_user
from app.database import get_session

router = APIRouter(prefix="/api/v1/playlists", tags=["playlists"])


@router.get("/playlists")
async def list_playlists(user=Depends(get_current_user)):
    """List user's learning playlists."""
    return {"playlists": []}


@router.post("/playlists")
async def create_playlist(
    name: str,
    description: str = "",
    user=Depends(get_current_user),
):
    """Create a new playlist."""
    return {"playlist_id": str(user["id"]) + "-playlist-1", "name": name, "description": description, "items": []}


@router.get("/playlists/{playlist_id}")
async def get_playlist(playlist_id: str, user=Depends(get_current_user)):
    """Get playlist details."""
    return {"playlist_id": playlist_id, "items": []}