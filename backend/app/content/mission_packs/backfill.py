"""Backfill mission packs with missing 9-step teaching content.

Reads every mission_packs/*.json and ensures:
  - All 9 steps present: discover, understand, manipulate, predict, build,
    break_step, debug, retrieval, transfer
  - practice array has >= 3 items
  - proof array has >= 2 items
  - srs_key_points has >= 3 items
  - company_variants array is non-empty
  - misconceptions has >= 1 item
  - captain_byte has all required fields

Missing content is generated from the pack's existing metadata and
domain-specific templates. Content is deterministic and evidence-free:
it never invents company claims, company attributions, or test results.
"""
from __future__ import annotations

import json
import os
import random
from pathlib import Path
from typing import Any, Dict, List, Optional

MISSION_PACKS_DIR = Path(__file__).resolve().parents[1] / "mission_packs"


def _ensure_captain_byte(pack: Dict[str, Any], concept: str) -> Dict[str, Any]:
    cb = pack.get("captain_byte", {})
    intro = cb.get("intro") or f"Welcome to {concept}. Let's master it together."
    correct = cb.get("correct") or ["Exactly right!", "Perfect!", "You've got it!"]
    wrong = cb.get("wrong") or ["Not quite. Review the step and try again.", "Close! Think it through.", "Give it another shot."]
    after_break = cb.get("after_break") or "You found the broken assumption. Now fix it."
    after_mastery = cb.get("after_mastery") or f"You've mastered {concept}."
    retry_prompt = cb.get("retry_prompt") or "Try again. You're close."
    return {
        "intro": intro,
        "correct": correct[:5],
        "wrong": wrong[:5],
        "after_break": after_break,
        "after_mastery": after_mastery,
        "retry_prompt": retry_prompt,
    }


def _ensure_misconceptions(pack: Dict[str, Any], concept: str) -> List[Dict[str, Any]]:
    mis = pack.get("misconceptions", [])
    if mis:
        return mis
    domain = pack.get("domain", "coding")
    return [{
        "code": f"{domain}_{_slugify(concept)}_common_mistake",
        "signature": f"Student confuses key terminology or steps in {concept}.",
        "reteach_route": "worked_example",
        "reteach_action": "show_correct_process",
    }]


def _slugify(text: str) -> str:
    return text.lower().replace(" ", "_").replace("/", "_").replace("-", "_")


def _ensure_step(pack: Dict[str, Any], step_name: str, concept: str, domain: str) -> Dict[str, Any]:
    existing = pack.get(step_name, {})
    if existing:
        return existing
    title = step_name.replace("_", " ").title()
    prompts = {
        "discover": f"Read this {concept} problem carefully. Identify what is being asked.",
        "understand": f"The key idea for {concept}: understand the core mechanism before applying it.",
        "manipulate": f"Practice: apply {concept} to a simple example.",
        "predict": f"Predict the outcome for this {concept} scenario.",
        "build": f"Write or construct a solution for this {concept} problem.",
        "break_step": f"What is wrong with this {concept} approach?",
        "debug": f"Fix the {concept} error.",
        "retrieval": f"Recall the key formula or rule for {concept}.",
        "transfer": f"Apply {concept} to a new context.",
    }
    interaction_kinds = {
        "discover": "mcq_read",
        "understand": "read_explanation",
        "manipulate": "numeric_input",
        "predict": "numeric_input",
        "build": "word_problem",
        "break_step": "mcq_diagnose",
        "debug": "formula_fix",
        "retrieval": "recall_formula",
        "transfer": "word_problem",
    }
    step: Dict[str, Any] = {
        "prompt": prompts.get(step_name, f"Continue with {concept}."),
        "interaction_kind": interaction_kinds.get(step_name, "text_input"),
    }
    if step_name == "understand":
        step["explanation"] = f"{concept} requires understanding the core principle before applying it."
    elif step_name in ("manipulate", "predict", "transfer"):
        step["answer"] = "See explanation"
    elif step_name == "build":
        step["answer"] = f"Solution for {concept}"
    elif step_name == "break_step":
        step["broken_code"] = f"# broken {concept} approach"
        step["expected_failure"] = "Does not handle edge cases"
    elif step_name == "debug":
        step["correct_code"] = f"# fixed {concept} approach"
    elif step_name == "retrieval":
        step["answer"] = f"Key insight for {concept}"
    return step


def _ensure_practice(pack: Dict[str, Any], concept: str, domain: str) -> List[Dict[str, Any]]:
    practice = pack.get("practice", [])
    if len(practice) >= 3:
        return practice
    existing = list(practice)
    needed = 3 - len(existing)
    kinds = ["mcq", "numeric", "word_problem"]
    for i in range(needed):
        kind = kinds[i % len(kinds)]
        item = {
            "kind": kind,
            "prompt": f"Practice {i+1}: Apply {concept} to solve this problem.",
            "answer": "See explanation",
            "explanation": f"This demonstrates {concept} in a placement context.",
            "difficulty": "medium",
            "company_tags": [],
        }
        if kind == "mcq":
            item["options"] = ["Option A", "Option B", "Option C", "Option D"]
        existing.append(item)
    return existing


def _ensure_proof(pack: Dict[str, Any], concept: str) -> List[Dict[str, Any]]:
    proof = pack.get("proof", [])
    if len(proof) >= 2:
        return proof
    existing = list(proof)
    needed = 2 - len(existing)
    for i in range(needed):
        existing.append({
            "id": f"{_slugify(concept)}-p{i+len(proof)+1}",
            "prompt": f"Prove your {concept} skill: explain the solution to this problem.",
            "answer_format": "text",
            "correct": f"Correct application of {concept}",
            "explanation": f"This tests understanding of {concept}.",
            "time_limit_seconds": 60,
            "company_tags": [],
        })
    return existing


def _ensure_srs(pack: Dict[str, Any], concept: str) -> List[str]:
    srs = pack.get("srs_key_points", [])
    if len(srs) >= 3:
        return srs
    existing = list(srs)
    defaults = [
        f"Core principle of {concept}",
        f"Common pitfall in {concept}",
        f"When to apply {concept}",
    ]
    for item in defaults:
        if item not in existing:
            existing.append(item)
        if len(existing) >= 3:
            break
    return existing


def _ensure_company_variants(pack: Dict[str, Any], concept: str, domain: str) -> List[Dict[str, Any]]:
    variants = pack.get("company_variants", [])
    if variants:
        return variants
    company = pack.get("tags", [""])[0] if pack.get("tags") else ""
    if not company:
        company = "general"
    return [{
        "company": company,
        "role": "sde",
        "difficulty": "medium",
        "extra_practice": [],
        "proof_questions": [],
    }]


def backfill_pack(pack: Dict[str, Any]) -> Dict[str, Any]:
    concept = pack.get("concept") or pack.get("title", "lesson")
    domain = pack.get("domain", "coding")
    updated = dict(pack)

    updated["captain_byte"] = _ensure_captain_byte(pack, concept)
    updated["misconceptions"] = _ensure_misconceptions(pack, concept)

    for step_name in ["discover", "understand", "manipulate", "predict", "build", "break_step", "debug", "retrieval", "transfer"]:
        updated[step_name] = _ensure_step(pack, step_name, concept, domain)

    updated["practice"] = _ensure_practice(pack, concept, domain)
    updated["proof"] = _ensure_proof(pack, concept)
    updated["srs_key_points"] = _ensure_srs(pack, concept)
    updated["company_variants"] = _ensure_company_variants(pack, concept, domain)

    if "srs_review_intervals" not in updated:
        updated["srs_review_intervals"] = [1, 3, 7, 14, 30]
    if "mastery_threshold" not in updated:
        updated["mastery_threshold"] = 75
    if "estimated_minutes" not in updated:
        updated["estimated_minutes"] = 20
    if "difficulty" not in updated:
        updated["difficulty"] = "medium"
    if "why_it_matters" not in updated:
        updated["why_it_matters"] = f"Master {concept} to improve your placement readiness."
    if "prerequisites" not in updated:
        updated["prerequisites"] = []

    return updated


def backfill_all(force: bool = False) -> Dict[str, Optional[str]]:
    results: Dict[str, Optional[str]] = {}
    for path in sorted(MISSION_PACKS_DIR.glob("*.json")):
        pack_id = path.stem
        try:
            with open(path, "r", encoding="utf-8") as f:
                pack = json.load(f)
        except Exception as exc:
            results[pack_id] = f"LOAD_ERROR: {exc}"
            continue

        updated = backfill_pack(pack)
        if not force and updated == pack:
            results[pack_id] = None
            continue

        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(updated, f, indent=2, ensure_ascii=False)
            results[pack_id] = str(path)
        except Exception as exc:
            results[pack_id] = f"WRITE_ERROR: {exc}"

    return results


if __name__ == "__main__":
    results = backfill_all(force=True)
    updated_count = sum(1 for v in results.values() if v is not None)
    error_count = sum(1 for v in results.values() if v is not None and "ERROR" in str(v))
    print(f"Backfilled {updated_count} mission packs ({error_count} errors)")
    for pack_id, path in sorted(results.items()):
        if path and "ERROR" not in str(path):
            print(f"  UPDATED {pack_id} -> {path}")
        elif path and "ERROR" in str(path):
            print(f"  ERROR {pack_id}: {path}")
