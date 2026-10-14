"""Unified Learning Service — Mimo-style learning flow orchestrator.

Flow:
  1. Captain Byte intro + concept story
  2. Interactive concept explanation (with animations)
  3. Guided exercise (first problem)
  4. Level quiz (3-5 questions)
  5. Personalized next problem (adaptive)

This service reuses:
  - LessonService for lesson content and code grading
  - adaptive_learning for skill assessment and weak areas
  - personalization for next-mission selection
  - question_store for practice problems
  - record_practice for gamification rewards
"""
from __future__ import annotations

import logging
import random
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.services.lesson import LessonService
from app.services.adaptive_learning import assess_user_skills, detect_weak_areas
from app.services.personalization import select_next_mission
from app.services.gamification import record_practice
from app.services import question_store
from app.content.curriculum.registry import get_lesson_dict

logger = logging.getLogger(__name__)

MASTERY_THRESHOLD = 70
QUIZ_QUESTIONS = 3


class UnifiedLearningService:
    """Orchestrates the unified learning flow for a user."""

    def __init__(self, user_id: str, topic_slug: Optional[str] = None):
        self.user_id = user_id
        self.topic_slug = topic_slug

    async def get_learning_step(self, step: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Return the requested learning step payload."""
        payload = payload or {}
        if step == "intro":
            return await self._intro(payload)
        if step == "concept":
            return await self._concept(payload)
        if step == "exercise":
            return await self._exercise(payload)
        if step == "quiz":
            return await self._quiz(payload)
        if step == "next":
            return await self._next(payload)
        raise ValueError(f"Unknown learning step: {step}")

    async def submit_exercise(self, code: str, language: str = "python", function_name: str = "") -> Dict[str, Any]:
        """Grade the guided exercise and return results + Captain Byte feedback."""
        exercise = await self._get_current_exercise()
        lesson = exercise.get("lesson_slug")
        step_index = exercise.get("step_index", 0)
        svc = self._lesson_service(lesson)
        lesson_data = svc.get_lesson()
        steps = lesson_data.get("guided_build", {}).get("steps", [])
        step = steps[step_index] if step_index < len(steps) else steps[-1]
        result = await svc.submit_build_step(
            user_code=code,
            function_name=function_name or step.get("function_name", ""),
            test_cases=step.get("test_cases", []),
            language=language,
        )
        passed = result.get("passed", False)
        captain_byte = self._captain_byte_feedback(passed, exercise.get("canonical_skill", ""))
        diamonds = 10 if passed else 0
        if passed:
            try:
                await record_practice(self.user_id, "lesson", 8 if passed else 4, {
                    "action": "exercise",
                    "lesson": lesson,
                    "topic": exercise.get("canonical_skill"),
                })
            except Exception:
                pass
        return {
            "passed": passed,
            "score": result.get("score", 0),
            "results": result.get("results", []),
            "captain_byte": captain_byte,
            "diamonds": diamonds,
            "next_step": "quiz" if passed else "exercise",
        }

    async def submit_quiz(self, answers: Dict[str, Any]) -> Dict[str, Any]:
        """Grade the quiz and decide next step."""
        quiz = await self._get_current_quiz()
        questions = quiz.get("questions", [])
        correct = 0
        for idx, q in enumerate(questions):
            user_answer = answers.get(str(idx))
            if q.get("type") == "mcq":
                correct_option = next((opt for opt in q.get("options", []) if opt.get("correct")), None)
                if correct_option and user_answer == correct_option.get("id"):
                    correct += 1
            elif q.get("type") == "code_tracing":
                expected = (q.get("expected_answer") or "").strip().lower()
                if expected and str(user_answer).strip().lower() == expected:
                    correct += 1
        score = round(correct / max(1, len(questions)) * 100, 1)
        passed = score >= MASTERY_THRESHOLD
        captain_byte = self._quiz_feedback(score, quiz.get("canonical_skill", ""))
        try:
            await record_practice(self.user_id, "lesson", score / 10, {
                "action": "quiz",
                "topic": quiz.get("canonical_skill"),
                "score": score,
            })
        except Exception:
            pass
        return {
            "score": score,
            "correct": correct,
            "total": len(questions),
            "passed": passed,
            "captain_byte": captain_byte,
            "next_step": "next" if passed else "concept",
        }

    async def _intro(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Captain Byte intro + topic story."""
        topic = self.topic_slug or payload.get("topic") or "arrays"
        lesson = self._load_lesson(topic)
        if not lesson:
            return {"topic": topic, "captain_byte": {"intro": "Let's get started!"}, "story": {}}
        captain_byte = lesson.get("captain_byte", {})
        story = lesson.get("story_context", {})
        return {
            "topic": topic,
            "lesson_id": lesson.get("lesson_id"),
            "title": lesson.get("title"),
            "captain_byte": {
                "intro": captain_byte.get("intro", "Let's learn this."),
                "mood": "briefing",
            },
            "story": {
                "title": story.get("title", ""),
                "narration": story.get("narration", ""),
                "setting": story.get("setting", ""),
                "character": story.get("character", ""),
            },
            "estimated_minutes": lesson.get("est_minutes", 10),
            "diamonds_reward": lesson.get("xp_reward", 50),
        }

    async def _concept(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Concept explanation with animations and Captain Byte guidance."""
        topic = self.topic_slug or payload.get("topic") or "arrays"
        lesson = self._load_lesson(topic)
        if not lesson:
            return {"topic": topic, "steps": [], "captain_byte": {}}
        discovery = lesson.get("discovery", {})
        prediction = lesson.get("prediction", {})
        return {
            "topic": topic,
            "lesson_id": lesson.get("lesson_id"),
            "title": lesson.get("title"),
            "discovery": {
                "title": discovery.get("title", ""),
                "conclusion": discovery.get("conclusion", ""),
                "steps": discovery.get("steps", [])[:4],
                "visual_primitives": discovery.get("visual_primitives", []),
            },
            "prediction": {
                "title": prediction.get("title", ""),
                "question": prediction.get("question", ""),
                "options": prediction.get("options", []),
                "explanation": prediction.get("explanation", ""),
            },
            "captain_byte": {
                "intro": lesson.get("captain_byte", {}).get("intro", "Follow along."),
                "mood": "guide",
            },
            "estimated_minutes": 5,
        }

    async def _exercise(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Return a guided build exercise for the current topic."""
        topic = self.topic_slug or payload.get("topic") or "arrays"
        lesson = self._load_lesson(topic)
        if not lesson:
            return {"topic": topic, "exercise": None}
        guided = lesson.get("guided_build", {})
        steps = guided.get("steps", [])
        step_index = payload.get("step_index", 0)
        if not steps:
            return {"topic": topic, "exercise": None}
        step = steps[min(step_index, len(steps) - 1)]
        return {
            "topic": topic,
            "lesson_id": lesson.get("lesson_id"),
            "title": lesson.get("title"),
            "step_index": step_index,
            "total_steps": len(steps),
            "exercise": {
                "title": step.get("title", ""),
                "description": step.get("description", ""),
                "function_name": step.get("function_name", ""),
                "signature": step.get("signature", ""),
                "starter_code": step.get("starter_code", ""),
                "test_cases": step.get("test_cases", []),
                "diamonds": step.get("diamonds", 10),
                "scaffolded_hints": step.get("scaffolded_hints", []),
            },
            "captain_byte": {
                "intro": guided.get("captain_byte_intro", lesson.get("captain_byte", {}).get("intro", "Build this.")),
                "mood": "challenge",
            },
        }

    async def _quiz(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Return a short level quiz for the current topic."""
        topic = self.topic_slug or payload.get("topic") or "arrays"
        lesson = self._load_lesson(topic)
        questions: List[Dict[str, Any]] = []
        if lesson:
            assessment = lesson.get("assessment", {})
            all_qs = assessment.get("questions", [])
            random.shuffle(all_qs)
            questions = all_qs[:QUIZ_QUESTIONS]
            canonical_skill = lesson.get("world_progression", {}).get("competency_id", topic)
        else:
            canonical_skill = topic
        if not questions:
            questions = self._fallback_quiz(topic)
        return {
            "topic": topic,
            "lesson_id": lesson.get("lesson_id") if lesson else None,
            "title": lesson.get("title") if lesson else topic,
            "questions": questions,
            "total_questions": len(questions),
            "mastery_threshold": MASTERY_THRESHOLD,
            "captain_byte": {
                "intro": (lesson.get("captain_byte", {}).get("intro") if lesson else "Let's check what you learned."),
                "mood": "assessment",
            },
            "canonical_skill": canonical_skill,
        }

    async def _next(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Select the next personalized problem using the personalization engine."""
        company = payload.get("company")
        role = payload.get("role")
        mission = await select_next_mission(self.user_id, company=company, role=role)
        topic_slug = mission.get("skill") or mission.get("domain_id") or self.topic_slug or "arrays"
        lesson = self._load_lesson(topic_slug)
        if mission.get("type") == "question" and mission.get("question_id"):
            try:
                q = question_store.get_question_for_serving(str(mission["question_id"]))
                if q:
                    return {
                        "type": "question",
                        "topic": topic_slug,
                        "question_id": q.get("id") or q.get("_id"),
                        "title": q.get("title") or q.get("question", ""),
                        "description": q.get("description") or q.get("question", ""),
                        "difficulty": q.get("difficulty", "medium"),
                        "why": mission.get("why", "Keep practicing."),
                        "priority": mission.get("priority", 5),
                        "company": company,
                        "role": role,
                    }
            except Exception:
                pass
        if lesson:
            return {
                "type": "lesson",
                "topic": topic_slug,
                "lesson_id": lesson.get("lesson_id"),
                "title": lesson.get("title"),
                "why": mission.get("why", "Let's continue learning."),
                "priority": mission.get("priority", 5),
                "estimated_minutes": lesson.get("est_minutes", 10),
                "diamonds_reward": lesson.get("xp_reward", 50),
                "company": company,
                "role": role,
            }
        return {
            "type": "explore",
            "topic": topic_slug,
            "title": mission.get("why", "Keep exploring."),
            "why": mission.get("why", "Keep exploring."),
            "priority": mission.get("priority", 5),
        }

    async def _get_current_exercise(self) -> Dict[str, Any]:
        topic = self.topic_slug or "arrays"
        lesson = self._load_lesson(topic)
        if not lesson:
            return {"lesson_slug": topic, "step_index": 0, "canonical_skill": topic}
        canonical_skill = lesson.get("world_progression", {}).get("competency_id", topic)
        return {"lesson_slug": topic, "step_index": 0, "canonical_skill": canonical_skill}

    async def _get_current_quiz(self) -> Dict[str, Any]:
        topic = self.topic_slug or "arrays"
        lesson = self._load_lesson(topic)
        if not lesson:
            return {"questions": [], "canonical_skill": topic}
        assessment = lesson.get("assessment", {})
        all_qs = assessment.get("questions", [])
        random.shuffle(all_qs)
        questions = all_qs[:QUIZ_QUESTIONS]
        canonical_skill = lesson.get("world_progression", {}).get("competency_id", topic)
        return {"questions": questions, "canonical_skill": canonical_skill}

    def _load_lesson(self, slug: str) -> Optional[Dict[str, Any]]:
        try:
            return get_lesson_dict(slug)
        except Exception:
            return None

    def _lesson_service(self, slug: str) -> LessonService:
        lesson = self._load_lesson(slug)
        if not lesson:
            raise ValueError(f"Lesson not found: {slug}")
        return LessonService(lesson)

    def _captain_byte_feedback(self, passed: bool, skill: str) -> Dict[str, Any]:
        theme = skill.lower()
        if "array" in theme or "hash" in theme:
            intro = "Nice. You stored and looked things up correctly." if passed else "Stop. What did you already store?"
        elif "search" in theme or "binary" in theme:
            intro = "Nice. You found the target efficiently." if passed else "Stop. Use the order to skip work."
        elif "sort" in theme:
            intro = "Nice. The list is in order." if passed else "Stop. Compare the right pair."
        elif "linked" in theme:
            intro = "Nice. You walked the chain correctly." if passed else "Stop. Track prev before changing next."
        elif "tree" in theme or "graph" in theme:
            intro = "Nice. You chose the right traversal." if passed else "Stop. Track visited nodes."
        elif "dp" in theme or "dynamic" in theme:
            intro = "Nice. You reused the subproblem result." if passed else "Stop. Don't recompute. Cache results."
        else:
            intro = "Nice work." if passed else "Try again. Trace it step by step."
        mood = "correct" if passed else "wrong"
        return {"intro": f"🧭 Captain Byte: {intro}", "mood": mood}

    def _quiz_feedback(self, score: float, skill: str) -> Dict[str, Any]:
        if score >= 90:
            intro = "You've got it. I'm removing the training wheels. Any problem in this topic."
            mood = "mastery"
        elif score >= MASTERY_THRESHOLD:
            intro = "Solid. You passed the level check. Let's apply this in a new context."
            mood = "correct"
        else:
            intro = "Not yet. Let's revisit the concept and try again."
            mood = "wrong"
        return {"intro": f"🧭 Captain Byte: {intro}", "mood": mood}

    def _fallback_quiz(self, topic: str) -> List[Dict[str, Any]]:
        return [
            {
                "type": "concept",
                "question": f"What is the main idea behind {topic}?",
                "options": [
                    {"id": "a", "text": "Store and retrieve efficiently", "correct": True},
                    {"id": "b", "text": "Loop through everything always", "correct": False},
                    {"id": "c", "text": "Avoid using data structures", "correct": False},
                    {"id": "d", "text": "Only use recursion", "correct": False},
                ],
                "explanation": f"{topic.title()} is about organizing data so you can access it efficiently.",
            },
            {
                "type": "code_tracing",
                "question": f"If you see a problem about {topic}, what's your first move?",
                "expected_answer": "identify pattern",
                "explanation": "Pattern recognition is the fastest path to the solution.",
            },
            {
                "type": "concept",
                "question": "When should you move from the current approach?",
                "options": [
                    {"id": "a", "text": "After it works", "correct": False},
                    {"id": "b", "text": "When you recognize a better pattern", "correct": True},
                    {"id": "c", "text": "Never", "correct": False},
                    {"id": "d", "text": "After 3 attempts", "correct": False},
                ],
                "explanation": "Pattern matching beats brute force every time.",
            },
        ]
