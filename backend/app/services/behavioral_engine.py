import re
from typing import Dict, Any, List
from app.services.ai import chat_completion, parse_json


class BehavioralEngine:
    """Strict STAR evaluation with prompt-and-push loop for incomplete answers."""

    # STAR component indicators (algorithmic detection)
    STAR_INDICATORS = {
        "situation": {
            "keywords": [
                "during", "when i", "at my", "in my", "while working",
                "at the time", "previously", "initially", "background",
            ],
            "patterns": [
                r'(?i)(during|when|at|in)\s+(my|the|our|a)',
                r'(?i)(previously|initially|background|context)',
            ],
        },
        "task": {
            "keywords": [
                "my role", "i was responsible", "i needed to", "my task",
                "i was asked", "i was tasked", "my objective", "goal",
            ],
            "patterns": [
                r'(?i)(my role|responsible for|tasked with|objective)',
                r'(?i)(needed to|had to|goal was)',
            ],
        },
        "action": {
            "keywords": [
                "i built", "i created", "i implemented", "i designed",
                "i led", "i managed", "i developed", "i analyzed",
                "i optimized", "i refactored", "i automated",
            ],
            "patterns": [
                r'(?i)\b(i\s+(built|created|implemented|designed|led|managed|developed|analyzed|optimized|refactored|automated|introduced|established))\b',
            ],
        },
        "result": {
            "keywords": [
                "resulting in", "which led to", "increased by", "reduced by",
                "improved by", "saved", "achieved", "accomplished",
            ],
            "patterns": [
                r'\d+%',
                r'\$\d+',
                r'\d+x\b',
                r'(?i)(resulting in|led to|increased|reduced|improved|saved|achieved)',
            ],
        },
    }

    def parse_star_components(self, text: str) -> Dict[str, Any]:
        """Algorithmically detect STAR components in text."""
        text_lower = text.lower()
        results = {}

        for component, indicators in self.STAR_INDICATORS.items():
            # Check keyword presence
            keyword_matches = sum(1 for kw in indicators["keywords"] if kw in text_lower)

            # Check pattern matches
            pattern_matches = sum(
                1 for p in indicators["patterns"]
                if re.search(p, text)
            )

            # Calculate component score
            total_signals = keyword_matches + pattern_matches
            if total_signals >= 3:
                score = 90
                status = "strong"
            elif total_signals >= 2:
                score = 70
                status = "present"
            elif total_signals >= 1:
                score = 50
                status = "weak"
            else:
                score = 0
                status = "missing"

            results[component] = {
                "score": score,
                "status": status,
                "keyword_matches": keyword_matches,
                "pattern_matches": pattern_matches,
            }

        return results

    def check_for_metrics(self, text: str) -> Dict[str, Any]:
        """Check if the answer contains quantifiable metrics."""
        metric_patterns = [
            (r'\d+%', "percentage"),
            (r'\$\d+', "dollar amount"),
            (r'\d+x\b', "multiplier"),
            (r'\d+ (users|customers|team members|hours|days|weeks)', "quantity"),
            (r'reduced.*by \d+', "reduction metric"),
            (r'increased.*by \d+', "increase metric"),
            (r'improved.*by \d+', "improvement metric"),
        ]

        found_metrics = []
        for pattern, metric_type in metric_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                found_metrics.append(metric_type)

        return {
            "has_metrics": len(found_metrics) > 0,
            "metric_count": len(found_metrics),
            "metric_types": found_metrics,
            "score": min(100, len(found_metrics) * 30),
        }

    async def evaluate_star_strict(
        self,
        question: str,
        answer: str,
        company: str = "",
    ) -> Dict[str, Any]:
        """
        Strict STAR evaluation with algorithmic pre-check + LLM analysis.
        Returns whether to prompt for more (prompt-and-push loop).
        """
        # Algorithmic pre-check
        star_components = self.parse_star_components(answer)
        metrics = self.check_for_metrics(answer)

        # Determine if prompt-and-push is needed
        missing_components = [
            comp for comp, data in star_components.items()
            if data["status"] in ["missing", "weak"]
        ]

        needs_push = len(missing_components) > 0 or not metrics["has_metrics"]

        # Determine which component to push for
        push_component = None
        push_message = None

        if star_components["result"]["status"] in ["missing", "weak"]:
            push_component = "result"
            push_message = (
                "Your actions were solid, but I need to know the impact. "
                "What happened next? Did the app speed up? Did users grow? "
                "Give me a metric to lock this bullet in."
            )
        elif star_components["action"]["status"] in ["missing", "weak"]:
            push_component = "action"
            push_message = (
                "I understand the situation and task, but I need more specifics on YOUR actions. "
                "What did YOU personally do? Use 'I' statements."
            )
        elif star_components["situation"]["status"] in ["missing", "weak"]:
            push_component = "situation"
            push_message = (
                "Help me understand the context better. "
                "When did this happen? What was the challenge?"
            )

        # Get LLM evaluation for detailed feedback
        system_prompt = (
            "You are an expert behavioral interviewer evaluating STAR answers.\n\n"
            "Evaluate:\n"
            "1. Was the situation clear and concise?\n"
            "2. Was the task clearly defined?\n"
            "3. Were actions specific and detailed?\n"
            "4. Was the result quantified?\n\n"
            "Return valid JSON with scores and feedback."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"""Question: {question}

Answer: {answer}

Company: {company or 'General'}

Evaluate this STAR answer."""},
        ]

        response = await chat_completion(messages)
        llm_result = parse_json(response)

        # Combine algorithmic + LLM results
        overall_score = (
            sum(c["score"] for c in star_components.values()) / 4 * 0.4 +
            metrics["score"] * 0.2 +
            llm_result.get("overall_score", 50) * 0.4
        )

        return {
            "overall_score": round(overall_score, 1),
            "star_breakdown": star_components,
            "metrics_analysis": metrics,
            "llm_feedback": llm_result,
            "needs_push": needs_push,
            "push_component": push_component,
            "push_message": push_message,
            "improvements": llm_result.get("improvements", []),
            "strengths": llm_result.get("strengths", []),
        }

    async def generate_star_template(
        self,
        question: str,
        company: str = "",
    ) -> Dict[str, Any]:
        """Generate a STAR answer template for practice."""
        system_prompt = (
            "Generate a STAR answer template that guides the user.\n"
            "Include guiding questions for each component.\n"
            "Return valid JSON."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Generate STAR template for: {question}\nCompany: {company or 'General'}"},
        ]

        response = await chat_completion(messages)
        return parse_json(response)

    async def generate_practice_questions(
        self,
        company: str,
        role: str,
        count: int = 5,
    ) -> List[Dict[str, Any]]:
        """Generate company-specific behavioral questions."""
        system_prompt = (
            f"Generate {count} behavioral interview questions for {company}.\n"
            "Include different categories: leadership, conflict, failure, success, teamwork.\n"
            "Return valid JSON with questions array."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Generate {count} behavioral questions for {role} at {company}."},
        ]

        response = await chat_completion(messages)
        result = parse_json(response)
        return result.get("questions", [])
