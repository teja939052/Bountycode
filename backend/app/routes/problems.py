from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

from app.models.problem import (
    ProblemBase, ProblemCreate, ProblemRead, 
    StudentCodeSubmission, JudgeResult, LockDefinition
)
from app.services.lock_engine import LockEngine, UnifiedJudge
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/v1/problems", tags=["problems"])

# ──────────────────────────────────────────────────────────────────
# In-memory problem store (replace with MongoDB in production)
# ──────────────────────────────────────────────────────────────────

PROBLEMS_DB: Dict[str, ProblemBase] = {}

def _seed_problems() -> None:
    """Populate the in-memory problem store on first load from seed_problems."""
    from pathlib import Path
    seed_module_path = Path(__file__).resolve().parents[2] / "scripts" / "seed_problems.py"
    if seed_module_path.exists():
        import importlib.util
        spec = importlib.util.spec_from_file_location("seed_problems", seed_module_path)
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except Exception:
            # Module imports app.* which may not be resolvable here; fall back quietly.
            return
        for pid, problem in module.seed_problems().items():
            PROBLEMS_DB.setdefault(pid, problem)

_seed_problems()

# Shared singleton engines so lock/SRS state persists across requests.
# (In production these should be backed by MongoDB instead of process memory.)
_LOCK_ENGINE = LockEngine()
_UNIFIED_JUDGE = UnifiedJudge()
_UNIFIED_JUDGE.locks = _LOCK_ENGINE


def get_lock_engine() -> LockEngine:
    return _LOCK_ENGINE


def get_unified_judge() -> UnifiedJudge:
    # Reuse the same LockEngine and SRS so progression/review state persists.
    return _UNIFIED_JUDGE


# ──────────────────────────────────────────────────────────────────
# Problem CRUD
# ──────────────────────────────────────────────────────────────────

@router.post("", response_model=ProblemRead, status_code=201)
async def create_problem(problem: ProblemCreate):
    """Create a new problem with Lock Definition."""
    if problem.id in PROBLEMS_DB:
        raise HTTPException(status_code=409, detail="Problem ID already exists")
    PROBLEMS_DB[problem.id] = problem
    return problem


@router.get("", response_model=List[ProblemRead])
async def list_problems(
    difficulty: Optional[str] = None,
    mode: Optional[str] = None,
    limit: int = Query(50, le=200),
    offset: int = 0,
):
    """List problems with optional filters."""
    problems = list(PROBLEMS_DB.values())
    
    if difficulty:
        problems = [p for p in problems if p.difficulty == difficulty]
    if mode:
        problems = [p for p in problems if p.mode == mode]
    
    return problems[offset:offset + limit]


@router.get("/{problem_id}", response_model=ProblemRead)
async def get_problem(problem_id: str):
    """Get full problem definition including locks and hints."""
    if problem_id not in PROBLEMS_DB:
        raise HTTPException(status_code=404, detail="Problem not found")
    return PROBLEMS_DB[problem_id]


@router.get("/{problem_id}/visible")
async def get_problem_visible(problem_id: str):
    """Get problem without hidden test cases / full solution (for students)."""
    if problem_id not in PROBLEMS_DB:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    problem = PROBLEMS_DB[problem_id]
    # Return only visible parts
    return {
        "id": problem.id,
        "title": problem.title,
        "description": problem.description,
        "mode": problem.mode,
        "difficulty": problem.difficulty,
        "locks": problem.locks,
        "test_cases": [tc for tc in problem.test_cases if not tc.get("is_hidden", False)],
        "hint_graph": problem.hint_graph,
        "learning_goal": problem.learning_goal,
        "time_complexity": problem.time_complexity,
        "space_complexity": problem.space_complexity,
        "estimated_xp": problem.estimated_xp,
    }


# ──────────────────────────────────────────────────────────────────
# Lock Engine Endpoints
# ──────────────────────────────────────────────────────────────────

@router.get("/{problem_id}/lock-state")
async def get_lock_state(
    problem_id: str,
    user=Depends(get_current_user),
    lock_engine: LockEngine = Depends(get_lock_engine),
):
    """Get current lock state for the authenticated user."""
    student_id = user["id"]
    state = lock_engine.get_lock_state(student_id, problem_id)
    problem = PROBLEMS_DB.get(problem_id)
    
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    current_lock = lock_engine.get_current_lock(problem, student_id)
    
    return {
        "problem_id": problem_id,
        "unlocked_locks": state["unlocked_locks"],
        "current_lock": current_lock.dict() if current_lock else None,
        "progress": f"{len(state['unlocked_locks'])}/{len(problem.locks)}",
        "attempts": state["attempts"],
        "hint_index": state["hint_index"],
        "misconceptions_hit": state["misconceptions_hit"],
    }


@router.post("/{problem_id}/reset-locks")
async def reset_locks(
    problem_id: str,
    user=Depends(get_current_user),
    lock_engine: LockEngine = Depends(get_lock_engine),
):
    """Reset lock state for retry."""
    student_id = user["id"]
    lock_engine.reset_lock_state(student_id, problem_id)
    return {"message": "Lock state reset", "problem_id": problem_id}


# ──────────────────────────────────────────────────────────────────
# Judge Endpoints
# ──────────────────────────────────────────────────────────────────

@router.post("/{problem_id}/check-lock", response_model=JudgeResult)
async def check_lock(
    problem_id: str,
    submission: StudentCodeSubmission,
    user=Depends(get_current_user),
    judge: UnifiedJudge = Depends(get_unified_judge),
):
    """
    Check student submission against current lock.
    This is the main "progressive" judge endpoint.
    """
    if problem_id not in PROBLEMS_DB:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    problem = PROBLEMS_DB[problem_id]
    submission.problem_id = problem_id
    student_id = user["id"]
    
    # Run through unified judge
    result = judge.judge(submission, problem, student_id)
    
    # If lock completed, record for SRS
    if result.success and result.mode == "complete":
        judge.record_completion(student_id, problem_id, True)
    elif result.success and result.mode == "lock_unlocked":
        # Could record partial progress
        pass
    elif not result.success:
        # Record failure for SRS (optional)
        judge.record_completion(student_id, problem_id, False)
    
    return result


@router.post("/{problem_id}/run", response_model=JudgeResult)
async def run_full_problem(
    problem_id: str,
    submission: StudentCodeSubmission,
    user=Depends(get_current_user),
    judge: UnifiedJudge = Depends(get_unified_judge),
):
    """
    Run the full problem (all test cases).
    Uses local runtime (Pyodide/Worker) for actual execution.
    """
    if problem_id not in PROBLEMS_DB:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    problem = PROBLEMS_DB[problem_id]
    submission.problem_id = problem_id
    student_id = user["id"]
    
    # In production: call local runtime service
    # For now, return behavioral judgment against all test cases
    
    # Get visible + hidden test cases
    test_cases = problem.test_cases
    if not test_cases:
        raise HTTPException(status_code=400, detail="No test cases defined for this problem")
    
    # This would actually execute code via local runtime
    # Placeholder for now
    return JudgeResult(
        success=True,
        mode="runtime",
        message="Code executed successfully (placeholder - local runtime not yet connected)",
        score=85.0,
        passed_tests=len([tc for tc in test_cases if not tc.get("is_hidden")]),
        total_tests=len(test_cases),
        xp_awarded=problem.estimated_xp,
        mastery_gain=problem.mastery_impact,
    )


@router.post("/{problem_id}/static-analysis")
async def static_analysis(
    problem_id: str,
    submission: StudentCodeSubmission,
    user=Depends(get_current_user),
):
    """Run static analysis on student code (no execution)."""
    from app.services.static_judge import StaticJudge
    
    if problem_id not in PROBLEMS_DB:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    static_judge = StaticJudge()
    result = static_judge.analyze(submission.code, submission.language)
    
    return {
        "problem_id": problem_id,
        "analysis": result,
    }


# ──────────────────────────────────────────────────────────────────
# SRS Endpoints
# ──────────────────────────────────────────────────────────────────

@router.get("/srs/due")
async def get_due_problems(
    user=Depends(get_current_user),
    judge: UnifiedJudge = Depends(get_unified_judge),
    limit: int = Query(10, le=50),
):
    """Get problems due for spaced repetition review."""
    student_id = user["id"]
    due = judge.get_next_due(student_id, limit)
    return {
        "due_problems": [
            {
                "problem_id": e.problem_id,
                "due_date": e.due_date,
                "times_shown": e.times_shown,
                "times_correct": e.times_correct,
                "mastery": judge.srs.get_mastery(student_id, e.problem_id),
            }
            for e in due
        ]
    }


@router.get("/srs/mastery/{problem_id}")
async def get_mastery(
    problem_id: str,
    user=Depends(get_current_user),
    judge: UnifiedJudge = Depends(get_unified_judge),
):
    """Get mastery percentage for a specific problem."""
    student_id = user["id"]
    mastery = judge.srs.get_mastery(student_id, problem_id)
    return {"problem_id": problem_id, "mastery": mastery}