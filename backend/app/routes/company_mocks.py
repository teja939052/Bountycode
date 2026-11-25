"""
Company-Specific Mock Portals — Real interview simulation for specific companies.
Each company has its own format, difficulty, and focus areas.

Migrated to PostgreSQL: assessment_attempts (assessment_type="company_mock").
"""
from datetime import datetime, timezone, timedelta
import random
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update

from app.middleware.auth import get_current_user
from app.database import get_session
from app.services.postgres_assessments import PostgresAssessmentService
from app.services.structured_logging import get_logger, log_context, request_id_var
from app.services.code_executor import CodeExecutionEngine

router = APIRouter(prefix="/api/v1/company-mocks", tags=["company-mocks"])
logger = get_logger(__name__)

# Company-specific mock test configurations
COMPANY_MOCK_CONFIGS = {
    "google": {
        "name": "Google SWE Mock",
        "description": "Google-style coding interview simulation",
        "rounds": [
            {
                "name": "Online Assessment",
                "type": "coding",
                "questions": 2,
                "time_minutes": 90,
                "difficulty": "medium",
                "focus": ["Arrays", "Dynamic Programming", "Graphs"],
                "format": "Each problem has 2 visible and 3 hidden test cases",
            },
            {
                "name": "Technical Phone Screen",
                "type": "coding",
                "questions": 1,
                "time_minutes": 45,
                "difficulty": "hard",
                "focus": ["Trees", "Graphs", "System Design"],
                "format": "One hard problem with follow-ups",
            },
            {
                "name": "Onsite Coding",
                "type": "coding",
                "questions": 2,
                "time_minutes": 60,
                "difficulty": "hard",
                "focus": ["Advanced Data Structures", "Algorithms"],
                "format": "Two medium-hard problems",
            },
            {
                "name": "System Design",
                "type": "system_design",
                "questions": 1,
                "time_minutes": 45,
                "difficulty": "hard",
                "focus": ["Scalability", "Distributed Systems"],
                "format": "Design a large-scale system",
            },
            {
                "name": "Behavioral",
                "type": "behavioral",
                "questions": 3,
                "time_minutes": 30,
                "difficulty": "medium",
                "focus": ["Leadership", "Collaboration", "Problem Solving"],
                "format": "STAR method questions",
            },
        ],
        "total_time_minutes": 270,
        "passing_score": 70,
        "interview_tips": [
            "Think out loud - Google values your thought process",
            "Ask clarifying questions before coding",
            "Start with a brute force approach, then optimize",
            "Discuss time and space complexity",
            "Handle edge cases explicitly",
        ],
    },
    "amazon": {
        "name": "Amazon SDE Mock",
        "description": "Amazon-style interview with Leadership Principles",
        "rounds": [
            {
                "name": "Online Assessment",
                "type": "coding",
                "questions": 2,
                "time_minutes": 70,
                "difficulty": "medium",
                "focus": ["Arrays", "Strings", "Linked Lists"],
                "format": "Two coding problems",
            },
            {
                "name": "Technical Phone Screen",
                "type": "coding",
                "questions": 1,
                "time_minutes": 45,
                "difficulty": "medium",
                "focus": ["Trees", "Dynamic Programming"],
                "format": "One coding problem",
            },
            {
                "name": "Loop Round 1 - Coding",
                "type": "coding",
                "questions": 1,
                "time_minutes": 45,
                "difficulty": "medium",
                "focus": ["Arrays", "Trees"],
                "format": "One coding problem",
            },
            {
                "name": "Loop Round 2 - System Design",
                "type": "system_design",
                "questions": 1,
                "time_minutes": 45,
                "difficulty": "medium",
                "focus": ["Scalability", "API Design"],
                "format": "System design question",
            },
            {
                "name": "Loop Round 3 - Leadership Principles",
                "type": "behavioral",
                "questions": 4,
                "time_minutes": 45,
                "difficulty": "medium",
                "focus": ["Customer Obsession", "Ownership", "Bias for Action", "Dive Deep"],
                "format": "Behavioral questions using STAR method",
            },
        ],
        "total_time_minutes": 250,
        "passing_score": 70,
        "leadership_principles": [
            "Customer Obsession",
            "Ownership",
            "Invent and Simplify",
            "Are Right, A Lot",
            "Learn and Be Curious",
            "Hire and Develop the Best",
            "Insist on the Highest Standards",
            "Think Big",
            "Bias for Action",
            "Frugality",
            "Earn Trust",
            "Dive Deep",
            "Have Backbone; Disagree and Commit",
            "Deliver Results",
        ],
        "interview_tips": [
            "Use STAR method for all behavioral questions",
            "Reference Amazon's Leadership Principles explicitly",
            "Show customer obsession in your answers",
            "Demonstrate ownership and accountability",
            "Be ready for follow-up questions",
        ],
    },
    "microsoft": {
        "name": "Microsoft SDE Mock",
        "description": "Microsoft-style interview focusing on clean code",
        "rounds": [
            {
                "name": "Online Assessment",
                "type": "coding",
                "questions": 2,
                "time_minutes": 60,
                "difficulty": "medium",
                "focus": ["Arrays", "Strings", "Trees"],
                "format": "Two coding problems",
            },
            {
                "name": "Technical Phone Screen",
                "type": "coding",
                "questions": 1,
                "time_minutes": 45,
                "difficulty": "medium",
                "focus": ["Data Structures", "Algorithms"],
                "format": "One coding problem with discussion",
            },
            {
                "name": "Onsite Round 1",
                "type": "coding",
                "questions": 1,
                "time_minutes": 45,
                "difficulty": "hard",
                "focus": ["Advanced Algorithms"],
                "format": "One hard coding problem",
            },
            {
                "name": "Onsite Round 2 - System Design",
                "type": "system_design",
                "questions": 1,
                "time_minutes": 45,
                "difficulty": "medium",
                "focus": ["Scalability", "Cloud"],
                "format": "System design question",
            },
            {
                "name": "Onsite Round 3 - Behavioral",
                "type": "behavioral",
                "questions": 3,
                "time_minutes": 30,
                "difficulty": "medium",
                "focus": ["Teamwork", "Problem Solving", "Growth Mindset"],
                "format": "Behavioral questions",
            },
        ],
        "total_time_minutes": 225,
        "passing_score": 70,
        "interview_tips": [
            "Write clean, readable code",
            "Microsoft values growth mindset",
            "Show collaboration and teamwork",
            "Discuss trade-offs in your solutions",
            "Ask thoughtful questions about the team",
        ],
    },
    "tcs": {
        "name": "TCS NQT Simulation",
        "description": "TCS National Qualifier Test — two-stage simulation (Foundation aptitude + Advanced programming). Pattern-relevant.",
        "rounds": [
            {
                "name": "Foundation: Numerical Ability",
                "type": "aptitude",
                "questions": 21,
                "time_minutes": 40,
                "difficulty": "easy",
                "focus": ["Percentages", "Time & Work", "Profit/Loss", "Averages", "Probability"],
                "format": "Multiple choice questions",
            },
            {
                "name": "Foundation: Reasoning Ability",
                "type": "logical",
                "questions": 25,
                "time_minutes": 50,
                "difficulty": "easy",
                "focus": ["Number Series", "Coding-Decoding", "Blood Relations", "Direction Sense"],
                "format": "Multiple choice questions",
            },
            {
                "name": "Foundation: Verbal Ability",
                "type": "verbal",
                "questions": 20,
                "time_minutes": 30,
                "difficulty": "easy",
                "focus": ["Sentence Completion", "Grammar", "Comprehension"],
                "format": "Multiple choice questions",
            },
            {
                "name": "Advanced: Programming Logic (MCQ)",
                "type": "cs_fundamentals",
                "questions": 10,
                "time_minutes": 25,
                "difficulty": "medium",
                "focus": ["Output prediction", "Pointers/data structures", "Debugging"],
                "format": "Multiple choice questions",
            },
            {
                "name": "Advanced: Coding",
                "type": "coding",
                "questions": 2,
                "time_minutes": 60,
                "difficulty": "medium",
                "focus": ["Arrays", "Strings", "Basic Logic"],
                "format": "Two coding problems",
            },
        ],
        "total_time_minutes": 190,
        "passing_score": 60,
        "provenance": "pattern-relevant",
        "interview_tips": [
            "No negative marking in the real NQT — never leave a question unanswered",
            "Foundation sections are time-boxed: move when the timer forces section end",
            "Practice basic coding patterns — the Advanced coding round favors clean, working solutions",
            "Review aptitude formulas (percentages, time & work) before attempting",
            "TCS values accuracy over complexity",
        ],
    },
}


@router.get("/companies")
async def list_company_mocks(user=Depends(get_current_user)):
    """List all available company-specific mock tests."""
    companies = []
    for company_id, config in COMPANY_MOCK_CONFIGS.items():
        companies.append({
            "id": company_id,
            "name": config["name"],
            "description": config["description"],
            "total_time_minutes": config["total_time_minutes"],
            "rounds_count": len(config["rounds"]),
            "passing_score": config["passing_score"],
        })
    return {"companies": companies}


@router.get("/{company_id}/config")
async def get_company_config(company_id: str, user=Depends(get_current_user)):
    """Get detailed configuration for a company mock test."""
    config = COMPANY_MOCK_CONFIGS.get(company_id.lower())
    if not config:
        raise HTTPException(status_code=404, detail="Company not found")
    return config


@router.post("/{company_id}/start")
async def start_company_mock(
    company_id: str,
    round_name: Optional[str] = None,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Start a company-specific mock test."""
    config = COMPANY_MOCK_CONFIGS.get(company_id.lower())
    if not config:
        raise HTTPException(status_code=404, detail="Company not found")

    # Determine which round to start
    if round_name:
        target_round = next((r for r in config["rounds"] if r["name"] == round_name), None)
        if not target_round:
            raise HTTPException(status_code=404, detail="Round not found")
        rounds_to_run = [target_round]
    else:
        rounds_to_run = config["rounds"]

    # Only coding rounds have a trusted grading path in this service today.
    all_questions = []
    executable_rounds = []
    unsupported_rounds = []
    from app.services import question_store

    company_bank = question_store.company_verified_bank(company_id)
    tagged_ids = {q.get("id") for q in company_bank.get("items", [])}
    for round_config in rounds_to_run:
        if round_config.get("type") != "coding":
            unsupported_rounds.append(round_config["name"])
            continue
        pool = question_store.find({
            "type": "coding",
            "difficulty": round_config["difficulty"],
            "topic": {"$in": round_config["focus"]},
        }).only_verified().to_list()
        pool.sort(key=lambda q: (0 if q.get("id") in tagged_ids else 1,))
        selected = random.sample(pool, min(round_config["questions"], len(pool)))
        if not selected:
            unsupported_rounds.append(round_config["name"])
            continue
        executable_rounds.append(round_config)
        for q in selected:
            doc = question_store.get_question_for_serving(q.get("id")) or dict(q)
            doc["id"] = q.get("id")
            doc["round"] = round_config["name"]
            doc.setdefault("topics", [doc.get("topic", "General")])
            doc.setdefault("company", company_id)
            all_questions.append(doc)

    if not all_questions:
        raise HTTPException(
            status_code=409,
            detail="No verified coding questions are currently available for this company mock.",
        )

    # Create mock test session in PostgreSQL
    now = datetime.now(timezone.utc)
    ends_at = now + timedelta(minutes=config["total_time_minutes"])

    assessment_service = PostgresAssessmentService(session)
    attempt = await assessment_service.create_assessment_attempt(
        user_id=UUID(user["id"]),
        assessment_id="company_mock",
        variant_id=f"{company_id}",
        idempotency_key=f"company_mock_{user['id']}_{company_id}_{now.isoformat()}",
    )

    # Store session data in attempt metadata
    attempt_metadata = {
        "company": company_id,
        "config": config,
        "rounds": executable_rounds,
        "unsupported_rounds": unsupported_rounds,
        "questions": all_questions,
        "answers": [],
        "current_round": 0,
        "current_question": 0,
        "status": "in_progress",
        "started_at": now.isoformat(),
        "ends_at": ends_at.isoformat(),
        "total_score": 0,
    }

    await session.execute(
        update(attempt.__class__)
        .where(attempt.__class__.id == attempt.id)
        .values(attempt_metadata=attempt_metadata)
    )

    rid = request_id_var.get("")
    logger.info(
        "assessment.attempt.started",
        extra=log_context(
            event="assessment.attempt.started",
            assessment_type="company_mock",
            company=company_id,
            attempt_id=str(attempt.id),
            request_id=rid,
        ),
    )

    # Do not send answer keys or hidden test cases to the browser.
    safe_questions = [
        {
            "id": q.get("id"),
            "question": q.get("question") or q.get("question_title", ""),
            "title": q.get("title") or q.get("question_title", ""),
            "difficulty": q.get("difficulty", "medium"),
            "topic": q.get("topic", "General"),
            "round": q.get("round"),
            "description": q.get("description", ""),
            "examples": q.get("examples", []),
            "constraints": q.get("constraints", []),
            "starter_code": q.get("starter_code", {}),
            "function_name": q.get("function_name", ""),
            "time_limit_seconds": q.get("time_limit_seconds", 10),
            "memory_limit_mb": q.get("memory_limit_mb", 256),
        }
        for q in all_questions
    ]
    return {
        "session_id": str(attempt.id),
        "company": company_id,
        "config": config,
        "rounds": executable_rounds,
        "unsupported_rounds": unsupported_rounds,
        "questions": safe_questions,
        "ends_at": ends_at.isoformat(),
    }


def _safe_question_dict(q: dict) -> dict:
    """Return a client-safe question dict (no answer keys/hidden tests)."""
    return {
        "id": q.get("id"),
        "question": q.get("question") or q.get("question_title", ""),
        "title": q.get("title") or q.get("question_title", ""),
        "difficulty": q.get("difficulty", "medium"),
        "topic": q.get("topic", "General"),
        "round": q.get("round"),
        "description": q.get("description", ""),
        "examples": q.get("examples", []),
        "constraints": q.get("constraints", []),
        "starter_code": q.get("starter_code", {}),
        "function_name": q.get("function_name", ""),
        "time_limit_seconds": q.get("time_limit_seconds", 10),
        "memory_limit_mb": q.get("memory_limit_mb", 256),
    }


async def _load_owned_mock_session(
    assessment_service: PostgresAssessmentService,
    session_id: str,
    user_id: str,
):
    """Load a company mock session while enforcing authenticated ownership."""
    try:
        attempt_id = UUID(session_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid session ID")

    attempt = await assessment_service.get_assessment_attempt(attempt_id)
    if not attempt:
        raise HTTPException(status_code=404, detail="Session not found")

    if str(attempt.user_id) != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return attempt, attempt.attempt_metadata or {}


@router.post("/{session_id}/answer")
async def submit_company_mock_answer(
    session_id: str,
    payload: dict,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Grade an owned mock coding question with the existing hidden-test judge."""
    assessment_service = PostgresAssessmentService(session)
    attempt, metadata = await _load_owned_mock_session(
        assessment_service, session_id, user["id"]
    )

    if metadata.get("status") != "in_progress":
        raise HTTPException(status_code=409, detail="Mock session is not in progress")
    if datetime.now(timezone.utc) >= datetime.fromisoformat(metadata.get("ends_at", datetime.now(timezone.utc).isoformat())):
        raise HTTPException(status_code=409, detail="Mock session has expired")

    question_id = str(payload.get("question_id") or "").strip()
    code = payload.get("code")
    language = str(payload.get("language") or "python").strip().lower()
    if not question_id:
        raise HTTPException(status_code=422, detail="question_id is required")
    if not isinstance(code, str) or not code.strip():
        raise HTTPException(status_code=422, detail="code is required")
    if len(code) > 120000:
        raise HTTPException(status_code=413, detail="Code submission is too large")

    questions = metadata.get("questions", [])
    question = next(
        (q for q in questions if str(q.get("id")) == question_id),
        None,
    )
    if not question:
        raise HTTPException(status_code=404, detail="Question is not part of this session")
    if any(str(a.get("question_id")) == question_id for a in metadata.get("answers", [])):
        raise HTTPException(status_code=409, detail="Question already submitted")

    from app.services import question_store
    trusted_question = question_store.get_question_for_serving(question_id)
    if not trusted_question:
        raise HTTPException(status_code=404, detail="Question content is unavailable")
    hidden_cases = trusted_question.get("hidden_test_cases") or []
    if not hidden_cases:
        raise HTTPException(status_code=409, detail="No hidden grading cases are available")

    engine = CodeExecutionEngine()
    execution = await engine.execute_against_test_cases(
        source_code=code,
        language=language,
        test_cases=[
            {
                "input": case.get("input", ""),
                "expected": case.get("expected", case.get("expected_output", "")),
                "is_hidden": True,
            }
            for case in hidden_cases
        ],
        function_name=trusted_question.get("function_name", "") or "",
    )
    if not execution.get("success", False):
        raise HTTPException(status_code=422, detail=execution.get("error") or "Code execution failed")

    passed_count = int(execution.get("passed_count", 0) or 0)
    total_count = int(execution.get("total_count", len(hidden_cases)) or len(hidden_cases))
    score = float(execution.get("score", 0) or 0)
    all_passed = bool(execution.get("all_passed", False))
    answer = {
        "question_id": question_id,
        "round": question.get("round") or "Coding",
        "language": language,
        "code": code,
        "passed": all_passed,
        "passed_count": passed_count,
        "total_cases": total_count,
        "score": score,
        "submitted_at": datetime.now(timezone.utc).isoformat(),
    }

    answers = metadata.get("answers", [])
    answers.append(answer)

    total_questions = len(questions)
    total_score = metadata.get("total_score", 0) + score / max(total_questions, 1)

    metadata["answers"] = answers
    metadata["total_score"] = total_score
    metadata["updated_at"] = datetime.now(timezone.utc).isoformat()

    await session.execute(
        update(attempt.__class__)
        .where(attempt.__class__.id == attempt.id)
        .values(attempt_metadata=metadata)
    )

    # Evidence emission is best-effort after authoritative grading/persistence.
    try:
        from app.services.study_engine import emit_learning_event
        from app.services.skill_taxonomy import canonical_skill_id
        skill_id = canonical_skill_id(trusted_question.get("topic", "")) or "dsa.uncategorized"
        await emit_learning_event(user["id"], {
            "activity_type": "question_solve",
            "source": "question_bank",
            "skill_id": skill_id,
            "question_id": question_id,
            "passed": all_passed,
            "score": score,
            "time_spent_seconds": max(0, int(payload.get("time_spent_seconds", 0) or 0)),
            "attempt_number": 1,
            "metadata": {
                "company_mock_session_id": session_id,
                "company": metadata.get("company"),
                "difficulty": trusted_question.get("difficulty", "medium"),
                "passed_count": passed_count,
                "total": total_count,
            },
        })
    except Exception:
        pass

    return {
        "success": True,
        "question_id": question_id,
        "is_correct": all_passed,
        "passed_count": passed_count,
        "total_count": total_count,
        "score": score,
        "summary": execution.get("summary", f"{passed_count}/{total_count} test cases passed"),
    }


@router.post("/{session_id}/complete")
async def complete_company_mock(
    session_id: str,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Complete a company mock session idempotently."""
    assessment_service = PostgresAssessmentService(session)
    attempt, metadata = await _load_owned_mock_session(
        assessment_service, session_id, user["id"]
    )

    if metadata.get("status") == "completed":
        return await get_mock_results(assessment_service, attempt, metadata)

    now = datetime.now(timezone.utc)
    metadata["status"] = "completed"
    metadata["completed_at"] = now.isoformat()
    metadata["updated_at"] = now.isoformat()

    await assessment_service.attempt_repo.complete(
        attempt.id, metadata.get("total_score", 0), completed_at=now
    )
    await session.execute(
        update(attempt.__class__)
        .where(attempt.__class__.id == attempt.id)
        .values(attempt_metadata=metadata)
    )

    return await get_mock_results(assessment_service, attempt, metadata)


@router.get("/{session_id}/status")
async def get_mock_status(
    session_id: str,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Get current mock test status."""
    assessment_service = PostgresAssessmentService(session)
    attempt, metadata = await _load_owned_mock_session(
        assessment_service, session_id, user["id"]
    )

    now = datetime.now(timezone.utc)
    ends_at = datetime.fromisoformat(metadata.get("ends_at", now.isoformat()))
    time_remaining = max(0, (ends_at - now).total_seconds())

    questions = metadata.get("questions", [])
    answers = metadata.get("answers", [])

    safe_questions = [_safe_question_dict(q) for q in questions]
    safe_answers = [
        {
            "question_id": answer.get("question_id"),
            "code": answer.get("code", ""),
            "language": answer.get("language", "python"),
            "is_correct": bool(answer.get("passed")),
            "passed_count": answer.get("passed_count", 0),
            "total_count": answer.get("total_cases", 0),
            "score": answer.get("score", 0),
            "summary": f"{answer.get('passed_count', 0)}/{answer.get('total_cases', 0)} hidden tests passed",
        }
        for answer in answers
    ]

    return {
        "session_id": session_id,
        "status": metadata.get("status"),
        "company": metadata.get("company"),
        "time_remaining_seconds": int(time_remaining),
        "current_round": metadata.get("current_round", 0),
        "questions_answered": len(answers),
        "total_questions": len(questions),
        "started_at": metadata.get("started_at"),
        "ends_at": metadata.get("ends_at"),
        "unsupported_rounds": metadata.get("unsupported_rounds", []),
        "answers": safe_answers,
        "questions": safe_questions,
    }


@router.get("/{session_id}/results")
async def get_mock_results(
    session_id: str,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Get complete mock test results."""
    assessment_service = PostgresAssessmentService(session)
    attempt, metadata = await _load_owned_mock_session(
        assessment_service, session_id, user["id"]
    )

    # Calculate round-wise scores
    round_scores = {}
    for answer in metadata.get("answers", []):
        round_name = answer.get("round", "Unknown")
        if round_name not in round_scores:
            round_scores[round_name] = {"total": 0, "score": 0, "count": 0}
        round_scores[round_name]["total"] += answer.get("total_cases", 0)
        round_scores[round_name]["score"] += answer.get("passed_count", 0)
        round_scores[round_name]["count"] += 1

    # Calculate overall score
    total_score = metadata.get("total_score", 0)
    passing_score = metadata.get("config", {}).get("passing_score", 70)
    passed = total_score >= passing_score

    return {
        "session_id": session_id,
        "company": metadata.get("company"),
        "total_score": total_score,
        "passing_score": passing_score,
        "passed": passed,
        "round_scores": round_scores,
        "completed_at": (metadata.get("completed_at") or datetime.now(timezone.utc)).isoformat(),
        "interview_tips": metadata.get("config", {}).get("interview_tips", []),
    }
