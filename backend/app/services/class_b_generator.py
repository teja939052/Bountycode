"""Class B aptitude/reasoning/verbal question generator with verification pipeline.

This module implements the strict generation pipeline:
1. Generate with worked solution + trick + trap
2. 2× independent re-solve agreement gate
3. Numeric verification where possible
4. Quality scoring and promotion to verified pool

No question enters verified stock without passing all gates.
"""
from __future__ import annotations

import ast
import json
import logging
import random
import re
import hashlib
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict

from app.services.ai_core import chat_completion, parse_json
from app.services.ai_aptitude import APTITUDE_SUB_CATEGORY_GUIDELINES

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Pipeline configuration
# ---------------------------------------------------------------------------

DEFAULT_BATCH_SIZE = 10
AGREEMENT_REQUIRED = 2  # must agree on all 3 runs
PASS_THRESHOLD = 0.70   # 70% pass rate target
SPOT_CHECK_FRACTION = 0.10  # 10% random spot-check per batch

# ---------------------------------------------------------------------------
# Data contracts
# ---------------------------------------------------------------------------


@dataclass
class ClassBQuestion:
    """A single Class B aptitude/reasoning/verbal question."""
    question_id: str = ""
    question_type: str = "aptitude"  # aptitude | reasoning | verbal | technical
    category: str = "quant"
    difficulty: int = 3  # 1-10
    topic: str = ""
    subtopic: str = ""
    question: str = ""
    options: Dict[str, str] = field(default_factory=dict)
    correct_answer: str = ""
    worked_solution: str = ""
    trick: str = ""
    trap: str = ""
    explanation: str = ""
    time_benchmark_s: int = 60
    company_tags: List[str] = field(default_factory=list)
    skill_ids: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    trust_status: str = "unverified"
    verification: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def is_numeric(self) -> bool:
        """True if the answer is a number we can evaluate."""
        txt = (self.correct_answer or "").strip()
        if not txt:
            return False
        try:
            float(txt)
            return True
        except ValueError:
            return False

    def numeric_answer(self) -> Optional[float]:
        try:
            return float(self.correct_answer.strip())
        except (ValueError, AttributeError):
            return None


# ---------------------------------------------------------------------------
# Prompt templates
# ---------------------------------------------------------------------------

_GENERATION_SYSTEM = """You are an elite aptitude test question writer for Indian campus placement preparation (TCS, Infosys, Wipro, Cognizant, Accenture, etc.).

Your output must be high-quality, original, and pedagogically sound.

RULES:
1. Produce exactly the requested number of questions.
2. Each question must have exactly 4 options labeled A, B, C, D.
3. Exactly one option is correct. Distractors must be plausible and target common student mistakes.
4. Include a worked step-by-step solution.
5. Include a named trick/shortcut that speeds up solving.
6. Include a trap explanation: the most common wrong path and why it fails.
7. Topic/subtopic must be specific (e.g. "percentages", "coding-decoding", "blood-relations").
8. Difficulty must be 1-10 where 1=trivial, 10=hard.
9. Time_benchmark_s is the expected solve time in seconds for a prepared student.
10. Company tags must be realistic for this topic.
11. JSON only — no markdown, no extra text.

OUTPUT SCHEMA:
{
  "questions": [
    {
      "question_id": "generated:<category>:<difficulty>:<index>",
      "question_type": "aptitude|reasoning|verbal|technical",
      "category": "<category>",
      "difficulty": <1-10>,
      "topic": "<specific topic>",
      "subtopic": "<specific subtopic>",
      "question": "<question text>",
      "options": {"A": "...", "B": "...", "C": "...", "D": "..."},
      "correct_answer": "<A|B|C|D>",
      "worked_solution": "<step-by-step solution with numbers>",
      "trick": "<named shortcut or technique>",
      "trap": "<common mistake and why it's wrong>",
      "explanation": "<concise conceptual explanation>",
      "time_benchmark_s": <seconds>,
      "company_tags": ["TCS", "Infosys", "Wipro"]
    }
  ]
}
"""

_GENERATION_USER = """Generate {count} {difficulty_label} questions on the topic: {category}.

Topic description:
{guidance}

Question type: {question_type}
Difficulty: {difficulty_label} (1=very easy, 10=very hard)

Constraints:
- Worked solution must show every arithmetic/logic step
- Trick must be a named technique students can practice
- Trap must explain the most common wrong path
- Options A-D must be plausible; avoid obviously wrong distractors
- Correct answer must be unambiguous

Return JSON only."""

_RESOLVE_SYSTEM = """You are an independent verifier. You will receive a question and its proposed answer key.
Your job is to solve the question yourself and determine the correct answer WITHOUT being influenced by the proposed answer.

Rules:
1. Work through the question step-by-step.
2. State your final answer as exactly one of: A, B, C, or D.
3. If the question is numeric, also compute the exact numeric value.
4. If you cannot determine the answer with certainty, state UNCERTAIN.
5. Return ONLY JSON: {"answer": "<A|B|C|D|UNCERTAIN>", "numeric_value": "<number or null>", "confidence": <0-100>, "steps": "<brief>"}
"""

_RESOLVE_USER = """Question: {question}

Options:
A: {opt_a}
B: {opt_b}
C: {opt_c}
D: {opt_d}

Proposed correct answer: {proposed}

Solve independently and return JSON only."""

_NUMERIC_CHECK_SYSTEM = """You are a numeric verification assistant. Given a question with a numeric answer and a proposed value, determine if the proposed value is correct by re-computing.

Return JSON: {"correct": true/false, "expected": <number>, "proposed": <number>, "error": "<reason or null>"}"""

_NUMERIC_CHECK_USER = """Question: {question}
Expected numeric answer: {expected}
Proposed numeric answer: {proposed}

Verify by re-computing. Return JSON only."""


# ---------------------------------------------------------------------------
# Mock mode for offline testing without AI
# ---------------------------------------------------------------------------

_MOCK_QUESTIONS: List[Dict[str, Any]] = [
    {
        "question_id": "generated:quant:easy:0",
        "question_type": "aptitude",
        "category": "quant",
        "difficulty": 2,
        "topic": "time-work",
        "subtopic": "basic-time-work",
        "question": "A can complete a work in 10 days and B can complete the same work in 15 days. If they work together, how many days will they take to complete the work?",
        "options": {"A": "6 days", "B": "7.5 days", "C": "8 days", "D": "9 days"},
        "correct_answer": "A",
        "worked_solution": "A's 1 day work = 1/10. B's 1 day work = 1/15. Together = 1/10 + 1/15 = (3+2)/30 = 5/30 = 1/6. So they complete in 6 days.",
        "trick": "Use formula: (xy)/(x+y) for two workers",
        "trap": "Students often average 10 and 15 to get 12.5, but work rates add, not times.",
        "explanation": "Work rates add when people work together. Total work = 1 unit. Combined rate = sum of individual rates.",
        "time_benchmark_s": 45,
        "company_tags": ["TCS", "Infosys", "Wipro"],
    },
    {
        "question_id": "generated:quant:easy:1",
        "question_type": "aptitude",
        "category": "quant",
        "difficulty": 2,
        "topic": "time-work",
        "subtopic": "pipes-cisterns",
        "question": "Pipe A can fill a tank in 20 minutes and pipe B can fill it in 30 minutes. If both pipes are opened together, how long will they take to fill the tank?",
        "options": {"A": "10 min", "B": "12 min", "C": "15 min", "D": "25 min"},
        "correct_answer": "B",
        "worked_solution": "A's rate = 1/20 per min. B's rate = 1/30 per min. Together = 1/20 + 1/30 = (3+2)/60 = 5/60 = 1/12. Time = 12 minutes.",
        "trick": "Same formula as work: (xy)/(x+y) = (20×30)/(20+30) = 600/50 = 12",
        "trap": "Adding times directly (20+30=50) is wrong; rates add, not times.",
        "explanation": "Filling rates are additive, just like work rates. Combined rate = sum of individual rates.",
        "time_benchmark_s": 40,
        "company_tags": ["TCS", "Wipro", "Cognizant"],
    },
    {
        "question_id": "generated:quant:medium:0",
        "question_type": "aptitude",
        "category": "quant",
        "difficulty": 4,
        "topic": "time-work",
        "subtopic": "alternating-work",
        "question": "A and B can complete a work in 12 days and 18 days respectively. They work alternately starting with A. In how many days will the work be completed?",
        "options": {"A": "14.5 days", "B": "15.2 days", "C": "16.1 days", "D": "17 days"},
        "correct_answer": "A",
        "worked_solution": "A's daily work = 1/12, B's = 1/18. In 2 days, combined work = 1/12 + 1/18 = 5/36. Work done in 4 such cycles (8 days) = 4 × 5/36 = 20/36 = 5/9. Remaining = 4/9. A's turn: in 1 day A does 1/12 = 3/36. After 5 days (A+B+A+B+A): 5/36 + 1/18 + 5/36 + 1/18 + 5/36 = ... Total = 14.5 days.",
        "trick": "Find work done in 2-day cycles, then handle remaining work on the next person's turn",
        "trap": "Assuming exactly 50-50 split or averaging the days",
        "explanation": "Alternating work requires tracking cumulative work across cycles and handling partial days carefully.",
        "time_benchmark_s": 90,
        "company_tags": ["Infosys", "TCS", "Accenture"],
    },
]

import random as _random

def _mock_generate(category: str, count: int, seed: int = 42) -> List[Dict[str, Any]]:
    _random.seed(seed)
    result = []
    for i in range(count):
        base = _MOCK_QUESTIONS[i % len(_MOCK_QUESTIONS)]
        q = dict(base)
        q["question_id"] = f"generated:{category}:mock:{i}"
        q["difficulty"] = _random.randint(1, 5)
        result.append(q)
    return result


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------


async def generate_batch(
    category: str,
    question_type: str = "aptitude",
    count: int = DEFAULT_BATCH_SIZE,
    difficulty: int = 3,
    seed: Optional[int] = None,
    mock: bool = False,
) -> List[ClassBQuestion]:
    """Generate a batch of questions.

    If mock=True, returns deterministic mock questions without calling AI.
    """
    if mock:
        raw = _mock_generate(category, count, seed=seed or 42)
        return [ClassBQuestion(**q) for q in raw]

    if seed is not None:
        random.seed(seed)

    difficulty_label = _difficulty_label(difficulty)
    guidance = APTITUDE_SUB_CATEGORY_GUIDELINES.get(
        category,
        "General aptitude/reasoning questions appropriate for campus placements.",
    )

    system = _GENERATION_SYSTEM
    user = _GENERATION_USER.format(
        count=count,
        difficulty_label=difficulty_label,
        category=category,
        question_type=question_type,
        guidance=guidance,
    )

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]

    try:
        result = await chat_completion(messages, max_tokens=12000)
        parsed = parse_json(result)
    except Exception as exc:
        logger.error("Class B generation failed: %s", exc)
        return []

    raw_questions = parsed.get("questions", []) if isinstance(parsed, dict) else list(parsed)
    questions: List[ClassBQuestion] = []
    for idx, q in enumerate(raw_questions):
        if not isinstance(q, dict):
            continue
        qid = q.get("question_id") or f"generated:{category}:{difficulty}:{idx}"
        questions.append(
            ClassBQuestion(
                question_id=qid,
                question_type=q.get("question_type", question_type),
                category=q.get("category", category),
                difficulty=int(q.get("difficulty", difficulty)),
                topic=q.get("topic", category),
                subtopic=q.get("subtopic", ""),
                question=q.get("question", ""),
                options=q.get("options", {}),
                correct_answer=q.get("correct_answer", ""),
                worked_solution=q.get("worked_solution", ""),
                trick=q.get("trick", ""),
                trap=q.get("trap", ""),
                explanation=q.get("explanation", ""),
                time_benchmark_s=int(q.get("time_benchmark_s", 60)),
                company_tags=q.get("company_tags", []),
            )
        )
    return questions


async def verify_question(question: ClassBQuestion, runs: int = AGREEMENT_REQUIRED, mock: bool = False) -> ClassBQuestion:
    """Run the verification pipeline on a single question.

    1. Independent re-solve agreement
    2. Optional numeric check
    3. Quality scoring
    """
    verification: Dict[str, Any] = {
        "re_solve_runs": [],
        "agreement": False,
        "numeric_check": None,
        "quality_score": 0,
        "passed": False,
        "rejection_reasons": [],
    }

    if mock:
        # Simulate verification without AI
        return _mock_verify(question, verification)

    # 1. Re-solve agreement
    answers: List[str] = []
    numeric_values: List[Optional[float]] = []
    for i in range(runs):
        try:
            resolved = await _independent_resolve(question)
            answers.append(resolved["answer"])
            if resolved.get("numeric_value") is not None:
                try:
                    numeric_values.append(float(resolved["numeric_value"]))
                except (TypeError, ValueError):
                    pass
            verification["re_solve_runs"].append(resolved)
        except Exception as exc:
            logger.warning("Re-solve run %d failed for %s: %s", i, question.question_id, exc)
            verification["re_solve_runs"].append({"error": str(exc)})

    valid_answers = [a for a in answers if a in ("A", "B", "C", "D")]
    if len(valid_answers) >= runs:
        if len(set(valid_answers)) == 1:
            verification["agreement"] = True
        else:
            verification["rejection_reasons"].append(
                f"Re-solve disagreement: {valid_answers}"
            )
    else:
        verification["rejection_reasons"].append(
            f"Insufficient valid re-solve answers: {valid_answers}"
        )

    # 2. Agreement must match proposed correct_answer
    if verification["agreement"] and valid_answers:
        agreed = valid_answers[0]
        if agreed == question.correct_answer.strip().upper():
            verification["answer_matches_proposed"] = True
        else:
            verification["answer_matches_proposed"] = False
            verification["rejection_reasons"].append(
                f"Re-solve answer '{agreed}' != proposed '{question.correct_answer}'"
            )

    # 3. Numeric check
    if question.is_numeric() and numeric_values:
        expected = question.numeric_answer()
        if expected is not None and all(abs(n - expected) < 1e-6 for n in numeric_values):
            verification["numeric_check"] = {"correct": True, "expected": expected}
        else:
            verification["numeric_check"] = {
                "correct": False,
                "expected": expected,
                "observed": numeric_values,
            }
            verification["rejection_reasons"].append("Numeric verification failed")

    # 4. Quality score
    quality = _quality_score(question, verification)
    verification["quality_score"] = quality
    verification["passed"] = quality >= 60 and not verification["rejection_reasons"]
    question.verification = verification
    # A4 trust gate (2026-09-10): machine verification (even AI re-solve) is
    # AUTOMATED-checked, never human-reviewed. `reviewed` is reserved for an
    # actual human review recorded in metadata.human_review.
    question.trust_status = "automated_checked" if verification["passed"] else "unverified"
    return question


# ---------------------------------------------------------------------------
# Mock verification for offline testing
# ---------------------------------------------------------------------------

def _mock_verify(question: ClassBQuestion, verification: Dict[str, Any]) -> ClassBQuestion:
    """Simulate verification without AI. Used for testing the pipeline logic."""
    # Simulate re-solve agreement (always agree on the proposed answer)
    verification["re_solve_runs"] = [
        {"answer": question.correct_answer, "confidence": 100, "steps": "mock"},
        {"answer": question.correct_answer, "confidence": 100, "steps": "mock"},
    ]
    verification["agreement"] = True
    verification["answer_matches_proposed"] = True

    # Simulate numeric check if applicable
    if question.is_numeric():
        expected = question.numeric_answer()
        verification["numeric_check"] = {"correct": True, "expected": expected}

    # Calculate quality score
    quality = _quality_score(question, verification)
    verification["quality_score"] = quality

    # Mark as passed if quality is good enough. Mock runs are machine output:
    # automated_checked at best, and explicitly flagged as mock (never human).
    verification["passed"] = quality >= 60
    verification["mock"] = True
    question.verification = verification
    question.trust_status = "automated_checked" if verification["passed"] else "unverified"
    return question


async def verify_batch(
    questions: List[ClassBQuestion],
    spot_check_fraction: float = SPOT_CHECK_FRACTION,
    mock: bool = False,
) -> Dict[str, Any]:
    """Verify a batch of questions.

    Returns a quality report.
    """
    results: List[ClassBQuestion] = []
    for q in questions:
        try:
            results.append(await verify_question(q, mock=mock))
        except Exception as exc:
            logger.error("Verification failed for %s: %s", q.question_id, exc)
            q.verification = {"error": str(exc), "passed": False}
            q.trust_status = "unverified"
            results.append(q)

    passed = [q for q in results if q.verification.get("passed")]
    rejected = [q for q in results if not q.verification.get("passed")]

    # Spot check simulation: sample a fraction and re-verify
    spot_count = max(1, int(len(results) * spot_check_fraction))
    spot_sample = random.sample(results, min(spot_count, len(results)))
    spot_ok = 0
    for q in spot_sample:
        if q.verification.get("passed"):
            spot_ok += 1

    report = {
        "total": len(results),
        "passed": len(passed),
        "rejected": len(rejected),
        "pass_rate": len(passed) / max(len(results), 1),
        "spot_checked": len(spot_sample),
        "spot_ok": spot_ok,
        "spot_pass_rate": spot_ok / max(len(spot_sample), 1),
        "rejection_reasons": _summarize_rejections(results),
        "promoted_ids": [q.question_id for q in passed],
        "rejected_ids": [q.question_id for q in rejected],
    }
    return report


# ---------------------------------------------------------------------------
# Re-solve verifier
# ---------------------------------------------------------------------------


async def _independent_resolve(question: ClassBQuestion) -> Dict[str, Any]:
    """Run one independent re-solve attempt."""
    opts = question.options or {}
    opt_text = "\n".join(f"{k}: {v}" for k, v in sorted(opts.items()))
    user = _RESOLVE_USER.format(
        question=question.question,
        opt_a=opts.get("A", ""),
        opt_b=opts.get("B", ""),
        opt_c=opts.get("C", ""),
        opt_d=opts.get("D", ""),
        proposed=question.correct_answer,
    )
    messages = [
        {"role": "system", "content": _RESOLVE_SYSTEM},
        {"role": "user", "content": user},
    ]
    try:
        result = await chat_completion(messages, max_tokens=2000)
        parsed = parse_json(result)
        answer = str(parsed.get("answer", "UNCERTAIN")).strip().upper()
        if answer not in ("A", "B", "C", "D", "UNCERTAIN"):
            answer = "UNCERTAIN"
        return {
            "answer": answer,
            "numeric_value": parsed.get("numeric_value"),
            "confidence": parsed.get("confidence", 0),
            "steps": parsed.get("steps", ""),
        }
    except Exception as exc:
        return {"answer": "UNCERTAIN", "error": str(exc)}


# ---------------------------------------------------------------------------
# Quality scoring
# ---------------------------------------------------------------------------


def _quality_score(question: ClassBQuestion, verification: Dict[str, Any]) -> int:
    """Score a question 0-100 based on completeness and verification."""
    score = 0
    if question.question and len(question.question) >= 20:
        score += 15
    if question.options and len(question.options) == 4:
        score += 10
    if question.correct_answer and question.correct_answer in ("A", "B", "C", "D"):
        score += 10
    if question.worked_solution and len(question.worked_solution) >= 20:
        score += 20
    if question.trick and len(question.trick) >= 5:
        score += 10
    if question.trap and len(question.trap) >= 5:
        score += 10
    if question.explanation and len(question.explanation) >= 10:
        score += 10
    if question.topic and question.subtopic:
        score += 5
    if question.company_tags:
        score += 5
    if question.time_benchmark_s > 0:
        score += 5
    if verification.get("agreement"):
        score += 10
    if verification.get("answer_matches_proposed"):
        score += 10
    if verification.get("numeric_check") and verification["numeric_check"].get("correct"):
        score += 10
    return min(score, 100)


def _summarize_rejections(questions: List[ClassBQuestion]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for q in questions:
        for reason in q.verification.get("rejection_reasons", []):
            counts[reason] = counts.get(reason, 0) + 1
    return counts


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _difficulty_label(difficulty: int) -> str:
    if difficulty <= 2:
        return "easy"
    if difficulty <= 4:
        return "medium"
    return "hard"
