"""Content Factory API — bulk import, verification, and coverage reporting.

Admin-only endpoints for managing question content at scale.
All mutations require admin role (enforced via get_current_user).
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.middleware.auth import get_current_user
from app.services.content_verification import ContentVerifier
from app.services.company_content import CompanyContentAnalyzer

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/admin/content", tags=["content-factory"])


# ── Request/Response models ──────────────────────────────────────────

class ImportRequest(BaseModel):
    questions: List[Dict[str, Any]] = Field(..., min_length=1, max_length=500)
    auto_verify: bool = Field(True, description="Run automated verification on import")
    dry_run: bool = Field(False, description="Validate without persisting")


class ImportResponse(BaseModel):
    imported: int = 0
    rejected: int = 0
    needs_review: int = 0
    errors: List[Dict[str, Any]] = Field(default_factory=list)
    verification_summary: Optional[Dict[str, Any]] = None


class CoverageResponse(BaseModel):
    companies: List[Dict[str, Any]] = Field(default_factory=list)
    gaps: List[Dict[str, Any]] = Field(default_factory=list)


# ── Helpers ──────────────────────────────────────────────────────────

def _require_admin(user: Dict[str, Any]) -> None:
    """Raise 403 if user is not admin."""
    role = user.get("role", "")
    is_admin = user.get("is_admin", False)
    if role != "admin" and not is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")


def _get_question_store():
    """Get the singleton question_store module."""
    from app.services import question_store as qs
    return qs


# ── Endpoints ────────────────────────────────────────────────────────

@router.post("/import", response_model=ImportResponse)
async def import_questions(
    req: ImportRequest,
    user: Dict[str, Any] = Depends(get_current_user),
):
    """Bulk import questions. Validates schema, optionally verifies, returns report."""
    _require_admin(user)

    qs = _get_question_store()
    verifier = ContentVerifier()

    imported = 0
    rejected = 0
    needs_review = 0
    errors: List[Dict[str, Any]] = []
    verification_reports: List[Dict[str, Any]] = []

    for idx, q in enumerate(req.questions):
        # ── Schema validation ──
        validation_error = _validate_schema(q)
        if validation_error:
            rejected += 1
            errors.append({"index": idx, "error": validation_error})
            continue

        # ── Duplicate check ──
        if _is_duplicate(q, qs._questions):
            rejected += 1
            errors.append({"index": idx, "error": "Duplicate question (same id or question text)"})
            continue

        # ── Automated verification ──
        if req.auto_verify and q.get("type") == "coding":
            try:
                report = await verifier.verify(q)
                verification_reports.append(report)
                if report["recommendation"] == "REJECT":
                    rejected += 1
                    errors.append({
                        "index": idx,
                        "error": f"Verification failed: {report['checks']}",
                    })
                    continue
                if report["recommendation"] == "HUMAN_REVIEW":
                    needs_review += 1
            except Exception as exc:
                logger.warning("Verification error for question %d: %s", idx, exc)
                needs_review += 1

        # ── Persist (unless dry run) ──
        if not req.dry_run:
            try:
                # Assign id if missing
                if not q.get("id") and not q.get("_id"):
                    q["id"] = f"imported_{idx:06d}"
                qs._questions.append(q)
                imported += 1
            except Exception as exc:
                rejected += 1
                errors.append({"index": idx, "error": f"Persist error: {exc}"})
        else:
            imported += 1  # dry run counts as would-be imported

    # Build verification summary
    verification_summary = None
    if verification_reports:
        passed = sum(1 for r in verification_reports if r.get("all_passed"))
        verification_summary = {
            "total_verified": len(verification_reports),
            "passed_all_checks": passed,
            "failed": len(verification_reports) - passed,
        }

    return ImportResponse(
        imported=imported,
        rejected=rejected,
        needs_review=needs_review,
        errors=errors[:20],  # cap error detail
        verification_summary=verification_summary,
    )


@router.post("/verify")
async def verify_questions(
    questions: List[Dict[str, Any]],
    user: Dict[str, Any] = Depends(get_current_user),
):
    """Run automated verification on provided questions without importing."""
    _require_admin(user)
    verifier = ContentVerifier()
    report = await verifier.verify_batch(questions)
    return report


@router.get("/coverage")
async def coverage_report(
    company: Optional[str] = None,
    user: Dict[str, Any] = Depends(get_current_user),
):
    """Get coverage report for company blueprints vs question bank."""
    _require_admin(user)
    qs = _get_question_store()
    analyzer = CompanyContentAnalyzer(qs._questions)
    return analyzer.coverage_report(company)


@router.get("/gaps")
async def coverage_gaps(
    company: Optional[str] = None,
    user: Dict[str, Any] = Depends(get_current_user),
):
    """Get flat list of coverage gaps (sections needing more content)."""
    _require_admin(user)
    qs = _get_question_store()
    analyzer = CompanyContentAnalyzer(qs._questions)
    return {"gaps": analyzer.gaps(company)}


@router.get("/section-questions")
async def section_questions(
    company: str,
    section: str,
    difficulty: Optional[str] = None,
    user: Dict[str, Any] = Depends(get_current_user),
):
    """Get verified questions matching a company + section."""
    _require_admin(user)
    qs = _get_question_store()
    analyzer = CompanyContentAnalyzer(qs._questions)
    return {
        "company": company,
        "section": section,
        "questions": analyzer.section_questions(company, section, difficulty),
    }


# ── Validation ───────────────────────────────────────────────────────

def _validate_schema(q: Dict[str, Any]) -> Optional[str]:
    """Validate a question has required fields. Returns error message or None."""
    if not isinstance(q, dict):
        return "Question must be a dict"

    required = ["question", "type"]
    for field in required:
        if field not in q or not q[field]:
            return f"Missing required field: {field}"

    qtype = q.get("type", "")
    if qtype not in ("coding", "mcq", "aptitude", "logical", "verbal", "technical"):
        return f"Unknown question type: {qtype}"

    # Coding questions need a solution
    if qtype == "coding":
        sol = q.get("solution")
        if not sol:
            return "Coding questions require a solution"
        if isinstance(sol, dict) and not sol.get("code"):
            return "Coding solution requires code"

    # All questions need some form of answer
    if qtype in ("mcq", "aptitude", "logical", "verbal"):
        if q.get("correct_answer") is None and not q.get("options"):
            return "MCQ/aptitude questions require correct_answer or options"

    return None


def _is_duplicate(q: Dict[str, Any], existing: List[Dict[str, Any]]) -> bool:
    """Check if a question is a duplicate of an existing one."""
    q_id = q.get("id") or q.get("_id")
    q_text = str(q.get(" ")).strip().lower() if False else str(q.get("question", "")).strip().lower()

    for ex in existing:
        # Same id
        if q_id and (ex.get("id") == q_id or str(ex.get("_id", "")) == str(q_id)):
            return True
        # Same question text (first 100 chars)
        ex_text = str(ex.get("question", "")).strip().lower()[:100]
        if q_text and q_text[:100] == ex_text:
            return True
    return False


@router.get('/corpus/summary')
async def corpus_summary(
    user: Dict[str, Any] = Depends(get_current_user),
):
    _require_admin(user)
    from app.services.content_corpus import corpus_summary as get_corpus_summary
    return get_corpus_summary()


@router.get('/corpus/concepts')
async def list_corpus_concepts(
    domain: Optional[str] = None,
    language: Optional[str] = None,
    category: Optional[str] = None,
    user: Dict[str, Any] = Depends(get_current_user),
):
    _require_admin(user)
    from app.services.content_corpus import get_all_concepts

    concepts = get_all_concepts()
    if domain:
        concepts = {k: v for k, v in concepts.items() if v.get('domain') == domain}
    if language:
        concepts = {k: v for k, v in concepts.items() if v.get('language') == language}
    if category:
        concepts = {k: v for k, v in concepts.items() if v.get('category') == category}

    return {
        'count': len(concepts),
        'concepts': list(concepts.values()),
    }


@router.get('/corpus/concepts/{concept_id}')
async def get_corpus_concept(
    concept_id: str,
    user: Dict[str, Any] = Depends(get_current_user),
):
    _require_admin(user)
    from app.services.content_corpus import get_concept, get_prerequisites, get_all_prerequisites

    concept = get_concept(concept_id)
    if not concept:
        raise HTTPException(status_code=404, detail=f'Concept not found: {concept_id}')

    return {
        'concept': concept,
        'prerequisites': get_prerequisites(concept_id),
        'all_prerequisites': sorted(get_all_prerequisites(concept_id)),
    }


@router.get('/corpus/validate')
async def validate_corpus(
    user: Dict[str, Any] = Depends(get_current_user),
):
    _require_admin(user)
    from app.services.content_corpus import validate_corpus as run_validation
    return run_validation()


@router.get('/corpus/queue')
async def get_generation_queue(
    domain: Optional[str] = None,
    language: Optional[str] = None,
    limit: int = 50,
    user: Dict[str, Any] = Depends(get_current_user),
):
    _require_admin(user)
    from app.services.content_factory import build_generation_queue
    queue = build_generation_queue(domain=domain, language=language, limit=limit)
    return {
        'count': len(queue),
        'queue': queue,
        'domain': domain,
        'language': language,
    }


@router.post('/corpus/generate')
async def generate_content(
    concept_ids: List[str],
    content_types: Optional[List[str]] = None,
    mode: str = 'dry_run',
    user: Dict[str, Any] = Depends(get_current_user),
):
    _require_admin(user)
    from app.services.content_factory import get_content_factory, MODE_PRODUCTION, MODE_DRY_RUN

    if mode not in (MODE_DRY_RUN, MODE_PRODUCTION):
        raise HTTPException(status_code=400, detail=f'Invalid mode: {mode}.')

    factory = get_content_factory(mode=mode)
    report = await factory.batch_generate(concept_ids, content_types=content_types)
    return report


@router.get('/corpus/readonly-check')
async def readonly_check(
    user: Dict[str, Any] = Depends(get_current_user),
):
    _require_admin(user)
    from app.services.content_factory import validate_generation_readonly
    return validate_generation_readonly()
