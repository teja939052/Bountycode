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
_expanded = False
_mongo_loaded = False

settings = get_settings()

# ---------------------------------------------------------------------------
# Consolidated JSON question bank (single-file fast load)
# ---------------------------------------------------------------------------
_BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_BANK_JSON = os.path.join(_BACKEND_ROOT, "app", "data", "questions_bank.json")

_SEED_FILES: list[str] = [
    "seed_questions_mega.py",
    "seed_questions_v2.py",
    "seed_questions_2000.py",
    "seed_questions.py",
    "seed_questions_extra.py",
    "seed_questions_faang.py",
    "seed_questions_500.py",
    "seed_questions_500_more.py",
    "seed_questions_300_more.py",
    "seed_questions_500_plus_2.py",
    "seed_questions_500_plus_3.py",
    "seed_questions_graph_dp.py",
    "massive_questions.py",
    "seed_questions_striver.py",
    "seed_questions_blind75.py",
    "seed_questions_neetcode150.py",
    "seed_questions_leetcode_extra.py",
]

# Number of unique-id variants appended per original question.
# Set to 0: variants were artificial `-v2/-v3/-v4` clones that padded the bank
# with identical questions. Users want quality, not clone count.
QUESTION_VARIANTS = 0

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
    """Best-effort Striver pattern detection from topic + title + description."""
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
    """Ensure every question has a string id."""
    if "_id" in q:
        q["id"] = str(q.pop("_id"))
    elif "id" not in q:
        q["id"] = f"q_{idx:06d}"
    else:
        q["id"] = str(q["id"])

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


def load_all():
    global _questions, _loaded
    if _loaded:
        return
    _questions = []

    # Fast path: use consolidated JSON bank if available and up-to-date
    if _json_bank_fresh() and _load_from_json_bank():
        _dedupe_and_filter()
        _apply_leetcode_meta()
        _expand_questions()
        _loaded = True
        logger.info("QuestionStore loaded %d questions total (via JSON bank)", len(_questions))
        return

    # Fallback: load from 17 individual Python seed files
    _load_from_seed_files()

    _dedupe_and_filter()
    _apply_leetcode_meta()
    _expand_questions()
    _loaded = True
    logger.info("QuestionStore loaded %d questions total (via seed files)", len(_questions))


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


def _expand_questions():
    """Scale up the question bank by appending `QUESTION_VARIANTS` unique-id
    variants of every loaded question. Variants preserve the original text,
    difficulty, topic, and company but carry a distinct `-v2`, `-v3`, ... id
    suffix, so users see (1 + QUESTION_VARIANTS)x the practice surface without
    rewriting the on-disk seed files. Idempotent: only runs once per process."""
    global _expanded, _questions
    if _expanded:
        return
    _expanded = True
    if QUESTION_VARIANTS <= 0:
        return
    originals = list(_questions)
    original = len(originals)
    for v in range(1, QUESTION_VARIANTS + 1):
        for q in originals:
            variant = dict(q)
            base_id = q.get("id") or ""
            suffix = "-v2" if v == 1 else f"-v{v+1}"
            variant["id"] = f"{base_id}{suffix}" if base_id else f"q_dup_{v}_{original}"
            _questions.append(_assign_id(variant, original))
    logger.info(
        "QuestionStore expanded from %d -> %d questions (%dx variants)",
        original, len(_questions), 1 + QUESTION_VARIANTS,
    )


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
    """A question is usable when it has a real statement and either test cases
    (compiler-runnable) or an explanation (readable). Pure MCQ stubs and
    auto-generated one-liners without any content are dropped."""
    title = str(q.get("question") or q.get("question_title") or "").strip()
    body = str(q.get("description") or q.get("explanation") or q.get("question") or "").strip()
    if not body or len(body) < 15:
        return False
    if not title or title.lower() in ("", "untitled", "question", "problem"):
        return False
    if q.get("testcases"):
        return True
    if q.get("options"):
        return False
    return True


def _dedupe_and_filter():
    """Remove auto-generated filler and collapse duplicate questions.

    - Drops malformed / placeholder / pure-MCQ entries.
    - Dedupes on a normalized title so the same LeetCode problem loaded from
      multiple seed files surfaces once (best-quality variant kept).
    - Merges curated-source tags (blind75 / neetcode150 / striver) so a
      problem that belongs to several curated lists keeps all of them.
    """
    global _questions
    seen: dict[str, dict] = {}
    dropped_filler = 0
    for q in _questions:
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
            if _quality_score(q) >= _quality_score(prev):
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
    before = len(_questions)
    _questions = list(seen.values())
    logger.info(
        "Dedupe: %d raw -> %d kept (%d filler dropped, %d dupes collapsed)",
        before, len(_questions), dropped_filler, before - len(_questions) - dropped_filler,
    )


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
    load_all()
    if not query:
        return len(_questions)
    return sum(1 for q in _questions if _match(q, query))


def find_one(query: dict) -> Optional[dict]:
    load_all()
    for q in _questions:
        if _match(q, query):
            return dict(q)
    return None


def find(query: Optional[dict] = None):
    load_all()
    return QuestionCursor(_questions, query)


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
        topic = _display_topic(q.get("topic") or "General")
        diff = q.get("difficulty") or "medium"
        if diff not in ("easy", "medium", "hard"):
            diff = "medium"
        entry = stats.setdefault(topic, {"topic": topic, "total": 0, "easy": 0, "medium": 0, "hard": 0})
        entry["total"] += 1
        entry[diff] += 1
    return sorted(stats.values(), key=lambda t: (-t["total"], t["topic"]))


async def load_from_mongo(collection=None):
    """Load user-submitted questions from MongoDB into memory."""
    global _questions, _mongo_loaded
    if _mongo_loaded:
        return
    
    try:
        if collection is None:
            from app.database import get_client
            db = get_client()[settings.DATABASE_NAME]
            collection = db["curated_questions"]
        
        existing_ids = {q["id"] for q in _questions}
        count = 0
        async for doc in collection.find({}):
            qid = str(doc.pop("_id", ""))
            if qid and qid not in existing_ids:
                doc["id"] = qid
                _questions.append(dict(doc))
                count += 1
        
        _mongo_loaded = True
        logger.info("Loaded %d questions from MongoDB (%d total)", count, len(_questions))
    except Exception as e:
        logger.warning("Failed to load from MongoDB: %s", e)


def insert_question(doc: dict) -> str:
    """Insert a user-submitted question into the in-memory store."""
    qid = doc.get("id") or str(uuid.uuid4())
    doc["id"] = qid
    _questions.append(dict(doc))
    return qid
