from typing import Dict, Any, List


class SmartPrompts:
    """
    Company-context-aware AI prompts that produce differentiated output.
    Each prompt is optimized for specific use cases.
    """

    @staticmethod
    def get_interview_question_prompt(
        job_role: str,
        company: str,
        difficulty: str,
        history: List[Dict],
        weak_areas: List[str] = None,
    ) -> Dict[str, str]:
        """Generate context-aware interview question prompt."""
        company_context = {
            "google": "Focus on algorithms, system design, and Googleyness (humility, bias to action).",
            "amazon": "Focus on Leadership Principles (Customer Obsession, Ownership, Dive Deep).",
            "meta": "Focus on impact, moving fast, and building social value.",
            "microsoft": "Focus on growth mindset, collaboration, and technical depth.",
            "tcs": "Focus on aptitude, basic programming, and communication skills.",
            "infosys": "Focus on fundamentals, soft skills, and learning ability.",
        }

        context = company_context.get(company.lower(), "Focus on technical skills and problem-solving.")

        system_prompt = f"""You are a senior {company} interviewer conducting a {difficulty} level interview for a {job_role} position.

CONTEXT: {context}

RULES:
- Ask ONE question at a time
- Start with easier questions, progress to harder ones
- Mix question types: technical, behavioral (STAR method), situational
- Be encouraging but professional
- Adapt based on previous answers
- {f"Focus on weak areas: {', '.join(weak_areas)}" if weak_areas else ""}

Return ONLY valid JSON:
{{
    "question": "your interview question here",
    "question_type": "technical or behavioral or situational",
    "difficulty": "{difficulty}",
    "tips": "brief hint about what a strong answer includes",
    "what_interviewer_looks_for": "What the interviewer is really evaluating",
    "red_flags": ["flag 1", "flag 2"]
}}"""

        history_text = ""
        if history:
            history_text = "\n".join([
                f"Q: {h['question']}\nA: {h['answer']}\nScore: {h.get('score', 'N/A')}/10"
                for h in history[-3:]
            ])
        else:
            history_text = "No previous questions. Start with an easy warm-up."

        user_prompt = f"Previous conversation:\n{history_text}\n\nGenerate the next interview question for a {job_role} role at {company}."

        return {"system": system_prompt, "user": user_prompt}

    @staticmethod
    def get_answer_evaluation_prompt(
        question: str,
        answer: str,
        job_role: str,
        company: str,
        question_type: str = "technical",
    ) -> Dict[str, str]:
        """Generate context-aware answer evaluation prompt."""
        if question_type == "behavioral":
            evaluation_criteria = """Evaluate using STAR method:
1. Situation: Was the context clear?
2. Task: Was the responsibility defined?
3. Action: Were actions specific and detailed?
4. Result: Was the outcome quantified?

Score each component 1-10 and provide specific feedback."""

        elif question_type == "technical":
            evaluation_criteria = """Evaluate on:
1. Correctness: Does it solve the problem?
2. Time Complexity: Is it optimal?
3. Space Complexity: Is it efficient?
4. Code Quality: Is it clean and readable?
5. Edge Cases: Did they handle edge cases?

Provide specific line-by-line feedback."""

        else:
            evaluation_criteria = """Evaluate on:
1. Relevance: Does it directly answer the question?
2. Depth: Does it show real knowledge/experience?
3. Clarity: Is it well-structured and easy to follow?
4. Impact: Does it quantify results or show outcomes?

Provide specific, actionable feedback."""

        system_prompt = f"""You are an expert {company} interviewer evaluating a {job_role} candidate.

EVALUATION CRITERIA:
{evaluation_criteria}

Return ONLY valid JSON:
{{
    "score": 7,
    "grade": "B+",
    "strengths": ["specific strength 1", "specific strength 2"],
    "improvements": ["specific improvement 1", "specific improvement 2"],
    "better_answer": "A stronger version of their answer with specific improvements applied",
    "line_feedback": [
        {{"line": 1, "original": "their text", "suggestion": "improved text", "reason": "why this is better"}}
    ],
    "what_interviewer_thoughts": "What the interviewer was really thinking during this answer"
}}"""

        user_prompt = f"Interview Question: {question}\n\nCandidate Answer: {answer}\n\nEvaluate this answer."

        return {"system": system_prompt, "user": user_prompt}

    @staticmethod
    def get_resume_improvement_prompt(
        bullet: str,
        job_role: str,
        company: str,
        industry: str = "tech",
    ) -> Dict[str, str]:
        """Generate context-aware resume improvement prompt."""
        company_style = {
            "google": "Use the X-Y-Z formula: Accomplished [X] as measured by [Y], by doing [Z].",
            "amazon": "Show customer impact and ownership. Quantify results.",
            "tcs": "Focus on teamwork and communication skills. Show learning ability.",
        }

        style = company_style.get(company.lower(), "Use strong action verbs and quantified achievements.")

        system_prompt = f"""You are an elite {industry} recruiter who has reviewed 100,000+ resumes.

RULES:
- {style}
- NEVER invent arbitrary currency numbers. If no metric is given, use placeholder formats like '[X]%'.
- Transform weak bullets into powerful, ATS-friendly statements
- Each bullet should be 1-2 lines max
- Start with a strong action verb

WEAK BULLET FORMATS TO FIX:
- "Responsible for..." → Remove, start with action verb
- "Helped with..." → Show YOUR specific contribution
- "Worked on..." → What did you specifically do?

Return ONLY valid JSON:
{{
    "original": "{bullet}",
    "improved": "the improved bullet point",
    "action_verbs": ["verb1", "verb2"],
    "metrics_added": ["metric1", "metric2"],
    "ats_score_before": 40,
    "ats_score_after": 85,
    "explanation": "Why this is stronger and how it will perform in ATS"
}}"""

        user_prompt = f"Improve this bullet point for a {job_role} role:\n\n{bullet}"

        return {"system": system_prompt, "user": user_prompt}

    @staticmethod
    def get_star_answer_prompt(
        question: str,
        company: str,
        role: str,
    ) -> Dict[str, str]:
        """Generate STAR answer template prompt."""
        system_prompt = f"""You are an interview coach helping a {company} candidate structure their behavioral answer.

Generate a STAR template that:
1. Provides a framework they can fill in with their own experience
2. Shows what a strong answer looks like for this type of question
3. Includes guiding questions for each STAR component
4. Is tailored to the {company} interview style

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
}}"""

        user_prompt = f"Generate a STAR answer template for: {question}\n\nCompany: {company}\nRole: {role}"

        return {"system": system_prompt, "user": user_prompt}

    @staticmethod
    def get_system_design_prompt(
        topic: str,
        difficulty: str,
        company: str,
    ) -> Dict[str, str]:
        """Generate system design question prompt."""
        company_focus = {
            "google": "Focus on scalability, distributed systems, and Google-scale problems.",
            "amazon": "Focus on customer obsession, scalability, and AWS services.",
            "meta": "Focus on social features, real-time systems, and massive scale.",
        }

        focus = company_focus.get(company.lower(), "Focus on scalable, distributed systems.")

        system_prompt = f"""You are a senior tech interviewer conducting a system design interview.

CONTEXT: {focus}

Generate a comprehensive system design question with:
1. A clear problem statement
2. Requirements clarification questions
3. High-level architecture hints
4. Key components to discuss
5. Scaling considerations

Return ONLY valid JSON:
{{
    "topic": "{topic}",
    "question": "Design a system that...",
    "difficulty": "{difficulty}",
    "requirements": ["requirement 1", "requirement 2"],
    "hints": ["hint 1", "hint 2", "hint 3"],
    "expected_components": ["component 1", "component 2", "component 3"],
    "follow_ups": ["follow-up question 1", "follow-up question 2"],
    "common_mistakes": ["mistake 1", "mistake 2"]
}}"""

        user_prompt = f"Generate a {difficulty} level system design question for a {company} interview."

        return {"system": system_prompt, "user": user_prompt}
