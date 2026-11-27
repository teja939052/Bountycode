"""Admin content management — in-memory & PostgreSQL-backed, no MongoDB."""
from datetime import datetime, timezone
from typing import Optional, List
import json
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.middleware.auth import get_current_user
from app.services import question_store as _qs
from app.services.audit_log import log_audit
from app.services.response_cache import invalidate_questions_cache

router = APIRouter(prefix="/api/v1/admin/content", tags=["admin-content"])


BACKEND_ROOT = Path(__file__).resolve().parents[2]
TRANCHE_LOG = BACKEND_ROOT / "app" / "data" / "tranche_log.json"
TRANCHE_STAGE_DIR = BACKEND_ROOT / "app" / "data" / "tranche_staging"
TRANCHE_PROMOTED = BACKEND_ROOT / "app" / "data" / "tranche_promoted.json"
TRANCHE_SOURCES = [
    BACKEND_ROOT / "app" / "data" / "parametric_practice_bank.json",
    BACKEND_ROOT / "app" / "data" / "auto_checked_from_bank.json",
]


def _load_tranche_log() -> dict:
    try:
        return json.loads(TRANCHE_LOG.read_text(encoding="utf-8"))
    except Exception:
        raise HTTPException(status_code=404, detail="tranche_log.json not found.")


def _source_index() -> dict:
    index = {}
    for src in TRANCHE_SOURCES:
        if not src.exists():
            continue
        try:
            for q in json.loads(src.read_text(encoding="utf-8")):
                if isinstance(q, dict) and q.get("id"):
                    index[str(q["id"])] = q
        except Exception:
            continue
    return index


def _iso(value):
    if isinstance(value, datetime):
        return value.isoformat()
    return value or ""


# ── Content module routes ────────────────────────────────────────────────

@router.post("")
async def create_content(body: dict, admin=Depends(lambda: None)):
    if not body.get("title"):
        raise HTTPException(status_code=400, detail="Missing required field: title")
    if not body.get("body"):
        raise HTTPException(status_code=400, detail="Missing required field: body")

    now = datetime.now(timezone.utc)
    content = ContentModule(
        title=body["title"],
        description=body.get("description", ""),
        category=body.get("category", "dsa"),
        difficulty=body.get("difficulty", "beginner"),
        body=body["body"],
        order=int(body.get("order", 0)),
        created_at=now,
        updated_at=now,
    )
    async with get_session() as session:
        await _get_content_repo(session).create(session, content)
    return {"id": str(content.id), "title": content.title, "description": content.description}


@router.get("")
async def list_content(
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    admin=Depends(lambda: None),
):
    async with get_session() as session:
        repo = ContentModuleRepository(session)
        items = await _get_content_repo(session).list(session, skip=(page - 1) * limit, limit=limit)
        total = await _get_content_repo(session).count(session)
    return {
        "content": [{"id": str(c.id), "title": c.title, "description": c.description} for c in items],
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit,
    }


@router.get("/tranches")
async def list_tranches(admin=Depends(lambda: None)):
    log = _load_tranche_log()
    out = []
    for t in log.get("tranches", []):
        stage = {}
        try:
            stage = await _load_stage(t["tranche"])
        except HTTPException:
            pass
        gates = stage.get("auto_gates") or {}
        out.append({
            "tranche": t["tranche"],
            "size": t.get("size", 0),
            "staged": t.get("staged", 0),
            "rejected": t.get("rejected", 0),
            "status": stage.get("status", "unknown"),
            "merged_at": stage.get("merged_at"),
            "reviewed_by": stage.get("reviewed_by"),
            "gates_passed": gates.get("passed"),
            "gates_failed": gates.get("failed"),
            "audit": stage.get("audit"),
        })
    return {
        "tranches": out,
        "pool": log.get("pool", 0),
        "staged_total": log.get("staged_total", 0),
        "serving_merged": log.get("serving_merged", False),
    }


@router.get("/tranches/{tranche_id}")
async def get_tranche(tranche_id: str, admin=Depends(lambda: None)):
    stage = await _load_stage(tranche_id)
    index = _source_index()
    sample_ids = stage.get("staged", [])[:20]
    sample = []
    for qid in sample_ids:
        q = index.get(str(qid))
        if not q:
            sample.append({"id": qid, "missing": True})
            continue
        sample.append({
            "id": q.get("id"),
            "question": (q.get("question") or q.get("statement") or "")[:500],
            "correct_answer": q.get("correct_answer"),
            "difficulty": q.get("difficulty"),
            "topic": q.get("topic"),
            "sub_topic": q.get("sub_topic"),
            "type": q.get("type"),
            "provenance": q.get("provenance"),
        })
    return {
        "tranche": tranche_id,
        "status": stage.get("status"),
        "size": stage.get("size", 0),
        "reviewed_by": stage.get("reviewed_by"),
        "merged_at": stage.get("merged_at"),
        "sample": sample,
        "sample_count": len(sample),
    }


@router.post("/tranches/{tranche_id}/approve")
async def approve_tranche(tranche_id: str, body: dict, admin=Depends(lambda: None)):
    signoff_name = str(body.get("signoff_name", "")).strip()
    if not body.get("confirm") is True or not signoff_name:
        raise HTTPException(status_code=400, detail="confirm:true and signoff_name are required")
    stage = await _load_stage(tranche_id)
    if stage.get("status") == "merged":
        return {"tranche": tranche_id, "status": "merged", "merged": 0,
                "merged_at": stage.get("merged_at"), "note": "already merged (idempotent)"}
    if stage.get("status") == "rejected":
        raise HTTPException(status_code=409, detail="Tranche was rejected; un-reject before approving")

    import sys as _sys2
    if str(BACKEND_ROOT) not in _sys2.path:
        _sys2.path.insert(0, str(BACKEND_ROOT))
    from scripts.auto_promote import run_gates, _norm_title as _nt
    from app.services import question_store as _qs
    _qs.load_all()
    _served = _qs.find().only_verified().to_list()
    _sids = {str(q.get("id")) for q in _served}
    _stitles = {_nt(q.get("question")) for q in _served}

    index = _source_index()
    now = datetime.now(timezone.utc)
    reviewer = f"{signoff_name} <admin>:"
    promoted, failures = [], []
    for qid in stage.get("staged", []):
        item = index.get(str(qid))
        if not item:
            failures.append({"id": qid, "reason": "missing_from_source"})
            continue
        res = run_gates(dict(item), _sids, _stitles)
        if not res["all_pass"]:
            failures.append({"id": qid, "reason": {k: v["detail"] for k, v in res["gates"].items() if not v["pass"]}})
            continue
        item = dict(item)
        item["verification_hash"] = res["verification_hash"]
        doc = dict(item)
        doc["trust_status"] = "reviewed"
        doc["review_method"] = "oracle_recompute_plus_sampling_v1"
        doc["reviewed_by"] = reviewer
        doc["reviewed_at"] = now.isoformat()
        doc["review_version"] = "2.0"
        if not doc.get("source_bank"):
            doc["source_bank"] = "tranche_promoted.json"
        promoted.append(doc)

    if failures:
        raise HTTPException(status_code=422, detail={
            "message": f"{len(failures)} staged items failed re-verification; nothing merged (rollback-safe)",
            "failures": failures[:50],
        })

    existing = []
    if TRANCHE_PROMOTED.exists():
        try:
            existing = json.loads(TRANCHE_PROMOTED.read_text(encoding="utf-8"))
        except Exception:
            existing = []
    have = {str(q.get("id")) for q in existing if isinstance(q, dict)}
    added = 0
    for doc in promoted:
        if str(doc["id"]) not in have:
            existing.append(doc)
            have.add(str(doc["id"]))
            added += 1
    TRANCHE_PROMOTED.write_text(json.dumps(existing, indent=1), encoding="utf-8")

    stage["status"] = "merged"
    stage["reviewed_by"] = reviewer
    stage["merged_at"] = now.isoformat()
    stage["merged_count"] = added
    await _save_stage(tranche_id, stage)
    try:
        from app.services.audit_log import log_audit
        await log_audit(user_id="admin", action="tranche.approve",
                        resource=f"tranche:{tranche_id}",
                        details={"reviewed_by": reviewer, "merged": added,
                                 "total_promoted": len(existing)})
    except Exception:
        pass
    try:
        from app.services.response_cache import invalidate_questions_cache
        await invalidate_questions_cache()
    except Exception:
        pass
    return {"tranche": tranche_id, "status": "merged", "merged": added,
            "total_promoted": len(existing), "reviewed_by": reviewer,
            "note": "Served after backend restart (in-memory bank reloads from file)."}


@router.post("/tranches/{tranche_id}/auto-promote")
async def auto_promote_tranche(tranche_id: str, admin=Depends(lambda: None)):
    import sys as _sys
    if str(BACKEND_ROOT) not in _sys.path:
        _sys.path.insert(0, str(BACKEND_ROOT))
    from scripts.auto_promote import run_tranche_gates, _norm_title
    from app.services import question_store as qs
    qs.load_all()
    served = qs.find().only_verified().to_list()
    served_ids = {str(q.get("id")) for q in served}
    served_titles = {_norm_title(q.get("question")) for q in served}
    index = _source_index()
    res = run_tranche_gates(tranche_id, index, served_ids, served_titles)
    stage = await _load_stage(tranche_id)
    stage["auto_gates"] = {"passed": len(res["passed"]), "failed": len(res["failed"]),
                           "failures": res["failed"][:20]}
    await _save_stage(tranche_id, stage)
    try:
        from app.services.audit_log import log_audit
        await log_audit(user_id="admin", action="tranche.auto_promote",
                        resource=f"tranche:{tranche_id}",
                        details={"gates_passed": len(res["passed"]),
                                 "gates_failed": len(res["failed"])})
    except Exception:
        pass
    sample = []
    for row in res["passed"][:20]:
        q = index.get(str(row["id"]), {})
        sample.append({"id": row["id"], "verification_hash": row["verification_hash"],
                       "question": str(q.get("question") or q.get("statement") or "")[:500],
                       "correct_answer": q.get("correct_answer")})
    return {"tranche": tranche_id, "gates_passed": len(res["passed"]),
            "gates_failed": len(res["failed"]), "failures": res["failed"][:20],
            "audit_sample": sample,
            "audit_instructions": "Spot-check these 20 against the 5 criteria. If 2+ fail, POST audit-result with failures>=2 to roll back."}


@router.post("/tranches/{tranche_id}/audit-result")
async def submit_tranche_audit(tranche_id: str, body: dict, admin=Depends(lambda: None)):
    try:
        failures = int(body.get("failures", 0))
    except (TypeError, ValueError):
        raise HTTPException(status_code=400, detail="failures must be an integer")
    notes = str(body.get("notes", ""))[:1000]
    stage = await _load_stage(tranche_id)
    if stage.get("status") == "merged":
        raise HTTPException(status_code=409, detail="Already merged; use served_quarantine for post-merge issues")
    today = datetime.now(timezone.utc).date().isoformat()
    for prior in stage.get("audits", []):
        if (prior.get("by") == "admin" and prior.get("failures") == failures
                and str(prior.get("at", ""))[:10] == today):
            return {"tranche": tranche_id, "status": stage.get("status"),
                    "audit_accepted": True, "duplicate_retry": True,
                    "note": "Identical audit already recorded today."}
    if failures >= 2:
        stage["status"] = "rejected"
        stage["reject_reason"] = f"spot-audit failed ({failures}): {notes}"[:500]
        stage["rejected_by"] = "admin"
        stage["rejected_at"] = datetime.now(timezone.utc).isoformat()
        await _save_stage(tranche_id, stage)
        try:
            from app.services.audit_log import log_audit
            await log_audit(user_id="admin", action="tranche.audit_rollback",
                            resource=f"tranche:{tranche_id}",
                            details={"failures": failures, "notes": notes[:200]})
        except Exception:
            pass
        return {"tranche": tranche_id, "status": "rolled_back", "failures": failures}
    audits = stage.get("audits", [])
    audits.append({"by": "admin", "failures": failures,
                   "notes": notes, "at": datetime.now(timezone.utc).isoformat()})
    stage["audits"] = audits
    await _save_stage(tranche_id, stage)
    try:
        from app.services.audit_log import log_audit
        await log_audit(user_id="admin", action="tranche.audit_accept",
                        resource=f"tranche:{tranche_id}",
                        details={"failures": failures, "notes": notes[:200]})
    except Exception:
        pass
    return {"tranche": tranche_id, "status": stage.get("status"), "audit_accepted": True,
            "note": "Audit recorded. Merge still requires approve (human sign-off)."}


@router.post("/tranches/{tranche_id}/reject")
async def reject_tranche(tranche_id: str, body: dict, admin=Depends(lambda: None)):
    reason = str(body.get("reason", "")).strip()
    if not reason:
        raise HTTPException(status_code=400, detail="reason is required")
    stage = await _load_stage(tranche_id)
    stage["status"] = "rejected"
    stage["reject_reason"] = reason
    stage["rejected_by"] = "admin"
    stage["rejected_at"] = datetime.now(timezone.utc).isoformat()
    await _save_stage(tranche_id, stage)
    try:
        from app.services.audit_log import log_audit
        await log_audit(user_id="admin", action="tranche.reject",
                        resource=f"tranche:{tranche_id}", details={"reason": reason[:200]})
    except Exception:
        pass
    return {"tranche": tranche_id, "status": "rejected"}


@router.get("/{content_id}")
async def get_content(content_id: str, admin=Depends(lambda: None)):
    content = await _get_content_repo(session).get_by_id(content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content module not found")
    return {"id": str(content.id), "title": content.title, "description": content.description}


@router.put("/{content_id}")
async def update_content(content_id: str, body: dict, admin=Depends(lambda: None)):
    content = await _get_content_repo(session).get_by_id(content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content module not found")
    updates = {k: v for k, v in body.items() if k in ("title", "description", "category", "difficulty", "body", "order")}
    if not updates:
        raise HTTPException(status_code=400, detail="No valid fields to update")
    if "order" in updates:
        try:
            updates["order"] = int(updates["order"])
        except (TypeError, ValueError):
            raise HTTPException(status_code=400, detail="order must be an integer")
    updates["updated_at"] = datetime.now(timezone.utc)
    async with get_session() as session:
        await _get_content_repo(session).update(session, content_id, updates)
    updated = await _get_content_repo(session).get_by_id(content_id)
    return {"id": str(updated.id), "title": updated.title, "description": updated.description}


@router.delete("/{content_id}")
async def delete_content(content_id: str, admin=Depends(lambda: None)):
    async with get_session() as session:
        await _get_content_repo(session).delete(session, content_id)
    return {"success": True}


# ── Assignment routes ────────────────────────────────────────────────────

@router.post("/assignments")
async def create_assignment(body: dict, admin=Depends(lambda: None)):
    if not body.get("title"):
        raise HTTPException(status_code=400, detail="Missing required field: title")

    assigned_to = body.get("assigned_to")
    if not assigned_to:
        raise HTTPException(status_code=400, detail="Missing required field: assigned_to")
    if isinstance(assigned_to, str):
        if assigned_to.strip().lower() == "all":
            assigned_to = "all"
        else:
            assigned_to = [e.strip().lower() for e in assigned_to.replace(";", ",").split(",") if e.strip()]
    elif isinstance(assigned_to, list):
        assigned_to = [str(e).strip().lower() for e in assigned_to if str(e).strip()]
    else:
        raise HTTPException(status_code=400, detail="assigned_to must be a list of emails or 'all'")
    if not assigned_to:
        raise HTTPException(status_code=400, detail="assigned_to must not be empty")

    content_id = body.get("content_id")
    content_title = ""
    if content_id:
        content = await _get_content_repo(session).get_by_id(content_id)
        content_title = content.title if content else ""

    due_date = None
    if body.get("due_date"):
        try:
            due_date = datetime.fromisoformat(str(body["due_date"]).replace("Z", "+00:00"))
        except ValueError:
            raise HTTPException(status_code=400, detail="due_date must be a valid ISO datetime string")

    try:
        max_score = int(body.get("max_score", 100))
    except (TypeError, ValueError):
        raise HTTPException(status_code=400, detail="max_score must be an integer")

    assignment = Assignment(
        title=body["title"],
        description=body.get("description", ""),
        content_id=content_id or None,
        content_title=content_title,
        assigned_to=assigned_to,
        due_date=due_date,
        max_score=max_score,
        created_at=datetime.now(timezone.utc),
    )
    async with get_session() as session:
        await _get_assignment_repo(session).create(session, assignment)
    return {"id": str(assignment.id), "title": assignment.title}


@router.get("/assignments")
async def my_assignments(user=Depends(get_current_user)):
    async with get_session() as session:
        repo = AssignmentRepository(session)
        assignments = await repo.get_by_user(user["id"])
    out = []
    for a in assignments:
        item = {"id": str(a.id), "title": a.title, "description": a.description}
        sub = await _get_submission_repo(session).get_by_assignment_and_user(str(a.id), user["id"])
        if sub:
            item["submission_status"] = sub.status
            item["score"] = sub.score
            item["feedback"] = sub.feedback or ""
            item["answer_text"] = sub.answer_text or ""
            item["submitted_at"] = _iso(sub.submitted_at)
            item["graded_at"] = _iso(sub.graded_at)
        else:
            item["submission_status"] = "pending"
            item["score"] = None
            item["feedback"] = ""
            item["answer_text"] = ""
            item["submitted_at"] = None
            item["graded_at"] = None
        out.append(item)
    return {"assignments": out}


@router.get("/assignments/admin")
async def admin_assignments(admin=Depends(lambda: None)):
    async with get_session() as session:
        repo = AssignmentRepository(session)
        assignments = await repo.list_all()
    out = []
    for a in assignments:
        item = {"id": str(a.id), "title": a.title}
        sub_repo = AssignmentSubmissionRepository(session)
        sub_count = await sub_repo.count_by_assignment(str(a.id))
        graded_count = await sub_repo.count_by_assignment_and_status(str(a.id), "graded")
        item["submission_count"] = sub_count
        item["graded_count"] = graded_count
        out.append(item)
    return {"assignments": out}


@router.post("/assignments/{assignment_id}/submit")
async def submit_assignment(assignment_id: str, body: dict, user=Depends(get_current_user)):
    assignment = await _get_assignment_repo(session).get_by_id(assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    email = user.get("email")
    assigned_to = assignment.assigned_to
    if assigned_to != "all" and (not email or email not in assigned_to):
        raise HTTPException(status_code=403, detail="This assignment is not assigned to you")

    answer_text = body.get("answer_text")
    if not answer_text or not str(answer_text).strip():
        raise HTTPException(status_code=400, detail="answer_text is required")

    now = datetime.now(timezone.utc)

    sub = await _get_submission_repo(session).get_by_assignment_and_user(assignment_id, user["id"])
    if sub:
        await _get_submission_repo(session).update(sub.id, {
            "answer_text": str(answer_text).strip(),
            "status": "submitted",
            "submitted_at": now,
            "score": None,
            "feedback": "",
        })
    else:
        submission = {
            "assignment_id": assignment_id,
            "user_id": str(user["id"]),
            "answer_text": str(answer_text).strip(),
            "status": "submitted",
            "submitted_at": now,
        }
        async with get_session() as session:
            await _get_submission_repo(session).create(session, submission)

    sub = await _get_submission_repo(session).get_by_assignment_and_user(assignment_id, user["id"])
    return {"id": str(sub.id), "status": sub.status, "answer_text": sub.answer_text}


@router.post("/assignments/{assignment_id}/review")
async def review_submission(assignment_id: str, body: dict, admin=Depends(lambda: None)):
    user_id = body.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required")

    try:
        score = int(body.get("score", 0))
    except (TypeError, ValueError):
        raise HTTPException(status_code=400, detail="score must be an integer")

    await _get_submission_repo(session).update_score(sub.id if 'sub' in dir() else "", score, body.get("feedback", ""))

    sub = await _get_submission_repo(session).get_by_assignment_and_user(assignment_id, user_id)
    return {"id": str(sub.id), "status": sub.status, "score": sub.score, "feedback": sub.feedback}


@router.get("/assignments/submissions")
async def all_submissions(
    assignment_id: Optional[str] = Query(None),
    admin=Depends(lambda: None),
):
    async with get_session() as session:
        repo = AssignmentSubmissionRepository(session)
        query = {}
        if assignment_id:
            query["assignment_id"] = assignment_id
        submissions = await repo.list_by_assignment(query)
    out = []
    for s in submissions:
        out.append({"id": str(s.id), "status": s.status, "score": s.score})
    return {"submissions": out}