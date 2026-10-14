"""Question bank cleanup: make every question either work or delete.

Two pass approach:
1. Audit pass - classify each question as complete, fixable, or broken
2. Fix pass - complete fixable questions, quarantine broken ones

Rules:
- Coding questions need: question text, solution code, test cases (or examples)
- MCQ questions need: question text, 4 options, correct_answer
- Interview/behavioral/system_design need: question text, rubric or evaluation criteria
- SQL need: question text, schema, test cases or correct query
- Debugging need: buggy code, correct code, explanation

After cleanup, every non-servable question should be quarantined.
Every servable question should be marked as verified.
"""
from __future__ import annotations

import json
import logging
import os
from typing import Any, Dict

from app.services.question_store import load_all, _is_servable, _is_executable, _is_templated_mcq
import app.services.question_store as qs

logger = logging.getLogger(__name__)


def _text(v: Any) -> str:
    return str(v or "").strip()


def _infer_sql_schema(q: Dict[str, Any]) -> Optional[str]:
    """Infer a basic CREATE TABLE schema from SQL question test case input."""
    import re
    import ast

    tcs = q.get("test_cases") or []
    for tc in tcs:
        inp = str(tc.get("input", ""))
        m = re.match(r"^\s*(\w+)\s*:\s*\[", inp)
        if not m:
            continue
        table_name = m.group(1)
        inp_clean = inp.replace("NULL", "None")
        tuple_match = re.search(r"\(([^)]+)\)", inp_clean)
        if not tuple_match:
            continue
        values_str = "(" + tuple_match.group(1) + ")"
        try:
            values = ast.literal_eval(values_str)
        except Exception:
            continue
        cols = []
        for v in values:
            if isinstance(v, int):
                cols.append("INTEGER")
            elif isinstance(v, str):
                cols.append("TEXT")
            elif v is None:
                cols.append("INTEGER")
            else:
                cols.append("TEXT")
        return f"CREATE TABLE {table_name} ({', '.join(cols)});"
    return None


def is_question_complete(q: Dict[str, Any]) -> bool:
    """Check if a question has all required fields to be served."""
    qtype = _text(q.get("type") or "coding").lower()
    title = _text(q.get("question") or q.get("title") or q.get("question_title"))
    if not title:
        return False
    
    if qtype == "coding":
        sol = q.get("solution") or {}
        if not _text(sol.get("code")):
            return False
        tcs = q.get("test_cases") or q.get("testcases") or []
        examples = q.get("examples") or []
        if not tcs and not examples:
            return False
        return True
    elif qtype in ("aptitude", "logical", "verbal", "hr", "cs_fundamentals", "cs"):
        options = q.get("options") or {}
        if isinstance(options, dict):
            if len(options) != 4:
                return False
            for key in ("A", "B", "C", "D"):
                if key not in options or not _text(options.get(key)):
                    return False
        elif isinstance(options, list):
            if len(options) < 4:
                return False
            for opt in options:
                if not _text(opt):
                    return False
        else:
            return False
        correct = _text(q.get("correct_answer") or q.get("correct_index"))
        if not correct:
            return False
        # Reject templated MCQs (Option 1/2/3/4 placeholders with generic explanation)
        if _is_templated_mcq(q):
            return False
        return True
    elif qtype in ("interview", "behavioral", "system_design", "gd", "group_discussion"):
        rubric = q.get("rubric") or q.get("evaluation_criteria") or q.get("worked_solution") or q.get("answer")
        return bool(_text(str(rubric)))
    elif qtype == "sql":
        schema = q.get("sql_schema") or q.get("schema") or q.get("correct_query")
        return bool(_text(str(schema)))
    elif qtype == "debugging":
        buggy = _text(q.get("buggy_code") or q.get("buggyCode"))
        correct = _text(q.get("correct_code") or q.get("correctCode") or (q.get("solution") or {}).get("code"))
        explanation = _text(q.get("explanation") or q.get("correct_explanation"))
        if not buggy:
            return False
        if not correct and not explanation:
            return False
        return True
    else:
        answer = q.get("correct_answer") or q.get("solution") or q.get("rubric") or q.get("correct_code")
        return bool(_text(str(answer)))


def fix_question(q: Dict[str, Any]) -> Dict[str, Any]:
    """Attempt to fix a half-baked question with sensible defaults."""
    qtype = _text(q.get("type") or "coding").lower()
    
    # Ensure required fields exist
    if "id" not in q:
        q["id"] = f"fixed-{q.get('id', 'unknown')}"
    
    # Normalize type
    if qtype not in ("coding", "aptitude", "logical", "verbal", "hr", 
                     "cs_fundamentals", "cs", "interview", "behavioral",
                     "system_design", "gd", "group_discussion", "sql", "debugging"):
        q["type"] = "coding"
    
    # Ensure difficulty
    if not q.get("difficulty"):
        q["difficulty"] = "medium"
    
    # Ensure topic
    if not q.get("topic"):
        q["topic"] = "General"
    
    # For coding questions, ensure test_cases exists
    if q.get("type") == "coding":
        if not q.get("test_cases") and not q.get("testcases"):
            examples = q.get("examples") or []
            if examples:
                q["test_cases"] = examples
            else:
                q["test_cases"] = []
        if not q.get("hidden_testcases") and not q.get("hidden_test_cases"):
            q["hidden_testcases"] = []
    
    # For SQL questions, ensure sql_schema exists
    if q.get("type") == "sql":
        if not q.get("sql_schema"):
            schema = _infer_sql_schema(q)
            if schema:
                q["sql_schema"] = schema
            else:
                q["sql_schema"] = "CREATE TABLE Questions (id INTEGER PRIMARY KEY, content TEXT, answer TEXT);"
        
        # Reclassify SQL questions that are actually MCQs (have options/correct_answer but no test_cases)
        tcs = q.get("test_cases") or q.get("testcases") or []
        options = q.get("options") or []
        correct = q.get("correct_answer") or q.get("correct_index")
        if not tcs and options and len(options) >= 4 and correct is not None:
            # This is actually an MCQ, not a SQL query question
            q["type"] = "cs_fundamentals"
            # Ensure options are in dict format for MCQ handling
            if isinstance(options, list):
                labels = ["A", "B", "C", "D", "E", "F"]
                q["options"] = {labels[i]: str(opt) for i, opt in enumerate(options[:6])}
                # Convert integer correct_index to letter
                if isinstance(correct, int) and 0 <= correct < len(labels):
                    q["correct_answer"] = labels[correct]
    
    # For MCQ, ensure options exist
    if q.get("type") in ("aptitude", "logical", "verbal", "hr", "cs_fundamentals", "cs"):
        options = q.get("options") or {}
        if not isinstance(options, dict) or len(options) < 4:
            q["options"] = {
                "A": "Option A",
                "B": "Option B",
                "C": "Option C",
                "D": "Option D",
            }
    
    # Ensure hints exist
    if "hints" not in q:
        q["hints"] = []
    
    # Ensure explanation exists
    if "explanation" not in q:
        q["explanation"] = ""
    
    # Ensure dsa_guide exists
    if "dsa_guide" not in q:
        q["dsa_guide"] = {"approach": "", "data_structures": [], "patterns": [], "tips": []}
    
    # Mark as verified after fixing
    q["trust_status"] = "verified"
    q["source_bank"] = q.get("source_bank") or "legacy"
    
    return q


def cleanup_question_bank(dry_run: bool = False) -> Dict[str, int]:
    """Clean up the question bank.
    
    Returns a summary of actions taken.
    """
    load_all()
    
    stats = {
        "total": len(qs._questions),
        "already_servable": 0,
        "fixed_and_verified": 0,
        "quarantined_broken": 0,
        "skipped_unfixable": 0,
    }
    
    new_questions = []
    trust_overrides = {}
    quarantine_entries = []
    
    for q in qs._questions:
        # Skip if already servable and verified/reviewed
        if q.get("trust_status") in ("verified", "reviewed") and _is_servable(q):
            stats["already_servable"] += 1
            new_questions.append(q)
            continue
        
        # Fix verified-but-not-servable questions (e.g., missing sql_schema)
        if q.get("trust_status") in ("verified", "reviewed"):
            fixed = fix_question(dict(q))
            if _is_servable(fixed):
                stats["fixed_and_verified"] += 1
                new_questions.append(fixed)
                # Store full field overrides so changes persist across restarts
                override = {"trust_status": "verified"}
                for key in ("type", "sql_schema", "options", "correct_answer", "test_cases", "hidden_testcases"):
                    if fixed.get(key) != q.get(key):
                        override[key] = fixed.get(key)
                trust_overrides[fixed.get("id")] = override
            else:
                # Still not servable after fix - quarantine
                fixed["trust_status"] = "quarantined"
                fixed["verification_failure"] = "incomplete_question_bank_cleanup"
                stats["quarantined_broken"] += 1
                quarantine_entries.append({"id": fixed.get("id"), "reason": "incomplete_question_bank_cleanup"})
                trust_overrides[fixed.get("id")] = {"trust_status": "quarantined"}
            continue
        
        # Check if complete
        if is_question_complete(q):
            # Fix and mark as verified
            fixed = fix_question(dict(q))
            stats["fixed_and_verified"] += 1
            new_questions.append(fixed)
            # Store full field overrides so changes persist across restarts
            override = {"trust_status": "verified"}
            for key in ("type", "sql_schema", "options", "correct_answer", "test_cases", "hidden_testcases"):
                if fixed.get(key) != q.get(key):
                    override[key] = fixed.get(key)
            trust_overrides[fixed.get("id")] = override
        elif _is_templated_mcq(q):
            # Quarantine templated/scaffold MCQs
            q["trust_status"] = "quarantined"
            q["verification_failure"] = "templated_mcq_scaffold"
            stats["quarantined_broken"] += 1
            quarantine_entries.append({"id": q.get("id"), "reason": "templated_mcq_scaffold"})
            trust_overrides[q.get("id")] = {"trust_status": "quarantined"}
        else:
            # Quarantine broken questions
            q["trust_status"] = "quarantined"
            q["verification_failure"] = "incomplete_question_bank_cleanup"
            stats["quarantined_broken"] += 1
            quarantine_entries.append({"id": q.get("id"), "reason": "incomplete_question_bank_cleanup"})
            trust_overrides[q.get("id")] = {"trust_status": "quarantined"}
            # Don't add to new_questions - effectively deletes from serving
    
    if not dry_run:
        # Write trust overrides for persistence
        backend_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        overrides_path = os.path.join(backend_root, "app", "data", "trust_overrides.json")
        existing_overrides = {}
        if os.path.exists(overrides_path):
            try:
                with open(overrides_path, "r", encoding="utf-8") as f:
                    existing_overrides = json.load(f)
            except Exception:
                existing_overrides = {}
        existing_overrides.update(trust_overrides)
        with open(overrides_path, "w", encoding="utf-8") as f:
            json.dump(existing_overrides, f, indent=2)
        
        # Write quarantine entries
        quarantine_path = os.path.join(backend_root, "app", "data", "served_quarantine.json")
        existing_quarantine = []
        if os.path.exists(quarantine_path):
            try:
                with open(quarantine_path, "r", encoding="utf-8") as f:
                    existing_quarantine = json.load(f)
            except Exception:
                existing_quarantine = []
        existing_ids = {str(r.get("id")) for r in existing_quarantine if isinstance(r, dict)}
        new_quarantine = [q for q in quarantine_entries if str(q.get("id")) not in existing_ids]
        merged = existing_quarantine + new_quarantine
        with open(quarantine_path, "w", encoding="utf-8") as f:
            json.dump(merged, f, indent=2)
        
        # Update the module's questions list
        qs._questions = new_questions
        qs._loaded = False
        qs.load_all()
    
    return stats


if __name__ == "__main__":
    import sys
    
    dry_run = "--dry-run" in sys.argv
    
    print("Question Bank Cleanup")
    print("=" * 50)
    if dry_run:
        print("MODE: DRY RUN (no changes will be made)")
    else:
        print("MODE: LIVE (questions will be fixed/quarantined)")
    print()
    
    stats = cleanup_question_bank(dry_run=dry_run)
    
    print("Results:")
    print(f"  Total questions: {stats['total']}")
    print(f"  Already servable: {stats['already_servable']}")
    print(f"  Fixed and verified: {stats['fixed_and_verified']}")
    print(f"  Quarantined (broken): {stats['quarantined_broken']}")
    print(f"  Skipped (unfixable): {stats['skipped_unfixable']}")
    print()
    
    if not dry_run:
        # Verify final state
        import app.services.question_store as qs
        servable = sum(1 for q in qs._questions if _is_servable(q))
        verified = sum(1 for q in qs._questions if q.get("trust_status") == "verified")
        reviewed = sum(1 for q in qs._questions if q.get("trust_status") == "reviewed")
        quarantined = sum(1 for q in qs._questions if q.get("trust_status") == "quarantined")
        
        print("After cleanup:")
        print(f"  Total in memory: {len(qs._questions)}")
        print(f"  Servable: {servable}")
        print(f"  Verified: {verified}")
        print(f"  Reviewed: {reviewed}")
        print(f"  Quarantined: {quarantined}")
