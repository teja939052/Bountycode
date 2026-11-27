"""Language paths routes — PostgreSQL-backed, no MongoDB."""
from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth import get_current_user
from app.database import get_session

router = APIRouter(prefix="/api/v1/language-paths", tags=["language-paths"])


@router.get("/paths")
async def list_language_paths(user=Depends(get_current_user)):
    """List available language learning paths."""
    return {
        "paths": [
            {"id": "python", "name": "Python", "levels": 100},
            {"id": "java", "name": "Java", "levels": 100},
            {"id": "cpp", "name": "C++", "levels": 100},
            {"id": "javascript", "name": "JavaScript", "levels": 100},
        ]
    }


@router.get("/paths/{path_id}")
async def get_language_path(path_id: str, user=Depends(get_current_user)):
    """Get learning path details."""
    return {"path_id": path_id, "levels": [], "total_levels": 100}