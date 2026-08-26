import random
from datetime import datetime, timezone
from typing import Dict, Any, List
from app.database import gamification_collection
from app.services.ai_core import chat_completion, parse_json


# Drill templates
DRILL_TEMPLATES = {
    "debugging": [
        {
            "type": "find_bug",
            "description": "Find and fix the bug in this code",
            "difficulty": "easy",
        },
        {
            "type": "predict_output",
            "description": "What does this code output?",
            "difficulty": "easy",
        },
        {
            "type": "optimize",
            "description": "Optimize this code for better time complexity",
            "difficulty": "medium",
        },
    ],
    "behavioral": [
        {
            "type": "star_quick",
            "description": "Quick STAR response in 2 minutes",
            "difficulty": "easy",
        },
        {
            "type": "lp_identify",
            "description": "Which Leadership Principle does this address?",
            "difficulty": "easy",
        },
    ],
    "resume": [
        {
            "type": "bullet_fix",
            "description": "Fix this weak bullet point",
            "difficulty": "easy",
        },
        {
            "type": "metric_add",
            "description": "Add a metric to this bullet",
            "difficulty": "easy",
        },
    ],
}


class DailyDrill:
    """5-minute daily placement drill for continuous engagement."""

    async def generate_daily_drill(self, user_id: str) -> Dict[str, Any]:
        """Generate a personalized daily drill based on weak areas."""
        # Get user's gamification profile
        profile = await gamification_collection.find_one({"user_id": user_id})

        # Determine weak areas
        weak_areas = []
        if profile:
            total_interviews = profile.get("total_interviews", 0)
            total_aptitude = profile.get("total_aptitude", 0)
            total_coding = profile.get("total_coding", 0)

            if total_interviews < 5:
                weak_areas.append("behavioral")
            if total_coding < 5:
                weak_areas.append("debugging")
            if total_aptitude < 3:
                weak_areas.append("resume")

        if not weak_areas:
            weak_areas = ["debugging", "behavioral", "resume"]

        # Pick one random weak area
        focus_area = random.choice(weak_areas)

        # Generate 3 quick questions
        questions = []

        # Question 1: Debugging
        q1 = await self._generate_debugging_question()
        questions.append(q1)

        # Question 2: Behavioral
        q2 = await self._generate_behavioral_question()
        questions.append(q2)

        # Question 3: Resume
        q3 = await self._generate_resume_question()
        questions.append(q3)

        # Shuffle questions
        random.shuffle(questions)

        return {
            "drill_id": f"drill_{datetime.now(timezone.utc).strftime('%Y%m%d')}",
            "focus_area": focus_area,
            "questions": questions,
            "time_limit": 300,  # 5 minutes
            "message": "Complete this 5-minute drill to maintain your streak!",
            "rewards": {
                "xp": 25,
                "streak_maintained": True,
                "pro_token_chance": 0.1,  # 10% chance to earn a Pro Token
            },
        }

    async def _generate_debugging_question(self) -> Dict[str, Any]:
        """Generate a quick debugging question."""
        messages = [
            {"role": "system", "content": "Generate a quick debugging question. Return valid JSON."},
            {"role": "user", "content": "Create a 30-second debugging challenge. Show code with a subtle bug."},
        ]

        response = await chat_completion(messages)
        result = parse_json(response)

        return {
            "type": "debugging",
            "question": result.get("question", "Find the bug in this code"),
            "code": result.get("code", ""),
            "options": result.get("options", ["Bug in line 3", "Bug in line 5", "No bug"]),
            "correct": result.get("correct", 0),
            "explanation": result.get("explanation", ""),
            "time_limit": 60,
        }

    async def _generate_behavioral_question(self) -> Dict[str, Any]:
        """Generate a quick behavioral question."""
        messages = [
            {"role": "system", "content": "Generate a quick behavioral question. Return valid JSON."},
            {"role": "user", "content": "Create a 60-second STAR method practice question."},
        ]

        response = await chat_completion(messages)
        result = parse_json(response)

        return {
            "type": "behavioral",
            "question": result.get("question", "Tell me about a time you faced a challenge"),
            "sample_answer": result.get("sample_answer", ""),
            "key_points": result.get("key_points", []),
            "time_limit": 120,
        }

    async def _generate_resume_question(self) -> Dict[str, Any]:
        """Generate a quick resume improvement question."""
        weak_bullets = [
            "Responsible for managing team projects",
            "Helped with customer service",
            "Worked on the backend system",
            "Participated in code reviews",
            "Assisted in data analysis",
        ]

        bullet = random.choice(weak_bullets)

        return {
            "type": "resume",
            "question": f"Improve this weak bullet point in 30 seconds:",
            "original_bullet": bullet,
            "hint": "Start with a strong action verb and add a metric",
            "time_limit": 60,
        }

    async def submit_drill(
        self,
        user_id: str,
        drill_id: str,
        answers: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Submit drill answers and get results."""
        # Calculate score
        correct = sum(1 for a in answers if a.get("correct", False))
        total = len(answers)
        score = (correct / total * 100) if total > 0 else 0

        # Check for Pro Token
        pro_token = random.random() < 0.1 and score >= 80

        # Update gamification
        xp_earned = 25 if score >= 60 else 10

        return {
            "score": score,
            "correct": correct,
            "total": total,
            "xp_earned": xp_earned,
            "pro_token_earned": pro_token,
            "message": self._get_drill_message(score),
            "streak_maintained": True,
        }

    def _get_drill_message(self, score: float) -> str:
        """Get encouraging message based on score."""
        if score >= 90:
            return "Perfect drill! You're interview-ready! 🔥"
        elif score >= 70:
            return "Great work! Keep the momentum going! 💪"
        elif score >= 50:
            return "Good effort! Practice makes perfect! 📈"
        else:
            return "Keep practicing! Every drill makes you stronger! 💡"
