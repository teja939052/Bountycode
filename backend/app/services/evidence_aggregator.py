"""Student Evidence Engine — ONE deterministic aggregation layer.

Every P0/P1/P2 performance view (heatmap, failure breakdown, solve-time
trend, company gap, reattempts, records, retention, pacing, complexity
signal, prep report) is a pure read-model over the SAME collected bundle
of canonical events. No second mastery/readiness/SRS/bank/analytics
system; no AI; no network. Same stored events → same numbers.

Event sources reused (fields as stored; missing fields degrade a metric
to insufficient-evidence, never invented):
  submissions      failure_class/skill_id/attempt_index/results[].execution_time
  learning_events  passed/score/time_spent_seconds/hints_used/attempt_number/skill_id
  oa_sessions      result.scorecard (time_taken/topic/section/score)
  aptitude_tests   answers[].is_correct/time_taken + score
  question_answers attempt_number/skill_id/time_taken/is_correct
  interviews       overall_score/created_at (+ breakdown)
  srs_cards/states repetitions/lapses/total_reviews/next_review/interval
  solved_problems  solve stamps (topic via question_store join at read time)
  skill_graph      oa_outcomes/interview_outcomes (EMA aggregates)

Trust: only evidence allowed by governance is consumed. Solves resolve
through readiness_engine._trust_weight (verified/reviewed = high-stakes,
automated_checked = learning-only, else excluded). Verdicts/failures come
from the deterministic judge, never model claims.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from app.services.readiness_engine import (
    _as_iso,
    _resolve_skill_domain,
    _trust_weight,
    build_target_profile,
    calculate_target_readiness,
    collect_target_evidence,
)

FAILURE_CLASSES = ("SUCCESS", "WRONG_ANSWER", "TIMEOUT", "RUNTIME_ERROR", "SYNTAX_ERROR")

# Heatmap color bands (deterministic thresholds, no model labels).
HEAT_GREEN = 75.0
HEAT_YELLOW = 55.0
HEAT_ORANGE = 40.0
MIN_PATTERN_EVENTS = 3


# ─── Small deterministic helpers ──────────────────────────────────────────

def _median(values: List[float]) -> Optional[float]:
    vals = sorted(float(v) for v in values if isinstance(v, (int, float)))
    if not vals:
        return None
    n = len(vals)
    mid = n // 2
    return round(vals[mid] if n % 2 else (vals[mid - 1] + vals[mid]) / 2, 1)


def _day(iso: Optional[str]) -> Optional[str]:
    if not iso:
        return None
    try:
        dt = datetime.fromisoformat(str(iso).replace("Z", "+00:00"))
        return dt.date().isoformat()
    except Exception:
        return None


def _days_ago(iso: Optional[str], now: datetime) -> Optional[int]:
    if not iso:
        return None
    try:
        dt = datetime.fromisoformat(str(iso).replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return (now - dt).days
    except Exception:
        return None


def _heat_color(accuracy: Optional[float], attempts: int) -> str:
    if attempts < MIN_PATTERN_EVENTS or accuracy is None:
        return "insufficient"
    if accuracy >= HEAT_GREEN:
        return "green"
    if accuracy >= HEAT_YELLOW:
        return "yellow"
    if accuracy >= HEAT_ORANGE:
        return "orange"
    return "red"


def _pattern_key(skill_id: Optional[str]) -> str:
    """Canonical pattern id for heatmap grouping (domain.subskill kept)."""
    if not skill_id:
        return "coding.uncategorized"
    try:
        from app.services.skill_taxonomy import canonical_skill_id, is_canonical
        if is_canonical(str(skill_id)):
            return str(skill_id)
        canon = canonical_skill_id(str(skill_id))
        if canon:
            return canon
    except Exception:
        pass
    return str(skill_id)


# ─── Collector (async I/O, zero AI) ───────────────────────────────────────

async def collect_student_evidence(user_id: str) -> Dict[str, Any]:
    """Fetch every canonical evidence list for one student (best-effort)."""
    from app.database import (
        aptitude_tests_collection,
        interviews_collection,
        learning_events_collection,
        oa_sessions_collection,
        question_answers_collection,
        solved_problems_collection,
        srs_cards_collection,
        srs_collection,
        submissions_collection,
    )

    async def _all(col_fn, filt, limit=5000, **kw):
        try:
            return await col_fn().find(filt, **kw).to_list(limit)
        except Exception:
            return []

    submissions = await _all(submissions_collection, {"user_id": user_id})
    events = await _all(learning_events_collection, {"user_id": user_id})
    oa_docs = await _all(oa_sessions_collection, {"user_id": user_id, "status": "completed"}, limit=200)
    apt_docs = await _all(aptitude_tests_collection, {"user_id": user_id}, limit=200)
    answers = await _all(question_answers_collection, {"user_id": user_id})
    interviews = await _all(interviews_collection, {"user_id": user_id, "status": "completed"}, limit=200)
    srs_cards = await _all(srs_cards_collection, {"user_id": user_id})
    srs_states = await _all(srs_collection, {"user_id": user_id})
    solved = await _all(solved_problems_collection, {"user_id": user_id})

    # Trust-gate solves (dedupe by question, keep first; trust via bank join).
    trusted_solves: List[Dict[str, Any]] = []
    seen_q: set = set()
    excluded_untrusted = 0
    for doc in solved:
        qid = str(doc.get("question_id") or "")
        if not qid or qid in seen_q:
            continue
        seen_q.add(qid)
        try:
            from app.services import question_store as qs
            q = qs.find_one({"_id": qid}) or qs.find_one({"id": qid})
            trust = str((q or {}).get("trust_status") or "")
        except Exception:
            trust = ""
        if _trust_weight(trust) <= 0:
            excluded_untrusted += 1
            continue
        trusted_solves.append(doc)

    return {
        "submissions": submissions,
        "learning_events": sorted(
            events, key=lambda e: str(e.get("timestamp") or e.get("created_at") or "")),
        "oa_sessions": oa_docs,
        "aptitude_tests": apt_docs,
        "question_answers": answers,
        "interviews": interviews,
        "srs_cards": srs_cards,
        "srs_states": srs_states,
        "solved_problems": trusted_solves,
        "excluded_untrusted_solves": excluded_untrusted,
    }


# ─── P0: pattern heatmap ──────────────────────────────────────────────────

def pattern_heatmap(bundle: Dict[str, Any]) -> Dict[str, Any]:
    """Per-pattern accuracy/first-attempt/time/hints/failures/transfer."""
    per: Dict[str, Dict[str, Any]] = {}

    def _slot(pid: str) -> Dict[str, Any]:
        return per.setdefault(pid, {
            "attempts": 0, "passes": 0, "first_attempts": 0, "first_passes": 0,
            "times": [], "hints": 0, "failures": {c: 0 for c in FAILURE_CLASSES},
            "transfer": [], "last_at": None,
        })

    # Learning events: pass/fail + time + hints + attempt order + transfer.
    by_question: Dict[str, List[Dict[str, Any]]] = {}
    for ev in bundle.get("learning_events", []):
        qid = str(ev.get("question_id") or ev.get("skill_id") or "")
        by_question.setdefault(qid, []).append(ev)
    for qid, evs in by_question.items():
        pid = _pattern_key((evs[-1].get("skill_id") if evs else None))
        first = evs[0]
        s = _slot(pid)
        s["first_attempts"] += 1
        if bool(first.get("passed")):
            s["first_passes"] += 1
        for ev in evs:
            activity = str(ev.get("activity_type") or "")
            passed = bool(ev.get("passed"))
            s["attempts"] += 1
            s["passes"] += 1 if passed else 0
            t = ev.get("time_spent_seconds")
            if isinstance(t, (int, float)) and t > 0:
                s["times"].append(float(t))
            h = ev.get("hints_used")
            if isinstance(h, (int, float)) and h > 0:
                s["hints"] += int(h)
            if any(k in activity for k in ("retest", "repair", "transfer")):
                s["transfer"].append(100.0 if passed else 0.0)
            iso = _as_iso(ev.get("timestamp") or ev.get("created_at"))
            if iso and (not s["last_at"] or iso > s["last_at"]):
                s["last_at"] = iso

    # Submissions: canonical failure classes + attempt order.
    for sub in bundle.get("submissions", []):
        pid = _pattern_key(sub.get("skill_id"))
        s = _slot(pid)
        fc = str(sub.get("failure_class") or "")
        if fc in FAILURE_CLASSES:
            s["failures"][fc] += 1

    # OA scorecard: section/topic accuracy + solve times.
    for sess in bundle.get("oa_sessions", []):
        result = sess.get("result") or {}
        for row in result.get("scorecard") or []:
            pid = _pattern_key(row.get("topic") or row.get("section"))
            s = _slot(pid)
            mx = float(row.get("max_marks", 0) or 0)
            got = float(row.get("marks_awarded", row.get("score", 0)) or 0)
            s["attempts"] += 1
            s["passes"] += 1 if (mx > 0 and got >= mx) or (mx <= 0 and got > 0) else 0
            t = row.get("time_taken")
            if isinstance(t, (int, float)) and t > 0:
                s["times"].append(float(t))

    patterns = []
    for pid, s in sorted(per.items()):
        acc = round(s["passes"] / s["attempts"] * 100, 1) if s["attempts"] else None
        first_rate = round(s["first_passes"] / s["first_attempts"] * 100, 1) if s["first_attempts"] else None
        fail_total = sum(s["failures"].values())
        patterns.append({
            "pattern_id": pid,
            "attempts": s["attempts"],
            "passes": s["passes"],
            "accuracy": acc,
            "color": _heat_color(acc, s["attempts"]),
            "first_attempt_rate": first_rate,
            "median_solve_time_s": _median(s["times"]),
            "solve_time_samples": len(s["times"]),
            "hints_used": s["hints"],
            "failures": dict(s["failures"]),
            "failure_evidence": fail_total,
            "transfer_rate": round(sum(s["transfer"]) / len(s["transfer"]), 1) if s["transfer"] else None,
            "last_practiced_at": s["last_at"],
        })
    weakest = next((p for p in sorted(
        [p for p in patterns if p["accuracy"] is not None],
        key=lambda p: (p["accuracy"], -p["attempts"])) if p["attempts"] >= MIN_PATTERN_EVENTS), None)
    return {
        "patterns": patterns,
        "weakest_pattern": weakest["pattern_id"] if weakest else None,
        "next_action": ({"type": "repair", "skill_id": weakest["pattern_id"],
                         "reason": "lowest accuracy with sufficient evidence"}
                        if weakest else None),
    }


# ─── P0: failure breakdown ────────────────────────────────────────────────

def failure_breakdown(bundle: Dict[str, Any], pattern_id: Optional[str] = None) -> Dict[str, Any]:
    """Judge-verdict distribution overall + per pattern + recent trend."""
    counts = {c: 0 for c in FAILURE_CLASSES}
    per_pattern: Dict[str, Dict[str, int]] = {}
    ordered: List[Tuple[str, str]] = []  # (submitted_at, class)

    for sub in bundle.get("submissions", []):
        fc = str(sub.get("failure_class") or "")
        if fc not in FAILURE_CLASSES:
            continue
        pid = _pattern_key(sub.get("skill_id"))
        if pattern_id and pid != pattern_id:
            continue
        counts[fc] += 1
        per_pattern.setdefault(pid, {c: 0 for c in FAILURE_CLASSES})[fc] += 1
        ordered.append((str(sub.get("submitted_at") or ""), fc))

    total = sum(counts.values())
    ordered.sort()
    recent = [c for _, c in ordered[-10:]]
    prior = [c for _, c in ordered[-20:-10]]
    def _fail_share(seq: List[str]) -> Optional[float]:
        if not seq:
            return None
        return round(sum(1 for c in seq if c != "SUCCESS") / len(seq) * 100, 1)

    top_failure = None
    fails = {k: v for k, v in counts.items() if k != "SUCCESS"}
    if fails and sum(fails.values()) > 0:
        top_failure = max(fails.items(), key=lambda kv: kv[1])[0]
    return {
        "pattern_id": pattern_id,
        "total_submissions": total,
        "counts": counts,
        "percentages": {k: round(v / total * 100, 1) if total else 0.0 for k, v in counts.items()},
        "top_failure": top_failure,
        "recent_fail_rate": _fail_share(recent),
        "prior_fail_rate": _fail_share(prior),
        "by_pattern": per_pattern,
        "sufficient": total >= 5,
    }


# ─── P0: solve-time trend ─────────────────────────────────────────────────

def _solve_time_samples(bundle: Dict[str, Any], pattern_id: Optional[str] = None) -> List[Tuple[str, float]]:
    """(iso, seconds) samples from OA scorecard + aptitude + answers + events."""
    out: List[Tuple[str, float]] = []

    def _take(iso: Optional[str], secs: Any, pid: Optional[str]):
        if pattern_id and pid != pattern_id:
            return
        if isinstance(secs, (int, float)) and secs > 0:
            out.append((iso or "", float(secs)))

    for sess in bundle.get("oa_sessions", []):
        result = sess.get("result") or {}
        at = _as_iso(sess.get("completed_at") or sess.get("created_at"))
        for row in result.get("scorecard") or []:
            _take(at, row.get("time_taken"), _pattern_key(row.get("topic") or row.get("section")))
    for t in bundle.get("aptitude_tests", []):
        at = _as_iso(t.get("completed_at") or t.get("created_at"))
        for a in t.get("answers") or []:
            _take(at, a.get("time_taken"), _pattern_key("aptitude.quantitative"))
    for a in bundle.get("question_answers", []):
        _take(_as_iso(a.get("created_at")), a.get("time_taken"), _pattern_key(a.get("skill_id")))
    for ev in bundle.get("learning_events", []):
        _take(_as_iso(ev.get("timestamp") or ev.get("created_at")),
              ev.get("time_spent_seconds"), _pattern_key(ev.get("skill_id")))
    return out


def solve_time_trend(bundle: Dict[str, Any], pattern_id: Optional[str] = None,
                     now: Optional[datetime] = None) -> Dict[str, Any]:
    """Median solve time over 7d/30d/90d/all (medians, never means)."""
    now = now or datetime.now(timezone.utc)
    samples = _solve_time_samples(bundle, pattern_id)
    windows = {"7d": 7, "30d": 30, "90d": 90, "all": None}
    medians = {}
    for label, days in windows.items():
        vals = [s for iso, s in samples
                if days is None or (_days_ago(iso, now) is not None and _days_ago(iso, now) <= days)]
        medians[label] = {"median_s": _median(vals), "samples": len(vals)}
    first = _median([s for _, s in samples[: len(samples) // 2]]) if len(samples) >= 4 else None
    second = _median([s for _, s in samples[len(samples) // 2:]]) if len(samples) >= 4 else None
    return {
        "pattern_id": pattern_id,
        "windows": medians,
        "trend_s": round(second - first, 1) if first is not None and second is not None else None,
        "sufficient": len(samples) >= 3,
    }


# ─── P0: company readiness gap ────────────────────────────────────────────

async def company_gap(user_id: str, role: str, company: str,
                      bundle: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Preparation score against the configured (role, company) target model.

    Wording contract: scores are "preparation against the configured target
    model" — never a probability of passing/hire.
    """
    profile = build_target_profile(role, company)
    evidence = await collect_target_evidence(user_id, profile)
    evidence.pop("__meta__", None)
    result = calculate_target_readiness(profile, evidence)
    sections = []
    for s in result["skills"]:
        target = s["threshold"] if s["critical"] else 70.0
        sections.append({
            "skill_id": s["skill_id"], "label": s.get("label", s["skill_id"]),
            "score": s["score"], "target": target,
            "gap": round(target - s["score"], 1),
            "critical": s["critical"], "status": s["status"],
        })
    primary = min(sections, key=lambda s: (s["score"] - s["target"])) if sections else None
    return {
        "role": role, "company": company,
        "preparation_score": result["score"],
        "evidence_coverage": result["coverage"],
        "status": result["status"],
        "sections": sections,
        "primary_gap": primary["skill_id"] if primary else None,
        "blockers": result["blockers"],
        "next_action": result["next_action"],
        "disclaimer": "Preparation score against the configured target model; not a hiring prediction.",
    }


# ─── P1: personal records ─────────────────────────────────────────────────

def personal_records(bundle: Dict[str, Any]) -> Dict[str, Any]:
    """Fastest solve, longest streak, first-attempt best, most improved/repaired."""
    samples = _solve_time_samples(bundle)
    correct_times = sorted(s for _, s in samples)
    fastest = correct_times[0] if correct_times else None

    # Longest daily streak with ≥1 pass.
    pass_days: set = set()
    for ev in bundle.get("learning_events", []):
        if ev.get("passed"):
            d = _day(_as_iso(ev.get("timestamp") or ev.get("created_at")) or "")
            if d:
                pass_days.add(d)
    longest = run = 0
    prev = None
    for d in sorted(pass_days):
        try:
            cur = datetime.fromisoformat(d).date()
            run = run + 1 if prev and (cur - prev).days == 1 else 1
            prev = cur
            longest = max(longest, run)
        except Exception:
            continue

    heat = pattern_heatmap(bundle)
    rated = [p for p in heat["patterns"] if p["first_attempt_rate"] is not None]
    best_first = max(rated, key=lambda p: p["first_attempt_rate"]) if rated else None

    # Most improved: second-half minus first-half accuracy per pattern.
    improved = None
    best_delta = 0.0
    by_q: Dict[str, List[bool]] = {}
    for ev in bundle.get("learning_events", []):
        pid = _pattern_key(ev.get("skill_id"))
        by_q.setdefault(pid, []).append(bool(ev.get("passed")))
    for pid, seq in by_q.items():
        if len(seq) >= 6:
            half = len(seq) // 2
            d = (sum(seq[half:]) / len(seq[half:]) - sum(seq[:half]) / len(seq[:half])) * 100
            if d > best_delta:
                best_delta, improved = d, pid

    # Most repaired: most repair/retest passes.
    repairs: Dict[str, int] = {}
    for ev in bundle.get("learning_events", []):
        if any(k in str(ev.get("activity_type") or "") for k in ("retest", "repair")) and ev.get("passed"):
            pid = _pattern_key(ev.get("skill_id"))
            repairs[pid] = repairs.get(pid, 0) + 1
    most_repaired = max(repairs.items(), key=lambda kv: kv[1])[0] if repairs else None

    return {
        "fastest_correct_solve_s": fastest,
        "longest_streak_days": longest,
        "best_first_attempt": ({"pattern_id": best_first["pattern_id"],
                                "rate": best_first["first_attempt_rate"]}
                               if best_first else None),
        "most_improved_pattern": ({"pattern_id": improved, "delta_pp": round(best_delta, 1)}
                                  if improved else None),
        "most_repaired_skill": most_repaired,
    }


# ─── P1: retention view + reattempt memory ────────────────────────────────

def retention_view(bundle: Dict[str, Any], now: Optional[datetime] = None) -> Dict[str, Any]:
    """Expose SRS state honestly: next reviews, due counts, retrieval history.

    No biological-forgetting claims — "next review" dates only.
    """
    now = now or datetime.now(timezone.utc)
    cards = list(bundle.get("srs_cards", [])) + list(bundle.get("srs_states", []))
    seen: Dict[str, Dict[str, Any]] = {}
    for c in cards:
        key = str(c.get("concept_id") or c.get("problem_id") or "")
        if not key or key in seen:
            continue
        seen[key] = c
    items, due = [], 0
    for key, c in seen.items():
        nxt = _as_iso(c.get("next_review"))
        is_due = bool(nxt) and _days_ago(nxt, now) is not None and _days_ago(nxt, now) >= 0
        due += 1 if is_due else 0
        items.append({
            "concept_id": key,
            "next_review": nxt,
            "due": is_due,
            "interval_days": c.get("interval", 0),
            "repetitions": c.get("repetitions", 0),
            "lapses": c.get("lapses", 0),
            "total_reviews": c.get("total_reviews", 0),
            "successful_retrievals": max(0, int(c.get("total_reviews", 0) or 0) - int(c.get("lapses", 0) or 0)),
        })
    items.sort(key=lambda i: i["next_review"] or "9999")
    return {"concepts": items, "due_count": due, "tracked_count": len(items)}


def reattempts_due(bundle: Dict[str, Any], now: Optional[datetime] = None) -> Dict[str, Any]:
    """Due SRS reviews joined with hint history: re-solve independently.

    Cards whose originating solve used hints resurface with hints hidden;
    outcome is recorded by the existing review flow (no second scheduler).
    """
    now = now or datetime.now(timezone.utc)
    hinted: set = set()
    for ev in bundle.get("learning_events", []):
        h = ev.get("hints_used")
        if isinstance(h, (int, float)) and h > 0:
            qid = ev.get("question_id") or ev.get("skill_id")
            if qid:
                hinted.add(str(qid))
    ret = retention_view(bundle, now)
    due_items = []
    for item in ret["concepts"]:
        if not item["due"]:
            continue
        key = item["concept_id"]
        needs_hint_hidden = key in hinted
        due_items.append({**item, "hints_hidden": needs_hint_hidden,
                          "reason": ("solved with hints — independent reattempt"
                                     if needs_hint_hidden else "scheduled review")})
    return {"due": due_items, "due_count": len(due_items)}


# ─── P2: pacing ───────────────────────────────────────────────────────────

def pacing(bundle: Dict[str, Any], target_date_iso: str, remaining_missions: int,
           now: Optional[datetime] = None) -> Dict[str, Any]:
    """Current vs required pace from the last 14d completion rate. Projection
    labeled as projection, never a promise."""
    now = now or datetime.now(timezone.utc)
    try:
        target = datetime.fromisoformat(str(target_date_iso).replace("Z", "+00:00"))
        if target.tzinfo is None:
            target = target.replace(tzinfo=timezone.utc)
    except Exception:
        return {"error": "invalid target_date_iso"}
    days_left = max(0, (target - now).days)
    cutoff = now.timestamp() - 14 * 86400
    done_14d = 0
    for ev in bundle.get("learning_events", []):
        iso = _as_iso(ev.get("timestamp") or ev.get("created_at"))
        try:
            ts = datetime.fromisoformat(str(iso).replace("Z", "+00:00")).timestamp() if iso else 0
        except Exception:
            ts = 0
        if ts >= cutoff and ev.get("passed"):
            done_14d += 1
    current_pace = round(done_14d / 14, 2)
    required = round(remaining_missions / max(1, days_left), 2) if days_left else float(remaining_missions)
    return {
        "days_remaining": days_left,
        "remaining_missions": remaining_missions,
        "current_pace_per_day": current_pace,
        "required_pace_per_day": required,
        "pace_gap_per_day": round(required - current_pace, 2),
        "projection": ("At the current pace this target is not reachable in time; "
                       f"increase to ~{required}/day." if required > current_pace else
                       "At the current pace the target completes in time."),
    }


# ─── P2: complexity signal (observed scaling, honest wording) ─────────────

def complexity_signal(bundle: Dict[str, Any], question_id: Optional[str] = None) -> Dict[str, Any]:
    """Observed runtime scaling from stored per-case execution times.

    Never claims proof of Big-O. Wording: "observed scaling suggests…".
    Expected complexity shown only when the bank carries it.
    """
    subs = [s for s in bundle.get("submissions", [])
            if (not question_id or s.get("question_id") == question_id)
            and s.get("failure_class") == "SUCCESS"]
    if not subs:
        return {"question_id": question_id, "sufficient": False,
                "message": "No successful judged submissions with timing yet."}
    points: List[Tuple[float, float]] = []
    for s in subs:
        for r in s.get("results") or []:
            try:
                size = len(str(r.get("input") or ""))
                t = float(r.get("execution_time") or 0)
            except (TypeError, ValueError):
                continue
            if size > 0 and t > 0:
                points.append((float(size), t))
    if len({p[0] for p in points}) < 3 or len(points) < 5:
        return {"question_id": question_id, "sufficient": False,
                "message": "Not enough varied input sizes with timing yet.",
                "samples": len(points)}
    points.sort()
    (s0, t0), (s1, t1) = points[0], points[-1]
    size_ratio = s1 / max(1e-9, s0)
    time_ratio = t1 / max(1e-9, t0)
    # Honest buckets: linear-ish / superlinear / steep.
    if time_ratio <= size_ratio * 1.5:
        suggestion = "Observed scaling suggests near-linear growth."
    elif time_ratio <= size_ratio ** 2 * 1.5:
        suggestion = "Observed scaling suggests superlinear growth — review loop nesting."
    else:
        suggestion = "Observed scaling suggests steep growth — likely needs a better approach."
    expected = None
    if question_id:
        try:
            from app.services import question_store as qs
            q = qs.find_one({"_id": question_id}) or qs.find_one({"id": question_id})
            expected = (q or {}).get("time_complexity") or (q or {}).get("complexity")
        except Exception:
            expected = None
    return {"question_id": question_id, "sufficient": True, "samples": len(points),
            "size_ratio": round(size_ratio, 2), "time_ratio": round(time_ratio, 2),
            "observed": suggestion, "expected_complexity": expected,
            "note": "Runtime evidence only; sandbox conditions vary."}


# ─── P2: portable prep report ─────────────────────────────────────────────

async def prep_report(user_id: str, role: str, company: Optional[str] = None) -> Dict[str, Any]:
    """Evidence report (labeled PlacementPro data, never employer certification)."""
    bundle = await collect_student_evidence(user_id)
    profile = build_target_profile(role, company)
    evidence = await collect_target_evidence(user_id, profile)
    evidence.pop("__meta__", None)
    readiness = calculate_target_readiness(profile, evidence)
    heat = pattern_heatmap(bundle)
    fails = failure_breakdown(bundle)
    recs = personal_records(bundle)
    return {
        "report": "PlacementPro Performance Report",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "target": {"role": role, "company": company},
        "evidence": {
            "coding_attempts": len(bundle["submissions"]),
            "assessments": len(bundle["oa_sessions"]) + len(bundle["aptitude_tests"]),
            "srs_reviews": sum(int(c.get("total_reviews", 0) or 0)
                               for c in list(bundle["srs_cards"]) + list(bundle["srs_states"])),
            "transfer_tasks": sum(1 for e in bundle["learning_events"]
                                  if any(k in str(e.get("activity_type") or "")
                                         for k in ("retest", "repair", "transfer"))),
            "mock_interviews": len(bundle["interviews"]),
        },
        "readiness": {"score": readiness["score"], "coverage": readiness["coverage"],
                      "status": readiness["status"]},
        "skills": [{"skill_id": s["skill_id"], "score": s["score"], "status": s["status"]}
                   for s in readiness["skills"]],
        "blockers": readiness["blockers"],
        "top_failure": fails["top_failure"],
        "records": recs,
        "weakest_pattern": heat["weakest_pattern"],
        "next_action": readiness["next_action"],
        "disclaimer": "PlacementPro student evidence — not an employer certification.",
    }
