"""
AI-Generated Editorials — Detailed explanations for every problem.
Generates step-by-step approach, code in multiple languages, and complexity analysis.
"""
from app.services.ai import chat_completion, parse_json


async def generate_editorial(question):
    """Generate a comprehensive editorial for a coding problem."""
    title = question.get("question_title", "Unknown")
    statement = question.get("statement", "")
    difficulty = question.get("difficulty", "medium")
    topics = question.get("topics", [])
    examples = question.get("examples", [])
    constraints = question.get("constraints", [])

    examples_text = "\n".join([
        f"Example {i+1}: Input: {e.get('input', 'N/A')}, Output: {e.get('output', 'N/A')}"
        for i, e in enumerate(examples[:3])
    ])

    prompt = f"""You are an expert coding instructor writing a detailed editorial for a coding problem.

Problem: {title}
Difficulty: {difficulty}
Topics: {', '.join(topics)}
Statement: {statement}

Examples:
{examples_text}

Constraints: {', '.join(constraints[:3]) if constraints else 'N/A'}

Write a comprehensive editorial in this EXACT JSON format:
{{
  "title": "{title}",
  "difficulty": "{difficulty}",
  "introduction": "2-3 sentences explaining what the problem asks and why it's important",
  "approach_1": {{
    "name": "Brute Force",
    "intuition": "Why this approach works (2-3 sentences)",
    "algorithm": "Step-by-step algorithm (numbered list)",
    "code": {{
      "python": "# Complete Python code",
      "java": "// Complete Java code",
      "cpp": "// Complete C++ code"
    }},
    "time_complexity": "O(n²)",
    "space_complexity": "O(1)",
    "explanation": "Detailed explanation of the code (3-4 sentences)"
  }},
  "approach_2": {{
    "name": "Optimal Solution",
    "intuition": "The key insight that makes this optimal",
    "algorithm": "Step-by-step algorithm",
    "code": {{
      "python": "# Complete Python code",
      "java": "// Complete Java code",
      "cpp": "// Complete C++ code"
    }},
    "time_complexity": "O(n)",
    "space_complexity": "O(n)",
    "explanation": "Detailed explanation"
  }},
  "key_insights": [
    "Important insight 1",
    "Important insight 2",
    "Important insight 3"
  ],
  "common_mistakes": [
    "Mistake 1 and how to avoid it",
    "Mistake 2 and how to avoid it"
  ],
  "similar_problems": [
    "Problem 1 (link if possible)",
    "Problem 2",
    "Problem 3"
  ],
  "interview_tips": [
    "Tip 1 for interviews",
    "Tip 2 for interviews"
  ],
  "visual_explanation": "Text-based visualization of the algorithm (e.g., array states, tree traversal)"
}}

Be thorough but concise. Code should be complete and runnable."""

    try:
        result = await chat_completion(
            messages=[{"role": "user", "content": prompt}],
            use_cache=True,
            max_tokens=3000,
        )
        editorial = parse_json(result)
        editorial["generated"] = True
        return editorial
    except Exception as e:
        return {
            "title": title,
            "difficulty": difficulty,
            "introduction": f"This problem tests your understanding of {', '.join(topics)}.",
            "approach_1": {
                "name": "Brute Force",
                "intuition": "Try all possible combinations",
                "algorithm": ["Iterate through all elements", "Check each combination", "Return the result"],
                "code": {"python": "# Code not available", "java": "// Code not available", "cpp": "// Code not available"},
                "time_complexity": "O(n²)",
                "space_complexity": "O(1)",
                "explanation": "The brute force approach checks all possibilities."
            },
            "approach_2": {
                "name": "Optimized",
                "intuition": "Use a more efficient data structure or algorithm",
                "algorithm": ["Use appropriate data structure", "Process elements efficiently", "Return result"],
                "code": {"python": "# Code not available", "java": "// Code not available", "cpp": "// Code not available"},
                "time_complexity": "O(n)",
                "space_complexity": "O(n)",
                "explanation": "The optimized approach reduces time complexity."
            },
            "key_insights": ["Think about the problem constraints", "Consider edge cases"],
            "common_mistakes": ["Off-by-one errors", "Not handling empty inputs"],
            "similar_problems": [],
            "interview_tips": ["Explain your approach before coding", "Test with edge cases"],
            "generated": False,
            "error": str(e),
        }


async def generate_editorial_batch(questions):
    """Generate editorials for multiple questions."""
    editorials = {}
    for q in questions:
        qid = str(q.get("_id", ""))
        editorial = await generate_editorial(q)
        editorials[qid] = editorial
    return editorials
