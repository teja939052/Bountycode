"""
AI Mock Debugger — Step-by-step code execution trace and feedback.
When a submission fails, AI walks through the code and identifies the error.
"""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Optional
from app.middleware.auth import get_current_user
from app.services.ai_core import chat_completion, parse_json
from app.services.code_executor import CodeExecutionEngine
from app.services.usage import require_pro_for_ai, plan_required

router = APIRouter(prefix="/api/v1/ai-debugger", tags=["ai-debugger"])
engine = CodeExecutionEngine()


@router.post("/analyze")
async def analyze_failed_submission(
    question_id: str,
    code: str,
    language: str,
    failed_test_case: Optional[dict] = None,
    user=Depends(require_pro_for_ai),
):
    """Analyze a failed code submission and provide step-by-step debugging help."""
    # Question content comes from the in-memory canonical store only
    # (Residency Rule, AGENTS.md): never MongoDB.
    from app.services import question_store
    question = question_store.get_question_for_serving(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Get the failed test case details
    test_case_info = ""
    if failed_test_case:
        test_case_info = f"""
Failed Test Case:
Input: {failed_test_case.get('input', 'N/A')}
Expected Output: {failed_test_case.get('expected', 'N/A')}
Your Output: {failed_test_case.get('actual', 'N/A')}
"""
    else:
        # Try to find a failing test case from visible test cases
        visible_cases = question.get("visible_test_cases", [])
        for case in visible_cases[:2]:
            result = await engine.execute_code(code, language, case.get("input", ""), timeout=5)
            if result["success"]:
                actual = result["stdout"].strip()
                expected = case.get("expected", "").strip()
                if actual != expected:
                    test_case_info = f"""
Failed Test Case:
Input: {case.get('input', 'N/A')}
Expected Output: {expected}
Your Output: {actual}
"""
                    break

    # Build AI prompt for debugging
    prompt = f"""You are an expert coding interviewer and debugger. A student submitted this code but it failed.

Problem: {question.get('question_title', 'Unknown')}
Statement: {question.get('statement', 'N/A')}

Student's Code ({language}):
```
{code}
```
{test_case_info}

Provide a detailed debugging analysis in this EXACT JSON format:
{{
  "error_type": "syntax|logic|runtime|timeout|edge_case",
  "error_line": <line number if identifiable, or null>,
  "error_explanation": "What exactly is wrong and why",
  "step_by_step_trace": [
    {{"step": 1, "line": <line>, "action": "What this line does", "state": "Variable values at this point"}},
    {{"step": 2, "line": <line>, "action": "What this line does", "state": "Variable values at this point"}}
  ],
  "root_cause": "The fundamental reason the code fails",
  "fix_suggestion": "Specific code change needed",
  "corrected_code": "<full corrected code if possible>",
  "tips": ["tip1", "tip2"],
  "similar_concepts": ["concept1", "concept2"]
}}

Be specific about line numbers and variable values. Think step by step through the failed test case."""

    try:
        result = await chat_completion(
            messages=[{"role": "user", "content": prompt}],
            use_cache=True,
            max_tokens=2000,
        )
        analysis = parse_json(result)
    except Exception as e:
        analysis = {
            "error_type": "unknown",
            "error_line": None,
            "error_explanation": "Unable to analyze the code at this time. Please try again.",
            "step_by_step_trace": [],
            "root_cause": "Analysis failed",
            "fix_suggestion": "Check your code logic carefully",
            "corrected_code": None,
            "tips": ["Try printing intermediate values", "Check edge cases"],
            "similar_concepts": [],
        }

    return {
        "question_id": question_id,
        "analysis": analysis,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


@router.post("/creative-coach")
async def creative_coach(
    request: Request,
    user=Depends(require_pro_for_ai),
):
    """Creative coach for free-form compiler work (no bank question needed).

    Modes: mentor (direct coaching), story (analogy-driven), boss (adversarial
    edge-case pressure). Returns the {title, mission, analogy, first_move,
    pitfalls, next_steps} shape the Compiler creative tab renders.
    """
    body = await request.json() if request.headers.get("content-type", "").startswith("application/json") else {}
    problem_description = str(body.get("problemDescription") or body.get("problem_description") or "")[:4000]
    code = str(body.get("code") or "")[:12000]
    language = str(body.get("language") or "python")[:32]
    topic = str(body.get("topic") or "")[:200]
    mode = str(body.get("mode") or "mentor").lower()
    if mode not in ("mentor", "story", "boss"):
        mode = "mentor"

    mode_brief = {
        "mentor": "Coach directly: name the single most important insight, then the concrete first code move.",
        "story": "Teach through one vivid real-world analogy that maps 1:1 onto the algorithm's moving parts.",
        "boss": "Act as an adversarial examiner: lead with the nastiest edge cases and where this code would break.",
    }[mode]

    prompt = f"""You are a creative coding coach. {mode_brief}

Problem: {problem_description or 'Free-form practice (no statement provided).'}
Topic: {topic or 'general problem solving'}
Language: {language}
Student's current code:
```
{code or '(no code yet)'}
```

Reply in this EXACT JSON format, no other text:
{{
  "title": "Short punchy session title (<= 6 words)",
  "mission": "One sentence: what to achieve in this session",
  "analogy": "A vivid analogy for the core idea (2-3 sentences)",
  "first_move": "The single concrete next code change to make",
  "micro_challenge": "One tiny exercise that proves the core idea (one sentence)",
  "edge_case_watch": "The single nastiest input to test against (one sentence)",
  "pep_talk": "One encouraging sentence, specific to this problem",
  "pitfalls": ["2-3 traps to avoid"],
  "next_steps": ["2-3 ordered follow-up moves"]
}}"""

    try:
        result = await chat_completion(
            messages=[{"role": "user", "content": prompt}],
            use_cache=True,
            max_tokens=800,
        )
        coaching = parse_json(result)
        if not isinstance(coaching, dict) or not coaching.get("mission"):
            raise ValueError("unparseable coach response")
    except Exception:
        coaching = {
            "title": "Creative Mind",
            "mission": "Break the problem into one tiny verifiable step, then build from there.",
            "analogy": "Think of the algorithm as an assembly line: each station does one simple job on every item that passes through.",
            "first_move": "Write a brute-force version that passes the smallest sample input, then optimize.",
            "micro_challenge": "Solve it by hand for 3 elements before writing any code.",
            "edge_case_watch": "Empty input and a single element — handle those first.",
            "pep_talk": "Every expert was once stuck on exactly this step. One small passing test changes everything.",
            "pitfalls": ["Optimizing before anything runs", "Ignoring empty/single-element inputs"],
            "next_steps": ["Get one sample passing", "Add one edge case", "Estimate time complexity"],
        }

    coaching["mode"] = mode
    coaching["generated_at"] = datetime.now(timezone.utc).isoformat()
    return coaching


@router.post("/hint")
async def get_progressive_hint(
    question_id: str,
    hint_level: int = 1,
    code: Optional[str] = None,
    user=Depends(require_pro_for_ai),
):
    """Get a progressive hint for a problem (3 levels: nudge → approach → solution)."""
    # Question content comes from the in-memory canonical store only
    # (Residency Rule, AGENTS.md): never MongoDB.
    from app.services import question_store
    question = question_store.get_question_for_serving(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    hints = question.get("hints", [])

    # Level 1: Nudge (don't give away the approach)
    # Level 2: Approach (explain the algorithm)
    # Level 3: Detailed solution hint

    if hint_level == 1:
        hint_text = hints[0] if hints else "Think about the time complexity. Can you do better than O(n²)?"
        hint_title = "Nudge"
    elif hint_level == 2:
        hint_text = hints[1] if len(hints) > 1 else "Consider using a hash map to store values you've seen."
        hint_title = "Approach"
    else:
        hint_text = hints[2] if len(hints) > 2 else hints[-1] if hints else "The optimal solution uses a single pass with a hash map."
        hint_title = "Solution Direction"

    # If user provided code, give personalized hint
    if code:
        prompt = f"""A student is stuck on this problem and submitted this code:

Problem: {question.get('question_title')}
Statement: {question.get('statement')}

Their Code:
```
{code}
```

Give them a HINT (not the solution) at level {hint_level}:
- Level 1: A gentle nudge about what to consider
- Level 2: The approach/algorithm to use
- Level 3: Specific implementation details

Current hint level: {hint_level}
Hint: {hint_text}

Respond with JSON:
{{
  "hint": "<personalized hint based on their code>",
  "what_to_consider": "<what they should think about>",
  "common_mistake": "<what most students get wrong>"
}}"""

        try:
            result = await chat_completion(
                messages=[{"role": "user", "content": prompt}],
                use_cache=True,
                max_tokens=500,
            )
            personalized = parse_json(result)
            hint_text = personalized.get("hint", hint_text)
        except Exception:
            pass

    return {
        "question_id": question_id,
        "hint_level": hint_level,
        "hint_title": hint_title,
        "hint": hint_text,
        "next_level_available": hint_level < 3,
    }


@router.post("/explain-error")
async def explain_error(
    error_message: str,
    code: str,
    language: str,
    user=Depends(require_pro_for_ai),
):
    """Explain a specific error message in student-friendly language."""
    prompt = f"""A student encountered this error while coding:

Error: {error_message}

Their Code ({language}):
```
{code}
```

Explain this error in simple, student-friendly language:
1. What the error means
2. Why it happened
3. How to fix it
4. How to prevent it in the future

Respond with JSON:
{{
  "explanation": "<simple explanation>",
  "why_it_happened": "<root cause>",
  "how_to_fix": "<specific fix>",
  "prevention_tips": ["tip1", "tip2"],
  "related_concepts": ["concept1", "concept2"]
}}"""

    try:
        result = await chat_completion(
            messages=[{"role": "user", "content": prompt}],
            use_cache=True,
            max_tokens=500,
        )
        explanation = parse_json(result)
    except Exception:
        explanation = {
            "explanation": "An error occurred while executing your code.",
            "why_it_happened": "Could not analyze the error automatically.",
            "how_to_fix": "Please check your code carefully.",
            "prevention_tips": ["Test with edge cases", "Add input validation"],
            "related_concepts": [],
        }

    return explanation


@router.post("/step-by-step")
async def step_by_step_trace(
    question_id: str,
    code: str,
    language: str,
    test_case_input: str,
    user=Depends(require_pro_for_ai),
):
    """Generate a step-by-step execution trace for a failed submission."""
    # Question content comes from the in-memory canonical store only
    # (Residency Rule, AGENTS.md): never MongoDB.
    from app.services import question_store
    question = question_store.get_question_for_serving(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    title = question.get("question_title", "Unknown")
    statement = question.get("statement", "")

    prompt = f"""You are an expert code debugger. Generate a step-by-step execution trace for this code.

Problem: {title}
Statement: {statement}

Code ({language}):
```
{code}
```

Input: {test_case_input}

Generate a detailed step-by-step trace showing variable states at each line. Format as JSON:
{{
  "steps": [
    {{
      "step_number": 1,
      "line": <line number>,
      "code_line": "the actual line of code",
      "action": "what this line does",
      "variables": {{"var1": "value1", "var2": "value2"}},
      "output_so_far": "any output generated so far",
      "explanation": "why this step matters"
    }}
  ],
  "error_found": {{
    "line": <line number where error occurs>,
    "type": "logic|runtime|off-by-one|wrong-approach",
    "explanation": "what went wrong",
    "fix": "how to fix it"
  }} or null if no error found,
  "final_output": "the output when code finishes",
  "suggestion": "overall improvement suggestion"
}}

Be specific about variable values and line numbers. Walk through the code exactly as it would execute."""

    try:
        result = await chat_completion(
            messages=[{"role": "user", "content": prompt}],
            use_cache=False,
            max_tokens=2000,
        )
        trace = parse_json(result)
    except Exception:
        trace = {
            "steps": [],
            "error_found": None,
            "final_output": "Trace generation failed",
            "suggestion": "Please try again or check your code manually."
        }

    return trace


@router.post("/suggest-fix")
async def suggest_fix(
    question_id: str,
    code: str,
    language: str,
    error_description: str,
    user=Depends(require_pro_for_ai),
):
    """AI suggests specific fixes for the code."""
    # Question content comes from the in-memory canonical store only
    # (Residency Rule, AGENTS.md): never MongoDB.
    from app.services import question_store
    question = question_store.get_question_for_serving(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    title = question.get("question_title", "Unknown")
    statement = question.get("statement", "")
    solution = question.get("solution", {})
    approach = solution.get("approach", "")

    prompt = f"""You are an expert coding tutor. A student is stuck on this problem and needs help.

Problem: {title}
Statement: {statement}
Correct Approach: {approach}

Student's Code ({language}):
```
{code}
```

Error/Issue: {error_description}

Provide specific, actionable fixes. Format as JSON:
{{
  "issues_found": [
    {{
      "line": <line number>,
      "issue": "what's wrong",
      "severity": "critical|warning|minor",
      "fix": "exact code change needed"
    }}
  ],
  "corrected_code": "<full corrected code>",
  "explanation": "why these changes work",
  "learning_points": ["concept1 to review", "concept2 to practice"],
  "similar_problems_to_practice": ["problem name 1", "problem name 2"]
}}

Be specific and provide exact code fixes, not vague suggestions."""

    try:
        result = await chat_completion(
            messages=[{"role": "user", "content": prompt}],
            use_cache=False,
            max_tokens=2000,
        )
        suggestion = parse_json(result)
    except Exception:
        suggestion = {
            "issues_found": [],
            "corrected_code": None,
            "explanation": "Could not generate fix suggestion. Please try again.",
            "learning_points": [],
            "similar_problems_to_practice": [],
        }

    return suggestion


@router.post("/rubber-duck")
async def rubber_duck_debug(
    question_id: str,
    code: str,
    language: str,
    user_thoughts: str,
    user=Depends(require_pro_for_ai),
):
    """Rubber duck debugging — AI helps you think through your approach."""
    # Question content comes from the in-memory canonical store only
    # (Residency Rule, AGENTS.md): never MongoDB.
    from app.services import question_store
    question = question_store.get_question_for_serving(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    title = question.get("question_title", "Unknown")
    statement = question.get("statement", "")

    prompt = f"""You are a friendly coding tutor helping a student debug their code using the rubber duck method.

Problem: {title}
Statement: {statement}

Student's Code ({language}):
```
{code}
```

Student's Thoughts: {user_thoughts}

Ask the student guiding questions to help them find the issue themselves. Don't give the answer directly — help them discover it.

Respond with JSON:
{{
  "response": "Your encouraging response to the student",
  "guiding_questions": [
    "question 1 to help them think",
    "question 2 to guide them",
    "question 3 to check understanding"
  ],
  "hint_level": 1,
  "encouragement": "A supportive message"
}}

Be encouraging and patient. Help them learn, not just solve."""

    try:
        result = await chat_completion(
            messages=[{"role": "user", "content": prompt}],
            use_cache=False,
            max_tokens=800,
        )
        response = parse_json(result)
    except Exception:
        response = {
            "response": "I'm here to help! Can you walk me through your thinking?",
            "guiding_questions": ["What does your code do step by step?", "Where do you think the issue might be?"],
            "hint_level": 1,
            "encouragement": "You're on the right track! Keep thinking through it."
        }

    return response
