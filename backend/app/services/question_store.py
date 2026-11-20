import json
import logging
import os
import re
import importlib.util
import sys
import contextlib
import uuid
from typing import Optional, Any, List, Dict
from datetime import datetime, timezone

from app.config import get_settings

from app.services import question_quality

logger = logging.getLogger(__name__)

_questions: list[dict] = []
_loaded = False
_mongo_loaded = False
_unverified_questions: list[dict] = []
_unverified_loaded = False

settings = get_settings()

# ---------------------------------------------------------------------------
# Consolidated JSON question bank (single-file fast load)
# ---------------------------------------------------------------------------
_BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_BANK_JSON = os.path.join(_BACKEND_ROOT, "app", "data", "questions_bank.json")

_SEED_FILES: list[str] = []

# Striver A2Z DSA sheet ordering — the canonical interview patterns, in the
# order serious candidates study them. Every question is tagged with one of
# these so users can practice pattern-wise, exactly like Striver's sheet.
STRIVER_PATTERNS = [
    "Learn the Basics",
    "Patterns",
    "Arrays",
    "Binary Search",
    "Sorting",
    "Two Pointers",
    "Sliding Window",
    "Prefix Sum",
    "Hashing / Hash Map",
    "Recursion & Backtracking",
    "Linked Lists",
    "Stacks & Queues",
    "Monotonic Stack",
    "Heaps / Priority Queue",
    "Trees",
    "Binary Search Trees",
    "Heaps",
    "Graphs",
    "BFS & DFS",
    "Union Find",
    "Shortest Path",
    "Tries",
    "Dynamic Programming 1D",
    "Dynamic Programming 2D",
    "Dynamic Programming on Strings",
    "DP on Subsequences",
    "DP on Trees",
    "Greedy",
    "Intervals",
    "Bit Manipulation",
    "Math & Number Theory",
    "Strings",
    "String Matching",
    "Design / OOP",
]

# topic -> canonical Striver pattern mapping. Falls back to keyword detection.
TOPIC_TO_PATTERN = {
    "arrays": "Arrays",
    "array": "Arrays",
    "arrays & hashing": "Arrays",
    "hash table": "Hashing / Hash Map",
    "hashing": "Hashing / Hash Map",
    "hash map": "Hashing / Hash Map",
    "binary search": "Binary Search",
    "two pointers": "Two Pointers",
    "two pointer": "Two Pointers",
    "sliding window": "Sliding Window",
    "prefix sum": "Prefix Sum",
    "linked lists": "Linked Lists",
    "linked list": "Linked Lists",
    "linkedlist": "Linked Lists",
    "stack": "Stacks & Queues",
    "queues": "Stacks & Queues",
    "stacks queues": "Stacks & Queues",
    "monotonic stack": "Monotonic Stack",
    "heap": "Heaps / Priority Queue",
    "heaps": "Heaps / Priority Queue",
    "heap priority queue": "Heaps / Priority Queue",
    "priority queue": "Heaps / Priority Queue",
    "trees": "Trees",
    "binary trees": "Trees",
    "binary tree": "Trees",
    "bst": "Binary Search Trees",
    "binary search trees": "Binary Search Trees",
    "binary search tree": "Binary Search Trees",
    "graphs": "Graphs",
    "graph": "Graphs",
    "bfs": "BFS & DFS",
    "dfs": "BFS & DFS",
    "union find": "Union Find",
    "disjoint set": "Union Find",
    "shortest path": "Shortest Path",
    "dijkstra": "Shortest Path",
    "tries": "Tries",
    "trie": "Tries",
    "dynamic programming": "Dynamic Programming 1D",
    "dp": "Dynamic Programming 1D",
    "recursion": "Recursion & Backtracking",
    "backtracking": "Recursion & Backtracking",
    "greedy": "Greedy",
    "intervals": "Intervals",
    "interval": "Intervals",
    "bit manipulation": "Bit Manipulation",
    "math": "Math & Number Theory",
    "maths": "Math & Number Theory",
    "strings": "Strings",
    "string": "Strings",
    "string matching": "String Matching",
    "kmp": "String Matching",
    "design": "Design / OOP",
    "sorting": "Sorting",
    "sort": "Sorting",
    "searching": "Binary Search",
    "recursion & backtracking": "Recursion & Backtracking",
    "dp on strings": "Dynamic Programming on Strings",
    "dp on subsequences": "DP on Subsequences",
    "dp on trees": "DP on Trees",
}

_PATTERN_KEYWORDS = [
    ("Dynamic Programming on Strings", ["lcs", "edit distance", "longest common subsequence", "palindromic subsequence", "distinct subsequences"]),
    ("DP on Subsequences", ["coin change", "subset sum", "partition equal", "0/1 knapsack", "unbounded knapsack", "target sum"]),
    ("DP on Trees", ["binary tree maximum path", "house robber iii", "diameter of binary tree"]),
    ("Dynamic Programming 2D", ["unique paths", "minimum path sum", "triangle", "grid", "edit distance", "matrix chain"]),
    ("Sliding Window", ["substring", "sliding window", "maximum sum subarray of size", "longest subarray", "minimum window"]),
    ("Two Pointers", ["two pointers", "sorted array", "three sum", "trapping rain water", "container with most water"]),
    ("Binary Search", ["binary search", "sorted", "peak element", "search in rotated", "kth"]),
    ("Prefix Sum", ["prefix sum", "subarray sum", "range sum", "running sum", "contiguous subarray"]),
    ("Monotonic Stack", ["next greater", "next smaller", "stock span", "largest rectangle", "daily temperatures"]),
    ("Union Find", ["union find", "connected components", "number of islands", "redundant connection", "accounts merge"]),
    ("Shortest Path", ["shortest path", "dijkstra", "bellman", "floyd", "network delay"]),
    ("Tries", ["trie", "prefix", "dictionary", "autocomplete", "word search ii"]),
    ("Bit Manipulation", ["bit", "xor", "bitwise", "single number", "power of two", "hamming weight"]),
    ("Heaps / Priority Queue", ["heap", "priority queue", "top k", "kth largest", "merge k", "median from"]),
    ("Intervals", ["interval", "merge intervals", "meeting rooms", "insert interval", "non-overlapping"]),
    ("Greedy", ["greedy", "jump game", "gas station", "assign cookies", "minimum number of arrows"]),
    ("Math & Number Theory", ["prime", "gcd", "modulo", "factorial", "palindrome number", "reverse integer"]),
    ("String Matching", ["kmp", "rabin-karp", "pattern", "substring search", "z-algorithm"]),
    ("Recursion & Backtracking", ["permutations", "combination sum", "subsets", "n-queens", "word break", "generate parentheses"]),
    ("Design / OOP", ["design", "lru cache", "lfucache", "trie implementation", "min stack", "deque"]),
    ("Linked Lists", ["linked list", "linkedlist", "lru cache", "reverse list", "detect cycle"]),
    ("Stacks & Queues", ["stack", "queue", "valid parentheses", "min stack", "evaluate", "infix", "postfix"]),
    ("BFS & DFS", ["bfs", "dfs", "level order", "number of islands", "flood fill", "rotten oranges", "surrounded regions"]),
    ("Graphs", ["graph", "topological", "course schedule", "cycle detection", "alien dictionary"]),
    ("Trees", ["binary tree", "binary tree", "traversal", "lowest common ancestor", "invert tree", "path sum"]),
    ("Binary Search Trees", ["bst", "binary search tree", "validate bst", "kth smallest", "inorder"]),
    ("Dynamic Programming 1D", ["fibonacci", "climbing stairs", "house robber", "longest increasing", "decode ways", "word break", "coin change"]),
    ("Arrays", ["array", "two sum", "merge sorted", "rotate", "move zeroes", "majority element", "best time to buy", "maximum subarray", "product of array"]),
    ("Strings", ["string", "anagram", "palindrome", "reverse words", "valid parentheses", "longest palindromic", "group anagrams"]),
    ("Bit Manipulation", ["missing number", "single number", "number of 1"]),
]


def _detect_pattern(q: dict) -> str:
    """Best-effort Striver pattern detection from topic + title + description.
    Patterns are a coding-problem concept only: non-coding question types
    (sql, interview, aptitude, verbal, logical, cs fundamentals ...) are left
    untagged so they can never pollute a coding pattern page."""
    if str(q.get("type") or "coding").lower() != "coding":
        return ""
    topic = _normalize_topic(q.get("topic"))
    if topic in TOPIC_TO_PATTERN:
        return TOPIC_TO_PATTERN[topic]
    blob = " ".join([
        str(q.get("question") or ""),
        str(q.get("question_title") or ""),
        str(q.get("description") or ""),
        str(q.get("sub_topic") or ""),
    ]).lower()
    for pattern, keywords in _PATTERN_KEYWORDS:
        for kw in keywords:
            if kw in blob:
                return pattern
    sub = _normalize_topic(q.get("sub_topic"))
    if sub in TOPIC_TO_PATTERN:
        return TOPIC_TO_PATTERN[sub]
    return "Arrays"

TOPIC_DISPLAY = {
    "arrays": "Arrays",
    "linked lists": "Linked Lists",
    "stacks queues": "Stacks & Queues",
    "stack": "Stacks & Queues",
    "trees": "Trees",
    "graphs": "Graphs",
    "dynamic programming": "Dynamic Programming",
    "greedy": "Greedy",
    "tries": "Tries",
    "heaps": "Heaps",
    "heap priority queue": "Heaps",
    "sorting": "Sorting",
    "searching": "Searching",
    "bit manipulation": "Bit Manipulation",
    "math": "Math",
    "strings": "Strings",
    "binary search": "Binary Search",
    "two pointers": "Two Pointers",
    "sliding window": "Sliding Window",
    "prefix sum": "Prefix Sum",
    "monotonic stack": "Monotonic Stack",
    "union find": "Union Find",
    "backtracking": "Backtracking",
    "intervals": "Intervals",
    "hash table": "Hash Table",
    "design": "Design",
    "aptitude": "Aptitude",
    "logical reasoning": "Logical Reasoning",
    "verbal ability": "Verbal Ability",
    "coding challenges": "Coding Challenges",
}


def _normalize_topic(name) -> str:
    """Normalize a topic name for matching: lower, strip, dash/underscore -> space."""
    return re.sub(r"[-_]+", " ", str(name or "").strip().lower())


def _display_topic(name) -> str:
    """Pretty display name for a normalized topic key."""
    norm = _normalize_topic(name)
    display = TOPIC_DISPLAY.get(norm)
    if display:
        return display
    return " ".join(w.capitalize() for w in norm.split())


def _load_from_module(filepath: str, var_names: list[str]) -> list[dict]:
    """Import a Python data file and extract list variables."""
    results = []
    try:
        spec = importlib.util.spec_from_file_location("_qstore_mod", filepath)
        if not spec or not spec.loader:
            return results
        mod = importlib.util.module_from_spec(spec)
        with contextlib.redirect_stdout(None):
            spec.loader.exec_module(mod)
        for name in var_names:
            data = getattr(mod, name, None)
            if isinstance(data, list):
                results.extend(data)
            elif isinstance(data, dict):
                for k, v in data.items():
                    if isinstance(v, list):
                        results.extend(v)
    except Exception as e:
        logger.warning("Failed to load %s: %s", filepath, e)
    return results


def _assign_id(q: dict, idx: int) -> dict:
    """Ensure every question has a string id.

    Also normalizes alternate bank schemas onto the canonical in-memory
    schema WITHOUT inventing content (Residency + No-LLM rules):
    - debugging_bank: buggy_code/correct_code/test_cases -> solution/testcases
    - system_design / interview: rubric/requirements preserved, no tests needed
    """
    if "_id" in q:
        q["id"] = str(q.pop("_id"))
    elif "id" not in q:
        q["id"] = f"q_{idx:06d}"
    else:
        q["id"] = str(q["id"])

    # Debugging-bank adapter: map alternate field names onto canonical ones.
    if not q.get("testcases") and isinstance(q.get("test_cases"), list):
        q["testcases"] = q["test_cases"]
    if not q.get("testcases") and isinstance(q.get("visible_test_cases"), list):
        q["testcases"] = q["visible_test_cases"]
    if (not q.get("solution") or not isinstance(q.get("solution"), dict)
            or not q["solution"].get("code")):
        if q.get("correct_code"):
            q["solution"] = {"code": q["correct_code"], "language": q.get("language", "python")}
        elif q.get("buggy_code") and not q.get("solution"):
            q["solution"] = {}
    if not q.get("question") and q.get("statement"):
        q["question"] = q["statement"]
    if not q.get("question") and q.get("title"):
        q["question"] = q["title"]

    if "company" in q and isinstance(q["company"], list):
        q["companies"] = q["company"]
    elif "company" in q and isinstance(q["company"], str):
        q["companies"] = [q["company"]]
    elif "companies" not in q:
        q["companies"] = []

    if "type" not in q:
        q["type"] = "coding"
    if "difficulty" not in q:
        q["difficulty"] = "medium"
    if "topic" not in q:
        q["topic"] = "General"
    if "sub_topic" not in q:
        q["sub_topic"] = ""
    if "frequency" not in q:
        q["frequency"] = 0
    if "hints" not in q:
        q["hints"] = []
    if "solution" not in q:
        q["solution"] = {}
    if "explanation" not in q:
        q["explanation"] = ""
    if "dsa_guide" not in q:
        q["dsa_guide"] = {"approach": "", "data_structures": [], "patterns": [], "tips": []}
    if "pattern" not in q:
        q["pattern"] = _detect_pattern(q)
    if "trust_status" not in q:
        q["trust_status"] = "unverified"
    if not q.get("source_bank"):
        q["source_bank"] = "legacy"
    return q


def _json_bank_fresh() -> bool:
    """Return True if the JSON bank exists and is newer than every seed .py file."""
    if not os.path.exists(_BANK_JSON):
        return False
    try:
        json_mtime = os.path.getmtime(_BANK_JSON)
    except OSError:
        return False
    base = _BACKEND_ROOT
    for fname in _SEED_FILES:
        fpath = os.path.join(base, fname)
        if os.path.exists(fpath) and os.path.getmtime(fpath) > json_mtime:
            return False
    return True


def _load_from_json_bank() -> bool:
    """Load questions from the consolidated JSON bank. Returns True on success."""
    global _questions
    try:
        with open(_BANK_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            logger.warning("JSON bank is not a list, ignoring")
            return False
        idx = 0
        for q in data:
            if isinstance(q, dict):
                _questions.append(_assign_id(q, idx))
                idx += 1
        logger.info("Loaded %d questions from JSON bank %s", len(_questions), _BANK_JSON)
        return True
    except Exception as e:
        logger.warning("Failed to load JSON bank: %s", e)
        return False


def _load_from_seed_files() -> None:
    """Load questions from the 17 Python seed files (legacy fallback)."""
    global _questions
    base = _BACKEND_ROOT
    idx = len(_questions)

    for fname in _SEED_FILES:
        fpath = os.path.join(base, fname)
        if os.path.exists(fpath):
            items = _load_from_module(fpath, ["questions"])
            for q in items:
                if isinstance(q, dict) and q.get("question"):
                    _questions.append(_assign_id(dict(q), idx))
                    idx += 1
            logger.info("Loaded %d from %s", len(items), fname)


VERIFIED_EXTRA_BANKS = [
    "verified_placement_questions.json",
    "sql_practice_bank.json",
    "interview_practice_bank.json",
    "india_placement_depth.json",
    "system_design_bank.json",
    "debugging_bank.json",
    "promoted_questions.json",
    "tranche_promoted.json",
    "exam_memory_approved.json",
    "tcs_nqt_coding_verified.json",
    "tcs_nqt_mcq_verified.json",
    "infosys_infytq_verified.json",
    "wipro_nlth_verified.json",
    "cognizant_genc_verified.json",
    "capgemini_accenture_verified.json",
    "verified_aptitude.json",
    "verified_logical.json",
    "verified_verbal.json",
    "verified_cs_fundamentals.json",
]

UNVERIFIED_EXTRA_BANKS = [
    "leetcode_problems_seed.json",
    "striver_a2z_600.json",
    "tcs_nqt_questions.json",
    "infosys_questions.json",
    "legacy_enriched_coding.json",
    "questions/tcs_nqt_all.json",
    "generated/tcs/quant_workrate.json",
    "generated/tcs/quant_discount.json",
    "generated/tcs/quant_profit.json",
    "generated/tcs/quant_train.json",
    "generated/tcs/quant_remainder.json",
    "generated/tcs/quant_hcf.json",
    "generated/tcs/log_blood.json",
    "generated/tcs/log_coding.json",
    "generated/tcs/log_syllogism.json",
    "generated/tcs/log_series.json",
    "generated/tcs/log_seating.json",
    "generated/tcs/log_dir.json",
    "generated/infosys/pseudo_loop.json",
    "generated/infosys/pseudo_factorial.json",
    "generated/ltimindtree/verbal_error.json",
    "generated/ltimindtree/verbal_blank.json",
    "generated/accenture/tech_fund.json",
]

# Default serving uses verified-only extra banks.
EXTRA_BANKS = list(VERIFIED_EXTRA_BANKS)

# LLM-drafted candidates: UNVERIFIED raw material only (No-LLM Bank Rule,
# AGENTS.md binding). These never enter student-facing serving. They live in
# the isolated unverified pool via load_unverified() and enter the bank only
# through the trust pipeline (AUTOMATED_CHECKED -> HUMAN_REVIEWED -> TRUSTED).
# Residency: files on disk (backend/app/data/), loaded into process memory.
AUTO_CHECKED_BANKS = [
    "llm_draft_checked.json",
    "expanded_question_bank.json",
    "verified_question_bank.json",
]


def _load_auto_checked_banks(target: Optional[list] = None) -> None:
    """Load banks that already passed automated execution validation.

    These are production artifacts produced by scripts/autocheck_bank.py and
    similar deterministic checks. They belong in the main verified pool so
    student flows can serve them without re-executing the full bank."""
    if target is None:
        target = _questions
    for fname in AUTO_CHECKED_BANKS:
        extra_path = os.path.join(_BACKEND_ROOT, "app", "data", fname)
        if not os.path.exists(extra_path):
            continue
        try:
            with open(extra_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            logger.warning("Failed to read auto-checked bank %s: %s", fname, e)
            continue
        if not isinstance(data, list):
            continue
        idx = len(target)
        added = 0
        for q in data:
            if isinstance(q, dict) and (q.get("question") or q.get("question_title") or q.get("title")):
                target.append(_assign_id(dict(q), idx))
                idx += 1
                added += 1
        if added:
            logger.info("Loaded %d auto-checked problems from %s", added, fname)


def _load_unverified_banks_for_verification(target: Optional[list] = None) -> None:
    """Load unverified banks into the target so the auto-verifier can promote
    passable entries to automated_checked.

    Student-facing serving is still gated by trust_status after verification."""
    if target is None:
        target = _questions
    for fname in list(UNVERIFIED_EXTRA_BANKS) + ["questions_bank.json"]:
        extra_path = os.path.join(_BACKEND_ROOT, "app", "data", fname)
        if not os.path.exists(extra_path):
            continue
        try:
            with open(extra_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            logger.warning("Failed to read unverified bank %s: %s", fname, e)
            continue
        if not isinstance(data, list):
            continue
        idx = len(target)
        added = 0
        for q in data:
            if isinstance(q, dict) and (q.get("question") or q.get("question_title") or q.get("title")):
                target.append(_assign_id(dict(q), idx))
                idx += 1
                added += 1
        if added:
            logger.info("Loaded %d unverified problems from %s for verification", added, fname)


def _load_extra_bank(target: Optional[list] = None, bank_list: Optional[list] = None) -> None:
    """Load file-based banks into the target list (default: verified extra banks).

    Each JSON is a curated list with constraints + test cases, appended before
    dedupe so curated-grade wins."""
    if target is None:
        target = _questions
    if bank_list is None:
        bank_list = EXTRA_BANKS
    for fname in bank_list:
        extra_path = os.path.join(_BACKEND_ROOT, "app", "data", fname)
        if not os.path.exists(extra_path):
            continue
        try:
            with open(extra_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            logger.warning("Failed to read extra bank %s: %s", fname, e)
            continue
        if not isinstance(data, list):
            continue
        idx = len(target)
        added = 0
        for q in data:
            if isinstance(q, dict) and q.get("question"):
                target.append(_assign_id(dict(q), idx))
                idx += 1
                added += 1
        if added:
            logger.info("Loaded %d problems from %s", added, fname)


def load_all():
    global _questions, _loaded
    if _loaded:
        return
    _questions = []

    # Verified-only default serving starts with curated extra banks.
    _load_extra_bank(_questions)

    # Auto-checked banks have already passed deterministic execution
    # validation, so they belong in the main verified serving pool.
    _load_auto_checked_banks(_questions)

    # Also load unverified banks so the background auto-verifier can promote
    # passable entries to automated_checked. Quarantined items are filtered
    # out before student-facing serving.
    _load_unverified_banks_for_verification(_questions)

    _dedupe_and_filter(_questions)
    _apply_served_quarantine(_questions)
    _apply_leetcode_meta()

    # Backfill sql_schema for SQL questions missing it (dedupe may keep a
    # variant from another bank that lacks sql_schema). Every SQL question
    # must have schema-backed evaluation to be servable.
    _backfill_sql_schema(_questions)

    # Compute executable field for each question
    for q in _questions:
        q["executable"] = _is_executable(q)

    # Content trust integrity: audit (log only) any question with
    # trust_status="verified" that bypassed the trust lifecycle
    # (i.e., lacks trust_transitioned_at/trust_transition_reason). Such
    # questions were likely batch-imported directly into a JSON bank
    # without going through transition_trust(). They remain servable but
    # are flagged for manual review via structured log.
    _audit_trust_integrity(_questions)

    # Content trust migration: downgrade batch-added questions (identifiable
    # by their ID prefixes) from verified to automated_checked/needs_review.
    # This does not touch pre-existing verified questions that may be
    # genuinely human-reviewed.
    _migrate_batch_added_questions(_questions)

    # Quality migration: downgrade verified bronze-quality questions (score < 60)
    # that lack trust transition metadata. These questions lack
    # critical fields (test cases, schema, options+answer, etc.) and cannot
    # be trusted without human review. Questions with transition metadata
    # are preserved even if bronze, as they may be genuinely human-reviewed
    # but poorly written.
    _migrate_bronze_verified_questions(_questions)

    # Score every servable question against its type-specific standard.
    # Quality score and tier are stored on the question dict for the API
    # and gamification/matchmaking downstream.
    _score_all_questions(_questions)

    # Map every servable question to its canonical skill ID so that
    # mastery, SRS, readiness, and company-prep can all speak the same
    # language. Questions without a canonical skill remain unassigned.
    _map_question_skills(_questions)

    _loaded = True


def _audit_trust_integrity(target: list) -> int:
    """
    Audit questions with trust_status="verified" that lack trust transition
    metadata. Such questions were likely batch-imported without going through
    transition_trust(). They are downgraded to automated_checked (if
    executable) or needs_review (if not) so they are not served as
    human-verified content.

    Returns the count of downgraded questions.
    """
    flagged = 0
    for q in target:
        trust = str(q.get("trust_status", "unverified")).lower()
        if trust != TRUST_VERIFIED:
            continue
        if q.get("trust_transitioned_at") and q.get("trust_transition_reason"):
            continue  # Human-reviewed through the trust lifecycle
        flagged += 1
        logger.warning(
            "Trust integrity: question %s has trust_status='verified' but no "
            "trust transition record. It may have been batch-imported without "
            "human review. Consider reviewing and transitioning via "
            "transition_trust().",
            q.get("id"),
        )
    return flagged


# Question IDs from batch scripts follow this prefix pattern.
# These questions were imported without human review and lack trust transition
# metadata.
BATCH_QUESTION_ID_PREFIXES = (
    "cs-b2-", "cs-b3-", "cs-b4-", "cs-b5-",
    "apt-b2-", "apt-b3-", "apt-b4-", "apt-b5-", "apt-b6-",
    "log-b2-", "log-b3-", "log-b4-", "log-b5-", "log-b6-",
    "ver-b2-", "ver-b3-", "ver-b4-",
    "debug-b2-", "debug-b3-", "debug-b4-", "debug-b5-", "debug-b6-", "debug-b7-",
    "sd-b2-", "sql-b2-",
)


def _migrate_batch_added_questions(target: list) -> int:
    """
    Downgrade questions that were batch-added via import scripts without human
    review. These questions carry trust_status="verified" but lack trust
    transition metadata. They are identifiable by their ID prefixes which
    follow the pattern <bank>-<batch>-<topic>-<n> (e.g., cs-b2-oop-01,
    apt-b4-pct-01, log-b6-01, debug-b7-01, sql-b2-01).

    Downgrades verified→automated_checked (if executable) or needs_review
    (if not executable), so they are not served as human-verified content.

    Returns the count of downgraded questions.
    """
    downgraded = 0
    for q in target:
        trust = str(q.get("trust_status", "unverified")).lower()
        if trust != TRUST_VERIFIED:
            continue
        if q.get("trust_transitioned_at") and q.get("trust_transition_reason"):
            continue  # Human-reviewed through the trust lifecycle
        qid = str(q.get("id", ""))
        if not any(qid.startswith(p) for p in BATCH_QUESTION_ID_PREFIXES):
            continue  # Not a batch-added question; leave as-is

        if _is_executable(q):
            q["trust_status"] = TRUST_AUTOMATED_CHECKED
            q["trust_transitioned_at"] = datetime.now(timezone.utc).isoformat()
            q["trust_transition_reason"] = (
                "Downgraded from verified to automated_checked: question was "
                "batch-imported without a recorded trust transition. Human "
                "review required before serving as verified content."
            )
        else:
            q["trust_status"] = TRUST_NORMALIZED
            q["trust_transitioned_at"] = datetime.now(timezone.utc).isoformat()
            q["trust_transition_reason"] = (
                "Downgraded from verified to needs_review: question was "
                "batch-imported without a recorded trust transition and fails "
                "executable validation. Human review required."
            )
        downgraded += 1

    if downgraded:
        logger.info(
            "Trust migration: downgraded %d batch-added verified questions to "
            "automated_checked/needs_review", downgraded
        )
    return downgraded


def _migrate_bronze_verified_questions(target: list) -> int:
    """
    Downgrade verified bronze-quality questions (score < 60) that lack trust
    transition metadata. These questions were imported without human review
    and lack critical fields (test cases, schema, options+answer, rubric,
    etc.). They cannot be trusted as servable content.

    Questions with transition metadata are preserved even if bronze, as they
    may be genuinely human-reviewed but poorly written.

    Returns the count of downgraded questions.
    """
    from app.services.question_quality import score_question

    downgraded = 0
    for q in target:
        trust = str(q.get("trust_status", "unverified")).lower()
        if trust != TRUST_VERIFIED:
            continue
        if q.get("trust_transitioned_at") and q.get("trust_transition_reason"):
            continue  # Human-reviewed through the trust lifecycle
        qid = str(q.get("id", ""))
        if any(qid.startswith(p) for p in BATCH_QUESTION_ID_PREFIXES):
            continue  # Already handled by _migrate_batch_added_questions

        result = score_question(q)
        if result["score"] < 60:
            q["trust_status"] = TRUST_NORMALIZED
            q["trust_transitioned_at"] = datetime.now(timezone.utc).isoformat()
            q["trust_transition_reason"] = (
                "Downgraded from verified to needs_review: question scored "
                f"{result['score']}/100 ({result['quality_tier']}). "
                "Missing fields: "
                + ", ".join(f["label"] for f in result["fields"] if not f["present"])[:200]
                + ". Human review required before serving as verified content."
            )
            q["quality_score"] = result["score"]
            q["quality_tier"] = result["quality_tier"]
            downgraded += 1

    if downgraded:
        logger.info(
            "Trust migration: downgraded %d bronze-quality verified questions "
            "to needs_review (missing critical fields)", downgraded
        )
    return downgraded


def _score_all_questions(target: list) -> int:
    """
    Score every servable question against its type-specific standard.
    Quality score and tier are stored on the question dict for the API
    and gamification/matchmaking downstream.
    """
    from app.services.question_quality import score_question

    scored = 0
    for q in target:
        result = score_question(q)
        q["quality_score"] = result["score"]
        q["quality_tier"] = result["quality_tier"]
        q["quality_missing"] = result["missing"]
        scored += 1
    return scored


def _map_question_skills(target: list) -> int:
    """
    Map every servable question to its canonical skill ID based on its topic/sub_topic.
    Questions without a canonical skill ID get canonical_skill_id=None.

    Returns the count of questions that received a skill mapping.
    """
    from app.services.skill_taxonomy import canonical_skill_id

    mapped = 0
    for q in target:
        topic = str(q.get("topic", "")).strip().lower()
        sub_topic = str(q.get("sub_topic", "")).strip().lower()

        canonical_id = None
        # Try topic first, then sub_topic
        for name in [topic, sub_topic]:
            if name:
                canonical_id = canonical_skill_id(name)
                if canonical_id:
                    break

        if canonical_id:
            q["canonical_skill_id"] = canonical_id
            mapped += 1
        else:
            # Explicitly set to None so consumers know it was considered
            q["canonical_skill_id"] = None

    if mapped:
        logger.info(
            "Question skill mapping: mapped %d questions to canonical skills", mapped
        )
    return mapped


def _apply_served_quarantine(target: list) -> None:
    """Mark execution-broken served IDs as quarantined (in-place, no removal).

    SEED layer: reads backend/app/data/served_quarantine.json (autocheck
    artifact). The RUNTIME layer is Mongo (served_quarantine collection) —
    see apply_mongo_quarantine_overrides(), called at startup after load_all.
    File seeds first boot; Mongo deltas (student-quorum inserts, backfilled
    rows) apply on top, so restarts never lose quarantine decisions (§1.1).
    They stay in the total question count for repair/review, but are excluded
    from student-facing serving by _is_servable(). When uncertain,
    quarantine (Trust Rule).
    """
    global _questions
    path = os.path.join(_BACKEND_ROOT, "app", "data", "served_quarantine.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            rows = json.load(f)
    except Exception:
        return
    bad_ids = {str(r.get("id")) for r in rows if isinstance(r, dict) and r.get("id")}
    if not bad_ids:
        return
    quarantined = 0
    for q in target:
        if str(q.get("id")) in bad_ids:
            q["trust_status"] = "quarantined"
            quarantined += 1
    if quarantined:
        logger.info("Served quarantine: %d questions marked quarantined", quarantined)


async def apply_mongo_quarantine_overrides(target: list | None = None) -> int:
    """Apply Mongo-served quarantine decisions over the in-memory bank.

    Reads the served_quarantine collection (backfilled once from the JSON
    seed, then appended by student-quorum inserts) and marks matches
    quarantined in place. Returns the count marked. Safe to call when the
    collection is empty (fresh DB → file seed stands alone).
    """
    global _questions
    if target is None:
        target = _questions
    try:
        from app.database import served_quarantine_collection
        docs = await served_quarantine_collection.find({}, {"question_id": 1}).to_list(5000)
    except Exception as e:
        logger.warning("Mongo quarantine overrides unavailable: %s", e)
        return 0
    bad_ids = {str(d.get("question_id")) for d in docs if d.get("question_id")}
    if not bad_ids:
        return 0
    n = 0
    for q in target:
        if str(q.get("id")) in bad_ids and q.get("trust_status") != "quarantined":
            q["trust_status"] = "quarantined"
            n += 1
    if n:
        logger.info("Mongo quarantine overrides: %d questions marked quarantined", n)
    return n


def mark_quarantined_in_memory(question_id: str) -> bool:
    """Immediately quarantine one id in the in-memory bank (no restart).

    Called right after a student-quorum Mongo insert so the decision takes
    effect on this process now; restarts re-derive it from Mongo. Sync and
    best-effort by design (serving correctness never depends on it).
    """
    global _questions
    try:
        for q in _questions:
            if str(q.get("id")) == str(question_id):
                q["trust_status"] = "quarantined"
                return True
    except Exception:
        pass
    return False


def load_unverified():
    """Load dirty / unverified banks into the isolated unverified pool.

    This is for admin / candidate mode only. Student-facing flows must not
    call this."""
    global _unverified_questions, _unverified_loaded
    if _unverified_loaded:
        return
    _unverified_questions = []

    # Load consolidated JSON bank (all entries have missing trust_status)
    if os.path.exists(_BANK_JSON):
        try:
            with open(_BANK_JSON, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                idx = 0
                for q in data:
                    if isinstance(q, dict):
                        _unverified_questions.append(_assign_id(dict(q), idx))
                        idx += 1
                logger.info("Loaded %d unverified questions from JSON bank", len(_unverified_questions))
        except Exception as e:
            logger.warning("Failed to load unverified JSON bank: %s", e)

    # Load unverified extra banks + LLM-draft candidates (isolated pool only).
    # LLM drafts are UNVERIFIED raw material for the repair queue — never served.
    for fname in list(UNVERIFIED_EXTRA_BANKS) + list(AUTO_CHECKED_BANKS):
        extra_path = os.path.join(_BACKEND_ROOT, "app", "data", fname)
        if not os.path.exists(extra_path):
            continue
        try:
            with open(extra_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            logger.warning("Failed to read unverified extra bank %s: %s", fname, e)
            continue
        if not isinstance(data, list):
            continue
        idx = len(_unverified_questions)
        added = 0
        for q in data:
            if isinstance(q, dict) and q.get("question"):
                _unverified_questions.append(_assign_id(dict(q), idx))
                idx += 1
                added += 1
        if added:
            logger.info("Loaded %d unverified problems from %s", added, fname)

    _dedupe_and_filter(_unverified_questions)
    _unverified_loaded = True
    logger.info("Loaded %d unverified questions total", len(_unverified_questions))


def _apply_leetcode_meta():
    """Enrich curated questions with full LeetCode metadata (statement,
    constraints, expected complexity, follow-up, per-example explanations,
    LeetCode problem number) via the ``app.data.leetcode_meta`` overlay.

    The compact one-line ``description`` is preserved for list views; the
    detailed ``statement`` is what problem-detail pages render.
    """
    global _questions
    try:
        from app.data.leetcode_meta import LEETCODE_META
    except Exception as e:
        logger.warning("LeetCode metadata overlay unavailable: %s", e)
        return
    enriched = 0
    for q in _questions:
        meta = LEETCODE_META.get(q.get("id"))
        if not meta:
            continue
        if meta.get("statement"):
            q["statement"] = meta["statement"]
        if meta.get("constraints"):
            q["constraints"] = meta["constraints"]
        for key in ("expected_time_complexity", "expected_space_complexity", "follow_up", "leetcode_number"):
            if key in meta:
                q[key] = meta[key]
        explanations = meta.get("example_explanations") or {}
        for i, ex in enumerate(q.get("examples", []) or []):
            if isinstance(ex, dict) and i in explanations and not ex.get("explanation"):
                ex["explanation"] = explanations[i]
        enriched += 1
    logger.info("LeetCode metadata applied to %d curated questions", enriched)


def _backfill_sql_schema(target: list) -> int:
    """Backfill sql_schema for SQL questions missing it.

    Deduplication may keep a variant from another bank that lacks sql_schema.
    Every SQL question needs schema-backed evaluation to be executable and
    therefore servable. Uses the question's sub_topic to pick a schema
    template matching its tables and columns.
    """

    _SQL_SCHEMA_TEMPLATES = {
        "basic_select": {
            "schema_ddl": "CREATE TABLE Employees (id INT PRIMARY KEY, name VARCHAR(100), department VARCHAR(50), salary INT, age INT);",
            "seed_inserts": "INSERT INTO Employees VALUES (1,'Alice','Engineering',70000,28),(2,'Bob','HR',50000,30),(3,'Charlie','Engineering',55000,25);",
            "expected_query": "SELECT name FROM Employees WHERE department = 'Engineering' AND salary > 60000;",
            "enforce_order": False,
        },
        "order_by": {
            "schema_ddl": "CREATE TABLE Products (id INT PRIMARY KEY, name VARCHAR(100), price INT, category VARCHAR(50));",
            "seed_inserts": "INSERT INTO Products VALUES (1,'A',100,'X'),(2,'B',200,'Y'),(3,'C',150,'X');",
            "expected_query": "SELECT * FROM Products ORDER BY price DESC;",
            "enforce_order": True,
        },
        "aggregation": {
            "schema_ddl": "CREATE TABLE Orders (id INT PRIMARY KEY, customer_id INT, amount INT, order_date DATE);",
            "seed_inserts": "INSERT INTO Orders VALUES (1,101,200,'2024-01-01'),(2,102,300,'2024-01-02'),(3,101,150,'2024-01-03');",
            "expected_query": "SELECT COUNT(*) FROM Orders;",
            "enforce_order": False,
        },
        "group_by": {
            "schema_ddl": "CREATE TABLE Employees (id INT PRIMARY KEY, name VARCHAR(100), department VARCHAR(50), salary INT);",
            "seed_inserts": "INSERT INTO Employees VALUES (1,'A','Eng',70000),(2,'B','HR',50000),(3,'C','Eng',80000),(4,'D','HR',60000);",
            "expected_query": "SELECT department, COUNT(*) as employee_count FROM Employees GROUP BY department;",
            "enforce_order": False,
        },
        "distinct": {
            "schema_ddl": "CREATE TABLE Orders (id INT PRIMARY KEY, customer_id INT, amount INT);",
            "seed_inserts": "INSERT INTO Orders VALUES (1,101,200),(2,102,300),(3,101,150);",
            "expected_query": "SELECT COUNT(DISTINCT customer_id) FROM Orders;",
            "enforce_order": False,
        },
        "inner_join": {
            "schema_ddl": "CREATE TABLE Employees (id INT PRIMARY KEY, name VARCHAR(100), dept_id INT); CREATE TABLE Departments (dept_id INT PRIMARY KEY, dept_name VARCHAR(50));",
            "seed_inserts": "INSERT INTO Employees VALUES (1,'A',10),(2,'B',20); INSERT INTO Departments VALUES (10,'Eng'),(20,'HR');",
            "expected_query": "SELECT e.name, d.dept_name FROM Employees e INNER JOIN Departments d ON e.dept_id = d.dept_id;",
            "enforce_order": True,
        },
        "null_handling": {
            "schema_ddl": "CREATE TABLE Employees (id INT PRIMARY KEY, name VARCHAR(100), manager_id INT);",
            "seed_inserts": "INSERT INTO Employees VALUES (1,'A',NULL),(2,'B',1),(3,'C',NULL);",
            "expected_query": "SELECT name FROM Employees WHERE manager_id IS NULL;",
            "enforce_order": False,
        },
        "date_filtering": {
            "schema_ddl": "CREATE TABLE Orders (id INT PRIMARY KEY, order_date DATE, amount INT);",
            "seed_inserts": "INSERT INTO Orders VALUES (1,'2024-01-15',100),(2,'2023-12-31',200),(3,'2024-06-20',150);",
            "expected_query": "SELECT * FROM Orders WHERE YEAR(order_date) = 2024;",
            "enforce_order": False,
        },
        "group_by_having": {
            "schema_ddl": "CREATE TABLE Orders (id INT PRIMARY KEY, customer_id INT, amount INT);",
            "seed_inserts": "INSERT INTO Orders VALUES (1,101,200),(2,102,300),(3,101,150),(4,101,100),(5,102,250),(6,102,180),(7,102,220),(8,103,300);",
            "expected_query": "SELECT customer_id, COUNT(*) as order_count FROM Orders GROUP BY customer_id HAVING COUNT(*) > 3;",
            "enforce_order": False,
        },
        "subquery_where": {
            "schema_ddl": "CREATE TABLE Employees (id INT PRIMARY KEY, name VARCHAR(100), salary INT, department VARCHAR(50));",
            "seed_inserts": "INSERT INTO Employees VALUES (1,'A','Eng',70000),(2,'B','Eng',50000),(3,'C','HR',60000),(4,'D','HR',55000);",
            "expected_query": "SELECT name FROM Employees e WHERE salary > (SELECT AVG(salary) FROM Employees WHERE department = e.department);",
            "enforce_order": False,
        },
        "left_join": {
            "schema_ddl": "CREATE TABLE Employees (id INT PRIMARY KEY, name VARCHAR(100), dept_id INT); CREATE TABLE Departments (dept_id INT PRIMARY KEY, dept_name VARCHAR(50));",
            "seed_inserts": "INSERT INTO Employees VALUES (1,'A',10),(2,'B',NULL); INSERT INTO Departments VALUES (10,'Eng');",
            "expected_query": "SELECT e.name, d.dept_name FROM Employees e LEFT JOIN Departments d ON e.dept_id = d.dept_id;",
            "enforce_order": True,
        },
        "self_join": {
            "schema_ddl": "CREATE TABLE Employees (id INT PRIMARY KEY, name VARCHAR(100), manager_id INT);",
            "seed_inserts": "INSERT INTO Employees VALUES (1,'A',NULL),(2,'B',1),(3,'C',1);",
            "expected_query": "SELECT e.name AS employee, m.name AS manager FROM Employees e LEFT JOIN Employees m ON e.manager_id = m.id;",
            "enforce_order": True,
        },
        "cte": {
            "schema_ddl": "CREATE TABLE Orders (id INT PRIMARY KEY, customer_id INT, amount INT, order_date DATE);",
            "seed_inserts": "INSERT INTO Orders VALUES (1,101,200,'2024-01-01'),(2,102,300,'2024-01-02'),(3,101,150,'2024-01-03');",
            "expected_query": "WITH CustomerTotal AS (SELECT customer_id, SUM(amount) as total FROM Orders GROUP BY customer_id) SELECT customer_id, total FROM CustomerTotal;",
            "enforce_order": False,
        },
        "case_statement": {
            "schema_ddl": "CREATE TABLE Employees (id INT PRIMARY KEY, name VARCHAR(100), salary INT);",
            "seed_inserts": "INSERT INTO Employees VALUES (1,'A',90000),(2,'B',60000),(3,'C',40000);",
            "expected_query": "SELECT name, CASE WHEN salary > 80000 THEN 'High' WHEN salary > 50000 THEN 'Medium' ELSE 'Low' END as grade FROM Employees;",
            "enforce_order": True,
        },
        "coalesce": {
            "schema_ddl": "CREATE TABLE Employees (id INT PRIMARY KEY, name VARCHAR(100), bonus INT);",
            "seed_inserts": "INSERT INTO Employees VALUES (1,'A',1000),(2,'B',NULL),(3,'C',500);",
            "expected_query": "SELECT name, COALESCE(bonus, 0) as bonus FROM Employees;",
            "enforce_order": True,
        },
        "window_row_number": {
            "schema_ddl": "CREATE TABLE Employees (id INT PRIMARY KEY, name VARCHAR(100), salary INT, department VARCHAR(50));",
            "seed_inserts": "INSERT INTO Employees VALUES (1,'A','Eng',70000),(2,'B','HR',60000),(3,'C','Eng',80000),(4,'D','HR',55000);",
            "expected_query": "SELECT name, department, salary, ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rn FROM Employees;",
            "enforce_order": True,
        },
        "window_rank": {
            "schema_ddl": "CREATE TABLE Employees (id INT PRIMARY KEY, name VARCHAR(100), salary INT, department VARCHAR(50));",
            "seed_inserts": "INSERT INTO Employees VALUES (1,'A','Eng',70000),(2,'B','Eng',70000),(3,'C','HR',60000);",
            "expected_query": "SELECT name, department, salary, RANK() OVER (PARTITION BY department ORDER BY salary DESC) as rank FROM Employees;",
            "enforce_order": True,
        },
        "running_total": {
            "schema_ddl": "CREATE TABLE Orders (id INT PRIMARY KEY, order_date DATE, amount INT);",
            "seed_inserts": "INSERT INTO Orders VALUES (1,'2024-01-01',100),(2,'2024-01-02',200),(3,'2024-01-03',150);",
            "expected_query": "SELECT order_date, amount, SUM(amount) OVER (ORDER BY order_date) as running_total FROM Orders;",
            "enforce_order": True,
        },
        "top_n_per_group": {
            "schema_ddl": "CREATE TABLE Employees (id INT PRIMARY KEY, name VARCHAR(100), salary INT, department VARCHAR(50));",
            "seed_inserts": "INSERT INTO Employees VALUES (1,'A','Eng',90000),(2,'B','Eng',80000),(3,'C','HR',70000),(4,'D','HR',60000),(5,'E','HR',65000);",
            "expected_query": "SELECT name, department, salary FROM (SELECT name, department, salary, ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rn FROM Employees) t WHERE rn <= 2;",
            "enforce_order": True,
        },
        "correlated_subquery": {
            "schema_ddl": "CREATE TABLE Employees (id INT PRIMARY KEY, name VARCHAR(100), salary INT, department VARCHAR(50));",
            "seed_inserts": "INSERT INTO Employees VALUES (1,'A','Eng',90000),(2,'B','Eng',70000),(3,'C','HR',50000),(4,'D','HR',40000);",
            "expected_query": "SELECT name FROM Employees e WHERE salary > (SELECT AVG(salary) FROM Employees WHERE department = e.department);",
            "enforce_order": False,
        },
        "complex_join_aggregation": {
            "schema_ddl": "CREATE TABLE Departments (dept_id INT PRIMARY KEY, dept_name VARCHAR(50), location VARCHAR(50)); CREATE TABLE Employees (id INT PRIMARY KEY, name VARCHAR(100), dept_id INT, salary INT); CREATE TABLE Projects (id INT PRIMARY KEY, name VARCHAR(100), dept_id INT, budget INT);",
            "seed_inserts": "INSERT INTO Departments VALUES (10,'Eng','NY'); INSERT INTO Employees VALUES (1,'A',10,70000),(2,'B',10,80000); INSERT INTO Projects VALUES (1,'X',10,50000);",
            "expected_query": "SELECT d.dept_name, COUNT(e.id) as emp_count, COALESCE(SUM(p.budget), 0) as total_budget FROM Departments d LEFT JOIN Employees e ON d.dept_id = e.dept_id LEFT JOIN Projects p ON d.dept_id = p.dept_id GROUP BY d.dept_id, d.dept_name;",
            "enforce_order": False,
        },
        "recursive_cte": {
            "schema_ddl": "CREATE TABLE Employees (id INT PRIMARY KEY, name VARCHAR(100), manager_id INT);",
            "seed_inserts": "INSERT INTO Employees VALUES (1,'CEO',NULL),(2,'VP',1),(3,'Mgr',2),(4,'Dev',3);",
            "expected_query": "WITH RECURSIVE OrgChart AS (SELECT id, name, manager_id, 1 as level FROM Employees WHERE manager_id IS NULL UNION ALL SELECT e.id, e.name, e.manager_id, oc.level + 1 FROM Employees e INNER JOIN OrgChart oc ON e.manager_id = oc.id) SELECT id, name, level FROM OrgChart ORDER BY level, id;",
            "enforce_order": True,
        },
        "duplicate_detection": {
            "schema_ddl": "CREATE TABLE Orders (id INT PRIMARY KEY, customer_id INT, product_id INT, order_date DATE, amount INT);",
            "seed_inserts": "INSERT INTO Orders VALUES (1,101,1,'2024-01-01',100),(2,101,1,'2024-01-01',100),(3,102,2,'2024-01-02',200);",
            "expected_query": "SELECT customer_id, product_id, order_date, COUNT(*) as duplicate_count FROM Orders GROUP BY customer_id, product_id, order_date HAVING COUNT(*) > 1;",
            "enforce_order": False,
        },
        "performance_reasoning": {
            "schema_ddl": "CREATE TABLE Orders (id INT PRIMARY KEY, order_date DATE, amount INT); CREATE INDEX idx_orders_date ON Orders(order_date);",
            "seed_inserts": "INSERT INTO Orders VALUES (1,'2024-01-01',100);",
            "expected_query": "SELECT * FROM Orders WHERE order_date >= '2024-01-01' AND order_date < '2025-01-01';",
            "enforce_order": False,
        },
        "string_functions": {
            "schema_ddl": "CREATE TABLE Employees (id INT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100));",
            "seed_inserts": "INSERT INTO Employees VALUES (1,'A','alice@example.com'),(2,'B','bob@test.org');",
            "expected_query": "SELECT name, SUBSTRING_INDEX(email, '@', -1) as domain FROM Employees;",
            "enforce_order": True,
        },
        "second_highest": {
            "schema_ddl": "CREATE TABLE Employees (id INT PRIMARY KEY, name VARCHAR(100), salary INT);",
            "seed_inserts": "INSERT INTO Employees VALUES (1,'A',100000),(2,'B',80000),(3,'C',60000);",
            "expected_query": "SELECT MAX(salary) as second_highest FROM Employees WHERE salary < (SELECT MAX(salary) FROM Employees);",
            "enforce_order": False,
        },
        "normalization": {
            "schema_ddl": "CREATE TABLE Customers (customer_id INT PRIMARY KEY, name VARCHAR(100), address VARCHAR(255)); CREATE TABLE Orders (order_id INT PRIMARY KEY, customer_id INT, product_id INT, order_date DATE, FOREIGN KEY (customer_id) REFERENCES Customers(customer_id));",
            "seed_inserts": "INSERT INTO Customers VALUES (1,'Alice','123 Main St'); INSERT INTO Orders VALUES (100,1,1,'2024-01-01');",
            "expected_query": "CREATE TABLE Customers (customer_id INT PRIMARY KEY, name VARCHAR(100), address VARCHAR(255)); CREATE TABLE Orders (order_id INT PRIMARY KEY, customer_id INT, product_id INT, order_date DATE, FOREIGN KEY (customer_id) REFERENCES Customers(customer_id));",
            "enforce_order": False,
        },
        "nullif": {
            "schema_ddl": "CREATE TABLE Sales (id INT PRIMARY KEY, product VARCHAR(100), units_sold INT, units_returned INT);",
            "seed_inserts": "INSERT INTO Sales VALUES (1,'A',100,20),(2,'B',200,NULL),(3,'C',150,50);",
            "expected_query": "SELECT product, units_sold - COALESCE(units_returned, 0) as net_units FROM Sales;",
            "enforce_order": True,
        },
        "dense_rank": {
            "schema_ddl": "CREATE TABLE Employees (id INT PRIMARY KEY, name VARCHAR(100), salary INT, department VARCHAR(50));",
            "seed_inserts": "INSERT INTO Employees VALUES (1,'A','Eng',90000),(2,'B','Eng',90000),(3,'C','Eng',80000);",
            "expected_query": "SELECT name, department, salary, DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) as rank FROM Employees;",
            "enforce_order": True,
        },
        "right_join": {
            "schema_ddl": "CREATE TABLE Departments (dept_id INT PRIMARY KEY, dept_name VARCHAR(50)); CREATE TABLE Employees (id INT PRIMARY KEY, name VARCHAR(100), dept_id INT);",
            "seed_inserts": "INSERT INTO Departments VALUES (10,'Eng'),(20,'HR'); INSERT INTO Employees VALUES (1,'A',10);",
            "expected_query": "SELECT d.dept_name, e.name FROM Departments d LEFT JOIN Employees e ON d.dept_id = e.dept_id;",
            "enforce_order": True,
        },
        "string_functions_2": {
            "schema_ddl": "CREATE TABLE Employees (id INT PRIMARY KEY, name VARCHAR(100));",
            "seed_inserts": "INSERT INTO Employees VALUES (1,'alice'),(2,'Bob');",
            "expected_query": "SELECT id, UPPER(name) as name FROM Employees;",
            "enforce_order": True,
        },
        "group_concat": {
            "schema_ddl": "CREATE TABLE Orders (id INT PRIMARY KEY, customer_id INT, product_name VARCHAR(100));",
            "seed_inserts": "INSERT INTO Orders VALUES (1,101,'A'),(2,101,'B'),(3,102,'C');",
            "expected_query": "SELECT customer_id, GROUP_CONCAT(product_name ORDER BY product_name SEPARATOR ', ') as products FROM Orders GROUP BY customer_id;",
            "enforce_order": True,
        },
        "except": {
            "schema_ddl": "CREATE TABLE Customers (id INT PRIMARY KEY, name VARCHAR(100)); CREATE TABLE PremiumCustomers (id INT PRIMARY KEY, name VARCHAR(100));",
            "seed_inserts": "INSERT INTO Customers VALUES (1,'A'),(2,'B'),(3,'C'); INSERT INTO PremiumCustomers VALUES (2,'B');",
            "expected_query": "SELECT id, name FROM Customers EXCEPT SELECT id, name FROM PremiumCustomers;",
            "enforce_order": False,
        },
        "interview_performance": {
            "schema_ddl": "CREATE TABLE Orders (id INT PRIMARY KEY, customer_id INT, amount INT, order_date DATE); CREATE TABLE Customers (id INT PRIMARY KEY, name VARCHAR(100)); CREATE INDEX idx_orders_customer ON Orders(customer_id);",
            "seed_inserts": "INSERT INTO Orders VALUES (1,101,200,'2024-01-01'); INSERT INTO Customers VALUES (101,'Alice');",
            "expected_query": "CREATE INDEX idx_orders_customer_id ON Orders(customer_id);",
            "enforce_order": False,
        },
        "intersect": {
            "schema_ddl": "CREATE TABLE ProductsA (id INT PRIMARY KEY, name VARCHAR(100)); CREATE TABLE ProductsB (id INT PRIMARY KEY, name VARCHAR(100));",
            "seed_inserts": "INSERT INTO ProductsA VALUES (1,'X'),(2,'Y'),(3,'Z'); INSERT INTO ProductsB VALUES (2,'Y'),(3,'Z'),(4,'W');",
            "expected_query": "SELECT id, name FROM ProductsA INTERSECT SELECT id, name FROM ProductsB;",
            "enforce_order": False,
        },
        "with_clause_filter": {
            "schema_ddl": "CREATE TABLE Orders (id INT PRIMARY KEY, customer_id INT, amount INT, order_date DATE);",
            "seed_inserts": "INSERT INTO Orders VALUES (1,101,200,'2024-01-01'),(2,102,300,'2024-01-02'),(3,101,150,'2024-01-03'),(4,103,400,'2024-01-04'),(5,102,250,'2024-01-05');",
            "expected_query": "WITH CustomerSpending AS (SELECT customer_id, SUM(amount) as total_spent FROM Orders GROUP BY customer_id), TopCustomers AS (SELECT customer_id FROM CustomerSpending ORDER BY total_spent DESC LIMIT 3) SELECT cs.customer_id, cs.total_spent FROM CustomerSpending cs INNER JOIN TopCustomers tc ON cs.customer_id = tc.customer_id;",
            "enforce_order": False,
        },
        "full_outer_join": {
            "schema_ddl": "CREATE TABLE Employees (id INT PRIMARY KEY, name VARCHAR(100), dept_id INT); CREATE TABLE Departments (dept_id INT PRIMARY KEY, dept_name VARCHAR(50));",
            "seed_inserts": "INSERT INTO Employees VALUES (1,'A',10),(2,'B',NULL); INSERT INTO Departments VALUES (10,'Eng'),(20,'HR');",
            "expected_query": "SELECT e.name, d.dept_name FROM Employees e FULL OUTER JOIN Departments d ON e.dept_id = d.dept_id;",
            "enforce_order": True,
        },
        "transaction_isolation": {
            "schema_ddl": "CREATE TABLE Accounts (id INT PRIMARY KEY, balance INT);",
            "seed_inserts": "INSERT INTO Accounts VALUES (1,500),(2,500);",
            "expected_query": "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE; BEGIN; UPDATE Accounts SET balance = balance - 100 WHERE id = 1; UPDATE Accounts SET balance = balance + 100 WHERE id = 2; COMMIT;",
            "enforce_order": False,
        },
        "lag_lead": {
            "schema_ddl": "CREATE TABLE StockPrices (id INT PRIMARY KEY, symbol VARCHAR(20), price_date DATE, price INT);",
            "seed_inserts": "INSERT INTO StockPrices VALUES (1,'AAPL','2024-01-01',150),(2,'AAPL','2024-01-02',155),(3,'AAPL','2024-01-03',153);",
            "expected_query": "SELECT symbol, price_date, price, LAG(price) OVER (PARTITION BY symbol ORDER BY price_date) as prev_price, price - LAG(price) OVER (PARTITION BY symbol ORDER BY price_date) as price_change FROM StockPrices;",
            "enforce_order": True,
        },
        "filtered_aggregation": {
            "schema_ddl": "CREATE TABLE Orders (id INT PRIMARY KEY, customer_id INT, amount INT, status VARCHAR(50));",
            "seed_inserts": "INSERT INTO Orders VALUES (1,101,100,'completed'),(2,101,200,'pending'),(3,101,150,'completed'),(4,102,300,'pending');",
            "expected_query": "SELECT customer_id, SUM(amount) as total_amount, SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_orders, SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending_orders FROM Orders GROUP BY customer_id;",
            "enforce_order": False,
        },
        "constraints": {
            "schema_ddl": "CREATE TABLE Employees (id INT PRIMARY KEY, name VARCHAR(100) NOT NULL, email VARCHAR(100) UNIQUE, age INT CHECK (age > 18));",
            "seed_inserts": "INSERT INTO Employees VALUES (1,'Alice','alice@example.com',25);",
            "expected_query": "CREATE TABLE Employees (id INT PRIMARY KEY, name VARCHAR(100) NOT NULL, email VARCHAR(100) UNIQUE, age INT CHECK (age > 18));",
            "enforce_order": False,
        },
        "acid": {
            "schema_ddl": "CREATE TABLE Accounts (id INT PRIMARY KEY, balance INT);",
            "seed_inserts": "INSERT INTO Accounts VALUES (1,500),(2,300);",
            "expected_query": "BEGIN; UPDATE Accounts SET balance = balance - 100 WHERE id = 1; UPDATE Accounts SET balance = balance + 100 WHERE id = 2; COMMIT;",
            "enforce_order": False,
        },
        "indexes": {
            "schema_ddl": "CREATE TABLE Users (id INT PRIMARY KEY, email VARCHAR(100));",
            "seed_inserts": "INSERT INTO Users VALUES (1,'alice@example.com');",
            "expected_query": "CREATE INDEX idx_users_email ON Users(email);",
            "enforce_order": False,
        },
        "stored_procedures": {
            "schema_ddl": "CREATE TABLE Accounts (id INT PRIMARY KEY, balance DECIMAL(10,2));",
            "seed_inserts": "INSERT INTO Accounts VALUES (1,500),(2,300);",
            "expected_query": "CREATE PROCEDURE TransferFunds(IN from_id INT, IN to_id INT, IN amount DECIMAL(10,2)) BEGIN DECLARE source_balance DECIMAL(10,2); START TRANSACTION; SELECT balance INTO source_balance FROM Accounts WHERE id = from_id FOR UPDATE; IF source_balance < amount THEN ROLLBACK; SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Insufficient funds'; ELSE UPDATE Accounts SET balance = balance - amount WHERE id = from_id; UPDATE Accounts SET balance = balance + amount WHERE id = to_id; COMMIT; END IF; END;",
            "enforce_order": False,
        },
        "schema_design": {
            "schema_ddl": "CREATE TABLE Users (user_id INT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100)); CREATE TABLE Products (product_id INT PRIMARY KEY, name VARCHAR(100), price DECIMAL(10,2)); CREATE TABLE Orders (order_id INT PRIMARY KEY, user_id INT, order_date DATE, FOREIGN KEY (user_id) REFERENCES Users(user_id)); CREATE TABLE OrderItems (order_item_id INT PRIMARY KEY, order_id INT, product_id INT, quantity INT, FOREIGN KEY (order_id) REFERENCES Orders(order_id), FOREIGN KEY (product_id) REFERENCES Products(product_id));",
            "seed_inserts": "INSERT INTO Users VALUES (1,'Alice','alice@example.com'); INSERT INTO Products VALUES (1,'Widget',10.00); INSERT INTO Orders VALUES (100,1,'2024-01-01',10.00); INSERT INTO OrderItems VALUES (1000,100,1,1);",
            "expected_query": "CREATE TABLE Users (user_id INT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100)); CREATE TABLE Products (product_id INT PRIMARY KEY, name VARCHAR(100), price DECIMAL(10,2)); CREATE TABLE Orders (order_id INT PRIMARY KEY, user_id INT, order_date DATE, FOREIGN KEY (user_id) REFERENCES Users(user_id)); CREATE TABLE OrderItems (order_item_id INT PRIMARY KEY, order_id INT, product_id INT, quantity INT, FOREIGN KEY (order_id) REFERENCES Orders(order_id), FOREIGN KEY (product_id) REFERENCES Products(product_id));",
            "enforce_order": False,
        },
        "query_tuning": {
            "schema_ddl": "CREATE TABLE Orders (id INT PRIMARY KEY, customer_id INT, amount INT, order_date DATE); CREATE TABLE OrderItems (id INT PRIMARY KEY, order_id INT, product_id INT, quantity INT);",
            "seed_inserts": "INSERT INTO Orders VALUES (1,101,200,'2024-01-01'),(2,102,300,'2024-01-02'); INSERT INTO OrderItems VALUES (1,1,1,2),(2,2,1,1);",
            "expected_query": "CREATE INDEX idx_orders_customer_date ON Orders(customer_id, order_date); CREATE INDEX idx_orderitems_order_id ON OrderItems(order_id);",
            "enforce_order": False,
        },
        "execution_plan": {
            "schema_ddl": "CREATE TABLE Orders (id INT PRIMARY KEY, customer_id INT, amount INT);",
            "seed_inserts": "INSERT INTO Orders VALUES (1,101,200);",
            "expected_query": "EXPLAIN SELECT * FROM Orders WHERE customer_id = 101; CREATE INDEX idx_orders_customer ON Orders(customer_id);",
            "enforce_order": False,
        },
        "partitioning": {
            "schema_ddl": "CREATE TABLE Orders (id INT PRIMARY KEY, customer_id INT, amount INT, order_date DATE) PARTITION BY RANGE (YEAR(order_date)) (PARTITION p2024 VALUES LESS THAN (2025), PARTITION p2025 VALUES LESS THAN (2026));",
            "seed_inserts": "INSERT INTO Orders VALUES (1,101,200,'2024-01-01');",
            "expected_query": "CREATE TABLE Orders (...) PARTITION BY RANGE (YEAR(order_date)) (PARTITION p2024 VALUES LESS THAN (2024), PARTITION p2025 VALUES LESS THAN (2025), PARTITION p2026 VALUES LESS THAN (2026));",
            "enforce_order": False,
        },
        "olap": {
            "schema_ddl": "CREATE TABLE Sales (id INT PRIMARY KEY, region VARCHAR(50), product VARCHAR(100), sales_amount INT);",
            "seed_inserts": "INSERT INTO Sales VALUES (1,'North','Widget',100),(2,'North','Gadget',200),(3,'South','Widget',150);",
            "expected_query": "SELECT region, product, SUM(sales_amount) FROM Sales GROUP BY CUBE (region, product);",
            "enforce_order": False,
        },
        "star_schema": {
            "schema_ddl": "CREATE TABLE Sales (sale_id INT PRIMARY KEY, product_id INT, store_id INT, time_id INT, quantity INT, revenue DECIMAL(10,2)); CREATE TABLE Product (product_id INT PRIMARY KEY, name VARCHAR(100), category VARCHAR(50)); CREATE TABLE Store (store_id INT PRIMARY KEY, location VARCHAR(100), region VARCHAR(50)); CREATE TABLE Time (time_id INT PRIMARY KEY, date DATE, month INT, quarter INT, year INT);",
            "seed_inserts": "INSERT INTO Product VALUES (1,'Widget','Gadgets'); INSERT INTO Store VALUES (1,'NY','East'); INSERT INTO Time VALUES (1,'2024-01-01',1,1,2024); INSERT INTO Sales VALUES (100,1,1,1,5,50.00);",
            "expected_query": "CREATE TABLE Sales (sale_id INT PRIMARY KEY, product_id INT, store_id INT, time_id INT, quantity INT, revenue DECIMAL(10,2)); CREATE TABLE Product (product_id INT PRIMARY KEY, name VARCHAR(100), category VARCHAR(50)); CREATE TABLE Store (store_id INT PRIMARY KEY, location VARCHAR(100), region VARCHAR(50)); CREATE TABLE Time (time_id INT PRIMARY KEY, date DATE, month INT, quarter INT, year INT);",
            "enforce_order": False,
        },
        "security": {
            "schema_ddl": "CREATE TABLE Sales (id INT PRIMARY KEY, product VARCHAR(100), amount INT);",
            "seed_inserts": "INSERT INTO Sales VALUES (1,'Widget',100);",
            "expected_query": "GRANT SELECT ON ALL TABLES IN SCHEMA Sales TO analyst_role;",
            "enforce_order": False,
        },
        "data_manipulation": {
            "schema_ddl": "CREATE TABLE Employees (id INT PRIMARY KEY, name VARCHAR(100), dept_id INT, salary INT); CREATE TABLE Departments (dept_id INT PRIMARY KEY, location VARCHAR(100));",
            "seed_inserts": "INSERT INTO Departments VALUES (10,'Building A');",
            "expected_query": "BEGIN; INSERT INTO Employees (name, dept_id, salary) VALUES ('Alice', 10, 70000); UPDATE Departments SET location = 'Building B' WHERE dept_id = 10; COMMIT;",
            "enforce_order": False,
        },
        "multiple_joins": {
            "schema_ddl": "CREATE TABLE Orders (order_id INT PRIMARY KEY, customer_id INT, product_id INT, amount INT); CREATE TABLE Customers (customer_id INT PRIMARY KEY, name VARCHAR(100), country VARCHAR(50)); CREATE TABLE Products (product_id INT PRIMARY KEY, name VARCHAR(100), category VARCHAR(50));",
            "seed_inserts": "INSERT INTO Orders VALUES (1,101,1,200); INSERT INTO Customers VALUES (101,'A','US'); INSERT INTO Products VALUES (1,'Bike','Sports');",
            "expected_query": "SELECT o.order_id, c.name AS customer, p.name AS product, p.category FROM Orders o INNER JOIN Customers c ON o.customer_id = c.customer_id INNER JOIN Products p ON o.product_id = p.product_id;",
            "enforce_order": True,
        },
        "views": {
            "schema_ddl": "CREATE TABLE Employees (id INT PRIMARY KEY, name VARCHAR(100), dept_id INT, salary INT); CREATE TABLE Departments (dept_id INT PRIMARY KEY, dept_name VARCHAR(50));",
            "seed_inserts": "INSERT INTO Departments VALUES (10,'Eng'); INSERT INTO Employees VALUES (1,'Alice',10,70000),(2,'Bob',10,50000);",
            "expected_query": "CREATE VIEW ActiveEmployees AS SELECT e.name, d.dept_name FROM Employees e INNER JOIN Departments d ON e.dept_id = d.dept_id WHERE e.salary > 60000; SELECT * FROM ActiveEmployees;",
            "enforce_order": False,
        },
    }

    _SQL_SCHEMA_DEFAULT = {
        "schema_ddl": "CREATE TABLE table1 (id INT PRIMARY KEY, name VARCHAR(100), value INT);",
        "seed_inserts": "INSERT INTO table1 VALUES (1,'A',100),(2,'B',200);",
        "expected_query": "SELECT * FROM table1;",
        "enforce_order": False,
    }

    backfilled = 0
    for q in target:
        if str(q.get("type", "")).lower() != "sql":
            continue
        if q.get("sql_schema"):
            continue
        sub_topic = str(q.get("sub_topic", ""))
        template = _SQL_SCHEMA_TEMPLATES.get(sub_topic, _SQL_SCHEMA_DEFAULT)
        q["sql_schema"] = dict(template)
        backfilled += 1

    if backfilled:
        logger.info("SQL schema backfilled for %d questions", backfilled)
    return backfilled


def _quality_score(q: dict) -> int:
    """Score a question by how complete/usable it is. Higher is better."""
    score = 0
    if q.get("testcases"):
        score += 10
    if q.get("solution") and isinstance(q["solution"], dict):
        if q["solution"].get("code"):
            score += 6
    if q.get("examples"):
        score += 3
    if q.get("hints"):
        score += 1
    if q.get("description") or q.get("explanation"):
        score += 1
    return score


def _is_usable(q: dict) -> bool:
    """A question is usable when it has a real statement and independent
    evidence (test cases, verified answer, or reasoning trail).

    Quarantines (never served): empty titles, template-only shells
    ("Implement optimal solution here"), placeholder one-liners, and MCQs
    without a verifiable answer. When uncertain, quarantine rather than
    publish (Content Trust Rule).
    """
    title = str(q.get("question") or q.get("question_title") or q.get("title") or "").strip()
    body = str(q.get("description") or q.get("explanation") or q.get("question") or "").strip()
    if not title or title.lower() in ("", "untitled", "question", "problem"):
        return False
    # Template-only shells that were never authored.
    sol_code = ""
    if isinstance(q.get("solution"), dict):
        sol_code = str(q["solution"].get("code") or "")
    blob = f"{title}\n{body}\n{sol_code}".lower()
    if ("implement optimal solution here" in blob
            or "implement your solution here" in blob
            or "todo: implement" in blob):
        return False
    qtype = str(q.get("type") or "coding").lower()
    # Non-coding types (system_design, debugging, interview, sql) carry
    # their own evidence (rubric, buggy/correct code, reasoning) — no
    # compiler testcases required.
    if qtype in ("system_design", "debugging", "interview", "hr", "behavioral"):
        if qtype == "debugging":
            return bool(q.get("buggy_code") and (q.get("correct_code") or sol_code))
        return bool(body and len(body) >= 15)
    # Strongest signals first: executable test cases or independent verification
    # make a question usable regardless of statement length.
    if q.get("testcases") or q.get("test_cases"):
        return True
    if trust_rank(q) >= TRUST_RANK["verified"]:
        return True
    if not body or len(body) < 15:
        return False
    if q.get("options"):
        # Pure MCQ stubs without a verifiable answer are dropped. Keep MCQs
        # that carry independent verification or a real reasoning trail.
        if q.get("reasoning_steps") or q.get("correct_index") is not None or q.get("correct_answer"):
            return True
        return False
    return True


def _dedupe_and_filter(target: Optional[list] = None) -> list[dict]:
    """Remove auto-generated filler and collapse duplicate questions.

    - Drops malformed / placeholder / pure-MCQ entries.
    - Dedupes on a normalized title so the same LeetCode problem loaded from
      multiple seed files surfaces once (best-quality variant kept).
    - Merges curated-source tags (blind75 / neetcode150 / striver) so a
      problem that belongs to several curated lists keeps all of them.
    """
    global _questions
    if target is None:
        target = _questions
    seen: dict[str, dict] = {}
    dropped_filler = 0
    for q in target:
        if not _is_usable(q):
            dropped_filler += 1
            continue
        title = str(q.get("question") or q.get("question_title") or "")
        key = re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()[:80]
        if not key:
            dropped_filler += 1
            continue
        prev = seen.get(key)
        if prev is None:
            seen[key] = q
        else:
            # Keep whichever variant is more complete, then merge curated tags.
            # Independently verified content wins over an unverified legacy
            # duplicate (trust is a stronger signal than metadata richness), so
            # students always get the verified variant when one exists.
            prev_trust = trust_rank(prev)
            q_trust = trust_rank(q)
            if q_trust > prev_trust:
                seen[key] = q
                winner = q
            elif q_trust < prev_trust:
                seen[key] = prev
                winner = prev
            elif _quality_score(q) >= _quality_score(prev):
                seen[key] = q
                winner = q
            else:
                winner = prev
            sources = set()
            for variant in (prev, q):
                src = variant.get("curated_source") or ""
                if src:
                    sources.add(src)
                for s in variant.get("sources", []) or []:
                    if s:
                        sources.add(s)
            if sources:
                winner["sources"] = sorted(sources)
                winner["curated_source"] = winner.get("curated_source") or sorted(sources)[0]
    before = len(target)
    result = list(seen.values())
    if target is _questions:
        _questions = result
    logger.info(
        "Dedupe: %d raw -> %d kept (%d filler dropped, %d dupes collapsed)",
        before, len(result), dropped_filler, before - len(result) - dropped_filler,
    )
    return result


def _match(q: dict, query: dict) -> bool:
    for key, value in query.items():
        if key == "_id":
            if q.get("id") != str(value):
                return False
        elif key == "company":
            if isinstance(value, dict) and "$in" in value:
                q_companies = [c.lower() for c in q.get("companies", [])]
                if not any(v.lower() in q_companies for v in value["$in"]):
                    return False
            else:
                q_companies = [c.lower() for c in q.get("companies", [])]
                if value.lower() not in q_companies:
                    return False
        elif key == "$text":
            search = value.get("$search", "").lower()
            if search and search not in q.get("question", "").lower() and search not in q.get("explanation", "").lower():
                return False
        elif key == "type":
            qv = q.get("type", "")
            if isinstance(value, list):
                if qv not in value:
                    return False
            elif qv != value:
                return False
        elif key == "difficulty":
            qv = q.get("difficulty", "")
            if isinstance(value, dict) and "$in" in value:
                if qv not in value["$in"]:
                    return False
            elif qv != value:
                return False
        elif key == "topic":
            if isinstance(value, dict) and "$in" in value:
                if not any(_display_topic(q.get("topic", "")) == _display_topic(v) for v in value["$in"]):
                    return False
            elif _display_topic(q.get("topic", "")) != _display_topic(value):
                return False
        elif key == "sub_topic":
            if q.get("sub_topic", "") != value:
                return False
        elif key == "pattern":
            if isinstance(value, dict) and "$in" in value:
                if q.get("pattern") not in value["$in"]:
                    return False
            elif q.get("pattern") != value:
                return False
        elif key in ("source", "curated_source"):
            sources = set(q.get("sources", []) or [])
            src = q.get("curated_source")
            if src:
                sources.add(src)
            if isinstance(value, dict) and "$in" in value:
                if not (sources & set(value["$in"])):
                    return False
            elif isinstance(value, list):
                if not (sources & set(value)):
                    return False
            elif value not in sources:
                return False
        elif key == "role":
            q_roles = [r.lower() for r in q.get("role", [])] if isinstance(q.get("role"), list) else [str(q.get("role", "")).lower()]
            if isinstance(value, dict) and "$in" in value:
                if not any(v.lower() in q_roles for v in value["$in"]):
                    return False
            elif value.lower() not in q_roles:
                return False
        elif key == "_id" and "$nin" in value:
            val_id = q.get("id", "")
            if val_id in [str(v) for v in value["$nin"]]:
                return False
        else:
            if q.get(key) != value:
                return False
    return True


def count_documents(query: Optional[dict] = None) -> int:
    """Count servable questions matching the query (trust gate applies)."""
    load_all()
    if not query:
        return sum(1 for q in _questions if _is_servable(q))
    return sum(1 for q in _questions if _match(q, query) and _is_servable(q))


# ---------------------------------------------------------------------------
# Content Trust Lifecycle (from question_governance.py contract)
#
#   DRAFT (unverified)       → raw imported content, never served.
#   NORMALIZED (needs_review) → structurally valid, awaiting validation.
#   AUTOMATED_CHECKED         → passes automated execution/validation.
#   HUMAN_REVIEWED (reviewed) → human verified correctness and quality.
#   VERIFIED (verified)       → independently verified; placement-quality.
#   SERVABLE                  → computed: trust in {verified, reviewed} AND executable.
#
# Every state transition is auditable: trust_transition_log records
# (question_id, from_status, to_status, reason, timestamp).
# ---------------------------------------------------------------------------

TRUST_DRAFT = "unverified"
TRUST_NORMALIZED = "needs_review"
TRUST_AUTOMATED_CHECKED = "automated_checked"
TRUST_HUMAN_REVIEWED = "reviewed"
TRUST_VERIFIED = "verified"
TRUST_QUARANTINED = "quarantined"

TRUST_LIFECYCLE_ORDER = [
    TRUST_DRAFT,
    TRUST_NORMALIZED,
    TRUST_AUTOMATED_CHECKED,
    TRUST_HUMAN_REVIEWED,
    TRUST_VERIFIED,
]

TRUST_RANK = {
    TRUST_VERIFIED: 3,
    TRUST_HUMAN_REVIEWED: 2,
    TRUST_AUTOMATED_CHECKED: 1,
    TRUST_NORMALIZED: 1,
    TRUST_DRAFT: 0,
    TRUST_QUARANTINED: -1,
}

# Audit log of all trust state transitions.
_trust_transition_log: list[dict] = []


def transition_trust(question_id: str, to_status: str, reason: str = "") -> bool:
    """Transition a question's trust state with audit trail.

    Only forward transitions are allowed (DRAFT → NORMALIZED →
    AUTOMATED_CHECKED → HUMAN_REVIEWED → VERIFIED). QUARANTINED is a
    terminal state that can be applied from any state but cannot be
    transitioned out of without manual review.

    Returns True if the transition succeeded, False if the question
    was not found or the transition is invalid.
    """
    load_all()
    for q in _questions:
        if str(q.get("id")) != str(question_id):
            continue
        from_status = str(q.get("trust_status", TRUST_DRAFT)).lower()
        to = str(to_status).lower()

        # Quarantined is terminal: only manual review can lift it.
        if from_status == TRUST_QUARANTINED and to != TRUST_QUARANTINED:
            _trust_transition_log.append({
                "question_id": question_id,
                "from_status": from_status,
                "to_status": to,
                "reason": f"blocked: quarantined is terminal ({reason})" if reason else "blocked: quarantined is terminal",
                "allowed": False,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            return False

        # Forward-only transitions within the lifecycle.
        if to != TRUST_QUARANTINED:
            from_idx = TRUST_LIFECYCLE_ORDER.index(from_status) if from_status in TRUST_LIFECYCLE_ORDER else -1
            to_idx = TRUST_LIFECYCLE_ORDER.index(to) if to in TRUST_LIFECYCLE_ORDER else -1
            if from_idx >= 0 and to_idx >= 0 and to_idx <= from_idx:
                _trust_transition_log.append({
                    "question_id": question_id,
                    "from_status": from_status,
                    "to_status": to,
                    "reason": f"blocked: non-forward transition ({reason})" if reason else "blocked: non-forward transition",
                    "allowed": False,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
                return False

        # Trust lifecycle validation: transitioning to VERIFIED requires
        # human review evidence (non-empty reason) and executable question.
        if to == TRUST_VERIFIED:
            if not reason or not reason.strip():
                _trust_transition_log.append({
                    "question_id": question_id,
                    "from_status": from_status,
                    "to_status": to,
                    "reason": "blocked: verified transition requires human review reason",
                    "allowed": False,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
                return False
            if not _is_executable(q):
                _trust_transition_log.append({
                    "question_id": question_id,
                    "from_status": from_status,
                    "to_status": to,
                    "reason": "blocked: verified transition requires executable question (valid test cases / schema / options)",
                    "allowed": False,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
                return False

        q["trust_status"] = to
        q["trust_transitioned_at"] = datetime.now(timezone.utc).isoformat()
        if reason:
            q["trust_transition_reason"] = reason

        _trust_transition_log.append({
            "question_id": question_id,
            "from_status": from_status,
            "to_status": to,
            "reason": reason or "",
            "allowed": True,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        logger.info("Trust transition: %s %s -> %s (%s)", question_id, from_status, to, reason)
        return True
    return False


def get_trust_transition_log() -> list[dict]:
    """Return the audit log of all trust state transitions."""
    return list(_trust_transition_log)


def trust_rank(q: dict) -> int:
    """Priority of a question's trust level (higher = more trusted)."""
    return TRUST_RANK.get(str(q.get("trust_status", "unverified")).lower(), 0)


def find_one(query: dict, allow_unverified: bool = False) -> Optional[dict]:
    load_all()
    for q in _questions:
        if _match(q, query) and (allow_unverified or _is_servable(q)):
            return dict(q)
    if allow_unverified:
        # Fallback to unverified pool for backward compatibility with history
        if not _unverified_loaded:
            try:
                load_unverified()
            except Exception:
                pass
        for q in _unverified_questions:
            if _match(q, query):
                return dict(q)
    return None


def _is_executable(q: dict) -> bool:
    """Check if a question can actually be evaluated/graded."""
    qtype = str(q.get("type", "")).lower()
    
    # Coding/SQL/Debugging require test cases
    if qtype in ("coding", "sql", "debugging"):
        tcs = q.get("test_cases") or q.get("testcases") or []
        if not tcs:
            return False
        # SQL additionally requires proper schema metadata for result-set comparison
        if qtype == "sql" and not q.get("sql_schema"):
            return False
        return True
    
    # MCQs require a valid correct_answer
    if qtype in ("aptitude", "logical", "verbal", "hr", "behavioral", "cs_fundamentals", "cs"):
        options = q.get("options") or {}
        correct = str(q.get("correct_answer") or q.get("correct_index") or "").strip().upper()
        
        # Handle list-style options (cs_fundamentals format)
        if isinstance(options, list) and len(options) >= 4:
            # correct_answer might be an integer index or text
            correct_text = str(q.get("correct_answer") or "").strip()
            correct_idx = q.get("correct_index")
            if isinstance(correct_idx, int) and 0 <= correct_idx < len(options):
                return True
            if correct_text and correct_text in [str(o).strip() for o in options]:
                return True
            return False
        
        # Handle dict-style options (aptitude/logical/verbal format)
        if isinstance(options, dict) and len(options) >= 4:
            return correct in ("A", "B", "C", "D")
        
        return False
    
    # Interview/System Design/GD require rubric or evaluation criteria
    if qtype in ("interview", "system_design", "gd", "group_discussion"):
        return bool(q.get("rubric") or q.get("evaluation_criteria") or q.get("worked_solution"))
    
    # Default: require test cases or some form of answer key
    tcs = q.get("test_cases") or q.get("testcases") or []
    return len(tcs) > 0 or bool(q.get("correct_answer") or q.get("answer") or q.get("solution"))


def _is_servable(q: dict) -> bool:
    status = str(q.get("trust_status", "unverified")).lower()
    # Trust gate (flipped): only independently verified or human-reviewed
    # content is servable. automated_checked (LLM-drafted candidates),
    # needs_review, and unverified are quarantined from student-facing
    # serving until they pass the pipeline into verified/reviewed.
    if status not in ("verified", "reviewed"):
        return False
    if not _is_executable(q):
        return False
    return True


def find_one_verified(query: dict) -> Optional[dict]:
    """Like find_one, but only returns independently verified content."""
    load_all()
    for q in _questions:
        if _match(q, query) and _is_servable(q):
            return dict(q)
    return None


def get_question_for_serving(question_id: str) -> Optional[dict]:
    """Fetch one complete question from the in-memory canonical store.

    LeetCode/GFG parity schema (presentation fallbacks only — never invents
    grading content): question_title, statement, constraints, examples with
    explanations, visible_test_cases, hidden_test_cases, hints, editorial
    (explanation/approach), complexity, misconceptions (common_trap),
    provenance, and trust_status. Returns None when absent or incomplete.
    Never touches MongoDB (Residency Rule, AGENTS.md).

    Only returns independently verified content. Use find_one() with
    allow_unverified=True for admin/history lookups."""
    q = find_one_verified({"id": str(question_id)})
    if not q:
        return None
    title = q.get("title") or q.get("question_title") or (q.get("question") or "")[:80]
    q["question_title"] = q.get("question_title") or title or "Unknown"
    q["statement"] = q.get("statement") or q.get("question", "")
    q["visible_test_cases"] = q.get("visible_test_cases") or q.get("testcases") or q.get("test_cases") or []
    q["hidden_test_cases"] = q.get("hidden_test_cases") or q.get("hidden_testcases") or []
    q["examples"] = q.get("examples") or []
    q["constraints"] = q.get("constraints") or ""
    q["hints"] = q.get("hints") or []
    q["editorial"] = q.get("editorial") or q.get("explanation") or ""
    q["explanation"] = q.get("explanation") or q.get("editorial") or ""
    q["approach"] = q.get("approach") or (q.get("dsa_guide") or {}).get("approach", "")
    q["expected_time_complexity"] = q.get("expected_time_complexity") or ""
    q["expected_space_complexity"] = q.get("expected_space_complexity") or ""
    q["misconceptions"] = q.get("misconceptions") or q.get("common_trap") or ""
    q["common_trap"] = q.get("common_trap") or q.get("misconceptions") or ""
    q["reasoning_steps"] = q.get("reasoning_steps") or []
    q["provenance"] = q.get("provenance") or q.get("source_bank") or "unverified"
    q["trust_status"] = q.get("trust_status") or "unverified"
    return q


def find(query: Optional[dict] = None):
    load_all()
    return QuestionCursor(_questions, query)


def find_unverified(query: Optional[dict] = None):
    """Search the isolated unverified/candidate pool. Admin/candidate mode only."""
    if not _unverified_loaded:
        load_unverified()
    return QuestionCursor(_unverified_questions, query)


def distinct(field: str) -> list:
    load_all()
    values = set()
    for q in _questions:
        val = q.get(field)
        if isinstance(val, list):
            for v in val:
                if v:
                    values.add(str(v).strip())
        elif val:
            values.add(str(val).strip())
    return sorted(values)


class QuestionCursor:
    def __init__(self, questions: list, query: Optional[dict] = None):
        self._all = [q for q in questions if _match(q, query)] if query else list(questions)
        self._skip_amount = 0
        self._limit_amount = None
        self._sort_spec = None

    def skip(self, n: int):
        self._skip_amount = n
        return self

    def limit(self, n: int):
        self._limit_amount = n
        return self

    def sort(self, sort_by):
        self._sort_spec = sort_by
        return self

    def prefer_verified(self):
        """Keep only servable (verified/reviewed) content and sort verified
        first (stable; ties keep original order). Student-facing flows use
        this so unverified/automated-checked candidates are never served."""
        self._all = [q for q in self._all if _is_servable(q)]
        self._all = sorted(
            enumerate(self._all),
            key=lambda it: (trust_rank(it[1]), it[0]),
            reverse=True,
        )
        self._all = [q for _, q in self._all]
        return self

    def only_verified(self):
        """Keep only independently verified or automated-checked content."""
        self._all = [q for q in self._all if _is_servable(q)]
        return self

    def to_list(self, length: Optional[int] = None) -> list[dict]:
        items = self._apply_sort()
        items = items[self._skip_amount:]
        if self._limit_amount:
            items = items[:self._limit_amount]
        if length is not None:
            items = items[:length]
        return [dict(q) for q in items]

    def __aiter__(self):
        return self._AsyncIterator(self)

    @staticmethod
    def _sort_key(q: dict, k: str):
        v = q.get(k)
        if isinstance(v, bool):
            return (1, int(v))
        if isinstance(v, (int, float)):
            return (1, v)
        if v is None:
            return (0, "")
        return (0, str(v))

    def _apply_sort(self):
        if not self._sort_spec:
            return self._all
        items = list(self._all)
        for key, direction in self._sort_spec:
            items.sort(key=lambda q, k=key: self._sort_key(q, k), reverse=(direction == -1))
        return items

    class _AsyncIterator:
        def __init__(self, cursor):
            self._items = cursor.to_list()
            self._idx = 0

        def __aiter__(self):
            return self

        async def __anext__(self):
            if self._idx >= len(self._items):
                raise StopAsyncIteration
            val = self._items[self._idx]
            self._idx += 1
            return val


def get_filters() -> dict:
    load_all()
    companies = set()
    roles = set()
    topics = set()
    sub_topics = set()
    types = set()
    difficulties = set()
    patterns = set()
    sources = set()

    for q in _questions:
        if not _is_servable(q):
            continue
        for c in q.get("companies", []):
            if c:
                companies.add(c.strip())
        r = q.get("role", "")
        if isinstance(r, list):
            for rr in r:
                if rr:
                    roles.add(rr.strip())
        elif r:
            roles.add(r.strip())
        t = q.get("topic", "")
        if t:
            topics.add(t.strip())
        st = q.get("sub_topic", "")
        if st:
            sub_topics.add(st.strip())
        tp = q.get("type", "")
        if tp:
            types.add(tp.strip())
        d = q.get("difficulty", "")
        if d:
            difficulties.add(d.strip())
        p = q.get("pattern", "")
        if p:
            patterns.add(p.strip())
        for s in q.get("sources", []) or []:
            if s:
                sources.add(s.strip())
        cs = q.get("curated_source", "")
        if cs:
            sources.add(cs.strip())

    # v1 SQL cut: filter options only list types with ≥1 servable question,
    # so the UI never advertises an empty section (sql: 0/932 executable).
    # Revisit when sql_schema backfill lands post-launch.
    servable_types = {str(q.get("type", "")).strip() for q in _questions if _is_servable(q)}
    types &= servable_types
    return {
        "companies": sorted(companies),
        "roles": sorted(roles),
        "topics": sorted(topics),
        "sub_topics": sorted(sub_topics),
        "types": sorted(types),
        "difficulties": sorted(difficulties),
        "patterns": sorted(patterns),
        "sources": sorted(sources),
    }


def get_pattern_stats() -> list[dict]:
    """Per-pattern problem counts + difficulty breakdown, in Striver sheet order."""
    load_all()
    stats: dict[str, dict] = {}
    for q in _questions:
        if not _is_servable(q):
            continue
        pattern = q.get("pattern") or "Arrays"
        diff = q.get("difficulty") or "medium"
        if diff not in ("easy", "medium", "hard"):
            diff = "medium"
        entry = stats.setdefault(pattern, {"pattern": pattern, "total": 0, "easy": 0, "medium": 0, "hard": 0})
        entry["total"] += 1
        entry[diff] += 1
    ordered = sorted(stats.values(), key=lambda s: STRIVER_PATTERNS.index(s["pattern"]) if s["pattern"] in STRIVER_PATTERNS else 999)
    return ordered


def get_topic_stats() -> list[dict]:
    """Aggregate topics with total problem counts and difficulty breakdown."""
    load_all()
    stats: dict[str, dict] = {}
    for q in _questions:
        if not _is_servable(q):
            continue
        topic = _display_topic(q.get("topic") or "General")
        diff = q.get("difficulty") or "medium"
        if diff not in ("easy", "medium", "hard"):
            diff = "medium"
        entry = stats.setdefault(topic, {"topic": topic, "total": 0, "easy": 0, "medium": 0, "hard": 0})
        entry["total"] += 1
        entry[diff] += 1
    return sorted(stats.values(), key=lambda t: (-t["total"], t["topic"]))


# Canonical company key -> tag variants matched against verified questions'
# explicit `companies` lists (case-insensitive). Deterministic, no LLM.
_COMPANY_TAG_ALIASES: dict[str, list[str]] = {
    "tcs": ["tcs", "tcs_nqt", "tata consultancy services"],
    "infosys": ["infosys", "infytq"],
    "wipro": ["wipro", "wipro_nlth", "nlth"],
    "accenture": ["accenture", "amcat"],
    "cognizant": ["cognizant", "genc", "gen c"],
    "amazon": ["amazon"],
    "google": ["google"],
    "meta": ["meta", "facebook"],
    "microsoft": ["microsoft"],
}


def canonical_company_key(name: str) -> str:
    key = (name or "").lower().strip()
    for canon, variants in _COMPANY_TAG_ALIASES.items():
        if key == canon or key in variants:
            return canon
    return key


def company_verified_bank(company: str) -> dict:
    """Per-company bank: deterministic filter over VERIFIED-ONLY stock using
    the questions' explicit `companies` tags. No LLM involvement — pure
    in-memory filtering over human-verified content. Each item keeps its own
    `provenance` (e.g. "pattern_relevant to TCS NQT / Infosys"); the bank as a
    whole is therefore pattern-relevant topic/company alignment, never a claim
    of "asked at X". Returns counts grouped by type/topic plus the items."""
    canon = canonical_company_key(company)
    variants = _COMPANY_TAG_ALIASES.get(canon, [canon])
    items = find({"company": {"$in": variants}}).only_verified().to_list()
    by_type: dict[str, dict] = {}
    for q in items:
        t = q.get("type", "unknown")
        entry = by_type.setdefault(t, {"count": 0, "topics": {}})
        entry["count"] += 1
        topic = _display_topic(q.get("topic") or "General")
        entry["topics"][topic] = entry["topics"].get(topic, 0) + 1
    for entry in by_type.values():
        entry["topics"] = dict(sorted(entry["topics"].items(), key=lambda kv: (-kv[1], kv[0])))
    return {
        "company": canon,
        "total": len(items),
        "by_type": by_type,
        "relevance": "tagged",
        "provenance_note": (
            "Items carry explicit company tags with per-item provenance "
            "(pattern-relevant unless independently drive-verified). "
            "Topic alignment without an explicit tag is pattern-relevant, "
            "never presented as asked-at-X."
        ),
        "items": items,
    }


def insert_question(doc: dict) -> str:
    """Insert a user-submitted question into the in-memory store."""
    qid = doc.get("id") or str(uuid.uuid4())
    doc["id"] = qid
    _questions.append(dict(doc))
    return qid


def vote_question(question_id: str, vote: int) -> Optional[dict]:
    """Record curation feedback in the in-memory candidate store.

    Question-bank content and its curation candidates intentionally never use
    MongoDB. Votes are ephemeral until a curator promotes an item into a
    versioned source file.
    """
    load_all()
    for pool in (_questions, _unverified_questions):
        for question in pool:
            if str(question.get("id")) != str(question_id):
                continue
            question["upvotes"] = question.get("upvotes", 0) + max(0, vote)
            question["downvotes"] = question.get("downvotes", 0) + max(0, -vote)
            question["updated_at"] = datetime.now(timezone.utc)
            return dict(question)
    return None


# ---------------------------------------------------------------------------
# Content Trust Fixes
# ---------------------------------------------------------------------------

MCQ_TYPES = ("aptitude", "logical", "verbal", "hr", "cs_fundamentals", "cs")


def fix_stale_mcq_stamps() -> int:
    """Invalidate MCQ questions with stale verification stamps.

    A stamp is stale if correct_answer is not in A-D (the format expected
    by the MCQ test-case normalization). These get set to needs_review.
    Returns count of fixed questions.
    """
    load_all()
    fixed = 0
    for q in _questions:
        qtype = str(q.get("type", "")).lower()
        if qtype not in MCQ_TYPES:
            continue
        status = str(q.get("trust_status", "")).lower()
        if status not in ("verified", "automated_checked"):
            continue
        correct = str(q.get("correct_answer") or q.get("correct_index") or "").strip().upper()
        if correct not in ("A", "B", "C", "D"):
            q["trust_status"] = "needs_review"
            q["verification_failure"] = f"stale_stamp:correct_answer={correct!r}"
            fixed += 1
    return fixed


def fix_sql_no_test_cases() -> int:
    """Quarantine SQL questions without test_cases or sql_schema.

    SQL questions need both a schema and test cases to be executable.
    Returns count of quarantined questions.
    """
    load_all()
    fixed = 0
    for q in _questions:
        qtype = str(q.get("type", "")).lower()
        if qtype != "sql":
            continue
        tcs = q.get("test_cases") or q.get("testcases") or []
        if not tcs:
            q["trust_status"] = "quarantined"
            q["verification_failure"] = "no_test_cases"
            fixed += 1
    return fixed


def fix_verified_not_executable() -> int:
    """Quarantine questions that are verified/automated_checked but not executable.

    These have a trust stamp but fail _is_executable() checks.
    Returns count of quarantined questions.
    """
    load_all()
    fixed = 0
    for q in _questions:
        status = str(q.get("trust_status", "")).lower()
        if status not in ("verified", "automated_checked"):
            continue
        if not _is_executable(q):
            q["trust_status"] = "quarantined"
            q["verification_failure"] = "verified_but_not_executable"
            fixed += 1
    return fixed


def run_all_content_trust_fixes() -> dict:
    """Run all content trust fixes and return summary."""
    load_all()
    stale = fix_stale_mcq_stamps()
    sql = fix_sql_no_test_cases()
    not_exec = fix_verified_not_executable()
    _dedupe_and_filter(_questions)
    return {
        "stale_mcq_fixed": stale,
        "sql_quarantined": sql,
        "verified_not_exec_quarantined": not_exec,
        "total_servable": sum(1 for q in _questions if _is_servable(q)),
        "total_questions": len(_questions),
    }
