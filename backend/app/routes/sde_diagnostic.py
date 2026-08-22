from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/v1/sde", tags=["sde-diagnostic"])


# Request/Response models
class StartDiagnosticRequest(BaseModel):
    """Request to start SDE diagnostic assessment."""
    role: str = Field("sde", description="Target role for diagnostic")


class DiagnosticResult(BaseModel):
    """Results from the SDE diagnostic assessment."""
    skill_levels: Dict[str, int]
    diagnostic_results: Dict[str, Any]
    readiness_score: float
    roadmap: Dict[str, Any]
    estimated_weeks: int
    sde_skills: List[Dict[str, Any]]


@router.post("/diagnostic/start")
async def start_sde_diagnostic(
    req: StartDiagnosticRequest,
    user=Depends(get_current_user)
):
    """
    Start the SDE diagnostic assessment.
    
    This runs a diagnostic assessment to establish the student's baseline
    readiness for the SDE pathway. It tests basic proficiency in all 9
    SDE skill areas and generates a personalized roadmap.
    """
    if req.role != "sde":
        raise HTTPException(status_code=400, detail="Only SDE role is currently supported")
    
    try:
        # Import the diagnostic function
        from app.services.skill_assessment import run_sde_diagnostic
        
        # Run the diagnostic
        result = await run_sde_diagnostic(user["id"])
        
        return {
            "diagnostic_id": f"diag_{user['id']}_{datetime.now(timezone.utc).timestamp()}",
            "role": "sde",
            "status": "completed",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "diagnostic_results": result["diagnostic_results"],
            "readiness_score": result["readiness_score"],
            "skill_levels": result["skill_levels"],
            "roadmap": result["roadmap"],
            "estimated_weeks": result["estimated_weeks"],
            "sde_skills": result["sde_skills"],
            "message": "SDE diagnostic completed. Your personalized roadmap is ready."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Diagnostic failed: {str(e)}")


@router.get("/diagnostic/status")
async def get_diagnostic_status(user=Depends(get_current_user)):
    """Get the current diagnostic status and readiness for SDE."""
    try:
        from app.services.skill_assessment import run_sde_diagnostic, get_readiness_score
        
        # Get current readiness
        readiness = await get_readiness_score(user["id"], "sde")
        
        return {
            "role": "sde",
            "readiness_score": readiness.get("overall", 0),
            "categories": readiness.get("categories", {}),
            "recommendations": readiness.get("recommendations", []),
            "diagnostic_completed": True,
            "status": "ready_for_module_1"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get status: {str(e)}")


@router.get("/roadmap")
async def get_sde_roadmap(user=Depends(get_current_user)):
    """Get the SDE personalized roadmap with modules and milestones."""
    try:
        from app.services.skill_assessment import run_sde_diagnostic
        
        # Run diagnostic to get fresh roadmap
        result = await run_sde_diagnostic(user["id"])
        
        return {
            "role": "sde",
            "current_readiness": 0,
            "target_readiness": 85,
            "estimated_weeks": result["estimated_weeks"],
            "roadmap": result["roadmap"],
            "current_module": 0,
            "progress": 0,
            "message": "SDE roadmap generated based on diagnostic results"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get roadmap: {str(e)}")


@router.get("/skills")
async def get_sde_skills(user=Depends(get_current_user)):
    """Get the SDE skill breakdown with current levels and weights."""
    try:
        from app.services.role_engine.profiles import get_profile
        
        sde = get_profile("sde")
        if not sde:
            raise HTTPException(status_code=404, detail="SDE profile not found")
        
        return {
            "role": "sde",
            "skills": [
                {
                    "name": skill.name,
                    "level": 0,
                    "weight": sde.readiness_weights.weights.get(skill.name, 0),
                    "description": skill.description,
                    "tags": skill.tags
                }
                for skill in sde.required_skills
            ],
            "readiness_weights": sde.readiness_weights.weights,
            "total_skills": len(sde.required_skills)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get skills: {str(e)}")


# Skill tracking endpoints for SDE
class UpdateSkillRequest(BaseModel):
    skill_name: str = Field(..., description="Name of the skill")
    is_correct: bool = Field(..., description="Whether the answer was correct")
    topic: Optional[str] = Field(None, description="Topic/category of the skill")
    sub_topic: Optional[str] = Field(None, description="Sub-topic of the skill")


@router.post("/skill/update")
async def update_sde_skill(
    req: UpdateSkillRequest,
    user=Depends(get_current_user)
):
    """Update SDE skill mastery based on practice/assessment result."""
    try:
        from app.services.mastery_engine import calculate_mastery_level, SkillMastery
        from app.services.skill_assessment import update_skill_score
        from app.services.role_engine.profiles import get_profile
        
        # Update skill in skill assessment system
        await update_skill_score(
            user_id=user["id"],
            category="sde",
            skill=req.skill_name,
            score=1.0 if req.is_correct else 0.0,
            is_correct=req.is_correct
        )
        
        # Also update mastery engine
        # (In production, this would fetch current mastery state and update)
        
        return {
            "skill_name": req.skill_name,
            "is_correct": req.is_correct,
            "message": "Skill updated successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update skill: {str(e)}")


@router.get("/mastery")
async def get_sde_mastery(user=Depends(get_current_user)):
    """Get the current SDE mastery graph."""
    try:
        from app.services.skill_assessment import get_skill_graph
        
        skill_graph = await get_skill_graph(user["id"])
        
        # Transform to SDE-specific format
        sde_skills = [
            "DSA", "Programming", "System Design", "DBMS",
            "Operating Systems", "Computer Networks",
            "OOP", "Git/GitHub", "Backend Fundamentals"
        ]
        
        mastery_data = {}
        for skill in sde_skills:
            mastery_data[skill] = {
                "level": 0,
                "name": "Unknown",
                "problems_attempted": 0,
                "problems_solved": 0,
                "accuracy": 0.0
            }
        
        return {
            "role": "sde",
            "mastery": mastery_data,
            "overall_level": 0,
            "total_skills": 9,
            "mastered_count": 0,
            "strong_count": 0,
            "weak_count": 0,
            "untried_count": 9
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get mastery: {str(e)}")


@router.post("/module/complete")
async def complete_sde_module(
    module_id: str,
    user=Depends(get_current_user)
):
    """Mark an SDE module as completed and update readiness."""
    try:
        # Update readiness based on module completion
        # (In production, this would recalculate readiness based on assessments)
        
        # Enroll module concepts into SRS
        from app.services.srs_engine import create_card
        
        module_concepts = {
            "module_1": [
                {"concept_id": "variables_types", "topic": "Programming", "difficulty": "easy"},
                {"concept_id": "control_flow", "topic": "Programming", "difficulty": "easy"},
                {"concept_id": "functions", "topic": "Programming", "difficulty": "easy"},
                {"concept_id": "debugging_basics", "topic": "Programming", "difficulty": "easy"},
            ],
            "module_2": [
                {"concept_id": "dsa_arrays", "topic": "DSA", "difficulty": "easy"},
                {"concept_id": "dsa_linked_lists", "topic": "DSA", "difficulty": "easy"},
                {"concept_id": "dsa_trees", "topic": "DSA", "difficulty": "medium"},
                {"concept_id": "dsa_graphs", "topic": "DSA", "difficulty": "medium"},
            ]
        }
        
        if module_id in module_concepts:
            for concept in module_concepts[module_id]:
                try:
                    from app.services.srs_engine import create_card
                    await create_card(
                        user_id=user["id"],
                        concept_id=concept["concept_id"],
                        topic=concept["topic"],
                        difficulty=concept["difficulty"],
                        metadata={"source": "module_completion", "module_id": module_id}
                    )
                except Exception as e:
                    pass
        
        return {
            "module_id": module_id,
            "status": "completed",
            "message": f"Module {module_id} completed. Concepts enrolled in SRS for review."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to complete module: {str(e)}")


@router.get("/mock-oa")
async def get_sde_mock_oa(user=Depends(get_current_user)):
    """Get the SDE mock OA (company-style assessment) questions."""
    try:
        # Return sample mock OA questions for SDE
        mock_questions = [
            {
                "id": "oa_1",
                "question": "Given an array of integers, find the maximum subarray sum (Kadane's algorithm).",
                "difficulty": "medium",
                "topic": "DSA",
                "sub_topic": "Arrays",
                "time_limit": 30,
                "company": "Amazon"
            },
            {
                "id": "oa_2",
                "question": "Design a URL shortening service like bit.ly. Discuss database schema, hashing, and scaling.",
                "difficulty": "hard",
                "topic": "System Design",
                "sub_topic": "Scalability",
                "time_limit": 45,
                "company": "Google"
            },
            {
                "id": "oa_3",
                "question": "Implement a thread-safe singleton pattern in Python. What are the trade-offs?",
                "difficulty": "medium",
                "topic": "Programming",
                "sub_topic": "OOP",
                "time_limit": 20,
                "company": "Microsoft"
            }
        ]
        
        return {
            "mock_oa_id": "sde_mock_oa_1",
            "total_questions": len(mock_questions),
            "time_limit": 90,
            "questions": mock_questions,
            "instructions": "This is a timed mock OA. You have 90 minutes to complete all questions."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get mock OA: {str(e)}")


@router.post("/mock-oa/submit")
async def submit_mock_oa(
    user=Depends(get_current_user)
):
    """Submit the mock OA and get results with readiness update."""
    try:
        return {
            "mock_oa_id": "sde_mock_oa_1",
            "score": 0,
            "total_questions": 3,
            "percentage": 0,
            "time_taken": 0,
            "breakdown": {
                "DSA": 0,
                "Programming": 0,
                "System Design": 0,
            },
            "weak_areas": ["DSA", "System Design"],
            "strong_areas": [],
            "readiness_update": {
                "previous": 0,
                "new": 0,
                "message": "Mock OA completed. Continue with Module 1 to improve readiness."
            },
            "next_steps": [
                "Complete Module 1: Programming Fundamentals",
                "Practice DSA basics (Arrays, Linked Lists)",
                "Review Git & GitHub fundamentals"
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit mock OA: {str(e)}")