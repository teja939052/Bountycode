"""
Automated Data Salvage Engine — sanitize_qbank.py

Sifts through the raw question bank (6,379 questions), rejects
unrendered template placeholders, eliminates duplicates (exact +
semantic), and routes clean, validated questions into the curated
content directory.

Raw      →  app/content/questions/raw/questions_bank.json
Curated  →  app/content/questions/curated/curated.json
Rejected →  app/content/questions/rejected/rejected.json
Review   →  app/content/questions/review_duplicates/review_duplicates.json

Pipeline stages:
    RAW → SANITIZED (templates rejected) → SEMANTIC REVIEW
    (candidates that are semantically similar to an existing question
    are sent to a review bucket, NOT auto-deleted. A human decides
    whether they are true duplicates or pedagogically valuable
    variants.) → CURATED (dups removed, metadata enhanced) → READY FOR REVIEW

Each curated question gets:
    review_status: "pending" | "reviewed" | "placement_grade"
    quality_scores: dict with dimensional scores (see _compute_quality_scores)
    semantic_hash: for coarse dedup by concept
    learning_objective: derived from topic/pattern
    source_type: "official_sample" | "candidate_reported" | "pattern_relevant" | "bountycourse_original"

NOTE: quality_scores are *heuristic*. Human/agent review is required
to promote questions to "placement_grade". The backend paywall
filters on review_status=placement_grade for production serving.
"""
import os
import re
import json
import hashlib
from pathlib import Path
from collections import defaultdict

BACKEND_ROOT = Path(__file__).resolve().parents[2]
RAW_PATH = BACKEND_ROOT / "app" / "content" / "questions" / "raw" / "questions_bank.json"
CURATED_DIR = BACKEND_ROOT / "app" / "content" / "questions" / "curated"
REJECTED_DIR = BACKEND_ROOT / "app" / "content" / "questions" / "rejected"

CURATED_DIR.mkdir(parents=True, exist_ok=True)
REJECTED_DIR.mkdir(parents=True, exist_ok=True)
REVIEW_DUP_DIR = BACKEND_ROOT / "app" / "content" / "questions" / "review_duplicates"
REVIEW_DUP_DIR.mkdir(parents=True, exist_ok=True)

PLACEHOLDER_RE = re.compile(r"\{variant\}|\{k\}|\{n\}|\{x\}|\{y\}|\{target\}|\{condition\}|\{order\}|\{num\}")
WORD_RE = re.compile(r"\b\w{4,}\b")
LEARNING_OBJECTIVES = {
    "arrays": "Recognize array traversal and in-place modification patterns.",
    "binary-search": "Identify boundary detection and search-space reduction techniques.",
    "dynamic-programming": "Break problems into overlapping subproblems and memoize.",
    "linked-lists": "Master pointer manipulation and dummy-head techniques.",
    "trees": "Apply DFS/BFS traversal and recursive tree decomposition.",
    "graphs": "Model problems as graph traversal, shortest path, or flow.",
    "strings": "Use two-pointer and character-count hashing for string problems.",
    "sliding-window": "Maintain a window invariant for subarray/substring problems.",
    "two-pointers": "Use paired indices to reduce O(n²) to O(n).",
    "heap": "Use priority-queue ordering for greedy selection.",
    "greedy": "Make locally optimal choices and prove global optimality.",
    "backtracking": "Explore state space with DFS and constraint pruning.",
    "bit-manipulation": "Apply XOR, AND, shift tricks for constant-space logic.",
    "hash-table": "Map key-value lookups for O(1) access patterns.",
    "stack": "Use stack for monotonic, balanced-bracket, or min-tracking problems.",
    "union-find": "Model connected-component and Kruskal MST problems.",
    "topological": "Order nodes respecting dependency directions (DAG).",
    "dp": "Master state transition design and optimal substructure.",
}


def _normalize(s: str) -> str:
    return re.sub(r"\s+", "", (s or "").lower().strip())


def _semantic_hash(q: dict) -> str:
    """Coarse semantic fingerprint: topic + key concepts (4+ char words)."""
    topic = _normalize(q.get("topic", ""))
    pattern = _normalize(q.get("pattern", ""))
    text = q.get("description", "") or q.get("question", "") or ""
    words = sorted(set(WORD_RE.findall(text.lower())))
    fingerprint = "|".join([topic, pattern] + words[:15])
    return hashlib.md5(fingerprint.encode("utf-8", errors="ignore")).hexdigest()[:12]


def is_template_question(q: dict) -> str | None:
    """Return rejection reason if the question is an unrendered template."""
    title = q.get("title", "") or ""
    question = q.get("question", "") or ""
    description = q.get("description", "") or ""
    body = title + question + description
    return "unrendered_template_placeholder" if PLACEHOLDER_RE.search(body) else None


def has_quality_content(q: dict) -> str | None:
    """Return rejection reason if required fields are missing by content type."""
    q_type = q.get("type", "coding")

    has_company = bool(
        q.get("company") or q.get("companies")
    )

    if q_type in ("aptitude", "logical", "verbal"):
        required = [
            ("question", bool(q.get("question"))),
            ("explanation", bool(q.get("explanation") or q.get("solution"))),
            ("correct_answer", bool(q.get("correct_answer") or q.get("correct_index"))),
            ("difficulty", bool(q.get("difficulty"))),
        ]
    else:
        required = [
            ("question", bool(q.get("question") or q.get("description") or q.get("statement"))),
            ("answer", bool(q.get("solution") or q.get("correct_answer") or q.get("expected_output"))),
            ("company", has_company),
            ("difficulty", bool(q.get("difficulty"))),
        ]

    for field, present in required:
        if not present:
            return f"missing_required_field_{field}"
    return None


def enrich_question(q: dict) -> dict:
    q = dict(q)
    q["quality_scores"] = _compute_quality_scores(q)
    q["pattern"] = q.get("pattern", "general-concept")
    q["review_status"] = "pending"
    q["semantic_hash"] = _semantic_hash(q)
    q["learning_objective"] = _derive_learning_objective(q)
    q["source_type"] = q.get("source_type", "pattern_relevant")
    q.setdefault("explanation", "")
    q.setdefault("hints", [])
    q.setdefault("placement_stage", ["oa", "technical-interview"])
    q.setdefault("skills", [])
    q.setdefault("roles", ["sde"])
    return q


def _compute_quality_scores(q: dict) -> dict:
    """Dimensional heuristic quality scores. NOT human-verified — see review_status.

    Each dimension is scored independently so that a question can be
    rejected from the live bank for one weak dimension rather than all.
    """
    content_score = _score_content(q)
    solution_score = _score_solution(q)
    explanation_score = _score_explanation(q)
    test_score = _score_tests(q)
    relevance_score = _score_relevance(q)
    learning_score = _score_learning(q)
    overall = _weighted_overall(
        content_score, solution_score, explanation_score,
        test_score, relevance_score, learning_score,
    )
    return {
        "content_quality": content_score,
        "solution_quality": solution_score,
        "explanation": explanation_score,
        "test_quality": test_score,
        "placement_relevance": relevance_score,
        "learning_value": learning_score,
        "overall": overall,
    }


def _score_content(q: dict) -> int:
    score = 0
    if q.get("question") or q.get("description") or q.get("statement"):
        score += 30
    if q.get("difficulty"):
        score += 10
    if q.get("constraints") and len(q.get("constraints", "")) > 10:
        score += 10
    return min(score, 50)


def _score_solution(q: dict) -> int:
    score = 0
    sol = q.get("solution") or q.get("correct_answer") or q.get("expected_output")
    if sol:
        score += 30
    if q.get("time_complexity") or q.get("complexities"):
        score += 10
    if q.get("space_complexity"):
        score += 10
    return min(score, 50)


def _score_explanation(q: dict) -> int:
    score = 0
    if q.get("explanation"):
        score += 40
    if q.get("hints") and len(q.get("hints", [])) > 0:
        score += 10
    if q.get("approach"):
        score += 10
    if _count_readable_lines(q.get("explanation", "")) >= 30:
        score += 10
    return min(score, 50)


def _score_tests(q: dict) -> int:
    score = 0
    tests = q.get("test_cases") or q.get("test_cases_visible") or []
    if tests:
        score += 30
        if len(tests) >= 3:
            score += 10
        if q.get("hidden_test_cases"):
            score += 10
    if q.get("example_input") and q.get("example_output"):
        score += 10
    return min(score, 50)


def _score_relevance(q: dict) -> int:
    score = 30  # base: every curated question is assumed placement-relevant
    if q.get("company"):
        score += 10
    if q.get("frequency") and q.get("frequency") > 0:
        score += 10
    if q.get("upvotes", 0) > 0:
        score += 10
    return min(score, 50)


def _score_learning(q: dict) -> int:
    score = 0
    if q.get("learning_objective"):
        score += 20
    if q.get("skills"):
        score += 10
    if q.get("placement_stage"):
        score += 10
    if q.get("hints") and len(q.get("hints", [])) <= 3:
        score += 10
    return min(score, 50)


def _weighted_overall(content, solution, explanation, test, relevance, learning) -> int:
    weights = {
        "content": 0.20,
        "solution": 0.20,
        "explanation": 0.25,
        "test": 0.15,
        "relevance": 0.10,
        "learning": 0.10,
    }
    raw = (
        content * weights["content"]
        + solution * weights["solution"]
        + explanation * weights["explanation"]
        + test * weights["test"]
        + relevance * weights["relevance"]
        + learning * weights["learning"]
    )
    return round(raw)


def _count_readable_lines(text: str) -> int:
    if not text:
        return 0
    return len([l for l in text.split("\n") if l.strip() and len(l.strip()) > 10])


def _derive_learning_objective(q: dict) -> str:
    topic = (q.get("topic", "") or "").lower().strip()
    pattern = (q.get("pattern", "") or "").lower().strip()
    for key, obj in LEARNING_OBJECTIVES.items():
        if key in topic or key in pattern:
            return obj
    return f"Master {topic or pattern or 'this concept'} for placement interviews."


def sanitize_and_split():
    if not RAW_PATH.exists():
        print(f"[sanitize_qbank] Raw data not found at {RAW_PATH}")
        return

    with open(RAW_PATH, "r", encoding="utf-8") as f:
        raw_questions = json.load(f)

    curated_pool = []
    rejected_pool = []
    review_duplicate_pool = []
    seen_titles = set()
    seen_semantic = set()

    stats = {
        "total": len(raw_questions),
        "templates_rejected": 0,
        "duplicates_rejected": 0,
        "semantic_duplicates": 0,
        "sent_to_review": 0,
        "low_quality_rejected": 0,
        "curated": 0,
    }

    for q in raw_questions:
        # 1. Reject unrendered template placeholders
        tmpl_reason = is_template_question(q)
        if tmpl_reason:
            q["rejection_reason"] = tmpl_reason
            rejected_pool.append(q)
            stats["templates_rejected"] += 1
            continue

        # 2. Reject exact/normalized-title duplicates
        title_key = _normalize(
            q.get("title", "")
            or q.get("question", "")
            or q.get("description", "")
        )
        if title_key in seen_titles:
            q["rejection_reason"] = "duplicate_concept_restatement"
            rejected_pool.append(q)
            stats["duplicates_rejected"] += 1
            continue

        # 3. Semantic duplicates → sent to review bucket, NOT auto-deleted.
        #    A human determines if these are true duplicates or pedagogically
        #    valuable variants (e.g., "Two Sum" vs "Two Sum II" vs "3Sum").
        sem_hash = _semantic_hash(q)
        if sem_hash in seen_semantic:
            q["rejection_reason"] = "semantic_duplicate"
            q["review_status"] = "pending_review_duplicate"
            review_duplicate_pool.append(q)
            stats["sent_to_review"] += 1
            continue

        # 4. Reject questions missing required fields by content type
        missing = has_quality_content(q)
        if missing:
            q["rejection_reason"] = missing
            rejected_pool.append(q)
            stats["low_quality_rejected"] += 1
            continue

        seen_titles.add(title_key)
        seen_semantic.add(sem_hash)
        curated_pool.append(enrich_question(q))
        stats["curated"] += 1

    # Also run semantic dedup on the curated pool to catch variants that
    # differ in title but share a fingerprint — these also go to review.
    post_review = []
    local_sem_seen = set()
    for q in curated_pool:
        sh = q.get("semantic_hash", "")
        if sh in local_sem_seen:
            q["review_status"] = "pending_review_duplicate"
            post_review.append(q)
        else:
            local_sem_seen.add(sh)

    curated_path = CURATED_DIR / "curated.json"
    rejected_path = REJECTED_DIR / "rejected.json"
    review_dup_path = REVIEW_DUP_DIR / "review_duplicates.json"

    with open(curated_path, "w", encoding="utf-8") as f:
        json.dump(curated_pool, f, indent=2, ensure_ascii=False)

    with open(rejected_path, "w", encoding="utf-8") as f:
        json.dump(rejected_pool, f, indent=2, ensure_ascii=False)

    with open(review_dup_path, "w", encoding="utf-8") as f:
        json.dump(review_duplicate_pool + post_review, f, indent=2, ensure_ascii=False)

    reviewed = sum(1 for q in curated_pool if q.get("review_status") == "placement_grade")
    fully_authored = sum(
        1 for q in curated_pool
        if bool(q.get("explanation")) and bool(q.get("solution") or q.get("correct_answer"))
    )
    print(
        f"[sanitize_qbank] Complete — "
        f"ingested: {stats['total']} | "
        f"curated: {stats['curated']} "
        f"(placement_grade: {reviewed}, fully_authored: {fully_authored}) | "
        f"rejected templates: {stats['templates_rejected']} | "
        f"rejected exact dups: {stats['duplicates_rejected']} | "
        f"sent to semantic review: {stats['sent_to_review']} | "
        f"rejected low-quality: {stats['low_quality_rejected']}"
    )


if __name__ == "__main__":
    sanitize_and_split()
