from typing import List, Dict
from app.services.ai import chat_completion, parse_json


# Company-specific question patterns
COMPANY_QUESTIONS = {
    "google": {
        "focus": ["algorithms", "system design", "code quality"],
        "difficulty": "hard",
        "typical_topics": ["graphs", "dynamic programming", "trees", "string manipulation"],
        "tips": "Google values clean code, optimal solutions, and ability to discuss trade-offs",
    },
    "amazon": {
        "focus": ["leadership principles", "system design", "coding"],
        "difficulty": "medium-hard",
        "typical_topics": ["arrays", "hashing", "trees", "graph algorithms"],
        "tips": "Amazon values customer obsession, ownership, and dive deep approach",
    },
    "meta": {
        "focus": ["coding", "system design", "product sense"],
        "difficulty": "hard",
        "typical_topics": ["graphs", "dynamic programming", "string manipulation"],
        "tips": "Meta values move fast, focus on impact, and build social value",
    },
    "microsoft": {
        "focus": ["coding", "system design", "problem solving"],
        "difficulty": "medium-hard",
        "typical_topics": ["arrays", "trees", "linked lists", "recursion"],
        "tips": "Microsoft values growth mindset and collaboration",
    },
    "tcs": {
        "focus": ["aptitude", "programming basics", "communication"],
        "difficulty": "easy-medium",
        "typical_topics": ["basic programming", "aptitude", "logical reasoning"],
        "tips": "TCS values communication skills and basic technical knowledge",
    },
    "infosys": {
        "focus": ["aptitude", "programming basics", "soft skills"],
        "difficulty": "easy-medium",
        "typical_topics": ["basic programming", "aptitude", "verbal ability"],
        "tips": "Infosys values learning ability and adaptability",
    },
}


async def generate_company_coding_challenge(
    company: str,
    role: str = "SDE",
    difficulty: str = None,
) -> Dict:
    """Generate a coding challenge specific to a company's style."""
    company_info = COMPANY_QUESTIONS.get(company.lower(), COMPANY_QUESTIONS["google"])
    
    if not difficulty:
        difficulty = company_info["difficulty"]
    
    messages = [
        {
            "role": "system",
            "content": f"""You are a coding challenge creator who generates problems in the style of {company.upper()} interviews.

Company focus: {', '.join(company_info['focus'])}
Typical topics: {', '.join(company_info['typical_topics'])}
Difficulty: {difficulty}

Create a coding problem that:
1. Matches {company}'s interview style
2. Tests the typical topics they focus on
3. Has clear examples and constraints
4. Includes multiple test cases
5. Has hints for getting unstuck

Return ONLY valid JSON:
{{
    "title": "Problem Title",
    "company": "{company}",
    "difficulty": "{difficulty}",
    "description": "Full problem description with examples",
    "examples": [
        {{"input": "example input", "output": "expected output", "explanation": "why"}}
    ],
    "constraints": ["constraint 1", "constraint 2"],
    "test_cases": [
        {{"input": "test input", "expected": "expected output"}}
    ],
    "hints": [
        {"level": 1, "hint": "vague hint"},
        {"level": 2, "hint": "more specific hint"},
        {"level": 3, "hint": "almost giving it away"}
    ],
    "time_limit_seconds": 2700,
    "topics": ["topic 1", "topic 2"],
    "company_tips": "{company_info['tips']}",
    "follow_up": "Advanced version of this problem"
}}""",
        },
        {
            "role": "user",
            "content": f"Generate a {difficulty} level coding challenge for a {role} interview at {company}.",
        },
    ]
    
    response = await chat_completion(messages)
    return parse_json(response)


async def generate_mock_interviewer_feedback(
    code: str,
    language: str,
    problem_description: str,
) -> Dict:
    """Act as an interviewer evaluating the code in real-time."""
    messages = [
        {
            "role": "system",
            "content": """You are a senior tech interviewer conducting a live coding interview.

Evaluate the candidate's code on:
1. Correctness - Does it solve the problem?
2. Time Complexity - Is it optimal?
3. Space Complexity - Is it efficient?
4. Code Quality - Is it clean and readable?
5. Edge Cases - Did they handle edge cases?

Provide feedback like a real interviewer would - constructive but direct.
Give hints if they're stuck, but don't give away the solution.

Return ONLY valid JSON:
{
    "verdict": "pass/needs_improvement/stuck",
    "correctness": "correct/incorrect/partial",
    "time_complexity": "O(n)",
    "space_complexity": "O(1)",
    "feedback": "interviewer-style feedback",
    "strengths": ["strength 1", "strength 2"],
    "improvements": ["improvement 1", "improvement 2"],
    "hints": ["hint 1", "hint 2"],
    "next_step": "what to do next",
    "score": 7
}""",
        },
        {
            "role": "user",
            "content": f"""Problem: {problem_description}

Candidate's Code ({language}):
{code}

Evaluate this code as an interviewer.""",
        },
    ]
    
    response = await chat_completion(messages)
    return parse_json(response)


async def explain_code_concept(
    concept: str,
    level: str = "intermediate",
) -> Dict:
    """Explain a coding concept at different difficulty levels."""
    messages = [
        {
            "role": "system",
            "content": f"""You are a friendly coding tutor who explains concepts clearly.

Explain the concept at {level} level:
- Beginner: Use analogies, simple examples, no jargon
- Intermediate: Include some technical details, common use cases
- Expert: Deep dive, edge cases, performance implications

Include:
1. What it is (simple definition)
2. Why it's important
3. How it works (step by step)
4. Common use cases
5. Example code snippet
6. Common mistakes to avoid

Return ONLY valid JSON:
{{
    "concept": "{concept}",
    "level": "{level}",
    "simple_definition": "one-sentence definition",
    "why_important": "why this matters",
    "how_it_works": "step-by-step explanation",
    "use_cases": ["use case 1", "use case 2"],
    "example_code": "code example",
    "common_mistakes": ["mistake 1", "mistake 2"],
    "related_concepts": ["concept 1", "concept 2"]
}}""",
        },
        {
            "role": "user",
            "content": f"Explain '{concept}' at {level} level for a coding interview.",
        },
    ]
    
    response = await chat_completion(messages)
    return parse_json(response)


async def generate_hint(
    problem_description: str,
    current_code: str,
    hint_level: int = 1,
) -> str:
    """Generate a progressive hint without giving away the solution."""
    messages = [
        {
            "role": "system",
            "content": f"""You are a coding interview coach giving progressive hints.

Hint level: {hint_level}/3
- Level 1: Vague nudge in the right direction
- Level 2: More specific approach suggestion
- Level 3: Almost giving away the key insight

Never give the full solution. Guide them to discover it themselves.
Be encouraging and supportive.

Return ONLY the hint text, no JSON needed.""",
        },
        {
            "role": "user",
            "content": f"""Problem: {problem_description}

Current code:
{current_code or 'No code yet'}

Give me a level {hint_level} hint.""",
        },
    ]
    
    response = await chat_completion(messages)
    return response
