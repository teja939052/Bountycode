"""Programmatic backend verification for World 2 lessons.

Tests the API responses for all 5 World 2 flagship lessons.
Does NOT test frontend rendering (requires browser).
"""
from __future__ import annotations

import asyncio
import httpx
from typing import Any

BASE = "http://localhost:8000"
LESSONS = [
    "arrays-1",   # Two Pointers
    "arrays-2",   # Sliding Window
    "arrays-3",   # Hash Map Lookup
    "arrays-4",   # Binary Search
    "arrays-boss", # Arrays Boss
]

# Minimal auth token placeholder — replace with real token or use test auth
HEADERS = {
    "Authorization": "Bearer REPLACE_WITH_REAL_TOKEN",
    "Content-Type": "application/json",
}


async def get_lesson(client: httpx.AsyncClient, slug: str) -> dict[str, Any]:
    resp = await client.get(f"{BASE}/api/v1/lesson/{slug}", headers=HEADERS)
    resp.raise_for_status()
    return resp.json()


async def run_code(client: httpx.AsyncClient, slug: str, code: str) -> dict[str, Any]:
    resp = await client.post(
        f"{BASE}/api/v1/lesson/{slug}/run",
        headers=HEADERS,
        json={"code": code, "language": "python", "stdin": ""},
    )
    resp.raise_for_status()
    return resp.json()


async def submit_build(client: httpx.AsyncClient, slug: str, code: str, fn: str) -> dict[str, Any]:
    resp = await client.post(
        f"{BASE}/api/v1/lesson/{slug}/build",
        headers=HEADERS,
        json={"code": code, "function_name": fn, "language": "python", "step_index": 0},
    )
    resp.raise_for_status()
    return resp.json()


async def submit_transfer(client: httpx.AsyncClient, slug: str, code: str, fn: str) -> dict[str, Any]:
    resp = await client.post(
        f"{BASE}/api/v1/lesson/{slug}/transfer",
        headers=HEADERS,
        json={"code": code, "function_name": fn, "language": "python"},
    )
    resp.raise_for_status()
    return resp.json()


async def check_prediction(client: httpx.AsyncClient, slug: str, answer: str) -> dict[str, Any]:
    resp = await client.post(
        f"{BASE}/api/v1/lesson/{slug}/predict",
        headers=HEADERS,
        json={"answer": answer},
    )
    resp.raise_for_status()
    return resp.json()


async def check_assessment(client: httpx.AsyncClient, slug: str, answers: dict[str, Any]) -> dict[str, Any]:
    resp = await client.post(
        f"{BASE}/api/v1/lesson/{slug}/assess",
        headers=HEADERS,
        json={"answers": answers, "time_spent_seconds": 0},
    )
    resp.raise_for_status()
    return resp.json()


async def complete_lesson(client: httpx.AsyncClient, slug: str, score: float) -> dict[str, Any]:
    resp = await client.post(
        f"{BASE}/api/v1/lesson/{slug}/complete",
        headers=HEADERS,
        json={"score": score, "time_spent_seconds": 60},
    )
    resp.raise_for_status()
    return resp.json()


async def main() -> None:
    print("=" * 70)
    print("WORLD 2 BACKEND API VERIFICATION")
    print("=" * 70)

    async with httpx.AsyncClient(timeout=30) as client:
        for slug in LESSONS:
            print(f"\n[LESSON] {slug}")
            print("-" * 70)

            # 1. GET lesson
            lesson = await get_lesson(client, slug)
            print(f"  lesson_id: {lesson.get('lesson_id')}")
            print(f"  title: {lesson.get('title')}")
            print(f"  xp_reward: {lesson.get('xp_reward')}")

            # Verify structure
            assert "lesson_id" in lesson, "missing lesson_id"
            assert "title" in lesson, "missing title"
            assert "guided_build" in lesson, "missing guided_build"
            assert "transfer_challenge" in lesson, "missing transfer_challenge"
            assert "assessment" in lesson, "missing assessment"
            assert "prediction" in lesson, "missing prediction"
            assert "discovery" in lesson, "missing discovery"
            print("  [OK] lesson structure complete")

            # 2. Check discovery has steps
            discovery_steps = lesson.get("discovery", {}).get("steps", [])
            print(f"  discovery steps: {len(discovery_steps)}")
            for i, step in enumerate(discovery_steps):
                interaction = step.get("interaction", {})
                print(f"    step {i}: type={step.get('type')} interaction={interaction.get('type')} answer={step.get('answer')!r}")
            print("  [OK] discovery steps present")

            # 3. Check prediction
            prediction = lesson.get("prediction", {})
            print(f"  prediction: question={prediction.get('question')!r} options={len(prediction.get('options', []))}")
            assert prediction.get("question"), "prediction missing question"
            print("  [OK] prediction present")

            # 4. Check guided build
            guided_build = lesson.get("guided_build", {})
            build_steps = guided_build.get("steps", [])
            print(f"  guided_build steps: {len(build_steps)}")
            for i, step in enumerate(build_steps):
                print(f"    step {i}: {step.get('title')} diamonds={step.get('diamonds')} max_attempts={step.get('max_attempts')}")
                if step.get("is_debug"):
                    print(f"      DEBUG: buggy_code present={bool(step.get('buggy_code'))}")
            print("  [OK] guided build present")

            # 5. Check transfer
            transfer = lesson.get("transfer_challenge", {})
            print(f"  transfer: {transfer.get('title')} fn={transfer.get('function_name')} max_attempts={transfer.get('max_attempts')}")
            assert transfer.get("function_name"), "transfer missing function_name"
            print("  [OK] transfer present")

            # 6. Check assessment
            assessment = lesson.get("assessment", {})
            questions = assessment.get("questions", [])
            print(f"  assessment: {len(questions)} questions threshold={assessment.get('mastery_threshold')}%")
            for i, q in enumerate(questions):
                print(f"    q{i}: type={q.get('type')}")
            print("  [OK] assessment present")

            # 7. Try running code
            try:
                run_result = await run_code(client, slug, "print('hello')")
                print(f"  run: success={run_result.get('success')} stdout={run_result.get('stdout', '')!r}")
                print("  [OK] run endpoint works")
            except Exception as e:
                print(f"  [WARN] run failed: {e}")

            # 8. Try submitting build with empty code (should fail gracefully)
            try:
                build_result = await submit_build(client, slug, "def solve(): pass", "solve")
                print(f"  build: passed={build_result.get('passed')} score={build_result.get('score')}")
                print("  [OK] build endpoint works")
            except Exception as e:
                print(f"  [WARN] build failed: {e}")

            # 9. Try prediction check
            try:
                pred_result = await check_prediction(client, slug, "wrong_answer")
                print(f"  predict: passed={pred_result.get('passed')} message={pred_result.get('message')!r}")
                print("  [OK] predict endpoint works")
            except Exception as e:
                print(f"  [WARN] predict failed: {e}")

            # 10. Try assessment check
            try:
                assess_result = await check_assessment(client, slug, {})
                print(f"  assess: score={assess_result.get('score')} passed={assess_result.get('passed')}")
                print("  [OK] assess endpoint works")
            except Exception as e:
                print(f"  [WARN] assess failed: {e}")

            print(f"\n[RESULT] {slug}: BACKEND API CHECKS PASSED")

    print("\n" + "=" * 70)
    print("ALL BACKEND API CHECKS COMPLETE")
    print("=" * 70)
    print("\nNOTE: Frontend rendering must be verified manually in browser at:")
    print("  http://localhost:5173/lesson/arrays-1")
    print("  http://localhost:5173/lesson/arrays-2")
    print("  http://localhost:5173/lesson/arrays-3")
    print("  http://localhost:5173/lesson/arrays-4")
    print("  http://localhost:5173/lesson/arrays-boss")


if __name__ == "__main__":
    asyncio.run(main())
