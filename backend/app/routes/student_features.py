from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.middleware.auth import get_current_user
from app.services.cheatsheet import CheatSheetGenerator
from app.services.anti_plagiarism import AntiPlagiarismEngine
from app.services.application_tracker import ApplicationTracker
from app.services.daily_drill import DailyDrill
from app.services.profile_sync import ProfileSync

router = APIRouter(prefix="/api/v1/student", tags=["student-features"])

# Initialize services
cheatsheet_gen = CheatSheetGenerator()
anti_plagiarism = AntiPlagiarismEngine()
app_tracker = ApplicationTracker()
daily_drill = DailyDrill()
profile_sync = ProfileSync()


# ============================================
# CHEAT SHEETS
# ============================================

class CheatSheetRequest(BaseModel):
    company: str
    topic: str


@router.post("/cheatsheet")
async def generate_cheatsheet(req: CheatSheetRequest, user=Depends(get_current_user)):
    """Generate interview survival cheat sheet."""
    return await cheatsheet_gen.generate_cheatsheet(req.company, req.topic)


@router.get("/cheatsheet/templates")
async def get_cheatsheet_templates():
    """Get available cheat sheet topics."""
    return {
        "topics": list(cheatsheet_gen.TOPIC_IMPLEMENTATIONS.keys()),
        "companies": list(cheatsheet_gen.COMPANY_BIASES.keys()),
    }


# ============================================
# ANTI-PLAGIARISM
# ============================================

class HumanizeRequest(BaseModel):
    bullet: str
    user_id: str = ""


class HumanizeResumeRequest(BaseModel):
    resume_text: str
    user_id: str = ""


@router.post("/humanize/bullet")
async def humanize_bullet(req: HumanizeRequest, user=Depends(get_current_user)):
    """Humanize a single bullet to avoid plagiarism detection."""
    humanized = anti_plagiarism.humanize_bullet(req.bullet, user["id"])
    variations = anti_plagiarism.generate_unique_variations(req.bullet, 3)

    return {
        "original": req.bullet,
        "humanized": humanized,
        "variations": variations,
        "plagiarism_check": anti_plagiarism.check_plagiarism_risk(humanized),
    }


@router.post("/humanize/resume")
async def humanize_resume(req: HumanizeResumeRequest, user=Depends(get_current_user)):
    """Humanize entire resume."""
    humanized = anti_plagiarism.humanize_resume(req.resume_text, user["id"])
    return {
        "original": req.resume_text,
        "humanized": humanized,
    }


# ============================================
# APPLICATION TRACKER
# ============================================

class CreateApplicationRequest(BaseModel):
    company: str
    role: str
    job_url: str = ""
    notes: str = ""


class UpdateStageRequest(BaseModel):
    application_id: str
    new_stage: str


@router.post("/applications")
async def create_application(req: CreateApplicationRequest, user=Depends(get_current_user)):
    """Create a new application entry."""
    return await app_tracker.create_application(
        user["id"], req.company, req.role, req.job_url, req.notes
    )


@router.get("/applications/pipeline")
async def get_pipeline(user=Depends(get_current_user)):
    """Get Kanban view of all applications."""
    return await app_tracker.get_user_pipeline(user["id"])


@router.put("/applications/stage")
async def update_stage(req: UpdateStageRequest, user=Depends(get_current_user)):
    """Update application stage."""
    return await app_tracker.update_stage(req.application_id, req.new_stage, user["id"])


@router.get("/applications/stats")
async def get_stats(user=Depends(get_current_user)):
    """Get application statistics."""
    return await app_tracker.get_stats(user["id"])


@router.delete("/applications/{application_id}")
async def delete_application(application_id: str, user=Depends(get_current_user)):
    """Delete an application."""
    return await app_tracker.delete_application(application_id, user["id"])


@router.get("/applications/stages")
async def get_stages():
    """Get available pipeline stages."""
    from app.services.application_tracker import PIPELINE_STAGES
    return {"stages": PIPELINE_STAGES}


# ============================================
# DAILY DRILL
# ============================================

class SubmitDrillRequest(BaseModel):
    drill_id: str
    answers: List[dict]


@router.post("/drill/daily")
async def get_daily_drill(user=Depends(get_current_user)):
    """Get today's 5-minute placement drill."""
    return await daily_drill.generate_daily_drill(user["id"])


@router.post("/drill/submit")
async def submit_drill(req: SubmitDrillRequest, user=Depends(get_current_user)):
    """Submit drill answers."""
    return await daily_drill.submit_drill(user["id"], req.drill_id, req.answers)


# ============================================
# PROFILE SYNC
# ============================================

class GitHubSyncRequest(BaseModel):
    github_url: str


class GenerateBulletsRequest(BaseModel):
    projects: List[dict]
    role: str = "Software Engineer"


@router.post("/sync/github")
async def sync_github(req: GitHubSyncRequest, user=Depends(get_current_user)):
    """Import profile from GitHub."""
    return await profile_sync.parse_github_profile(req.github_url)


@router.post("/sync/generate-bullets")
async def generate_bullets(req: GenerateBulletsRequest, user=Depends(get_current_user)):
    """Generate resume bullets from GitHub projects."""
    return await profile_sync.generate_resume_bullets_from_projects(req.projects, req.role)


@router.get("/sync/linkedin")
async def linkedin_info():
    """Get LinkedIn sync instructions."""
    return await profile_sync.parse_linkedin_about("")
