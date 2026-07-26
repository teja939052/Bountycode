from typing import List, Dict
from app.services.ai import chat_completion, parse_json


async def evaluate_star_answer(
    question: str,
    answer: str,
    company: str = "",
    leadership_principles: List[str] = None,
) -> Dict:
    """Evaluate a behavioral answer using the STAR method."""
    principles_text = ""
    if leadership_principles:
        principles_text = f"\n\nEvaluate against these leadership principles: {', '.join(leadership_principles)}"
    
    messages = [
        {
            "role": "system",
            "content": f"""You are an expert behavioral interviewer who evaluates answers using the STAR method.

STAR stands for:
- Situation: What was the context?
- Task: What was your responsibility?
- Action: What specific actions did you take?
- Result: What was the outcome (with metrics)?

Evaluate the candidate's answer on each STAR component:
1. Was the situation clearly described?
2. Was the task clearly defined?
3. Were the actions specific and detailed?
4. Was the result quantified and impactful?

Also evaluate:
- Relevance to the question
- Communication clarity
- Depth of experience shown
{principles_text}

Return ONLY valid JSON:
{{
    "star_breakdown": {{
        "situation": {{"score": 7, "feedback": "specific feedback", "what_was_missing": "what could be improved"}},
        "task": {{"score": 8, "feedback": "specific feedback", "what_was_missing": "what could be improved"}},
        "action": {{"score": 6, "feedback": "specific feedback", "what_was_missing": "what could be improved"}},
        "result": {{"score": 5, "feedback": "specific feedback", "what_was_missing": "what could be improved"}}
    }},
    "overall_score": 6.5,
    "strengths": ["strength 1", "strength 2"],
    "improvements": ["improvement 1", "improvement 2"],
    "better_answer_structure": {{
        "situation": "How to better describe the situation",
        "task": "How to better describe the task",
        "action": "How to better describe the actions",
        "result": "How to better describe the result"
    }},
    "red_flags": ["flag 1", "flag 2"],
    "communication_grade": "B+"
}}""",
        },
        {
            "role": "user",
            "content": f"""Question: {question}

Candidate's Answer: {answer}

Company: {company or 'General'}
{principles_text}

Evaluate this behavioral answer using STAR method.""",
        },
    ]
    
    response = await chat_completion(messages)
    return parse_json(response)


async def generate_star_answer_template(
    question: str,
    company: str = "",
    role: str = "",
) -> Dict:
    """Generate a template for structuring a STAR answer."""
    messages = [
        {
            "role": "system",
            "content": f"""You are an interview coach helping a candidate structure their behavioral answer.

Generate a STAR template that:
1. Provides a framework they can fill in with their own experience
2. Shows what a strong answer looks like for this type of question
3. Includes guiding questions for each STAR component
4. Is tailored to the {company or 'general'} interview style

Return ONLY valid JSON:
{{
    "question": "{question}",
    "star_template": {{
        "situation": {{
            "guiding_questions": ["What was the context?", "When did this happen?"],
            "example_structure": "In my role at [Company], we were facing [Challenge]...",
            "tips": "Be specific but concise"
        }},
        "task": {{
            "guiding_questions": ["What was your specific responsibility?", "What were you accountable for?"],
            "example_structure": "I was responsible for [Specific Task]...",
            "tips": "Show ownership"
        }},
        "action": {{
            "guiding_questions": ["What specific steps did you take?", "What was your approach?"],
            "example_structure": "I decided to [Action 1], then [Action 2]...",
            "tips": "Use 'I' not 'we', be detailed"
        }},
        "result": {{
            "guiding_questions": ["What was the outcome?", "How did you measure success?"],
            "example_structure": "As a result, [Metric] improved by [X]%...",
            "tips": "Quantify everything possible"
        }}
    }},
    "sample_answer": "A complete sample answer using this template",
    "common_mistakes": ["mistake 1", "mistake 2"],
    "what_interviewer_looks_for": "What the interviewer is evaluating"
}}""",
        },
        {
            "role": "user",
            "content": f"Generate a STAR answer template for: {question}\n\nCompany: {company or 'General'}\nRole: {role or 'General'}",
        },
    ]
    
    response = await chat_completion(messages)
    return parse_json(response)


async def generate_practice_questions(
    company: str,
    role: str,
    count: int = 5,
) -> List[Dict]:
    """Generate company-specific behavioral practice questions."""
    messages = [
        {
            "role": "system",
            "content": f"""You are an expert interviewer who creates behavioral questions for {company} interviews.

Generate {count} behavioral questions that:
1. Are commonly asked at {company}
2. Test different leadership principles/competencies
3. Vary in difficulty
4. Cover different scenarios (conflict, leadership, failure, success, teamwork)

Return ONLY valid JSON:
{{
    "questions": [
        {{
            "question": "Tell me about a time when...",
            "category": "leadership/conflict/failure/success/teamwork",
            "difficulty": "easy/medium/hard",
            "what_we_evaluate": "What the interviewer is looking for",
            "star_focus": "Which STAR component is most important",
            "tips": "How to approach this question"
        }}
    ]
}}""",
        },
        {
            "role": "user",
            "content": f"Generate {count} behavioral interview questions for a {role} position at {company}.",
        },
    ]
    
    response = await chat_completion(messages)
    parsed = parse_json(response)
    return parsed.get("questions", [])
