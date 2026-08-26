import json
from typing import Dict, Any, List
from app.services.ai_core import chat_completion, parse_json


class CodingEngine:
    """Cost-optimized coding challenge engine with single-pass hint generation."""

    def __init__(self):
        self.COMPANY_STYLES = {
            "google": {
                "focus": ["algorithms", "system design", "code quality"],
                "difficulty": "hard",
                "topics": ["graphs", "dynamic programming", "trees", "strings"],
            },
            "amazon": {
                "focus": ["leadership principles", "system design", "coding"],
                "difficulty": "medium-hard",
                "topics": ["arrays", "hashing", "trees", "graphs"],
            },
            "meta": {
                "focus": ["coding", "system design", "product sense"],
                "difficulty": "hard",
                "topics": ["graphs", "dynamic programming", "strings"],
            },
            "microsoft": {
                "focus": ["coding", "system design", "problem solving"],
                "difficulty": "medium-hard",
                "topics": ["arrays", "trees", "linked lists", "recursion"],
            },
            "tcs": {
                "focus": ["aptitude", "programming basics", "communication"],
                "difficulty": "easy-medium",
                "topics": ["basic programming", "aptitude", "logical reasoning"],
            },
        }

    async def generate_challenge_with_hints(
        self,
        company: str = "google",
        role: str = "SDE",
        difficulty: str = None,
    ) -> Dict[str, Any]:
        """
        Generate a coding challenge AND all 3 hint levels in ONE API call.
        Reduces cost from 4 calls to 1.
        """
        company_info = self.COMPANY_STYLES.get(company.lower(), self.COMPANY_STYLES["google"])
        if not difficulty:
            difficulty = company_info["difficulty"]

        system_prompt = (
            f"You are a coding interview question designer for {company.upper()} style interviews.\n\n"
            "Generate a complete coding challenge with:\n"
            "1. Problem statement with examples\n"
            "2. Constraints\n"
            "3. Test cases\n"
            "4. THREE levels of hints (progressive, not giving away the answer)\n"
            "5. Solution approach explanation\n\n"
            "HINT LEVELS:\n"
            "- Level 1: High-level approach (which technique to use)\n"
            "- Level 2: Data structure/algorithm hint (more specific)\n"
            "- Level 3: Pseudocode logic (almost giving it away)\n\n"
            "Return valid JSON matching the schema."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"""Generate a {difficulty} coding challenge for {company} {role} interview.

Topics to focus on: {', '.join(company_info['topics'][:3])}

Include all 3 hint levels in a single response."""},
        ]

        response = await chat_completion(messages)
        result = parse_json(response)

        # Ensure hints are structured correctly
        hints = result.get("hints", {})
        if isinstance(hints, list):
            hints = {
                "level_1": hints[0] if len(hints) > 0 else "Think about the approach",
                "level_2": hints[1] if len(hints) > 1 else "Consider using a specific data structure",
                "level_3": hints[2] if len(hints) > 2 else "Here's the key insight",
            }

        return {
            "challenge": {
                "title": result.get("title", "Coding Challenge"),
                "description": result.get("description", ""),
                "examples": result.get("examples", []),
                "constraints": result.get("constraints", []),
                "test_cases": result.get("test_cases", []),
                "difficulty": difficulty,
                "company": company,
                "topics": result.get("topics", []),
            },
            "hints": hints,  # Single-pass hint matrix
            "solution_approach": result.get("solution_approach", result.get("approach", "")),
            "time_limit": result.get("time_limit_seconds", 2700),
        }

    async def evaluate_as_interviewer(
        self,
        code: str,
        language: str,
        problem_description: str,
    ) -> Dict[str, Any]:
        """
        Act as a live interviewer evaluating code in real-time.
        Returns structured feedback like a real interviewer would give.
        """
        system_prompt = (
            "You are a senior tech interviewer conducting a live coding interview.\n\n"
            "Evaluate the candidate's code on:\n"
            "1. CORRECTNESS: Does it solve the problem?\n"
            "2. TIME COMPLEXITY: Is it optimal?\n"
            "3. SPACE COMPLEXITY: Is it efficient?\n"
            "4. CODE QUALITY: Is it clean and readable?\n"
            "5. EDGE CASES: Did they handle edge cases?\n\n"
            "Feedback style:\n"
            "- Be direct but constructive\n"
            "- Give hints if stuck, don't give solutions\n"
            "- Use interviewer language ('I see...', 'What if...', 'Can you optimize...')\n\n"
            "Return valid JSON."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"""PROBLEM:
{problem_description}

CANDIDATE'S CODE ({language}):
```{language}
{code}
```

Evaluate this as an interviewer. Be specific and helpful."""},
        ]

        response = await chat_completion(messages)
        result = parse_json(response)

        return {
            "verdict": result.get("verdict", "needs_improvement"),
            "correctness": result.get("correctness", "partial"),
            "time_complexity": result.get("time_complexity", "O(n)"),
            "space_complexity": result.get("space_complexity", "O(1)"),
            "feedback": result.get("feedback", ""),
            "strengths": result.get("strengths", []),
            "improvements": result.get("improvements", []),
            "interviewer_hints": result.get("hints", result.get("interviewer_hints", [])),
            "score": result.get("score", 5),
            "would_pass": result.get("score", 5) >= 7,
        }

    async def get_hint(
        self,
        problem_description: str,
        current_code: str,
        hint_level: int = 1,
    ) -> Dict[str, Any]:
        """
        Get a single hint at the specified level.
        Uses the pre-generated hint matrix if available, otherwise generates on demand.
        """
        system_prompt = (
            f"You are a coding interview coach giving a level {hint_level}/3 hint.\n\n"
            "HINT LEVELS:\n"
            "- Level 1: High-level approach direction\n"
            "- Level 2: Specific data structure/algorithm\n"
            "- Level 3: Key insight (almost giving it away)\n\n"
            "NEVER give the full solution. Guide them to discover it.\n"
            "Be encouraging and supportive.\n\n"
            "Return ONLY the hint text, no JSON needed."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"""Problem: {problem_description}

Current code:
{current_code or 'No code yet'}

Give me a level {hint_level} hint."""},
        ]

        response = await chat_completion(messages)

        return {
            "hint": response.strip(),
            "level": hint_level,
            "next_level_available": hint_level < 3,
        }

    async def explain_concept(
        self,
        concept: str,
        level: str = "intermediate",
    ) -> Dict[str, Any]:
        """Explain a coding concept at different difficulty levels."""
        system_prompt = (
            f"You are a coding tutor explaining '{concept}' at {level} level.\n\n"
            "Include:\n"
            "1. Simple definition (1-2 sentences)\n"
            "2. Why it matters for interviews\n"
            "3. How it works (step by step)\n"
            "4. Common use cases\n"
            "5. Example code snippet\n"
            "6. Common mistakes to avoid\n\n"
            "Return valid JSON."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Explain '{concept}' at {level} level for coding interviews."},
        ]

        response = await chat_completion(messages)
        return parse_json(response)
