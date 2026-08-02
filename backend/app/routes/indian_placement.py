"""
Indian Company Placement Mock Tests.
Company-specific aptitude, coding, and HR rounds matching real campus placement patterns.
"""
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import curated_questions_collection
from app.data.indian_companies import (
    INDIAN_COMPANIES, get_all_companies, get_company_detail, get_company_mock_sections
)

router = APIRouter(prefix="/api/v1/indian-placement", tags=["indian-placement"])


@router.get("/companies")
async def list_indian_companies():
    """List all supported Indian companies with placement patterns."""
    return {"companies": get_all_companies()}


@router.get("/{company_id}")
async def get_company(company_id: str):
    """Get detailed company info including exam pattern, HR questions, tips, coding patterns."""
    detail = get_company_detail(company_id)
    if not detail:
        raise HTTPException(status_code=404, detail="Company not found")
    return detail


@router.get("/{company_id}/mock-config")
async def get_mock_config(company_id: str):
    """Get mock test configuration (sections, questions, time limits)."""
    sections = get_company_mock_sections(company_id)
    if not sections:
        raise HTTPException(status_code=404, detail="No mock test available for this company")
    company = INDIAN_COMPANIES.get(company_id.lower())
    return {
        "company": company["name"],
        "exam_pattern": company["exam_pattern"],
        "sections": sections,
    }


@router.get("/{company_id}/hr-questions")
async def get_hr_questions(company_id: str):
    """Get commonly asked HR/behavioral questions for this company."""
    company = INDIAN_COMPANIES.get(company_id.lower())
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return {
        "company": company["name"],
        "hr_questions": company.get("hr_questions", []),
        "tips": company.get("tips", []),
    }


@router.get("/{company_id}/coding-patterns")
async def get_coding_patterns(company_id: str):
    """Get commonly asked coding patterns for this company."""
    company = INDIAN_COMPANIES.get(company_id.lower())
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return {
        "company": company["name"],
        "coding_patterns": company.get("coding_patterns", []),
        "focus_areas": company.get("focus_areas", []),
    }


class StartPlacementTestRequest(BaseModel):
    company_id: str
    section_name: Optional[str] = None  # If None, start full mock


@router.post("/start-mock")
async def start_placement_mock(req: StartPlacementTestRequest, user=Depends(get_current_user)):
    """Start a company-specific placement mock test.
    Pulls real questions from the curated_questions collection matching the company's pattern.
    """
    company = INDIAN_COMPANIES.get(req.company_id.lower())
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    sections = get_company_mock_sections(req.company_id)
    if not sections:
        raise HTTPException(status_code=400, detail="No test sections available")

    collection = curated_questions_collection()

    # If specific section requested, filter to that
    target_sections = sections["sections"]
    if req.section_name:
        target_sections = [s for s in target_sections if s["name"].lower() == req.section_name.lower()]
        if not target_sections:
            raise HTTPException(status_code=404, detail=f"Section '{req.section_name}' not found")

    all_questions = []
    for section in target_sections:
        # For each section, try to pull questions from DB
        if section.get("types", [None])[0] in ["Problem Solving", "MCQ on Programming", "Basic Coding"]:
            # Coding section - pull from curated_questions
            query = {"type": "coding"}
            if section.get("topics"):
                # Map company topics to our topic names
                topic_map = {
                    "Arrays": "Arrays", "Strings": "Strings",
                    "Linked Lists": "Linked Lists", "Trees": "Trees",
                    "Dynamic Programming": "Dynamic Programming",
                    "Recursion": "Recursion", "Math": "Math",
                }
                topics = []
                for t in section["topics"]:
                    if t in topic_map:
                        topics.append(topic_map[t])
                if topics:
                    query["topic"] = {"$in": topics}

            pipeline = [
                {"$match": query},
                {"$sample": {"size": min(section["questions"], 5)}},
                {"$project": {
                    "question_title": 1, "statement": 1, "difficulty": 1,
                    "topics": 1, "visible_test_cases": 1, "constraints": 1,
                    "examples": 1, "hints": 1, "solution": 1,
                }}
            ]

            section_questions = []
            async for doc in collection.aggregate(pipeline):
                doc["id"] = str(doc.pop("_id"))
                section_questions.append(doc)

            # If not enough DB questions, pad with AI-generated ones
            remaining = section["questions"] - len(section_questions)
            for _ in range(remaining):
                section_questions.append({
                    "id": f"ai_{_}",
                    "question_title": f"Practice: {section['topics'][_ % len(section['topics'])]}",
                    "statement": f"Solve a problem related to {section['topics'][_ % len(section['topics'])]}",
                    "difficulty": section.get("difficulty", "easy"),
                    "is_ai_generated": True,
                })

            all_questions.append({
                "section_name": section["name"],
                "section_type": section.get("types", ["coding"])[0],
                "time_minutes": section["time_minutes"],
                "questions": section_questions,
            })

        else:
            # Aptitude/Verbal/English sections - use MCQs from curated_questions
            query = {"type": {"$in": ["aptitude", "behavioral"]}}

            pipeline = [
                {"$match": query},
                {"$sample": {"size": min(section["questions"], 10)}},
                {"$project": {
                    "question": 1, "options": 1, "correct_answer": 1,
                    "explanation": 1, "topic": 1, "difficulty": 1,
                }}
            ]

            section_questions = []
            async for doc in collection.aggregate(pipeline):
                doc["id"] = str(doc.pop("_id"))
                section_questions.append(doc)

            remaining = section["questions"] - len(section_questions)
            for _ in range(remaining):
                topic = section.get("topics", ["General"])[_ % len(section.get("topics", ["General"]))]
                section_questions.append({
                    "id": f"apt_{_}",
                    "question": f"Practice question on {topic}",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_answer": "Option A",
                    "topic": topic,
                    "is_ai_generated": True,
                })

            all_questions.append({
                "section_name": section["name"],
                "section_type": section.get("types", ["aptitude"])[0],
                "time_minutes": section["time_minutes"],
                "questions": section_questions,
            })

    # Calculate total time
    total_time = sum(s["time_minutes"] for s in all_questions)

    return {
        "company": company["name"],
        "company_id": req.company_id,
        "exam_pattern": company["exam_pattern"],
        "sections": all_questions,
        "total_time_minutes": total_time,
        "total_questions": sum(len(s["questions"]) for s in all_questions),
        "package": company["package"],
        "eligibility": company["eligibility"],
    }
