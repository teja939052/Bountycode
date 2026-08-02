from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Any
from uuid import uuid4
from app.database import users_collection, generated_projects_collection
from app.middleware.auth import get_current_user
from app.services.ai import generate_project as ai_generate_project
from app.services.ai import review_project as ai_review_project
from app.services.ai import improve_code as ai_improve_code
from app.services.ai import generate_setup_instructions

router = APIRouter(prefix="/api/v1/projects", tags=["projects"])


class GenerateRequest(BaseModel):
    description: str
    language: str = "python"
    framework: str = ""


class FileItem(BaseModel):
    path: str
    content: str
    language: str


class ReviewRequest(BaseModel):
    files: List[FileItem]


class ImproveRequest(BaseModel):
    file_path: str
    content: str
    language: str
    aspect: str = "readability"


class SaveRequest(BaseModel):
    files: List[FileItem]
    description: str
    tech_stack: List[str]
    setup_instructions: str


@router.post("/generate")
async def generate_project(req: GenerateRequest, user=Depends(get_current_user)):
    try:
        result = await ai_generate_project(req.description, req.language, req.framework)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI generation failed: {str(e)}")

    project_id = uuid4().hex[:12]
    doc = {
        "project_id": project_id,
        "user_id": user["id"],
        "files": result.get("files", []),
        "description": result.get("description", req.description),
        "tech_stack": result.get("tech_stack", []),
        "setup_instructions": result.get("setup_instructions", ""),
        "language": req.language,
        "framework": req.framework,
        "created_at": datetime.now(timezone.utc),
    }
    await generated_projects_collection.insert_one(doc)

    return {
        "project_id": project_id,
        "files": doc["files"],
        "description": doc["description"],
        "tech_stack": doc["tech_stack"],
        "setup_instructions": doc["setup_instructions"],
    }


@router.post("/review")
async def review_project(req: ReviewRequest, user=Depends(get_current_user)):
    files_dicts = [f.model_dump() for f in req.files]
    try:
        result = await ai_review_project(files_dicts)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI review failed: {str(e)}")
    return result


@router.post("/improve")
async def improve_code(req: ImproveRequest, user=Depends(get_current_user)):
    try:
        result = await ai_improve_code(req.content, req.language, req.aspect)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI improvement failed: {str(e)}")
    return result


@router.post("/save")
async def save_project(req: SaveRequest, user=Depends(get_current_user)):
    project_id = uuid4().hex[:12]
    doc = {
        "project_id": project_id,
        "user_id": user["id"],
        "files": [f.model_dump() for f in req.files],
        "description": req.description,
        "tech_stack": req.tech_stack,
        "setup_instructions": req.setup_instructions,
        "created_at": datetime.now(timezone.utc),
    }
    await generated_projects_collection.insert_one(doc)
    return {"project_id": project_id, "message": "Project saved"}


@router.get("/history")
async def get_history(user=Depends(get_current_user)):
    cursor = generated_projects_collection.find(
        {"user_id": user["id"]},
        sort=[("created_at", -1)],
        limit=50,
    )
    projects = []
    async for doc in cursor:
        projects.append({
            "project_id": doc["project_id"],
            "description": doc.get("description", ""),
            "tech_stack": doc.get("tech_stack", []),
            "language": doc.get("language", ""),
            "framework": doc.get("framework", ""),
            "created_at": doc["created_at"].isoformat(),
        })
    return {"projects": projects}


@router.get("/{project_id}")
async def get_project(project_id: str, user=Depends(get_current_user)):
    doc = await generated_projects_collection.find_one({
        "project_id": project_id,
        "user_id": user["id"],
    })
    if not doc:
        raise HTTPException(status_code=404, detail="Project not found")
    return {
        "project_id": doc["project_id"],
        "files": doc.get("files", []),
        "description": doc.get("description", ""),
        "tech_stack": doc.get("tech_stack", []),
        "setup_instructions": doc.get("setup_instructions", ""),
        "created_at": doc["created_at"].isoformat(),
    }
