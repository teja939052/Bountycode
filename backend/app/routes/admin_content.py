from datetime import datetime, timezone
from typing import Optional
import json
import re
import sys
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Query
from bson import ObjectId
from app.middleware.auth import get_current_user, require_admin
from app.database import (
    users_collection,
    content_modules_collection,
    assignments_collection,
    assignment_submissions_collection,
    content_tranches_collection,
)
from app.services.gamification import record_practice

router = APIRouter(prefix="/api/v1/admin/content", tags=["admin-content"])

BACKEND_ROOT = Path(__file__).resolve().parents[2]
TRANCHE_LOG = BACKEND_ROOT / "app" / "data" / "tranche_log.json"
TRANCHE_STAGE_DIR = BACKEND_ROOT / "app" / "data" / "tranche_staging"
TRANCHE_SOURCES = [
    BACKEND_ROOT / "app" / "data" / "parametric_practice_bank.json",
    BACKEND_ROOT / "app" / "data" / "auto_checked_from_bank.json",
]
TRANCHE_PROMOTED = BACKEND_ROOT / "app" / "data" / "tranche_promoted.json"
TRANCHE_ROLLBACK_DAYS = 7


def _load_tranche_log() -> dict:
    try:
        return json.loads(TRANCHE_LOG.read_text(encoding="utf-8"))
    except Exception:
        raise HTTPException(status_code=404, detail="tranche_log.json not found. Run scripts/promote_tranche.py first.")


async def _load_stage(tid: str) -> dict:
    """Load tranche workflow state: Mongo primary, seed-file fallback.

    §1.1 migration: stage status (staged/merged/rejected + signoff) lives in
    the content_tranches collection so restarts never lose curation progress.
    The tranche_staging/*.json files are seed-only (one-time backfill).
    """
    try:
        doc = await content_tranches_collection.find_one({"tranche_id": tid})
    except Exception:
        doc = None
    if doc:
        doc.pop("_id", None)
        return doc
    path = TRANCHE_STAGE_DIR / f"{tid}.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Tranche '{tid}' not found")
    return json.loads(path.read_text(encoding="utf-8"))


async def _save_stage(tid: str, body: dict) -> None:
    """Persist tranche workflow state to Mongo (upsert)."""
    from datetime import datetime, timezone
    doc = dict(body)
    doc["tranche_id"] = tid
    doc["updated_at"] = datetime.now(timezone.utc).isoformat()
    await content_tranches_collection.update_one(
        {"tranche_id": tid}, {"$set": doc}, upsert=True)


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


def _verify_tranche_item(item: dict):
    """Re-verify one staged item with the independent oracle (no LLM)."""
    if str(sys.path[0]) != str(BACKEND_ROOT):
        sys.path.insert(0, str(BACKEND_ROOT))
    prov = item.get("provenance", "")
    if "parametric generator" in prov or str(item.get("id", "")).startswith("parametric-"):
        from scripts.verify_parametric_bank import recompute
        try:
            exp = recompute(item)
        except Exception as e:
            return False, f"oracle_error:{e}"[:160]
        if exp is None:
            return False, "oracle_unresolvable"
        if exp != item.get("correct_answer"):
            return False, f"oracle_mismatch:{exp!r}"[:160]
        return True, "oracle_recompute_pass"
    from scripts.autocheck_bank import check_one
    tcs = list(item.get("testcases", [])) + list(item.get("hidden_testcases", []))
    fake = {"id": item.get("id"), "solution": item.get("solution"),
            "test_cases": [{"input": t.get("input", ""),
                            "output": t.get("expected", t.get("output", ""))} for t in tcs]}
    ok, reason, p, total = check_one(fake)
    return ok, (f"exec_pass:{p}/{total}" if ok else reason[:160])
assignments_router = APIRouter(prefix="/api/v1/assignments", tags=["assignments"])

EDITABLE_CONTENT_FIELDS = ("title", "description", "category", "difficulty", "body", "order")


def _iso(value):
    if isinstance(value, datetime):
        return value.isoformat()
    return value or ""


def serialize_content(c):
    return {
        "id": str(c["_id"]),
        "title": c.get("title", ""),
        "description": c.get("description", ""),
        "category": c.get("category", ""),
        "difficulty": c.get("difficulty", ""),
        "body": c.get("body", ""),
        "order": c.get("order", 0),
        "created_at": _iso(c.get("created_at")),
        "updated_at": _iso(c.get("updated_at")),
    }


def serialize_assignment(a):
    return {
        "id": str(a["_id"]),
        "title": a.get("title", ""),
        "description": a.get("description", ""),
        "content_id": str(a["content_id"]) if a.get("content_id") else None,
        "content_title": a.get("content_title", ""),
        "assigned_to": a.get("assigned_to", []),
        "due_date": _iso(a.get("due_date")),
        "max_score": a.get("max_score", 0),
        "created_at": _iso(a.get("created_at")),
    }


def serialize_submission(s):
    return {
        "id": str(s["_id"]),
        "assignment_id": s.get("assignment_id", ""),
        "user_id": s.get("user_id", ""),
        "answer_text": s.get("answer_text", ""),
        "status": s.get("status", "submitted"),
        "score": s.get("score"),
        "feedback": s.get("feedback", ""),
        "submitted_at": _iso(s.get("submitted_at")),
        "graded_at": _iso(s.get("graded_at")),
    }


async def _find_content_or_404(content_id: str):
    try:
        content = await content_modules_collection().find_one({"_id": ObjectId(content_id)})
    except Exception:
        raise HTTPException(status_code=404, detail="Content module not found")
    if not content:
        raise HTTPException(status_code=404, detail="Content module not found")
    return content


async def _find_assignment_or_404(assignment_id: str):
    try:
        assignment = await assignments_collection().find_one({"_id": ObjectId(assignment_id)})
    except Exception:
        raise HTTPException(status_code=404, detail="Assignment not found")
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment


@router.post("")
async def create_content(body: dict, admin=Depends(require_admin)):
    if not body.get("title"):
        raise HTTPException(status_code=400, detail="Missing required field: title")
    if not body.get("body"):
        raise HTTPException(status_code=400, detail="Missing required field: body")

    now = datetime.now(timezone.utc)
    content_doc = {
        "title": body["title"],
        "description": body.get("description", ""),
        "category": body.get("category", "dsa"),
        "difficulty": body.get("difficulty", "beginner"),
        "body": body["body"],
        "order": int(body.get("order", 0)),
        "created_at": now,
        "updated_at": now,
    }
    result = await content_modules_collection().insert_one(content_doc)
    content_doc["_id"] = result.inserted_id
    return serialize_content(content_doc)


@router.get("")
async def list_content(
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    admin=Depends(require_admin),
):
    query = {}
    if category:
        query["category"] = category
    if search:
        safe_search = re.escape(search)
        query["$or"] = [
            {"title": {"$regex": safe_search, "$options": "i"}},
            {"description": {"$regex": safe_search, "$options": "i"}},
        ]

    total = await content_modules_collection().count_documents(query)
    cursor = content_modules_collection().find(query).sort("order", 1).skip((page - 1) * limit).limit(limit)
    content = []
    async for c in cursor:
        content.append(serialize_content(c))

    return {
        "content": content,
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit,
    }


@router.get("/tranches")
async def list_tranches(admin=Depends(require_admin)):
    """List staged promotion tranches (sign-off queue)."""
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
async def get_tranche(tranche_id: str, admin=Depends(require_admin)):
    """Tranche detail + deterministic 20-item review sample."""
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
async def approve_tranche(tranche_id: str, body: dict, admin=Depends(require_admin)):
    """Human sign-off + auto-merge.

    The admin identity IS the HUMAN_REVIEWED stamp (No-LLM Bank Rule):
    re-verifies every staged item, flips survivors to reviewed, appends to
    tranche_promoted.json (served after backend restart). Idempotent.
    """
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
    reviewer = f"{signoff_name} <{admin.get('email', '')}>:{now.date().isoformat()}"
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
        await log_audit(user_id=str(admin.get("id", "")), action="tranche.approve",
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
async def auto_promote_tranche(tranche_id: str, admin=Depends(require_admin)):
    """Run the five deterministic gates over a staged tranche (no LLM).

    Records evidence (per-item verification hashes) and returns a 20-item
    audit sample for spot-check. NEVER flips trust_status and NEVER merges —
    merge stays behind approve (human sign-off).
    """
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
        await log_audit(user_id=str(admin.get("id", "")), action="tranche.auto_promote",
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
async def submit_tranche_audit(tranche_id: str, body: dict, admin=Depends(require_admin)):
    """Record a human spot-check outcome. failures>=2 rolls back (rejects) the tranche."""
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
        # Idempotent retry: same reviewer, same verdict, same day → replay, don't duplicate.
        if (prior.get("by") == admin.get("email", "") and prior.get("failures") == failures
                and str(prior.get("at", ""))[:10] == today):
            return {"tranche": tranche_id, "status": stage.get("status"),
                    "audit_accepted": True, "duplicate_retry": True,
                    "note": "Identical audit already recorded today."}
    if failures >= 2:
        stage["status"] = "rejected"
        stage["reject_reason"] = f"spot-audit failed ({failures}): {notes}"[:500]
        stage["rejected_by"] = admin.get("email", "")
        stage["rejected_at"] = datetime.now(timezone.utc).isoformat()
        await _save_stage(tranche_id, stage)
        try:
            from app.services.audit_log import log_audit
            await log_audit(user_id=str(admin.get("id", "")), action="tranche.audit_rollback",
                            resource=f"tranche:{tranche_id}",
                            details={"failures": failures, "notes": notes[:200]})
        except Exception:
            pass
        return {"tranche": tranche_id, "status": "rolled_back", "failures": failures}
    audits = stage.get("audits", [])
    audits.append({"by": admin.get("email", ""), "failures": failures,
                   "notes": notes, "at": datetime.now(timezone.utc).isoformat()})
    stage["audits"] = audits
    await _save_stage(tranche_id, stage)
    try:
        from app.services.audit_log import log_audit
        await log_audit(user_id=str(admin.get("id", "")), action="tranche.audit_accept",
                        resource=f"tranche:{tranche_id}",
                        details={"failures": failures, "notes": notes[:200]})
    except Exception:
        pass
    return {"tranche": tranche_id, "status": stage.get("status"), "audit_accepted": True,
            "note": "Audit recorded. Merge still requires approve (human sign-off)."}


@router.post("/tranches/{tranche_id}/reject")
async def reject_tranche(tranche_id: str, body: dict, admin=Depends(require_admin)):
    """Reject a tranche with a reason (rollback path)."""
    reason = str(body.get("reason", "")).strip()
    if not reason:
        raise HTTPException(status_code=400, detail="reason is required")
    stage = await _load_stage(tranche_id)
    if stage.get("status") == "merged":
        raise HTTPException(status_code=409, detail="Already merged; remove items via served_quarantine instead")
    stage["status"] = "rejected"
    stage["reject_reason"] = reason
    stage["rejected_by"] = admin.get("email", "")
    stage["rejected_at"] = datetime.now(timezone.utc).isoformat()
    await _save_stage(tranche_id, stage)
    try:
        from app.services.audit_log import log_audit
        await log_audit(user_id=str(admin.get("id", "")), action="tranche.reject",
                        resource=f"tranche:{tranche_id}", details={"reason": reason[:200]})
    except Exception:
        pass
    return {"tranche": tranche_id, "status": "rejected"}


@router.get("/{content_id}")
async def get_content(content_id: str, admin=Depends(require_admin)):
    content = await _find_content_or_404(content_id)
    return serialize_content(content)


@router.put("/{content_id}")
async def update_content(content_id: str, body: dict, admin=Depends(require_admin)):
    await _find_content_or_404(content_id)
    updates = {k: v for k, v in body.items() if k in EDITABLE_CONTENT_FIELDS}
    if not updates:
        raise HTTPException(status_code=400, detail="No valid fields to update")
    if "order" in updates:
        try:
            updates["order"] = int(updates["order"])
        except (TypeError, ValueError):
            raise HTTPException(status_code=400, detail="order must be an integer")
    updates["updated_at"] = datetime.now(timezone.utc)
    await content_modules_collection().update_one({"_id": ObjectId(content_id)}, {"$set": updates})
    updated = await content_modules_collection().find_one({"_id": ObjectId(content_id)})
    return serialize_content(updated)


@router.delete("/{content_id}")
async def delete_content(content_id: str, admin=Depends(require_admin)):
    try:
        result = await content_modules_collection().delete_one({"_id": ObjectId(content_id)})
    except Exception:
        raise HTTPException(status_code=404, detail="Content module not found")
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Content module not found")
    return {"success": True}


@assignments_router.post("")
async def create_assignment(body: dict, admin=Depends(require_admin)):
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
        content = await _find_content_or_404(content_id)
        content_title = content.get("title", "")

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

    assignment_doc = {
        "title": body["title"],
        "description": body.get("description", ""),
        "content_id": content_id or None,
        "content_title": content_title,
        "assigned_to": assigned_to,
        "due_date": due_date,
        "max_score": max_score,
        "created_at": datetime.now(timezone.utc),
    }
    result = await assignments_collection().insert_one(assignment_doc)
    assignment_doc["_id"] = result.inserted_id
    return serialize_assignment(assignment_doc)


@assignments_router.get("")
async def my_assignments(user=Depends(get_current_user)):
    email = user.get("email")
    query = {"$or": [{"assigned_to": "all"}]}
    if email:
        query["$or"].append({"assigned_to": email})
    user_id = str(user["_id"])

    assignments = []
    async for a in assignments_collection().find(query).sort("created_at", -1):
        item = serialize_assignment(a)
        submission = await assignment_submissions_collection().find_one(
            {"assignment_id": item["id"], "user_id": user_id}
        )
        if submission:
            item["submission_status"] = submission.get("status", "submitted")
            item["score"] = submission.get("score")
            item["feedback"] = submission.get("feedback", "")
            item["answer_text"] = submission.get("answer_text", "")
            item["submitted_at"] = _iso(submission.get("submitted_at"))
            item["graded_at"] = _iso(submission.get("graded_at"))
        else:
            item["submission_status"] = "pending"
            item["score"] = None
            item["feedback"] = ""
            item["answer_text"] = ""
            item["submitted_at"] = None
            item["graded_at"] = None
        assignments.append(item)

    return {"assignments": assignments}


@assignments_router.get("/admin")
async def admin_assignments(admin=Depends(require_admin)):
    assignments = []
    async for a in assignments_collection().find({}).sort("created_at", -1):
        item = serialize_assignment(a)
        item["submission_count"] = await assignment_submissions_collection().count_documents(
            {"assignment_id": item["id"]}
        )
        item["graded_count"] = await assignment_submissions_collection().count_documents(
            {"assignment_id": item["id"], "status": "graded"}
        )
        assignments.append(item)
    return {"assignments": assignments}


@assignments_router.post("/{assignment_id}/submit")
async def submit_assignment(assignment_id: str, body: dict, user=Depends(get_current_user)):
    assignment = await _find_assignment_or_404(assignment_id)

    email = user.get("email")
    assigned_to = assignment.get("assigned_to", [])
    if assigned_to != "all" and (not email or email not in assigned_to):
        raise HTTPException(status_code=403, detail="This assignment is not assigned to you")

    answer_text = body.get("answer_text")
    if not answer_text or not str(answer_text).strip():
        raise HTTPException(status_code=400, detail="answer_text is required")

    now = datetime.now(timezone.utc)
    filter_query = {"assignment_id": assignment_id, "user_id": str(user["_id"])}
    existing = await assignment_submissions_collection().find_one(filter_query)
    if existing:
        await assignment_submissions_collection().update_one(filter_query, {"$set": {
            "answer_text": str(answer_text).strip(),
            "status": "submitted",
            "submitted_at": now,
            "score": None,
            "feedback": "",
            "graded_at": None,
        }})
    else:
        submission_doc = {
            "assignment_id": assignment_id,
            "user_id": str(user["_id"]),
            "answer_text": str(answer_text).strip(),
            "status": "submitted",
            "submitted_at": now,
        }
        result = await assignment_submissions_collection().insert_one(submission_doc)
        submission_doc["_id"] = result.inserted_id
        try:
            await record_practice(user["id"], "assignment", 10, role=user.get("role") or user.get("target_role") or "sde")
        except Exception:
            pass
        return serialize_submission(submission_doc)

    updated = await assignment_submissions_collection().find_one(filter_query)
    return serialize_submission(updated)


@assignments_router.post("/{assignment_id}/review")
async def review_submission(assignment_id: str, body: dict, admin=Depends(require_admin)):
    await _find_assignment_or_404(assignment_id)

    user_id = body.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required")

    filter_query = {"assignment_id": assignment_id, "user_id": str(user_id)}
    submission = await assignment_submissions_collection().find_one(filter_query)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found for this user")

    try:
        score = int(body.get("score", 0))
    except (TypeError, ValueError):
        raise HTTPException(status_code=400, detail="score must be an integer")

    await assignment_submissions_collection().update_one(filter_query, {"$set": {
        "status": "graded",
        "score": score,
        "feedback": body.get("feedback", ""),
        "graded_at": datetime.now(timezone.utc),
    }})

    updated = await assignment_submissions_collection().find_one(filter_query)
    return serialize_submission(updated)


@assignments_router.get("/submissions")
async def all_submissions(
    assignment_id: Optional[str] = Query(None),
    admin=Depends(require_admin),
):
    query = {}
    if assignment_id:
        query["assignment_id"] = assignment_id

    submissions = []
    async for s in assignment_submissions_collection().find(query).sort("submitted_at", -1):
        item = serialize_submission(s)
        if ObjectId.is_valid(item["user_id"]):
            user = await users_collection().find_one({"_id": ObjectId(item["user_id"])})
            item["user_email"] = user.get("email", "") if user else ""
            item["user_name"] = user.get("name", "") if user else ""
        else:
            item["user_email"] = ""
            item["user_name"] = ""
        if ObjectId.is_valid(item["assignment_id"]):
            assignment = await assignments_collection().find_one({"_id": ObjectId(item["assignment_id"])})
            item["assignment_title"] = assignment.get("title", "") if assignment else ""
        else:
            item["assignment_title"] = ""
        submissions.append(item)

    return {"submissions": submissions}


@router.get("/questions/verification-report")
async def question_verification_report(admin=Depends(require_admin)):
    from app.services.auto_verify import verify_all_questions
    result = await verify_all_questions()
    return result.to_dict()


@router.get("/questions/verification-stats")
async def question_verification_stats(admin=Depends(require_admin)):
    from app.services import question_store
    question_store.load_all()
    total = len(question_store._questions)
    by_status: dict = {}
    for q in question_store._questions:
        status = str(q.get("trust_status", "unverified")).lower()
        by_status[status] = by_status.get(status, 0) + 1
    return {"total": total, "by_status": by_status}
