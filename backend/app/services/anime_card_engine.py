"""Anime Card Engine — progress, prove judge, SRS recall, and tracing playback."""
from __future__ import annotations

import asyncio
import logging
from typing import Any
from datetime import datetime, timezone

from app.content.curriculum.anime_cards import get_pilot_atoms, get_atom
from app.services.spaced_repetition import SpacedRepetitionEngine, SRSState, ReviewGrade
from app.database import (
    anime_cards_collection,
    anime_card_progress_collection,
    srs_cards_collection,
)
from app.middleware.auth import get_current_user

logger = logging.getLogger(__name__)


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _emit(event: str, user_id: str, card_id: str, payload: dict[str, Any]) -> None:
    logger.info(
        "anime_card_signal",
        extra={"event": event, "user_id": user_id, "card_id": card_id, **payload},
    )


def _default_recall_result() -> dict[str, Any]:
    return {"grade": "again", "interval": 0, "next_review": None}


def _default_prove_result() -> dict[str, Any]:
    return {"passed": False, "score": 0.0, "output": "", "error": "", "test_cases": 0, "failures": 0}


async def list_cards(language_id: str) -> list[dict[str, Any]]:
    return get_pilot_atoms(language_id)


async def get_card(card_id: str) -> dict[str, Any] | None:
    return get_atom(card_id)


async def get_trace_steps(card_id: str) -> list[dict[str, Any]]:
    atom = get_atom(card_id)
    if not atom:
        return []
    return atom.get("tracing", {}).get("steps", [])


async def judge_recall(card_id: str, user_id: str, selected: str) -> dict[str, Any]:
    atom = get_atom(card_id)
    if not atom:
        return _default_recall_result()
    answer = atom.get("recall", {}).get("answer", "")
    correct = selected.strip().lower() == answer.strip().lower()
    col = srs_cards_collection()
    existing = await col.find_one({"user_id": user_id, "concept_id": f"anime:{card_id}"})
    engine = SpacedRepetitionEngine()
    if existing:
        state = SRSState(
            concept_id=f"anime:{card_id}",
            user_id=user_id,
            interval=existing.get("interval_days", existing.get("interval", 0)),
            repetitions=existing.get("review_count", existing.get("repetitions", 0)),
            ease_factor=existing.get("ease_factor", 2.5),
        )
        grade = ReviewGrade.GOOD if correct else ReviewGrade.AGAIN
        state = engine.review(state, grade)
    else:
        state = engine.create_new_card(f"anime:{card_id}", user_id)
        state = engine.review(state, ReviewGrade.GOOD if correct else ReviewGrade.AGAIN)
    await col.update_one(
        {"user_id": user_id, "concept_id": f"anime:{card_id}"},
        {"$set": _srs_doc(state)},
        upsert=True,
    )
    _emit(
        "recall_reviewed",
        user_id,
        card_id,
        {"correct": correct, "grade": "good" if correct else "again", "interval": state.interval},
    )
    return {
        "grade": "good" if correct else "again",
        "interval": state.interval,
        "next_review": state.next_review.isoformat() if state.next_review else None,
    }


def _srs_doc(state: SRSState) -> dict[str, Any]:
    return {
        "concept_id": state.concept_id,
        "user_id": state.user_id,
        "interval_days": state.interval,
        "review_count": state.repetitions,
        "ease_factor": state.ease_factor,
        "next_review": state.next_review.isoformat() if state.next_review else None,
        "updated_at": utcnow().isoformat(),
    }


async def judge_prove(card_id: str, user_id: str, code: str) -> dict[str, Any]:
    atom = get_atom(card_id)
    if not atom:
        return _default_prove_result()
    prove = atom.get("prove", {})
    public_cases = prove.get("test_cases", [])
    hidden_cases = prove.get("hidden_tests", [])
    mastery_threshold = float(prove.get("mastery_threshold", 1.0))
    common_failures = prove.get("common_failures", [])
    all_cases = [*public_cases, *hidden_cases]
    failures: list[dict[str, Any]] = []
    for tc in all_cases:
        result = await _run_case(prove.get("language", "python"), code, tc)
        if not result.get("ok"):
            failures.append(result)
    passed = len(all_cases) == 0 or (len(failures) / len(all_cases)) <= (1.0 - mastery_threshold)
    score = 10.0 if passed else max(0.0, 10.0 * (1.0 - len(failures) / max(len(all_cases), 1)))
    _emit(
        "prove_reviewed",
        user_id,
        card_id,
        {
            "passed": passed,
            "score": score,
            "test_cases": len(all_cases),
            "failures": len(failures),
            "hidden_tests": len(hidden_cases),
            "mastery_threshold": mastery_threshold,
        },
    )
    return {
        "passed": passed,
        "score": score,
        "output": failures[0].get("output", "") if failures else "",
        "error": failures[0].get("error", "") if failures else "",
        "test_cases": len(all_cases),
        "failures": len(failures),
        "hidden_tests": len(hidden_cases),
        "mastery_threshold": mastery_threshold,
        "common_failures": common_failures,
    }


async def _run_case(language: str, code: str, tc: dict[str, Any]) -> dict[str, Any]:
    if language not in {"python", "javascript", "java"}:
        return {"ok": False, "error": "unsupported-language", "output": ""}

    stdin = ""
    if "input" in tc:
        stdin = str(tc.get("input", ""))

    try:
        if language == "java":
            return await _run_java_case(code, tc)
        from app.services.local_sandbox import execute_local

        result = await execute_local(code, language, stdin=stdin, timeout=5)
        stdout = result.get("stdout", "") or ""
        stderr = result.get("stderr", "") or ""
        compile_error = result.get("compile_error") or result.get("error")
        success = result.get("success", False)

        expected = tc.get("expected")
        if expected is None:
            expected = tc.get("output")

        if not success or compile_error:
            return {"ok": False, "error": compile_error or stderr or "execution-failed", "output": stdout}

        actual = stdout.strip()
        if isinstance(expected, bool):
            expected_str = str(expected).strip()
            ok = actual.lower() == expected_str.lower()
        elif isinstance(expected, (int, float)):
            try:
                ok = float(actual) == float(expected)
            except Exception:
                ok = False
        else:
            ok = actual == str(expected).strip()

        return {"ok": ok, "error": "" if ok else f"expected {expected!r}, got {actual!r}", "output": stdout}
    except Exception as exc:
        return {"ok": False, "error": f"runner-error: {exc}", "output": ""}


async def _run_java_case(code: str, tc: dict[str, Any]) -> dict[str, Any]:
    import re
    from app.services.docker_sandbox import get_docker_sandbox

    class_match = re.search(r"public\s+class\s+(\w+)", code)
    method_match = re.search(r"public\s+static\s+\w+\s+(\w+)\s*\(([^)]*)\)", code)
    if not class_match or not method_match:
        return {"ok": False, "error": "Could not parse Java class/method signature", "output": ""}

    class_name = class_match.group(1)
    method_name = method_match.group(1)
    params = method_match.group(2).strip()

    arg_exprs = []
    if params:
        for raw in params.split(","):
            raw = raw.strip()
            if "int" in raw:
                arg_exprs.append("1")
            elif "String" in raw:
                arg_exprs.append('"a"')
            elif "boolean" in raw:
                arg_exprs.append("true")
            else:
                arg_exprs.append("1")

    test_value = tc.get("x", 1)
    if len(arg_exprs) >= 1:
        arg_exprs[0] = str(test_value)

    wrapper = (
        code.rstrip()
        + f"\n\npublic class {class_name}Runner {{\n"
        + f"    public static void main(String[] args) {{\n"
        + f"        try {{\n"
        + f"            {class_name} obj = new {class_name}();\n"
        + f"            Object result = obj.{method_name}({', '.join(arg_exprs)});\n"
        + f"            System.out.println(result);\n"
        + f"        }} catch (Exception e) {{\n"
        + f"            System.err.println(e.getMessage());\n"
        + f"        }}\n"
        + f"    }}\n"
        + f"}}\n"
    )

    sandbox = get_docker_sandbox()
    result = await sandbox.execute(wrapper, "java", stdin=stdin, timeout=10)
    stdout = (result.stdout or "").strip()
    stderr = (result.stderr or "").strip()
    compile_error = result.compile_error or result.error

    if not result.success or compile_error:
        return {"ok": False, "error": compile_error or stderr or "execution-failed", "output": stdout}

    expected = tc.get("expected")
    if expected is None:
        expected = tc.get("output")

    if isinstance(expected, bool):
        expected_str = str(expected).strip()
        ok = stdout.lower() == expected_str.lower()
    elif isinstance(expected, (int, float)):
        try:
            ok = float(stdout) == float(expected)
        except Exception:
            ok = False
    else:
        ok = stdout == str(expected).strip()

    return {"ok": ok, "error": "" if ok else f"expected {expected!r}, got {stdout!r}", "output": stdout}


async def record_card_progress(user_id: str, card_id: str, step: str, score: float) -> None:
    col = anime_card_progress_collection()
    await col.update_one(
        {"user_id": user_id, "card_id": card_id},
        {"$set": {f"steps.{step}": {"done": True, "score": score, "ts": utcnow().isoformat()}}},
        upsert=True,
    )
    _emit("step_completed", user_id, card_id, {"step": step, "score": score})
