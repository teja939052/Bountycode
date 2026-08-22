from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.database import users_collection, company_prep_collection
from app.middleware.auth import get_current_user
from app.services.ai import generate_behavioral_question, generate_interview_tips, generate_coding_challenge
from app.services.usage import check_and_reset_monthly_usage, can_use_feature
from app.config import get_settings
from app.services.response_cache import cached
from bson import ObjectId

router = APIRouter(prefix="/api/v1/company", tags=["company-prep"])
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
    "accenture": {
        "name": "Accenture",
        "interview_rounds": ["Aptitude Test", "Technical Round", "Managerial Round"],
        "focus_areas": ["Aptitude", "Programming Basics", "Client Communication"],
    },
    "cognizant": {
        "name": "Cognizant",
        "interview_rounds": ["Aptitude Test", "Technical Interview", "HR Interview"],
        "focus_areas": ["Aptitude", "Coding Basics", "Communication"],
    },
    "capgemini": {
        "name": "Capgemini",
        "interview_rounds": ["Aptitude Test", "Technical Interview", "HR Interview"],
        "focus_areas": ["Aptitude", "Core CS", "Problem Solving"],
    },
    "hcl-tech": {
        "name": "HCL Tech",
        "interview_rounds": ["Aptitude Test", "Technical Interview", "HR Interview"],
        "focus_areas": ["Aptitude", "Programming", "Soft Skills"],
    },
    "tech-mahindra": {
        "name": "Tech Mahindra",
        "interview_rounds": ["Aptitude Test", "Technical Interview", "HR Interview"],
        "focus_areas": ["Aptitude", "Coding Basics", "Communication"],
    },
    "adobe": {
        "name": "Adobe",
        "leadership_principles": ["Customer obsession", "Innovation", "Craftsmanship", "Collaboration"],
        "interview_rounds": ["Phone Screen", "Technical Round", "Onsite"],
        "focus_areas": ["Coding", "Design", "Product Thinking", "Communication"],
    },
    "oracle": {
        "name": "Oracle",
        "leadership_principles": ["Customer success", "Technical depth", "Ownership", "Execution"],
        "interview_rounds": ["Phone Screen", "Technical Round", "Manager Round"],
        "focus_areas": ["Coding", "Databases", "System Design", "Enterprise Thinking"],
    },
    "salesforce": {
        "name": "Salesforce",
        "leadership_principles": ["Trust", "Customer success", "Equality", "Innovation"],
        "interview_rounds": ["Phone Screen", "Technical Round", "Behavioral Round"],
        "focus_areas": ["Coding", "System Design", "Product Sense", "Behavioral"],
    },
    "uber": {
        "name": "Uber",
        "leadership_principles": ["Move fast", "Build for scale", "Ownership", "Bias for action"],
        "interview_rounds": ["Phone Screen", "Coding Round", "System Design Round"],
        "focus_areas": ["Coding", "Distributed Systems", "Real-time Design", "Problem Solving"],
    },
}


def _build_prep_mix(company_key: str, company_info: dict) -> list:
    focus = {area.lower() for area in company_info.get("focus_areas", [])}

    if company_key in {"amazon"}:
        return [
            {"track": "behavioral", "weight": 40, "questions": 8, "reason": "Leadership Principles dominate the loop."},
            {"track": "coding", "weight": 30, "questions": 6, "reason": "Expect strong algorithmic coding rounds."},
            {"track": "system_design", "weight": 20, "questions": 4, "reason": "Design trade-offs matter for mid-level+ roles."},
            {"track": "aptitude", "weight": 10, "questions": 2, "reason": "Useful for campus and online assessment prep."},
        ]

    if company_key in {"google", "meta", "microsoft", "uber", "adobe", "oracle", "salesforce"}:
        return [
            {"track": "coding", "weight": 45, "questions": 10, "reason": "Core algorithmic depth is a major hiring signal."},
            {"track": "system_design", "weight": 25, "questions": 5, "reason": "Architecture and trade-offs are heavily evaluated."},
            {"track": "behavioral", "weight": 20, "questions": 4, "reason": "Communication and collaboration still matter."},
            {"track": "aptitude", "weight": 10, "questions": 2, "reason": "Light aptitude refreshers help round out prep."},
        ]

    if company_key in {"tcs", "infosys", "wipro", "accenture", "cognizant", "capgemini", "hcl-tech", "tech-mahindra"}:
        return [
            {"track": "aptitude", "weight": 45, "questions": 12, "reason": "Campus drives usually start with aptitude filtering."},
            {"track": "coding", "weight": 30, "questions": 8, "reason": "Basic DS and scripting problems are common."},
            {"track": "behavioral", "weight": 15, "questions": 4, "reason": "HR and communication rounds are decisive."},
            {"track": "technical_basics", "weight": 10, "questions": 3, "reason": "CS fundamentals often decide the final round."},
        ]

    if "aptitude" in focus:
        return [
            {"track": "aptitude", "weight": 40, "questions": 10, "reason": "This company prioritizes speed and accuracy."},
            {"track": "coding", "weight": 30, "questions": 6, "reason": "Coding still appears in technical rounds."},
            {"track": "behavioral", "weight": 20, "questions": 4, "reason": "Clear communication and attitude matter."},
            {"track": "system_design", "weight": 10, "questions": 2, "reason": "Only relevant for stronger engineering roles."},
        ]

    return [
        {"track": "coding", "weight": 35, "questions": 8, "reason": "A strong coding base is a safe default."},
        {"track": "behavioral", "weight": 25, "questions": 5, "reason": "STAR stories are universally useful."},
        {"track": "system_design", "weight": 25, "questions": 5, "reason": "Higher-level thinking rounds out the prep mix."},
        {"track": "aptitude", "weight": 15, "questions": 3, "reason": "Useful for aptitude screening and warm-up."},
    ]


def _build_prep_modules(company_key: str, company_info: dict) -> list:
    mix = _build_prep_mix(company_key, company_info)
    focus_areas = company_info.get("focus_areas", [])
    return [
        {
            "title": "Company Snapshot",
            "description": f"Understand how {company_info['name']} interviews and what signals they reward.",
            "focus": focus_areas[:3],
        },
        {
            "title": "Question Mix",
            "description": "Spend prep time in proportion to the likely interview distribution.",
            "focus": [f"{item['track'].replace('_', ' ').title()} - {item['weight']}%" for item in mix],
        },
        {
            "title": "Depth Drill",
            "description": "Solve harder variants, explain trade-offs, and defend edge cases aloud.",
            "focus": ["Hidden test cases", "Follow-up questions", "Complexity analysis"],
        },
    ]


@router.get("/companies")
@cached(ttl=3600, key_prefix="company")
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

    question = await generate_behavioral_question(req.company, req.role)

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
@cached(ttl=3600, key_prefix="company")
async def get_company_guide(company: str, user=Depends(get_current_user)):
    company_info = TOP_COMPANIES.get(company.lower())

    if not company_info:
        raise HTTPException(status_code=404, detail=f"Company '{company}' not found. Available: {list(TOP_COMPANIES.keys())}")

    company_key = company.lower()

    return {
        "company": company_info["name"],
        "interview_process": company_info.get("interview_rounds", []),
        "focus_areas": company_info.get("focus_areas", []),
        "leadership_principles": company_info.get("leadership_principles", []),
        "question_mix": _build_prep_mix(company_key, company_info),
        "prep_modules": _build_prep_modules(company_key, company_info),
        "tips": [
            f"Research {company_info['name']}'s recent projects and products",
            f"Practice {', '.join(company_info.get('focus_areas', ['coding'])[:3])}",
            "Prepare STAR method stories for behavioral questions",
            "Review the company's engineering blog for insights",
        ],
    }
