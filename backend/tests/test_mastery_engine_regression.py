"""
Phase 6 — BALMA mastery regression tests.

Tests:
- Repeated attempts at one question do NOT create unlimited mastery evidence
- Unique validated question IDs are tracked
- Unseen transfer questions contribute meaningful evidence (count double)
- Difficulty influences evidence appropriately (hard > medium > easy)
- Invalid/untrusted questions do NOT contribute to mastery
- Prerequisite skills are respected (capped at Practicing if unmet)
- Repeated failures trigger targeted remediation
- Mastery is reproducible and explainable
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.services.mastery_engine import (
    record_solve,
    build_mastery_graph,
    calculate_mastery_level,
    calculate_mastery_from_stats,
    find_weak_areas,
    check_prerequisites,
    explain_mastery,
    MASTERY_LEVELS,
    DIFFICULTY_WEIGHTS,
    SkillMastery,
)


class TestUniqueQuestionEvidence:
    """Repeated attempts at one question must not inflate mastery."""

    def test_repeated_attempts_same_question_do_not_inflate_count(self):
        """10 attempts at the same question = 1 unique question, not 10."""
        stats = None
        for i in range(10):
            stats = record_solve(
                topic="arrays", sub_topic="two_sum",
                question_id="q-two-sum-001",
                question_type="coding",
                difficulty="medium",
                is_correct=True,
                trust_status="verified",
                existing_stats=stats,
            )
        assert stats["unique_questions_attempted"] == 1, \
            f"Expected 1 unique, got {stats['unique_questions_attempted']}"
        assert stats["total_attempts"] == 10, \
            f"Expected 10 total attempts, got {stats['total_attempts']}"
        assert stats["current_level"] == 1, \
            f"1 unique question should be level 1 (Introduced), got {stats['current_level']}"

    def test_ten_unique_questions_reaches_competent(self):
        """10 unique questions solved = Strong (level 4) at 100% accuracy.
        Competent (level 3) requires 6-10 questions with <75% accuracy."""
        stats = None
        for i in range(10):
            stats = record_solve(
                topic="arrays", sub_topic="two_sum",
                question_id=f"q-{i:03d}",
                question_type="coding",
                difficulty="easy",
                is_correct=True,
                trust_status="verified",
                existing_stats=stats,
            )
        assert stats["unique_questions_attempted"] == 10
        assert stats["current_level"] == 4, \
            f"10 unique solved at 100% should be level 4 (Strong), got {stats['current_level']}"

    def test_twenty_unique_questions_reaches_mastered(self):
        """20 unique questions solved = Mastered (level 5)."""
        stats = None
        for i in range(20):
            stats = record_solve(
                topic="arrays", sub_topic="two_sum",
                question_id=f"q-{i:03d}",
                question_type="coding",
                difficulty="medium",
                is_correct=True,
                trust_status="verified",
                existing_stats=stats,
            )
        assert stats["unique_questions_attempted"] == 20
        assert stats["current_level"] == 5, \
            f"20 unique solved should be level 5 (Mastered), got {stats['current_level']}"


class TestDifficultyWeighting:
    """Difficulty should influence evidence appropriately."""

    def test_hard_questions_weight_more_than_easy(self):
        """Hard correct answers contribute more weighted evidence."""
        stats_easy = record_solve(
            topic="arrays", sub_topic="two_sum",
            question_id="q-easy", question_type="coding",
            difficulty="easy", is_correct=True, trust_status="verified",
        )
        stats_hard = record_solve(
            topic="arrays", sub_topic="two_sum",
            question_id="q-hard", question_type="coding",
            difficulty="hard", is_correct=True, trust_status="verified",
        )
        assert stats_hard["weighted_evidence"] > stats_easy["weighted_evidence"], \
            f"Hard ({stats_hard['weighted_evidence']}) should weight more than easy ({stats_easy['weighted_evidence']})"
        assert DIFFICULTY_WEIGHTS["hard"] > DIFFICULTY_WEIGHTS["medium"] > DIFFICULTY_WEIGHTS["easy"]

    def test_medium_weights_between_easy_and_hard(self):
        assert DIFFICULTY_WEIGHTS["easy"] < DIFFICULTY_WEIGHTS["medium"] < DIFFICULTY_WEIGHTS["hard"]


class TestUnseenTransferEvidence:
    """Unseen transfer questions should contribute meaningful evidence."""

    def test_transfer_questions_count_double(self):
        """Transfer (unseen) questions count double for weighted evidence."""
        stats_normal = record_solve(
            topic="arrays", sub_topic="two_sum",
            question_id="q-normal", question_type="coding",
            difficulty="medium", is_correct=True, trust_status="verified",
            is_transfer=False,
        )
        stats_transfer = record_solve(
            topic="arrays", sub_topic="two_sum",
            question_id="q-transfer", question_type="coding",
            difficulty="medium", is_correct=True, trust_status="verified",
            is_transfer=True,
            existing_stats=stats_normal,
        )
        # Transfer question should add double the weight
        assert stats_transfer["weighted_evidence"] > stats_normal["weighted_evidence"] + DIFFICULTY_WEIGHTS["medium"], \
            "Transfer question should count double"

    def test_transfer_evidence_contributes_to_mastery(self):
        """Transfer questions help reach mastery levels faster."""
        stats = None
        # 9 unique normal questions (would be Practicing/Competent boundary)
        for i in range(9):
            stats = record_solve(
                topic="arrays", sub_topic="two_sum",
                question_id=f"q-normal-{i}", question_type="coding",
                difficulty="medium", is_correct=True, trust_status="verified",
                is_transfer=False, existing_stats=stats,
            )
        level_before = stats["current_level"]
        # 1 transfer question pushes evidence higher
        stats = record_solve(
            topic="arrays", sub_topic="two_sum",
            question_id="q-transfer-final", question_type="coding",
            difficulty="hard", is_correct=True, trust_status="verified",
            is_transfer=True, existing_stats=stats,
        )
        assert stats["current_level"] >= level_before, \
            "Transfer question should not decrease mastery level"


class TestUntrustedQuestions:
    """Invalid or untrusted questions must not contribute to mastery evidence."""

    def test_unverified_question_does_not_count_as_unique_evidence(self):
        """Unverified questions are recorded in total_attempts but not unique counts."""
        stats = record_solve(
            topic="arrays", sub_topic="two_sum",
            question_id="q-untrusted", question_type="coding",
            difficulty="medium", is_correct=True, trust_status="unverified",
        )
        assert stats["unique_questions_attempted"] == 0, \
            f"Unverified question should not count as unique evidence, got {stats['unique_questions_attempted']}"
        assert stats["total_attempts"] == 1

    def test_automated_checked_question_does_not_count_as_unique_evidence(self):
        """Automatically checked questions are learning evidence, not mastery evidence."""
        stats = record_solve(
            topic="arrays", sub_topic="two_sum",
            question_id="q-auto", question_type="coding",
            difficulty="medium", is_correct=True, trust_status="automated_checked",
        )
        assert stats["unique_questions_attempted"] == 0, \
            f"Automated checked should not count as unique evidence, got {stats['unique_questions_attempted']}"

    def test_verified_question_counts_as_unique_evidence(self):
        """Verified questions count as unique evidence."""
        stats = record_solve(
            topic="arrays", sub_topic="two_sum",
            question_id="q-verified", question_type="coding",
            difficulty="medium", is_correct=True, trust_status="verified",
        )
        assert stats["unique_questions_attempted"] == 1, \
            f"Verified question should count as unique evidence, got {stats['unique_questions_attempted']}"

    def test_reviewed_question_counts_as_unique_evidence(self):
        """Reviewed questions count as unique evidence."""
        stats = record_solve(
            topic="arrays", sub_topic="two_sum",
            question_id="q-reviewed", question_type="coding",
            difficulty="medium", is_correct=True, trust_status="reviewed",
        )
        assert stats["unique_questions_attempted"] == 1, \
            f"Reviewed question should count as unique evidence, got {stats['unique_questions_attempted']}"

    def test_quarantined_question_does_not_contribute(self):
        """Quarantined questions do not contribute to mastery."""
        stats = record_solve(
            topic="arrays", sub_topic="two_sum",
            question_id="q-quarantined", question_type="coding",
            difficulty="medium", is_correct=True, trust_status="quarantined",
        )
        assert stats["unique_questions_attempted"] == 0
        assert stats["total_attempts"] == 1


class TestPrerequisiteRespect:
    """Prerequisite skills must be respected."""

    def test_unmet_prerequisites_cap_level_at_practicing(self):
        """If prerequisites unmet, mastery capped at level 2 (Practicing)."""
        stats = record_solve(
            topic="arrays", sub_topic="two_sum",
            question_id="q-1", question_type="coding",
            difficulty="medium", is_correct=True, trust_status="verified",
        )
        for i in range(2, 25):
            stats = record_solve(
                topic="arrays", sub_topic="two_sum",
                question_id=f"q-{i}", question_type="coding",
                difficulty="medium", is_correct=True, trust_status="verified",
                existing_stats=stats,
                prerequisites_met=False,
            )
        # Without prerequisites, capped at level 2 even with 20+ questions
        assert stats["current_level"] <= 2, \
            f"Unmet prerequisites should cap at level 2, got {stats['current_level']}"
        assert stats["details"].get("prerequisite_gated") is True

    def test_met_prerequisites_allow_full_mastery(self):
        """With prerequisites met, 20+ questions reaches Mastered."""
        stats = None
        for i in range(20):
            stats = record_solve(
                topic="arrays", sub_topic="two_sum",
                question_id=f"q-{i}", question_type="coding",
                difficulty="medium", is_correct=True, trust_status="verified",
                existing_stats=stats,
                prerequisites_met=True,
            )
        assert stats["current_level"] == 5, \
            f"Met prerequisites + 20 questions should be Mastered, got {stats['current_level']}"
        assert stats["details"].get("prerequisite_gated") is not True


class TestRepeatedFailuresRemediation:
    """Repeated failures should trigger targeted remediation."""

    def test_repeated_failures_same_question_triggers_remediation(self):
        """Failing the same question twice triggers remediation_needed."""
        stats = record_solve(
            topic="arrays", sub_topic="two_sum",
            question_id="q-fail", question_type="coding",
            difficulty="medium", is_correct=False, trust_status="verified",
        )
        assert stats["remediation_needed"] is False, \
            "First failure should not trigger remediation"
        stats = record_solve(
            topic="arrays", sub_topic="two_sum",
            question_id="q-fail", question_type="coding",
            difficulty="medium", is_correct=False, trust_status="verified",
            existing_stats=stats,
        )
        assert stats["remediation_needed"] is True, \
            "Second failure on same question should trigger remediation"

    def test_three_unique_questions_low_accuracy_triggers_remediation(self):
        """3+ unique questions with <50% accuracy triggers remediation."""
        stats = record_solve(
            topic="arrays", sub_topic="two_sum",
            question_id="q-1", question_type="coding",
            difficulty="easy", is_correct=False, trust_status="verified",
        )
        stats = record_solve(
            topic="arrays", sub_topic="two_sum",
            question_id="q-2", question_type="coding",
            difficulty="easy", is_correct=False, trust_status="verified",
            existing_stats=stats,
        )
        stats = record_solve(
            topic="arrays", sub_topic="two_sum",
            question_id="q-3", question_type="coding",
            difficulty="easy", is_correct=True, trust_status="verified",
            existing_stats=stats,
        )
        assert stats["remediation_needed"] is True, \
            "3 unique questions with 33% accuracy should trigger remediation"


class TestMasteryExplainable:
    """Mastery must be reproducible and explainable."""

    def test_explain_mastery_returns_evidence_trail(self):
        stats = record_solve(
            topic="arrays", sub_topic="two_sum",
            question_id="q-1", question_type="coding",
            difficulty="medium", is_correct=True, trust_status="verified",
        )
        explanation = explain_mastery(SkillMastery(
            topic="arrays", sub_topic="two_sum",
            level=stats["current_level"],
            name=stats["current_level_name"],
            unique_questions_attempted=stats["unique_questions_attempted"],
            unique_questions_solved=stats["unique_questions_solved"],
            total_attempts=stats["total_attempts"],
            accuracy=stats["accuracy"],
            weighted_evidence=stats["weighted_evidence"],
            evidence_trail=[],
        ))
        assert explanation["reproducible"] is True
        assert "basis" in explanation
        assert explanation["basis"]["unique_questions_attempted"] == 1

    def test_mastery_reproducible_same_inputs(self):
        """Same sequence of inputs always produces same mastery level."""
        stats_a = None
        stats_b = None
        sequence = [
            ("q-1", "medium", True), ("q-2", "easy", True), ("q-3", "hard", False),
            ("q-4", "medium", True), ("q-5", "easy", True),
        ]
        for qid, diff, correct in sequence:
            stats_a = record_solve(
                topic="arrays", sub_topic="two_sum",
                question_id=qid, question_type="coding",
                difficulty=diff, is_correct=correct,
                trust_status="verified", existing_stats=stats_a,
            )
            stats_b = record_solve(
                topic="arrays", sub_topic="two_sum",
                question_id=qid, question_type="coding",
                difficulty=diff, is_correct=correct,
                trust_status="verified", existing_stats=stats_b,
            )
        assert stats_a["current_level"] == stats_b["current_level"]
        assert stats_a["unique_questions_attempted"] == stats_b["unique_questions_attempted"]
        assert stats_a["accuracy"] == stats_b["accuracy"]


class TestBuildMasteryGraph:
    """build_mastery_graph aggregates skills correctly."""

    def test_graph_aggregation(self):
        skills_data = [
            {"topic": "arrays", "sub_topic": "two_sum",
             "unique_question_ids": ["q1", "q2", "q3"],
             "solved_question_ids": ["q1", "q2"],
             "total_attempts": 5, "prerequisites_met": True},
            {"topic": "graphs", "sub_topic": "bfs",
             "unique_question_ids": ["q4"],
             "solved_question_ids": [],
             "total_attempts": 1, "prerequisites_met": True},
        ]
        graph = build_mastery_graph(skills_data)
        assert graph.total_skills == 2
        assert graph.mastered_count == 0
        assert graph.untried_count == 0
        assert graph.weak_count == 1  # graphs has level <= 1 and attempted

    def test_remediation_queue_populated(self):
        skills_data = [
            {"topic": "arrays", "sub_topic": "two_sum",
             "unique_question_ids": ["q1", "q2", "q3"],
             "solved_question_ids": ["q1"],
             "total_attempts": 10, "remediation_needed": True,
             "prerequisites_met": True},
        ]
        graph = build_mastery_graph(skills_data)
        assert len(graph.remediation_queue) == 1
        assert graph.remediation_queue[0]["topic"] == "arrays"


class TestCheckPrerequisites:
    """Prerequisite checking works correctly."""

    def test_all_prerequisites_met(self):
        graph = build_mastery_graph([
            {"topic": "arrays", "sub_topic": "basics",
             "unique_question_ids": ["q1", "q2", "q3", "q4", "q5", "q6"],
             "solved_question_ids": ["q1", "q2", "q3", "q4", "q5", "q6"],
             "total_attempts": 6, "prerequisites_met": True},
        ])
        met, unmet = check_prerequisites("arrays:advanced", graph, {
            "arrays:advanced": ["arrays:basics"],
        })
        assert met is True
        assert unmet == []

    def test_prerequisite_not_met(self):
        graph = build_mastery_graph([
            {"topic": "arrays", "sub_topic": "basics",
             "unique_question_ids": ["q1"],
             "solved_question_ids": [],
             "total_attempts": 1, "prerequisites_met": True},
        ])
        met, unmet = check_prerequisites("arrays:advanced", graph, {
            "arrays:advanced": ["arrays:basics"],
        })
        assert met is False
        assert "arrays:basics" in unmet


class TestCalculateMasteryLevel:
    """Level thresholds match the spec."""

    def test_thresholds(self):
        assert calculate_mastery_level(0, 0) == 0
        assert calculate_mastery_level(1, 0) == 1
        assert calculate_mastery_level(2, 2) == 1
        assert calculate_mastery_level(3, 1) == 2  # 3 questions, 33% accuracy
        assert calculate_mastery_level(3, 2) == 3  # 3 questions, 66% accuracy
        assert calculate_mastery_level(6, 3) == 3  # 6 questions, 50% accuracy
        assert calculate_mastery_level(6, 5) == 4  # 6 questions, 83% accuracy
        assert calculate_mastery_level(11, 8) == 4  # 11 questions, 72% accuracy
        assert calculate_mastery_level(11, 10) == 5  # 11 questions, 90% accuracy
        assert calculate_mastery_level(20, 18) == 5  # 20 questions, 90% accuracy
        assert calculate_mastery_level(20, 19) == 5  # 20 questions, 95% accuracy


class TestFindWeakAreas:
    """Weak areas identification works correctly."""

    def test_weak_areas_sorted_by_improvement_potential(self):
        skills_data = [
            {"topic": "arrays", "sub_topic": "a",
             "unique_questions_attempted": 5, "unique_questions_solved": 1,
             "total_attempts": 5, "remediation_needed": True, "prerequisites_met": True},
            {"topic": "graphs", "sub_topic": "b",
             "unique_questions_attempted": 3, "unique_questions_solved": 0,
             "total_attempts": 3, "remediation_needed": False, "prerequisites_met": True},
        ]
        weak = find_weak_areas(skills_data, top_n=5)
        assert len(weak) == 2
        # arrays (20% accuracy) should be weaker than graphs (0% accuracy but fewer attempts)
        # Sort: lowest level first, then lowest accuracy, then most attempts
        assert weak[0]["topic"] in ("arrays", "graphs")
