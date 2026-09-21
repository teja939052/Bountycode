"""Interview-specific AI prompts and functions."""

import json
import random
import logging
from typing import List, Dict, Any
from app.services.ai_core import chat_completion, parse_json, assign_companies

logger = logging.getLogger(__name__)

# How many questions per session are drawn from the curated bank before
# switching to LLM generation. Bank = cheaper + higher quality + company-specific.
FIRST_BANK_QUESTIONS = 3

# Difficulty-aware scoring: a correct answer on a hard question deserves more
# credit than the same score on an easy question. These multipliers normalize
# an answer's value against the difficulty it was asked at.
DIFFICULTY_WEIGHTS = {"easy": 0.9, "medium": 1.0, "hard": 1.1}

# Per-company + per-question-type rubric weights. Weights are what a given
# company actually scores candidates on (Google: algorithms; Amazon: STAR/LPs;
# TCS: communication + basics). Each dict sums to 1.0.
COMPANY_RUBRIC_WEIGHTS: Dict[str, Dict[str, Dict[str, float]]] = {
    "google": {
        "default": {"technical": 0.45, "problem_solving": 0.25, "depth": 0.20, "communication": 0.10},
        "behavioral": {"communication": 0.35, "depth": 0.30, "problem_solving": 0.20, "technical": 0.15},
        "coding": {"technical": 0.50, "problem_solving": 0.25, "depth": 0.15, "communication": 0.10},
    },
    "amazon": {
        "default": {"technical": 0.30, "problem_solving": 0.25, "communication": 0.25, "depth": 0.20},
        "behavioral": {"communication": 0.40, "depth": 0.30, "problem_solving": 0.15, "technical": 0.15},
        "coding": {"technical": 0.40, "problem_solving": 0.30, "depth": 0.15, "communication": 0.15},
    },
    "meta": {
        "default": {"technical": 0.35, "problem_solving": 0.30, "depth": 0.20, "communication": 0.15},
        "behavioral": {"communication": 0.35, "depth": 0.30, "problem_solving": 0.20, "technical": 0.15},
    },
    "microsoft": {
        "default": {"problem_solving": 0.30, "technical": 0.30, "depth": 0.20, "communication": 0.20},
    },
    "tcs": {
        "default": {"communication": 0.30, "technical": 0.30, "problem_solving": 0.25, "depth": 0.15},
    },
    "infosys": {
        "default": {"communication": 0.30, "technical": 0.30, "problem_solving": 0.25, "depth": 0.15},
    },
    "wipro": {
        "default": {"communication": 0.30, "technical": 0.30, "problem_solving": 0.25, "depth": 0.15},
    },
    "uber": {
        "default": {"technical": 0.40, "problem_solving": 0.30, "depth": 0.20, "communication": 0.10},
    },
}

# Default weights when a company has no specific rubric (fair split).
DEFAULT_RUBRIC_WEIGHTS = {"technical": 0.30, "problem_solving": 0.25, "depth": 0.20, "communication": 0.25}

# How much the heuristic communication-style analysis (filler words, structure,
# examples, metrics) blends into the communication dimension of the score.
COMMUNICATION_BLEND = 0.30

COMPANY_PROFILES = {
    "google": {
        "interview_style": "Google focuses on algorithms, data structures, and problem-solving. They value clean code, optimal solutions, and discussing trade-offs. Questions are medium-to-hard LeetCode style. Expect 2 coding rounds (45 min each), 1 system design, 1 behavioral.",
        "evaluation_rubric": "Evaluate: (1) Algorithm correctness and optimization, (2) Code cleanliness, (3) Communication while coding, (4) Edge cases, (5) Time/space complexity discussion.",
        "leadership_principles": [],
    },
    "amazon": {
        "interview_style": "Amazon is heavily behavioral (Leadership Principles) mixed with coding. Every answer should demonstrate LPs like Customer Obsession, Ownership, Bias for Action, Dive Deep. STAR method is critical.",
        "evaluation_rubric": "Evaluate: (1) STAR method completeness, (2) LP alignment, (3) Specificity and metrics, (4) Customer impact, (5) Ownership shown.",
        "leadership_principles": ["Customer Obsession", "Ownership", "Invent and Simplify", "Are Right A Lot", "Learn and Be Curious", "Hire and Develop the Best", "Insist on the Highest Standards", "Bias for Action", "Dive Deep", "Have Backbone; Disagree and Commit", "Deliver Results"],
    },
    "meta": {
        "interview_style": "Meta combines coding with product sense. They value Move Fast, impact, and building social value. Coding often has a product angle. 2 coding rounds + system design + behavioral.",
        "evaluation_rubric": "Evaluate: (1) Technical execution, (2) Product thinking, (3) Speed of execution, (4) Impact quantification, (5) Collaboration.",
        "leadership_principles": [],
    },
    "microsoft": {
        "interview_style": "Microsoft values growth mindset and collaboration. Coding is typically medium-hard. They care about how you think through problems, not just the solution. 3-4 rounds total.",
        "evaluation_rubric": "Evaluate: (1) Problem decomposition, (2) Code quality, (3) Testing mindset, (4) Collaboration signals, (5) Growth mindset demonstration.",
        "leadership_principles": [],
    },
    "tcs": {
        "interview_style": "TCS focuses on aptitude, programming basics, and communication. Questions are easier but they value clarity, confidence, and willingness to learn. Include basic coding and verbal ability.",
        "evaluation_rubric": "Evaluate: (1) Basic programming knowledge, (2) Communication clarity, (3) Aptitude and logical thinking, (4) Willingness to learn, (5) Confidence.",
        "leadership_principles": [],
    },
    "infosys": {
        "interview_style": "Infosys values learning ability, adaptability, and soft skills. They test aptitude, basic programming, and verbal ability. Questions are straightforward.",
        "evaluation_rubric": "Evaluate: (1) Learning aptitude, (2) Communication skills, (3) Basic technical knowledge, (4) Adaptability, (5) Problem-solving approach.",
        "leadership_principles": [],
    },
    "wipro": {
        "interview_style": "Wipro tests aptitude, basic coding, and communication skills. Similar to TCS/Infosys level. They value teamwork and adaptability.",
        "evaluation_rubric": "Evaluate: (1) Aptitude skills, (2) Basic programming, (3) Communication, (4) Team orientation, (5) Adaptability.",
        "leadership_principles": [],
    },
    "uber": {
        "interview_style": "Uber focuses on coding, system design, and problem-solving at scale. They value real-time systems thinking, marketplace dynamics, and efficient code.",
        "evaluation_rubric": "Evaluate: (1) Algorithmic thinking, (2) System design for real-time systems, (3) Code efficiency, (4) Edge case handling, (5) Scalability awareness.",
        "leadership_principles": [],
    },
}

# Interview modes (P3): Behavioral / Coding / System Design / HR / Technical.
# A mode constrains the generated question_type and injects mode-specific
# briefing + evaluation emphasis into the prompts. "mixed" (or unknown) keeps
# the legacy unconstrained behavior.
INTERVIEW_MODES: Dict[str, Dict[str, str]] = {
    "behavioral": {
        "question_type": "behavioral",
        "brief": "MODE: BEHAVIORAL. Ask a STAR-method behavioral question about past experience, teamwork, conflict, ownership, or leadership. Demand specific situations with measurable outcomes.",
        "eval": "Score STAR completeness ruthlessly: vague answers without Situation/Task/Action/Result and metrics cap at 5.",
        "followup": "Drill the weakest STAR element (usually Result/metrics or specificity of Action).",
    },
    "coding": {
        "question_type": "coding",
        "brief": "MODE: CODING. Ask a specific coding/algorithm problem with clear input/output, constraints, and at least one edge case worth discussing. Expect complexity analysis in follow-ups.",
        "eval": "Score algorithm correctness, efficiency, edge-case handling, and complexity awareness. Hand-wavy solutions cap at 5.",
        "followup": "Challenge with one edge case, one complexity/optimality probe, or one scaling variant of their approach.",
    },
    "system_design": {
        "question_type": "technical",
        "brief": "MODE: SYSTEM DESIGN. Ask a design question (e.g. URL shortener, rate limiter, feed, chat) requiring components, data flow, capacity reasoning, and explicit trade-offs. No pure-syntax questions.",
        "eval": "Score component correctness, capacity estimation, bottleneck identification, and trade-off depth. Buzzword-only answers cap at 5.",
        "followup": "Attack the bottleneck: 10x traffic, a component failure, or a consistency-vs-availability trade-off.",
    },
    "hr": {
        "question_type": "behavioral",
        "brief": "MODE: HR SCREEN. Ask about motivation, strengths/weaknesses, why this company/role, teamwork, and culture fit. Keep it conversational; probe self-awareness and honesty.",
        "eval": "Score self-awareness, specificity, company alignment, and honesty. Generic praise about the company caps at 5.",
        "followup": "Ask for a concrete example or a moment that proves the claim.",
    },
    "technical": {
        "question_type": "technical",
        "brief": "MODE: TECHNICAL. Ask a deep technical question on fundamentals (DSA, OS, DBMS, OOP, networks) demanding precise mechanisms, not definitions.",
        "eval": "Score depth of mechanism understanding and trade-off awareness. Definition-only answers cap at 5.",
        "followup": "Go one level deeper into the mechanism or ask for the trade-off of the alternative.",
    },
}


def _mode_cfg(mode: str) -> Dict[str, str]:
    return INTERVIEW_MODES.get((mode or "mixed").lower().strip(), {})


# Mode rubric floors: the interview mode guarantees its lead dimension a
# minimum voice in the company weights (renormalized to sum 1.0). This extends
# the COMPANY_RUBRIC_WEIGHTS resolution below — it is not a new rubric table.
_MODE_WEIGHT_FLOORS: Dict[str, Dict[str, float]] = {
    "behavioral": {"communication": 0.35},
    "hr": {"communication": 0.35},
    "coding": {"technical": 0.45},
    "system_design": {"depth": 0.30},
    "technical": {"technical": 0.35},
}


async def _get_student_context(user_id: str) -> str:
    """Build a compact, evidence-based summary of the student's actual learning
    and assessment history (skill graph, active repair missions, past interviews,
    recent OA outcomes) so interview questions are personalized to real student
    state — not a script. Tolerant of missing data; returns "" when empty."""
    try:
        from app.database import (
            skill_graph_collection,
            interviews_collection,
            repair_missions_collection,
            oa_sessions_collection,
        )
        parts: List[str] = []

        # 1) Skill graph: per-section scores + OA outcomes (already fed by the
        #    canonical OA readiness signal).
        gdoc = await skill_graph_collection.find_one({"user_id": user_id}) or {}
        cats = gdoc.get("categories", {})
        if cats:
            cat_lines = []
            for sec, data in list(cats.items())[:12]:
                score = data.get("score", 0) if isinstance(data, dict) else data
                cat_lines.append(f"  - {sec}: {score}/10")
            parts.append("Known skill levels:\n" + "\n".join(cat_lines))
        oa_outcomes = gdoc.get("oa_outcomes", [])
        if oa_outcomes:
            oa_lines = []
            for o in oa_outcomes[-3:]:
                weak = sorted(o.get("sections", {}), key=lambda k: o["sections"][k])[:3]
                oa_lines.append(
                    f"  - {o.get('company', '')}: overall {o.get('overall', 0):.0f}% "
                    f"| weakest sections: {', '.join(weak)}"
                )
            parts.append("Recent OA outcomes:\n" + "\n".join(oa_lines))

        # 2) Active repair missions = weaknesses the student is currently fixing.
        mission_rows = []
        async for doc in repair_missions_collection.find(
            {"user_id": user_id, "status": {"$in": ["pending", "in_progress"]}}
        ).sort("created_at", -1).limit(5):
            mission_rows.append(
                f"  - {doc.get('title', '')} [{doc.get('status')}] "
                f"(weaknesses: {', '.join(doc.get('weaknesses', [])[:4])})"
            )
        if mission_rows:
            parts.append("Active repair missions (specific weaknesses the student must now fix):\n" + "\n".join(mission_rows))

        # 3) Recent completed OAs (limit 3): real prior assessment performance + diagnosis.
        oa_session_rows = []
        cursor = oa_sessions_collection.find(
            {"user_id": user_id, "status": "completed"}
        ).sort("created_at", -1).limit(3)
        async for doc in cursor:
            result = doc.get("result", {}) or {}
            row = f"  - {doc.get('company', '')} OA: readiness {result.get('overall_readiness', 'n/a')}% ({result.get('verdict', '')})"
            weak = result.get("weak_areas", [])
            if weak:
                row += f" | weak: {', '.join(weak[:3])}"
            if result.get("diagnosis"):
                row += f" | diagnosis: {result.get('diagnosis')}"
            oa_session_rows.append(row)
        if oa_session_rows:
            parts.append("Recent completed assessments (past performance):\n" + "\n".join(oa_session_rows))

        # 4) Past interviews (limit 5): evidence of interview strengths/weaknesses.
        prev_interviews = []
        async for doc in interviews_collection.find(
            {"user_id": user_id}
        ).sort("created_at", -1).limit(5):
            prev_interviews.append(
                f"  - {doc.get('company', 'general')} / {doc.get('job_role', '')}: "
                f"score {doc.get('overall_score', 'n/a')}, "
                f"weaknesses: {', '.join(doc.get('weaknesses', [])[:3])}"
            )
        if prev_interviews:
            parts.append("Recent interview history (how the student performed in past interviews):\n" + "\n".join(prev_interviews))

        if not parts:
            return ""
        return "\n\n".join(parts)
    except Exception as e:
        logger.debug(f"Could not build student context: {e}")
        return ""


async def generate_interview_question(
    job_role: str,
    history: List[Dict[str, Any]],
    company: str = "general",
    difficulty: str = "medium",
    user_id: str = None,
    mode: str = "mixed",
    candidate_context: str = None,
) -> Dict[str, Any]:
    try:
        from app.data.interview_question_bank import get_questions_by_company
        asked_ids = {h.get("question_id", "") for h in history if h.get("question_id")}
        # Use the curated question bank for the first few questions (cheaper,
        # higher-quality, company-specific) instead of the LLM. After that we
        # generate dynamically so each session feels fresh.
        if len(history) < FIRST_BANK_QUESTIONS:
            pool = get_questions_by_company(company)
            if not pool:
                pool = get_questions_by_company("general")
            if pool:
                asked_questions = {
                    (h.get("question", "") or "").strip().lower()
                    for h in history if h.get("question")
                }
                available = [
                    q for q in pool
                    if (q.get("id", "") not in asked_ids)
                    and (q.get("question", "").strip().lower() not in asked_questions)
                ] or pool
                q = random.choice(available)
                return {
                    "question": q["question"],
                    "question_type": q.get("category", "behavioral"),
                    "tips": "Think carefully and structure your answer using a framework.",
                    "difficulty": q.get("difficulty", difficulty),
                    "company": company,
                    "follow_up_expected": q.get("category") == "technical",
                    "companies": assign_companies(),
                    "question_id": q.get("id", ""),
                }
    except Exception:
        pass

    company_key = company.lower()
    profile = COMPANY_PROFILES.get(company_key, None)

    company_context = ""
    if profile:
        company_context = f"""
The candidate is interviewing at {company.upper()}.
Interview style: {profile['interview_style']}
Evaluation rubric: {profile['evaluation_rubric']}
{'Leadership Principles to focus on: ' + ', '.join(profile['leadership_principles']) if profile['leadership_principles'] else ''}
"""

    history_text = ""
    if history:
        avg_score = sum(h.get("score", 5) for h in history) / len(history)
        last_types = [h.get("question_type", "technical") for h in history[-3:]]
        history_text = f"""
Previous questions and answers:
{json.dumps(history[-5:], indent=2)}
Average score so far: {avg_score:.1f}/10
Recent question types: {', '.join(last_types)}
Questions answered: {len(history)}
"""
        if avg_score >= 8 and difficulty == "medium":
            difficulty = "hard"
        elif avg_score >= 9 and difficulty == "easy":
            difficulty = "medium"
        elif avg_score < 4 and difficulty == "hard":
            difficulty = "medium"
        elif avg_score < 3 and difficulty == "medium":
            difficulty = "easy"
    else:
        history_text = "This is the first question. Start with an easier, introductory question."

    # Personalize from the student's real learning + assessment history so the
    # interview targets their actual weaknesses (evidence-driven, not generic).
    student_context = ""
    if user_id:
        student_context = await _get_student_context(user_id)

    identify_student_txt = "Use the provided student context to recognize this specific student's actual learning and assessment history (skill levels, active repair weaknesses, past OA/interview performance)." if student_context else ""

    mode_cfg = _mode_cfg(mode)
    mode_brief = mode_cfg.get("brief", "")
    candidate_block = (
        "CANDIDATE CONTEXT (resume/profile — ground questions in their real background; do NOT invent experience for them):\n" + candidate_context
        if candidate_context else ""
    )

    system_prompt = f"""You are an expert technical interviewer for {job_role} positions.
{company_context}
{identify_student_txt}
{mode_brief}
{candidate_block}
You must generate interview questions that are realistic, challenging, and appropriate for the target difficulty.
Questions should be deep enough to support a follow-up drilldown on edge cases, trade-offs, scaling, or measurable impact.

DIFFICULTY GUIDELINES:
- easy: Fundamentals, basic concepts, entry-level
- medium: Intermediate concepts, applied knowledge, mid-level
- hard: Advanced concepts, system-level thinking, senior-level

QUESTION TYPES (mix these):
- "technical": Data structures, algorithms, coding concepts, system knowledge
- "behavioral": STAR method questions, past experiences, team dynamics
- "situational": Hypothetical scenarios, "what would you do if..."
- "coding": Specific coding problems, algorithm design, debugging

{history_text}
{('STUDENT CONTEXT (personalize the next question to this student — target their weak areas and reinforce what they are currently repairing; do not repeat topics they already mastered):\n' + student_context) if student_context else ''}
 
Generate the NEXT question. Avoid repeating topics from history.
{company_context}
You must generate interview questions that are realistic, challenging, and appropriate for the target difficulty.
Questions should be deep enough to support a follow-up drilldown on edge cases, trade-offs, scaling, or measurable impact.

DIFFICULTY GUIDELINES:
- easy: Fundamentals, basic concepts, entry-level
- medium: Intermediate concepts, applied knowledge, mid-level
- hard: Advanced concepts, system-level thinking, senior-level

QUESTION TYPES (mix these):
- "technical": Data structures, algorithms, coding concepts, system knowledge
- "behavioral": STAR method questions, past experiences, team dynamics
- "situational": Hypothetical scenarios, "what would you do if..."
- "coding": Specific coding problems, algorithm design, debugging

{history_text}

Generate the NEXT question. Avoid repeating topics from history.
The output MUST be valid JSON with this exact structure:
{{
    "question": "The interview question text",
    "question_type": "technical|behavioral|situational|coding",
    "tips": "Brief hints or guidance for the candidate",
    "difficulty": "{difficulty}",
    "company": "{company}",
    "follow_up_expected": true or false
}}

Return ONLY the JSON object. No markdown, no explanation."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Generate the next interview question for a {job_role} position at {company}."},
    ]

    result = await chat_completion(messages)
    parsed = parse_json(result)

    # Mode constraint: the interview mode dictates the question type so a
    # "coding" interview never drifts into generic behavioral questions.
    if mode_cfg.get("question_type"):
        parsed["question_type"] = mode_cfg["question_type"]

    parsed.setdefault("question", "Tell me about yourself and your experience.")
    parsed.setdefault("question_type", "technical")
    parsed.setdefault("tips", "Be specific and provide concrete examples.")
    parsed.setdefault("difficulty", difficulty)
    parsed.setdefault("company", company)
    parsed.setdefault("follow_up_expected", True)
    if not parsed.get("companies"):
        parsed["companies"] = assign_companies()

    return parsed


async def evaluate_answer(
    question: str,
    answer: str,
    job_role: str,
    company: str = "general",
    question_type: str = "technical",
    difficulty: str = "medium",
    time_taken: int = None,
    mode: str = None,
) -> Dict[str, Any]:
    company_key = company.lower()
    profile = COMPANY_PROFILES.get(company_key, None)

    evaluation_context = ""
    if profile:
        evaluation_context = f"""
Company-specific evaluation rubric for {company.upper()}:
{profile['evaluation_rubric']}
Focus your evaluation on what this company specifically values.
"""

    type_guidance = ""
    if question_type == "behavioral":
        type_guidance = """
This is a BEHAVIORAL question. Evaluate using STAR method:
- Situation: Did they describe the context clearly?
- Task: Did they explain their specific responsibility?
- Action: Did they detail concrete actions they took?
- Result: Did they share measurable outcomes?
Penalize vague answers without specific examples or metrics.
"""
    elif question_type == "technical":
        type_guidance = """
This is a TECHNICAL question. Evaluate:
- Correctness of the technical approach
- Depth of understanding (not just surface-level)
- Awareness of trade-offs and alternatives
- Code quality and optimization (if applicable)
"""
    elif question_type == "coding":
        type_guidance = """
This is a CODING question. Evaluate:
- Algorithm correctness and efficiency
- Code structure and readability
- Edge case handling
- Time and space complexity awareness
"""
    elif question_type == "situational":
        type_guidance = """
This is a SITUATIONAL question. Evaluate:
- Logical reasoning and decision-making
- Awareness of stakeholders and impact
- Practicality of the proposed approach
- Communication clarity
"""

    difficulty_context = f"This question was asked at {difficulty} difficulty." if difficulty else ""

    time_context = ""
    if time_taken is not None and time_taken > 0:
        # A reasonable answer typically takes 45–180s. Very fast (<30s) usually
        # means shallow; very slow (>300s) means unsure. Reward deliberate but
        # efficient answers.
        time_context = (
            f"The candidate took {int(time_taken)} seconds to answer. "
            "A strong answer is usually 60-180s: complete but not rambling. "
            "Note extreme speed or slowness in your evaluation of depth and confidence."
        )

    system_prompt = f"""You are an expert interviewer evaluating a candidate for {job_role} positions.
{evaluation_context}
{type_guidance}
{("MODE-SPECIFIC SCORING (" + (mode or "").upper() + " interview): " + _mode_cfg(mode).get("eval", "") + " " + _mode_cfg(mode).get("followup", "")) if _mode_cfg(mode) else ""}
{difficulty_context}
{time_context}

You must evaluate the candidate's answer honestly and provide constructive feedback.

SCORING GUIDELINES:
- 1-3: Poor — major gaps, incorrect, or very vague
- 4-5: Below average — partially correct but missing key points
- 6-7: Average — solid answer with room for improvement
- 8-9: Good — strong answer with minor improvements possible
- 10: Excellent — exceptional, comprehensive, insightful

The output MUST be valid JSON with this exact structure:
{{
    "score": 7,
    "breakdown": {{
        "technical": 7,
        "communication": 6,
        "problem_solving": 8,
        "depth": 6
    }},
    "strengths": ["strength 1", "strength 2"],
    "improvements": ["improvement 1", "improvement 2"],
    "better_answer": "An example of what a stronger answer would look like...",
    "follow_up": "A sharp drilldown follow-up question targeting the weakest dimension of this answer (empty if the answer was complete)",
    "reaction": "fire|thumbsup|muscle|memo|thinking|clap"
}}

REACTION EMOJI GUIDE:
- "fire" (score 9-10): Exceptional answer
- "clap" (score 7-8): Strong answer, well done
- "muscle" (score 5-6): Decent effort, keep going
- "thinking" (score 3-4): Needs more thought
- "memo" (score 1-2): Study more on this topic

Return ONLY the JSON object. No markdown, no explanation."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Question: {question}\n\nCandidate Answer: {answer}\n\nEvaluate this answer."},
    ]

    result = await chat_completion(messages)
    parsed = parse_json(result)

    parsed.setdefault("score", 5)
    parsed["score"] = max(1, min(10, int(parsed["score"])))
    parsed.setdefault("breakdown", {"technical": 5, "communication": 5, "problem_solving": 5, "depth": 5})
    parsed.setdefault("strengths", ["Attempted the question"])
    parsed.setdefault("improvements", ["Provide more detail and examples"])
    parsed.setdefault("better_answer", "A stronger answer would include more specifics and metrics.")
    parsed.setdefault("follow_up", "")

    # Normalize the breakdown to 1-10
    for dim in ("technical", "communication", "problem_solving", "depth"):
        parsed["breakdown"][dim] = max(1, min(10, int(parsed["breakdown"].get(dim, 5))))

    # ── Difficulty-aware + rubric-weighted score ──
    # The breakdown dims are weighted by what THIS company values for THIS
    # question type, then multiplied by the difficulty multiplier so a hard
    # question 7 ranks above an easy 7. Final is clamped 1-10.
    weights = COMPANY_RUBRIC_WEIGHTS.get(
        company_key, {}
    ).get(question_type) or COMPANY_RUBRIC_WEIGHTS.get(company_key, {}).get("default") or DEFAULT_RUBRIC_WEIGHTS

    # Apply mode floors (renormalized) so the mode's lead dimension always
    # counts: a coding interview is technical-led even at a STAR-heavy company.
    floors = _MODE_WEIGHT_FLOORS.get((mode or "").lower().strip(), {})
    if floors:
        weights = dict(weights)
        for dim, floor in floors.items():
            if weights.get(dim, 0) < floor:
                weights[dim] = floor
        total_w = sum(weights.values()) or 1.0
        weights = {d: round(v / total_w, 3) for d, v in weights.items()}

    weighted = sum(parsed["breakdown"][dim] * weights.get(dim, 0.25) for dim in ("technical", "communication", "problem_solving", "depth"))
    difficulty_mult = DIFFICULTY_WEIGHTS.get(difficulty, 1.0)
    adjusted = max(1, min(10, round(weighted * difficulty_mult, 1)))

    # Blend: the raw LLM score + the rubric-weighted breakdown (60/40) so the
    # score reflects both holistic judgment and structured rubric.
    raw_llm = parsed["score"]
    blended = round(0.6 * raw_llm + 0.4 * adjusted, 1)
    parsed["score"] = max(1, min(10, round(blended)))
    parsed["raw_llm_score"] = raw_llm
    parsed["difficulty_multiplier"] = difficulty_mult
    parsed["rubric_weights"] = weights

    # ── Communication-style heuristic blend ──
    # Zero-LLM signal: filler words, structure, examples, metrics, length.
    try:
        from app.services.interview_enhanced import analyze_communication_style
        comm = await analyze_communication_style(answer)
        comm_norm = comm["score"] / 10.0  # 0-10 scale
        # Blend heuristic into the communication dimension only (not the whole score).
        comm_llm = parsed["breakdown"].get("communication", 5)
        blended_comm = round(COMMUNICATION_BLEND * comm_norm + (1 - COMMUNICATION_BLEND) * comm_llm, 1)
        parsed["breakdown"]["communication"] = max(1, min(10, blended_comm))
        parsed["communication_analysis"] = comm
    except Exception as e:
        logger.debug(f"Communication analysis failed: {e}")

    score = parsed["score"]
    if score >= 9:
        parsed.setdefault("reaction", "fire")
    elif score >= 7:
        parsed.setdefault("reaction", "clap")
    elif score >= 5:
        parsed.setdefault("reaction", "muscle")
    elif score >= 3:
        parsed.setdefault("reaction", "thinking")
    else:
        parsed.setdefault("reaction", "memo")

    return parsed