from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List, Dict, Any

from app.services.assessment_engine import AssessmentEngine, AssessmentSession, AssessmentDefinition
from app.services import question_store
from app.config import get_settings

settings = get_settings()
router = APIRouter(prefix="/api/v1/company-prep", tags=["company-prep"])

# Company blueprints loaded from data
try:
    from app.data.company_blueprints import company_blueprints
    BLUEPRINTS = company_blueprints["company_blueprints"]
except Exception:
    BLUEPRINTS = {}

# Question bank access
def get_company_questions(company: str, difficulty: Optional[str] = None, limit: int = 50):
    """Get company-specific questions from the question store."""
    questions = question_store.find({"company": {"$in": [company]}})
    qs = question_store.find({"company": {"$in": [company]}}).to_list()
    # Filter by difficulty if specified
    if difficulty:
        qs = [q for q in qs if q.get("difficulty") == difficulty]
    # Return up to limit
    return qs[:limit] if limit else qs

def get_company_blueprint(company_name: str) -> Optional[dict]:
    """Get company preparation blueprint."""
    for key, bp in BLUEPRINTS.items():
        if bp.get("name", "").lower() == company_name.lower():
            return bp
    # Also try matching by key
    if company_name.lower() in key.lower():
        return BLUEPRINTS.get(key)
    return None


@router.get("/blueprints")
async def list_blueprints():
    """List all company preparation blueprints."""
    return {"blueprints": list(BLUEPRINTS.values())}


@router.get("/blueprints/{company_name}")
async def get_blueprint(company_name: str):
    """Get a specific company preparation blueprint."""
    bp = get_company_blueprint(company_name)
    if not bp:
        raise HTTPException(status_code=404, detail="Company blueprint not found")
    return bp


@router.get("/{company}/questions")
async def company_questions(
    company: str,
    difficulty: Optional[str] = Query(None),
    limit: int = Query(50),
    engine: Any = Depends(lambda: None),  # placeholder
):
    """Get company-specific questions."""
    questions = get_company_questions(company, difficulty, limit)
    return {
        "company": company,
        "questions": questions,
        "count": len(questions),
        "difficulty": difficulty,
    }


@router.get("/{company}/readiness")
async def company_readiness(company: str):
    """Get company readiness assessment."""
    # This would integrate with the assessment engine
    bp = get_company_blueprint(company)
    if not bp:
        raise HTTPException(status_code=404, detail="Company blueprint not found")
    
    # Generate a basic readiness report based on available questions
    # In a full implementation, this would use the assessment engine
    return {
        "company": company,
        "readiness": "Not yet assessed",
        "blueprint": bp.get("name", company),
        "competencies": bp.get("competencies", []),
        "suggested_study_plan": "Start with Foundation assessment",
    }


@router.post("/{company}/start-assessment")
async def start_company_assessment(
    company: str,
    ai_mode: str = Query("prohibited"),
    engine_dep: Any = Depends(lambda: None),
):
    """Start a company-specific assessment."""
    bp = get_company_blueprint(company)
    if not bp:
        raise HTTPException(status_code=404, detail="Company blueprint not found")
    
    # Create assessment session
    # In full implementation, would use AssessmentDefinition and AssessmentSession
    return {
        "company": company,
        "assessment_id": f"{company.lower()}_assessment",
        "blueprint": bp.get("name", company),
        "ai_mode": ai_mode,
        "stages": bp.get("structure", {}),
        "message": f"Assessment started for {bp.get('name', company)}",
    }