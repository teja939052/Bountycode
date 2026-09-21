from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import json
import random
from dataclasses import dataclass, field

from app.models.problem import (
    ProblemBase, LockDefinition, LockType, MisconceptionType, 
    HintLevel, StudentCodeSubmission, JudgeResult, SRSEntry
)
from app.services.static_judge import StaticJudge
from app.services.behavioral_judge import BehavioralJudge


# ──────────────────────────────────────────────────────────────────
# Lock Engine — The Core "Key" System
# ──────────────────────────────────────────────────────────────────

class LockEngine:
    """
    Manages the Lock & Key progression for each problem.
    Tracks which locks are unlocked, hint progression, misconception detection.
    """

    def __init__(self):
        self.static_judge = StaticJudge()
        self.behavioral_judge = BehavioralJudge()
        # In production: persist to MongoDB
        self._lock_states: Dict[str, Dict[str, Any]] = {}  # student_id -> {problem_id: state}
        self._misconception_counts: Dict[str, Dict[str, int]] = {}  # student_id -> {misconception: count}

    def get_lock_state(self, student_id: str, problem_id: str) -> Dict[str, Any]:
        """Get current lock state for student on problem."""
        key = f"{student_id}:{problem_id}"
        if key not in self._lock_states:
            self._lock_states[key] = {
                "unlocked_locks": [],
                "current_lock_index": 0,
                "hint_index": 0,
                "attempts": 0,
                "misconceptions_hit": [],
                "last_activity": datetime.utcnow().isoformat(),
            }
        return self._lock_states[key]

    def reset_lock_state(self, student_id: str, problem_id: str):
        """Reset lock state (for retry / new session)."""
        key = f"{student_id}:{problem_id}"
        self._lock_states[key] = {
            "unlocked_locks": [],
            "current_lock_index": 0,
            "hint_index": 0,
            "attempts": 0,
            "misconceptions_hit": [],
            "last_activity": datetime.utcnow().isoformat(),
        }

    def get_current_lock(self, problem: ProblemBase, student_id: str) -> Optional[LockDefinition]:
        """Get the lock the student should be working on."""
        state = self.get_lock_state(student_id, problem.id)
        locks = problem.locks
        idx = state["current_lock_index"]
        if idx < len(locks):
            return locks[idx]
        return None  # All locks unlocked

    def check_lock(self, problem: ProblemBase, student_id: str, 
                   student_input: str, language: str) -> JudgeResult:
        """
        Main entry point: check if student's input unlocks the current lock.
        Returns JudgeResult with unlock status, hints, misconceptions.
        """
        state = self.get_lock_state(student_id, problem.id)
        current_lock = self.get_current_lock(problem, student_id)

        if not current_lock:
            return JudgeResult(
                success=True,
                mode="complete",
                message="🏆 All locks unlocked! Problem mastered.",
                score=100.0,
                xp_awarded=problem.estimated_xp,
                mastery_gain=problem.mastery_impact,
            )

        state["attempts"] += 1
        state["last_activity"] = datetime.utcnow().isoformat()

        # Check the lock based on its type
        passed, feedback = self.static_judge.check_lock(student_input, current_lock.dict(), language)

        if passed:
            # Unlock this lock
            state["unlocked_locks"].append(current_lock.id)
            state["current_lock_index"] += 1
            state["hint_index"] = 0  # Reset hints for next lock

            # Check if all locks unlocked
            if state["current_lock_index"] >= len(problem.locks):
                return JudgeResult(
                    success=True,
                    mode="complete",
                    message="🏆 LOCK BROKEN! All concepts mastered.",
                    score=100.0,
                    xp_awarded=problem.estimated_xp,
                    mastery_gain=problem.mastery_impact,
                    lock_unlocked=current_lock.id,
                )

            # Move to next lock
            next_lock = problem.locks[state["current_lock_index"]]
            return JudgeResult(
                success=True,
                mode="lock_unlocked",
                message=f"✓ {current_lock.label} unlocked! {feedback}",
                lock_unlocked=current_lock.id,
                hint_text=f"Next: {next_lock.hint_text}",
            )

        else:
            # Lock not passed - provide hint
            hint_result = self._provide_hint(problem, student_id, current_lock, student_input, language)
            return JudgeResult(
                success=False,
                mode="hint",
                message=feedback,
                hint_index=state["hint_index"],
                hint_text=hint_result.hint_text,
                misconception=hint_result.misconception,
            )

    def _provide_hint(self, problem: ProblemBase, student_id: str,
                      current_lock: LockDefinition, student_input: str, language: str) -> "HintResult":
        """Generate deterministic hint based on misconception detection."""
        state = self.get_lock_state(student_id, problem.id)

        # Detect misconception from student input
        misconception = self._detect_misconception(current_lock, student_input, language)

        if misconception:
            state["misconceptions_hit"].append(misconception.value)
            # Track count for adaptive hinting
            key = f"{student_id}:{problem.id}"
            if key not in self._misconception_counts:
                self._misconception_counts[key] = {}
            self._misconception_counts[key][misconception.value] = \
                self._misconception_counts[key].get(misconception.value, 0) + 1

        # Get hint from hint graph
        hint_index = min(state["hint_index"], len(problem.hint_graph) - 1)
        hint = problem.hint_graph[hint_index] if problem.hint_graph else None

        state["hint_index"] += 1

        # Generate tutor message based on misconception
        tutor_msg = self._generate_tutor_message(current_lock, misconception, 
                                                  self._misconception_counts.get(f"{student_id}:{problem.id}", {}).get(misconception.value, 1))

        return HintResult(
            hint_text=hint.text if hint else tutor_msg,
            misconception=misconception,
        )

    def _detect_misconception(self, lock: LockDefinition, student_input: str, language: str) -> Optional[MisconceptionType]:
        """Deterministic misconception detection."""
        # Check rejected patterns first
        if lock.rejected:
            for pattern in lock.rejected:
                if pattern.lower() in student_input.lower():
                    return lock.misconception

        # Lock-specific detection
        if lock.type == LockType.CODE_EXPRESSION:
            return self._detect_code_misconception(lock, student_input)
        elif lock.type == LockType.FIX_THE_BUG:
            return self._detect_bug_misconception(lock, student_input)
        
        return lock.misconception  # Default to associated misconception

    def _detect_code_misconception(self, lock: LockDefinition, code: str) -> Optional[MisconceptionType]:
        """Detect misconception from code expression."""
        code_lower = code.lower()
        
        # Binary search specific
        if "high = mid - 1" in code_lower and "target" in code_lower:
            if ">" in code or "greater" in code_lower:
                return MisconceptionType.WRONG_BOUNDARY
        
        if "low = mid + 1" in code_lower and "<" in code:
            return MisconceptionType.WRONG_BOUNDARY

        # Off by one
        if "mid + 1" in code and "high" in code:
            return MisconceptionType.OFF_BY_ONE
        
        # Incorrect midpoint
        if "mid =" in code and ("low + high" not in code and "high - low" not in code):
            return MisconceptionType.INCORRECT_MIDPOINT

        return lock.misconception

    def _detect_bug_misconception(self, lock: LockDefinition, code: str) -> Optional[MisconceptionType]:
        """Detect misconception from bug fix."""
        code_lower = code.lower()
        
        if "high = mid - 1" in code_lower and "target" in code_lower and ">" in code:
            return MisconceptionType.WRONG_BOUNDARY
        
        if "low = mid + 1" in code_lower and "<" in code:
            return MisconceptionType.WRONG_BOUNDARY

        if "while low < high" in code_lower:
            return MisconceptionType.INCORRECT_TERMINATION

        return lock.misconception

    def _generate_tutor_message(self, lock: LockDefinition, 
                                misconception: Optional[MisconceptionType], 
                                hit_count: int) -> str:
        """Generate tutor character message based on misconception and frequency."""
        
        tutor_messages = {
            MisconceptionType.WRONG_BOUNDARY: [
                "🧭 Captain Byte: You found the target! But you're walking toward the wrong half of the island.",
                "🧭 Captain Byte: The target is larger than the middle value. Which side holds the larger numbers?",
                "🧭 Captain Byte: Think about it — if target > arr[mid], the answer must be in the RIGHT half. So which boundary moves?",
            ],
            MisconceptionType.OFF_BY_ONE: [
                "🧭 Captain Byte: Close! But you're off by one step. What happens when low == high?",
                "🧭 Captain Byte: The loop condition matters. Should it be <= or < when low == high?",
            ],
            MisconceptionType.INCORRECT_MIDPOINT: [
                "🧭 Captain Byte: The midpoint formula is your compass. What's (low + high) // 2?",
                "🧭 Captain Byte: Integer division is key here. No floating point allowed!",
            ],
            MisconceptionType.INCORRECT_TERMINATION: [
                "🧭 Captain Byte: Your loop might run forever! When should it stop?",
                "🧭 Captain Byte: The search space must shrink every iteration. Does yours?",
            ],
        }

        messages = tutor_messages.get(misconception, [
            f"🧭 Captain Byte: {lock.hint_text}",
        ])

        # Return appropriate message based on hit count
        idx = min(hit_count - 1, len(messages) - 1)
        return messages[idx]


# ──────────────────────────────────────────────────────────────────
# Hint Result
# ──────────────────────────────────────────────────────────────────

@dataclass
class HintResult:
    hint_text: str
    misconception: Optional[MisconceptionType]


# ──────────────────────────────────────────────────────────────────
# SRS (Spaced Repetition System) — SuperMemo-2 Algorithm
# ──────────────────────────────────────────────────────────────────

class SRSService:
    """Spaced Repetition System using SuperMemo-2 algorithm."""

    def __init__(self):
        # In production: persist to MongoDB
        self._entries: Dict[str, SRSEntry] = {}

    def get_entry(self, student_id: str, problem_id: str) -> SRSEntry:
        key = f"{student_id}:{problem_id}"
        if key not in self._entries:
            self._entries[key] = SRSEntry(
                problem_id=problem_id,
                student_id=student_id,
                last_attempt=datetime.utcnow().isoformat(),
                correct=False,
                easiness_factor=2.5,
                repetition_interval=1,
                due_date=datetime.utcnow().isoformat(),
                times_shown=0,
                times_correct=0,
            )
        return self._entries[key]

    def record_attempt(self, student_id: str, problem_id: str, correct: bool) -> SRSEntry:
        """Record an attempt and update SRS schedule."""
        entry = self.get_entry(student_id, problem_id)
        entry.last_attempt = datetime.utcnow().isoformat()
        entry.times_shown += 1

        if correct:
            entry.times_correct += 1
            # SuperMemo-2 algorithm
            if entry.times_correct == 1:
                entry.repetition_interval = 1
            elif entry.times_correct == 2:
                entry.repetition_interval = 6
            else:
                entry.repetition_interval = round(entry.repetition_interval * entry.easiness_factor)

            # Update easiness factor based on quality (assuming quality=5 for correct)
            entry.easiness_factor = max(1.3, entry.easiness_factor + 0.1)
        else:
            # Reset on failure
            entry.times_correct = 0
            entry.repetition_interval = 1
            entry.easiness_factor = max(1.3, entry.easiness_factor - 0.2)

        entry.due_date = (datetime.utcnow() + timedelta(days=entry.repetition_interval)).isoformat()
        entry.correct = correct

        return entry

    def get_due_problems(self, student_id: str, limit: int = 20) -> List[SRSEntry]:
        """Get problems due for review."""
        now = datetime.utcnow()
        due = [
            e for e in self._entries.values() 
            if e.student_id == student_id and datetime.fromisoformat(e.due_date) <= now
        ]
        due.sort(key=lambda x: x.due_date)
        return due[:limit]

    def get_mastery(self, student_id: str, problem_id: str) -> float:
        """Calculate mastery percentage (0-100)."""
        entry = self.get_entry(student_id, problem_id)
        if entry.times_shown == 0:
            return 0.0
        # Mastery based on correct rate and recency
        correct_rate = entry.times_correct / entry.times_shown
        recency_factor = 1.0 if entry.correct else 0.5
        return round(correct_rate * recency_factor * 100, 1)


# ──────────────────────────────────────────────────────────────────
# Unified Judge Service — Combines All Three Layers
# ──────────────────────────────────────────────────────────────────

class UnifiedJudge:
    """
    Orchestrates all three layers:
    Layer 1: Static Judge (AST + patterns)
    Layer 2: Behavioral Judge (precomputed tests)
    Layer 3: Local Runtime (Pyodide/Worker) - optional
    Layer 4: Lock Engine (pedagogical progression)
    """

    def __init__(self):
        self.static = StaticJudge()
        self.behavioral = BehavioralJudge()
        self.locks = LockEngine()
        self.srs = SRSService()

    def judge(self, submission: StudentCodeSubmission, problem: ProblemBase,
              student_id: Optional[str] = None) -> JudgeResult:
        """
        Full judgment pipeline.
        """
        student_id = student_id or "default_user"
        
        # Get current lock
        current_lock = self.locks.get_current_lock(problem, student_id)
        
        if not current_lock:
            # Problem already mastered - run full behavioral test
            return self._judge_full_problem(submission, problem, student_id)

        # Check against current lock (Layer 1 + Lock Engine)
        if current_lock.type == LockType.RUNTIME:
            # For runtime locks, we'd use local runtime
            # For now, fall back to behavioral
            return self._judge_runtime_lock(submission, problem, student_id, current_lock)
        
        # Static/Concept locks
        return self.locks.check_lock(problem, student_id, submission.code, submission.language)

    def _judge_full_problem(self, submission: StudentCodeSubmission, 
                            problem: ProblemBase, student_id: str) -> JudgeResult:
        """Run full problem judgment (behavioral tests)."""
        # This would use local runtime for actual execution
        # For now, return a placeholder
        return JudgeResult(
            success=True,
            mode="behavioral",
            message="Full problem execution would run here (local runtime)",
            score=100.0,
        )

    def _judge_runtime_lock(self, submission: StudentCodeSubmission,
                            problem: ProblemBase, student_id: str,
                            lock: LockDefinition) -> JudgeResult:
        """Judge a runtime lock using local execution."""
        # This would call localRuntime.executePython/JS
        # For now, return hint to use runtime
        return JudgeResult(
            success=False,
            mode="runtime",
            message="This lock requires code execution. Use the Run button.",
            hint_text="Write the complete function and click Run to test against hidden cases.",
        )

    def record_completion(self, student_id: str, problem_id: str, correct: bool):
        """Record completion for SRS."""
        self.srs.record_attempt(student_id, problem_id, correct)

    def get_next_due(self, student_id: str, limit: int = 5) -> List[SRSEntry]:
        return self.srs.get_due_problems(student_id, limit)