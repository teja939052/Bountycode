"""
Indian Company Placement Mock Tests.
Company-specific aptitude, coding, and HR rounds matching real campus placement patterns.
"""
from datetime import datetime, timezone, timedelta
import random
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.middleware.auth import get_current_user
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
    """Get pattern-relevant HR/behavioral questions for this company (pattern alignment, never historically-asked claims)."""
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
    """Get pattern-relevant coding patterns for this company (pattern alignment, never historically-asked claims)."""
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
    Pulls verified questions from the in-memory canonical bank matching the
    company's pattern. Thin sections serve fewer real questions — no padding.
    """
    company = INDIAN_COMPANIES.get(req.company_id.lower())
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    sections = get_company_mock_sections(req.company_id)
    if not sections:
        raise HTTPException(status_code=400, detail="No test sections available")

    # Verified company bank first (in-memory, Residency Rule + No-LLM Bank
    # Rule): explicit company tags over TRUSTED stock, general verified
    # backfill. Thin sections serve FEWER REAL questions — never fabricated
    # placeholders, never invented answers.
    from app.services import question_store
    bank = question_store.company_verified_bank(req.company_id)
    tagged_ids = {q.get("id") for q in bank["items"]}

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

            pool = question_store.find(query).only_verified().to_list()
            pool.sort(key=lambda q: (0 if q.get("id") in tagged_ids else 1,))

            section_questions = []
            for q in random.sample(pool, min(section["questions"], 5, len(pool))) if pool else []:
                doc = question_store.get_question_for_serving(q.get("id")) or dict(q)
                doc["id"] = str(q.get("id", ""))
                for k in ("solution", "hidden_test_cases", "hidden_testcases"):
                    doc.pop(k, None)
                section_questions.append(doc)

            all_questions.append({
                "section_name": section["name"],
                "section_type": section.get("types", ["coding"])[0],
                "time_minutes": section["time_minutes"],
                "questions": section_questions,
            })

        else:
            # Aptitude/Verbal/English sections — verified MCQs, client-safe:
            # answer keys and explanations are never exposed.
            pool = question_store.find(
                {"type": {"$in": ["aptitude", "behavioral"]}}
            ).only_verified().to_list()
            pool.sort(key=lambda q: (0 if q.get("id") in tagged_ids else 1,))

            section_questions = []
            for q in random.sample(pool, min(section["questions"], 10, len(pool))) if pool else []:
                doc = question_store.get_question_for_serving(q.get("id")) or dict(q)
                doc["id"] = str(q.get("id", ""))
                for k in ("correct_answer", "correct_index", "_correct_index",
                           "_explanation", "explanation", "solution"):
                    doc.pop(k, None)
                section_questions.append(doc)

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
