from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.database import users_collection, company_prep_collection
from app.middleware.auth import get_current_user
from app.services.ai import generate_behavioral_question, generate_interview_tips, generate_coding_challenge
from app.services.usage import check_and_reset_monthly_usage, can_use_feature
from app.config import get_settings
from bson import ObjectId

router = APIRouter(prefix="/api/company", tags=["company-prep"])
settings = get_settings()

TOP_COMPANIES = {
    "google": {
        "name": "Google",
        "leadership_principles": ["Lead by example", "Care deeply", "Be humble", "Be authentic"],
        "interview_rounds": ["Phone Screen", "Technical Phone Screen", "Onsite (4-5 rounds)"],
        "focus_areas": ["Coding", "System Design", "Googleyness", "General Cognitive Ability"],
    },
    "amazon": {
        "name": "Amazon",
        "leadership_principles": ["Customer Obsession", "Ownership", "Invent and Simplify", "Are Right, A Lot", "Learn and Be Curious", "Hire and Develop the Best", "Insist on the Highest Standards", "Think Big", "Bias for Action", "Frugality", "Earn Trust", "Dive Deep", "Have Backbone; Disagree and Commit", "Deliver Results"],
        "interview_rounds": ["Phone Screen", "Online Assessment", "Onsite (5 rounds)"],
        "focus_areas": ["Leadership Principles", "Coding", "System Design", "Behavioral"],
    },
    "meta": {
        "name": "Meta (Facebook)",
        "leadership_principles": ["Move Fast", "Be Bold", "Focus on Impact", "Build Social Value", "Be Open", "Meta Values"],
        "interview_rounds": ["Phone Screen", "Onsite (3-4 rounds)"],
        "focus_areas": ["Coding", "System Design", "Behavioral", "Product Sense"],
    },
    "microsoft": {
        "name": "Microsoft",
        "leadership_principles": ["Growth Mindset", "Customer-Obsessed", "Diverse and Inclusive", "One Microsoft", "Making a difference"],
        "interview_rounds": ["Phone Screen", "Onsite (3-5 rounds)"],
        "focus_areas": ["Coding", "System Design", "Behavioral", "Azure Knowledge"],
    },
    "apple": {
        "name": "Apple",
        "leadership_principles": ["Attention to Detail", "Secrecy", "Collaboration", "Excellence"],
        "interview_rounds": ["Phone Screen", "Onsite (6-8 rounds)"],
        "focus_areas": ["Coding", "System Design", "Domain Expertise", "Culture Fit"],
    },
    "netflix": {
        "name": "Netflix",
        "leadership_principles": ["Judgment", "Communication", "Impact", "Curiosity", "Innovation", "Courage", "Passion", "Inclusion", "Integrity", "Selflessness"],
        "interview_rounds": ["Phone Screen", "Take Home", "Onsite (4-6 rounds)"],
        "focus_areas": ["Coding", "System Design", "Culture Fit", "Impact"],
    },
    "tcs": {
        "name": "TCS",
        "interview_rounds": ["Aptitude Test", "Technical Interview", "HR Interview"],
        "focus_areas": ["Aptitude", "Technical Basics", "Communication"],
    },
    "infosys": {
        "name": "Infosys",
        "interview_rounds": ["Aptitude Test", "Technical Interview", "HR Interview"],
        "focus_areas": ["Aptitude", "Programming Basics", "Soft Skills"],
    },
    "wipro": {
        "name": "Wipro",
        "interview_rounds": ["Aptitude Test", "Technical Interview", "HR Interview"],
        "focus_areas": ["Aptitude", "Technical Fundamentals", "Communication"],
    },
}


@router.get("/companies")
async def get_companies():
    return {
        "companies": [
            {
                "id": key,
                "name": info["name"],
                "leadership_principles": info.get("leadership_principles", []),
                "interview_rounds": info.get("interview_rounds", []),
                "focus_areas": info.get("focus_areas", []),
            }
            for key, info in TOP_COMPANIES.items()
        ]
    }


class BehavioralRequest(BaseModel):
    company: str
    role: str


class TipsRequest(BaseModel):
    company: str
    role: str
    round_type: str


class CodingChallengeRequest(BaseModel):
    difficulty: str = "medium"
    topic: str = "arrays"
    language: str = "python"


@router.post("/behavioral")
async def get_behavioral_question(req: BehavioralRequest, user=Depends(get_current_user)):
    company_info = TOP_COMPANIES.get(req.company.lower(), {})
    leadership_principles = company_info.get("leadership_principles", [])

    question = await generate_behavioral_question(req.company, req.role, leadership_principles)

    return {
        "company": req.company,
        "role": req.role,
        "question": question,
    }


@router.post("/tips")
async def get_interview_tips(req: TipsRequest, user=Depends(get_current_user)):
    tips = await generate_interview_tips(req.company, req.role, req.round_type)

    return {
        "company": req.company,
        "role": req.role,
        "round_type": req.round_type,
        "tips": tips,
    }


@router.post("/coding-challenge")
async def get_coding_challenge(req: CodingChallengeRequest, user=Depends(get_current_user)):
    challenge = await generate_coding_challenge(req.difficulty, req.topic, req.language)

    return {
        "challenge": challenge,
    }


@router.get("/{company}/guide")
async def get_company_guide(company: str, user=Depends(get_current_user)):
    company_info = TOP_COMPANIES.get(company.lower())

    if not company_info:
        raise HTTPException(status_code=404, detail=f"Company '{company}' not found. Available: {list(TOP_COMPANIES.keys())}")

    return {
        "company": company_info["name"],
        "interview_process": company_info.get("interview_rounds", []),
        "focus_areas": company_info.get("focus_areas", []),
        "leadership_principles": company_info.get("leadership_principles", []),
        "tips": [
            f"Research {company_info['name']}'s recent projects and products",
            f"Practice {', '.join(company_info.get('focus_areas', ['coding'])[:3])}",
            "Prepare STAR method stories for behavioral questions",
            "Review the company's engineering blog for insights",
        ],
    }
