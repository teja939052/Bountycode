from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from app.middleware.auth import get_current_user
from app.services.resume_engine import ResumeEngine
from app.services.coding_engine import CodingEngine
from app.services.behavioral_engine import BehavioralEngine
from app.services.free_ats_tool import FreeATSTool
from app.services.ats_semantic import semantic_score
from app.services.monetization import check_feature_access, record_feature_usage
from app.services.ai import chat_completion, parse_json

router = APIRouter(prefix="/api/v1/enhanced", tags=["enhanced"])

# Initialize engines
resume_engine = ResumeEngine()
coding_engine = CodingEngine()
behavioral_engine = BehavioralEngine()
free_ats = FreeATSTool()


# ============================================
# FREE ATS TOOL (Marketing - No auth required)
# ============================================

class FreeATSRequest(BaseModel):
    resume_text: str


@router.post("/free/ats-check")
async def free_ats_check(req: FreeATSRequest):
    """
    Free ATS checker - the marketing hook.
    No auth required. Zero LLM cost. Algorithmic only.
    """
    return free_ats.analyze(req.resume_text)


# ============================================
# RESUME FEATURES (Auth required)
# ============================================

class ImproveBulletRequest(BaseModel):
    bullet: str
    job_role: str = ""


class ImproveBulletsRequest(BaseModel):
    bullets: List[str]
    job_role: str = ""


class TailorResumeRequest(BaseModel):
    resume_text: str
    job_description: str
    job_role: str = ""


class MissingBulletRequest(BaseModel):
    resume_text: str
    job_description: str
    missing_skill: str


@router.post("/resume/improve-bullet")
async def improve_single_bullet(req: ImproveBulletRequest, user=Depends(get_current_user)):
    # Check access
    access = await check_feature_access(user["id"], "resume_bullet_improve")
    if not access["allowed"]:
        raise HTTPException(status_code=403, detail=access.get("upgrade_message", "Daily limit reached"))

    result = await resume_engine.improve_bullet_strict(req.bullet, req.job_role)
    await record_feature_usage(user["id"], "resume_bullet_improve")
    return result


@router.post("/resume/improve-bullets")
async def improve_multiple_bullets(req: ImproveBulletsRequest, user=Depends(get_current_user)):
    access = await check_feature_access(user["id"], "resume_bullet_improve")
    if not access["allowed"]:
        raise HTTPException(status_code=403, detail=access.get("upgrade_message", "Daily limit reached"))

    results = []
    for bullet in req.bullets:
        if bullet.strip():
            result = await resume_engine.improve_bullet_strict(bullet, req.job_role)
            results.append(result)
            await record_feature_usage(user["id"], "resume_bullet_improve")
    return {"improvements": results}


@router.post("/resume/ats-checklist")
async def get_ats_checklist(resume_text: str, user=Depends(get_current_user)):
    return resume_engine.verify_ats_formatting(resume_text)


@router.post("/resume/tailor")
async def tailor_resume(req: TailorResumeRequest, user=Depends(get_current_user)):
    access = await check_feature_access(user["id"], "resume_tailor")
    if not access["allowed"]:
        raise HTTPException(status_code=403, detail=access.get("upgrade_message", "Daily limit reached"))

    result = await resume_engine.tailor_resume_strict(req.resume_text, req.job_description, req.job_role)
    await record_feature_usage(user["id"], "resume_tailor")
    return result


@router.post("/resume/missing-bullet")
async def generate_missing_bullet(req: MissingBulletRequest, user=Depends(get_current_user)):
    """The wallet puller - generates a bullet for missing skills."""
    access = await check_feature_access(user["id"], "missing_bullet_generator")
    if not access["allowed"]:
        raise HTTPException(status_code=403, detail="Pro feature - Upgrade to generate missing bullets")

    result = await resume_engine.generate_missing_bullet(
        req.resume_text, req.job_description, req.missing_skill
    )
    await record_feature_usage(user["id"], "missing_bullet_generator")
    return result


# ============================================
# CODING FEATURES
# ============================================

class CompanyCodingRequest(BaseModel):
    company: str
    role: str = "SDE"
    difficulty: str = None


class CodeReviewRequest(BaseModel):
    code: str
    language: str
    problem_description: str


class HintRequest(BaseModel):
    problem_description: str
    current_code: str = ""
    hint_level: int = 1


class ConceptRequest(BaseModel):
    concept: str
    level: str = "intermediate"


class CreativeMindRequest(BaseModel):
    problem_description: str
    code: str = ""
    language: str = "python"
    topic: str = ""
    mode: str = "mentor"


@router.post("/coding/company-challenge")
async def company_coding_challenge(req: CompanyCodingRequest, user=Depends(get_current_user)):
    access = await check_feature_access(user["id"], "coding_challenge")
    if not access["allowed"]:
        raise HTTPException(status_code=403, detail=access.get("upgrade_message", "Daily limit reached"))

    result = await coding_engine.generate_challenge_with_hints(req.company, req.role, req.difficulty)
    await record_feature_usage(user["id"], "coding_challenge")
    return result


@router.post("/coding/interviewer-feedback")
async def interviewer_feedback(req: CodeReviewRequest, user=Depends(get_current_user)):
    access = await check_feature_access(user["id"], "interview_practice")
    if not access["allowed"]:
        raise HTTPException(status_code=403, detail=access.get("upgrade_message", "Daily limit reached"))

    result = await coding_engine.evaluate_as_interviewer(req.code, req.language, req.problem_description)
    await record_feature_usage(user["id"], "interview_practice")
    return result


@router.post("/coding/hint")
async def get_hint(req: HintRequest, user=Depends(get_current_user)):
    # Level 3 hints are Pro only
    if req.hint_level >= 3:
        access = await check_feature_access(user["id"], "hint_level_3")
        if not access["allowed"]:
            raise HTTPException(status_code=403, detail="Level 3 hints are a Pro feature")

    result = await coding_engine.get_hint(req.problem_description, req.current_code, req.hint_level)
    await record_feature_usage(user["id"], f"hint_level_{req.hint_level}")
    return result


@router.post("/coding/explain")
async def explain_concept(req: ConceptRequest, user=Depends(get_current_user)):
    access = await check_feature_access(user["id"], "concept_explanation")
    if not access["allowed"]:
        raise HTTPException(status_code=403, detail=access.get("upgrade_message", "Daily limit reached"))

    result = await coding_engine.explain_concept(req.concept, req.level)
    await record_feature_usage(user["id"], "concept_explanation")
    return result


@router.post("/coding/creative-mind")
async def creative_mind(req: CreativeMindRequest, user=Depends(get_current_user)):
    access = await check_feature_access(user["id"], "creative_mind")
    if not access["allowed"]:
        raise HTTPException(status_code=403, detail=access.get("upgrade_message", "Daily limit reached"))

    system_prompt = f"""You are PlacementPro's creative coding coach.
Turn the problem into something memorable, motivating, and practical.
Stay accurate, but make the answer feel like a mini adventure or boss battle.

Respond in valid JSON with:
{{
  "title": "Short punchy title",
  "mission": "One-sentence mission statement",
  "analogy": "A vivid analogy that explains the core idea",
  "first_move": "The very first action the student should take",
  "micro_challenge": "A fun mini challenge to try next",
  "edge_case_watch": "A reminder about a tricky edge case",
  "pep_talk": "A short motivational line",
  "mode": "{req.mode}"
}}

Keep it concise, useful, and uplifting. Avoid generic fluff."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"""Problem:
{req.problem_description}

Language: {req.language}
Topic: {req.topic or "general"}
Current code:
```{req.language}
{req.code or "// no code yet"}
```"""},
    ]

    result = await chat_completion(messages, max_tokens=700)
    parsed = parse_json(result)
    parsed.setdefault("title", "Creative Mind")
    parsed.setdefault("mission", "Break the problem into a win you can see.")
    parsed.setdefault("analogy", "Think of it like finding the shortest path through a puzzle room.")
    parsed.setdefault("first_move", "Start with the brute-force version, then trim the waste.")
    parsed.setdefault("micro_challenge", "Can you explain the solution in 3 bullet points before coding?")
    parsed.setdefault("edge_case_watch", "Check empty input, duplicates, and off-by-one boundaries.")
    parsed.setdefault("pep_talk", "You already have the shape of the solution. Now let the code catch up.")
    parsed["mode"] = req.mode

    await record_feature_usage(user["id"], "creative_mind")
    return parsed


# ============================================
# BEHAVIORAL FEATURES
# ============================================

class STARRequest(BaseModel):
    question: str
    answer: str
    company: str = ""


class STARTemplateRequest(BaseModel):
    question: str
    company: str = ""


class PracticeQuestionsRequest(BaseModel):
    company: str
    role: str
    count: int = 5


@router.post("/behavioral/evaluate-star")
async def evaluate_star(req: STARRequest, user=Depends(get_current_user)):
    access = await check_feature_access(user["id"], "star_evaluation")
    if not access["allowed"]:
        raise HTTPException(status_code=403, detail=access.get("upgrade_message", "Daily limit reached"))

    result = await behavioral_engine.evaluate_star_strict(req.question, req.answer, req.company)
    await record_feature_usage(user["id"], "star_evaluation")
    return result


@router.post("/behavioral/star-template")
async def star_template(req: STARTemplateRequest, user=Depends(get_current_user)):
    return await behavioral_engine.generate_star_template(req.question, req.company)


@router.post("/behavioral/practice-questions")
async def practice_questions(req: PracticeQuestionsRequest, user=Depends(get_current_user)):
    return {"questions": await behavioral_engine.generate_practice_questions(req.company, req.role, req.count)}


# ============================================
# SEMANTIC ATS (Upgrade path)
# ============================================

class SemanticATSRequest(BaseModel):
    resume_text: str
    job_description: str = ""


@router.post("/ats/semantic")
async def semantic_ats(req: SemanticATSRequest, user=Depends(get_current_user)):
    """
    Hybrid ATS score: semantic similarity + keyword/formatting checks.
    Pro-only deeper analysis; free gets overall score.
    """
    result = semantic_score(req.resume_text, req.job_description or None)
    return result
