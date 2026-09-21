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
    
    # Compute executable field for each question
    for q in _questions:
        q["executable"] = _is_executable(q)
    
    _loaded = True
    logger.info("QuestionStore loaded %d questions total", len(_questions))


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


TRUST_RANK = {"verified": 3, "reviewed": 2, "automated_checked": 1, "needs_review": 1, "unverified": 0, "quarantined": -1}


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
