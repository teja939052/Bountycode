from typing import List, Dict, Optional
from app.services.ai import chat_completion, parse_json


async def generate_follow_up_question(
    original_question: str,
    user_answer: str,
    job_role: str,
    conversation_history: List[Dict],
) -> Dict:
    """Generate a dynamic follow-up question based on user's answer."""
    
    history_text = "\n".join([
        f"Q: {h.get('question', '')}\nA: {h.get('answer', '')}"
        for h in conversation_history[-3:]  # Last 3 exchanges
    ])
    
    messages = [
        {
            "role": "system",
            "content": f"""You are an expert interviewer conducting a {job_role} interview.

Based on the candidate's previous answer, generate a smart follow-up question that:
1. Digs deeper into their response
2. Challenges their reasoning
3. Tests their problem-solving ability
4. Reveals their thought process

The follow-up should feel natural and conversational, not scripted.

Return ONLY valid JSON:
{{
    "follow_up_question": "The follow-up question",
    "purpose": "What you're trying to evaluate",
    "difficulty": "easy/medium/hard",
    "expected_answer_type": "What kind of answer you're looking for",
    "red_flags": ["What would indicate a weak answer"]
}}""",
        },
        {
            "role": "user",
            "content": f"""Original Question: {original_question}

Candidate's Answer: {user_answer}

Previous Conversation:
{history_text}

Generate a smart follow-up question based on their answer.""",
        },
    ]
    
    response = await chat_completion(messages)
    return parse_json(response)


async def generate_model_answer(
    question: str,
    job_role: str,
    difficulty: str = "medium",
) -> Dict:
    """Generate a model answer for comparison."""
    
    messages = [
        {
            "role": "system",
            "content": f"""You are a top candidate interviewing for a {job_role} position.

Provide a model answer that demonstrates:
1. Clear structure (STAR method for behavioral, clean logic for technical)
2. Specific examples and metrics
3. Depth of knowledge
4. Communication clarity

Return ONLY valid JSON:
{{
    "model_answer": "The ideal answer",
    "key_points": ["point 1", "point 2", "point 3"],
    "what_makes_it_great": "Why this answer stands out",
    "common_mistakes": ["mistake 1", "mistake 2"]
}}""",
        },
        {
            "role": "user",
            "content": f"Provide a model answer for this {difficulty} level question: {question}",
        },
    ]
    
    response = await chat_completion(messages)
    return parse_json(response)


async def analyze_communication_style(
    answer: str,
) -> Dict:
    """Analyze communication style and provide feedback."""
    
    # Simple heuristics
    word_count = len(answer.split())
    sentences = answer.split(".")
    sentence_count = len([s for s in sentences if s.strip()])
    
    # Filler words
    filler_words = ["um", "uh", "like", "you know", "basically", "actually", "literally"]
    filler_count = sum(1 for word in filler_words if word in answer.lower())
    
    # Check for structure
    has_structure = any(marker in answer.lower() for marker in ["first", "second", "third", "finally", "additionally"])
    
    # Check for examples
    has_examples = any(marker in answer.lower() for marker in ["for example", "such as", "specifically", "instance"])
    
    # Check for metrics
    import re
    has_metrics = bool(re.search(r'\d+[%x$]|\d+ (percent|times|users|customers|team)', answer.lower()))
    
    # Score
    score = 50  # Base
    if word_count >= 50:
        score += 10  # Detailed
    if sentence_count >= 3:
        score += 10  # Well-structured
    if has_structure:
        score += 10
    if has_examples:
        score += 10
    if has_metrics:
        score += 10
    if filler_count <= 2:
        score += 5
    if word_count > 200:
        score -= 5  # Too verbose
    
    feedback = []
    if filler_count > 3:
        feedback.append(f"Reduce filler words (found {filler_count}: um, uh, like)")
    if not has_structure:
        feedback.append("Use numbered points or transition words for clarity")
    if not has_examples:
        feedback.append("Add specific examples to strengthen your answer")
    if not has_metrics:
        feedback.append("Include quantifiable results (numbers, percentages)")
    if word_count < 30:
        feedback.append("Provide more detail - aim for 50-150 words per answer")
    
    return {
        "score": min(100, score),
        "word_count": word_count,
        "sentence_count": sentence_count,
        "filler_words": filler_count,
        "has_structure": has_structure,
        "has_examples": has_examples,
        "has_metrics": has_metrics,
        "feedback": feedback,
        "communication_grade": "A" if score >= 85 else "B" if score >= 70 else "C" if score >= 55 else "D",
    }


async def generate_dynamic_difficulty(
    current_level: str,
    recent_scores: List[float],
    questions_answered: int,
) -> str:
    """Dynamically adjust difficulty based on performance."""
    
    if not recent_scores:
        return current_level
    
    avg_score = sum(recent_scores) / len(recent_scores)
    recent_trend = recent_scores[-1] - recent_scores[0] if len(recent_scores) > 1 else 0
    
    # Level up conditions
    if avg_score >= 8 and questions_answered >= 3:
        if current_level == "easy":
            return "medium"
        elif current_level == "medium":
            return "hard"
    
    # Level down conditions
    if avg_score < 5 or recent_trend < -2:
        if current_level == "hard":
            return "medium"
        elif current_level == "medium":
            return "easy"
    
    return current_level
