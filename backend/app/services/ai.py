"""AI service module with circuit breaker, retry logic, and caching."""

import json
import time
import hashlib
import asyncio
import random
import logging
from typing import List, Dict, Any, Optional
import httpx
from app.config import get_settings
from app.services.cache import cache

logger = logging.getLogger(__name__)
settings = get_settings()

# Company tag pool for questions
COMPANY_TAGS = ["TCS", "Infosys", "Wipro", "Cognizant", "HCL Tech", "Accenture", "Capgemini",
                "Tech Mahindra", "L&T Infotech", "Mphasis", "Hexaware", "IBM", "Flipkart",
                "Zomato", "Razorpay", "Google", "Microsoft", "Amazon"]
MASS_RECRUITERS = ["TCS", "Infosys", "Wipro", "Cognizant"]


def assign_companies(count: int = None) -> List[str]:
    """Pick 2-5 random companies. Mass recruiters appear ~30% more often."""
    if count is None:
        count = random.randint(2, 5)
    count = max(2, min(5, count))

    # Build weighted pool: mass recruiters get 30% boost
    weighted = list(COMPANY_TAGS)
    for c in MASS_RECRUITERS:
        weighted.extend([c, c])  # double presence ≈ +33% weight

    selected = set()
    while len(selected) < count and weighted:
        pick = random.choice(weighted)
        selected.add(pick)
        # Remove all instances of picked company to avoid duplicates
        weighted = [c for c in weighted if c != pick]

    return sorted(selected)

MAX_RETRIES = settings.OPENROUTER_MAX_RETRIES
RETRY_DELAY = 1.0

FALLBACK_MODELS = [
    "google/gemini-2.0-flash-001",
    "meta-llama/llama-3.1-8b-instruct:free",
    "microsoft/phi-3-mini-128k-instruct:free",
    "deepseek/deepseek-chat-v3-0324:free",
]

# Circuit breaker state
circuit_breaker = {
    "failures": 0,
    "last_failure_time": 0,
    "is_open": False,
    "threshold": 5,
    "recovery_time": 60,
}

# HTTP client with connection pooling
_http_client: Optional[httpx.AsyncClient] = None


async def _get_http_client() -> httpx.AsyncClient:
    """Get or create HTTP client with connection pooling."""
    global _http_client
    if _http_client is None or _http_client.is_closed:
        _http_client = httpx.AsyncClient(
            timeout=httpx.Timeout(settings.OPENROUTER_TIMEOUT, connect=10.0),
            limits=httpx.Limits(
                max_connections=20,
                max_keepalive_connections=10,
                keepalive_expiry=60.0
            ),
            http2=True,
        )
        logger.info("HTTP client initialized for AI service")
    return _http_client


async def close_http_client():
    """Close the HTTP client gracefully."""
    global _http_client
    if _http_client and not _http_client.is_closed:
        await _http_client.aclose()
        _http_client = None
        logger.info("HTTP client closed")


def _check_circuit_breaker() -> bool:
    """Check if circuit breaker allows requests."""
    if circuit_breaker["is_open"]:
        if time.time() - circuit_breaker["last_failure_time"] > circuit_breaker["recovery_time"]:
            circuit_breaker["is_open"] = False
            circuit_breaker["failures"] = 0
            logger.info("Circuit breaker closed — resuming normal operation")
            return True
        logger.warning("Circuit breaker is open — using fallback models")
        return False
    return True


def _record_failure():
    """Record a failure for the circuit breaker."""
    circuit_breaker["failures"] += 1
    circuit_breaker["last_failure_time"] = time.time()
    if circuit_breaker["failures"] >= circuit_breaker["threshold"]:
        circuit_breaker["is_open"] = True
        logger.warning("Circuit breaker opened — too many failures")


def _record_success():
    """Record a success for the circuit breaker."""
    circuit_breaker["failures"] = 0
    circuit_breaker["is_open"] = False


def _make_cache_key(messages: List[Dict], model: str) -> str:
    """Generate a cache key based on messages and model."""
    content = json.dumps(messages, sort_keys=True) + model
    return hashlib.sha256(content.encode()).hexdigest()[:16]


async def _call_openrouter(messages: List[Dict], model: str) -> str:
    """Make a single API call to OpenRouter with connection pooling."""
    if not settings.OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY not configured")
    
    client = await _get_http_client()
    
    try:
        response = await client.post(
            settings.OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://placementpro.app",
                "X-Title": "PlacementPro",
            },
            json={
                "model": model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 2000,
                "top_p": 0.9,
            },
            timeout=settings.OPENROUTER_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except httpx.TimeoutException as e:
        logger.warning(f"OpenRouter timeout for model {model}: {e}")
        raise
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            logger.warning(f"Rate limit hit for model {model}, waiting before retry")
        elif e.response.status_code >= 500:
            logger.warning(f"OpenRouter server error for model {model}: {e}")
        else:
            logger.error(f"OpenRouter error for model {model}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error calling OpenRouter: {e}")
        raise


async def chat_completion(
    messages: List[Dict], 
    model: Optional[str] = None, 
    use_cache: bool = True,
    temperature: float = 0.7,
    max_tokens: int = 2000
) -> str:
    """
    Get a chat completion from OpenRouter with retries, fallback, and caching.
    
    Args:
        messages: List of message dicts with 'role' and 'content'
        model: Optional model name (uses default if not specified)
        use_cache: Whether to use cached responses
        temperature: Temperature parameter (0.0-1.0)
        max_tokens: Maximum tokens to generate
    
    Returns:
        The generated text response
    """
    primary_model = model or settings.OPENROUTER_MODEL

    # Check cache
    if use_cache:
        cache_key = _make_cache_key(messages, primary_model)
        cached = await cache.get("ai", cache_key)
        if cached:
            logger.debug(f"Cache hit for {primary_model}")
            return cached

    # Check circuit breaker
    if not _check_circuit_breaker():
        # Try fallback models only
        for fallback in FALLBACK_MODELS:
            if fallback != primary_model:
                try:
                    result = await _call_openrouter(messages, fallback)
                    _record_success()
                    if use_cache:
                        await cache.set("ai", cache_key, result, ttl=3600)
                    return result
                except Exception as e:
                    logger.warning(f"Fallback model {fallback} failed: {e}")
                    continue
        raise Exception("AI service temporarily unavailable (circuit breaker open)")

    # Try primary model, then fallbacks
    models_to_try = [primary_model] + [m for m in FALLBACK_MODELS if m != primary_model]

    for model_to_use in models_to_try:
        for attempt in range(MAX_RETRIES):
            try:
                result = await _call_openrouter(messages, model_to_use)
                _record_success()
                if use_cache:
                    cache_key = _make_cache_key(messages, primary_model)
                    await cache.set("ai", cache_key, result, ttl=3600)
                return result
            except Exception as e:
                if attempt == MAX_RETRIES - 1:
                    _record_failure()
                    logger.error(f"AI call failed after {MAX_RETRIES} retries: {e}")
                    break
                wait_time = RETRY_DELAY * (2 ** attempt)  # Exponential backoff
                logger.warning(f"Attempt {attempt + 1} failed, retrying in {wait_time}s: {e}")
                await asyncio.sleep(wait_time)

    raise Exception("AI service temporarily unavailable")


def parse_json(text: str) -> Dict[str, Any]:
    """
    Parse JSON from text, handling markdown code blocks and common LLM formatting issues.
    
    Args:
        text: Text containing JSON (possibly in markdown code block)
    
    Returns:
        Parsed dictionary
    """
    text = text.strip()
    
    # Remove markdown code blocks
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    
    if text.endswith("```"):
        text = text[:-3]
    
    text = text.strip()
    
    # Try parsing as-is
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # Try to extract JSON object from text
    start = text.find("{")
    end = text.rfind("}") + 1
    if start != -1 and end > start:
        try:
            return json.loads(text[start:end])
        except json.JSONDecodeError:
            pass
    
    # Try to extract JSON array from text
    start = text.find("[")
    end = text.rfind("]") + 1
    if start != -1 and end > start:
        try:
            return json.loads(text[start:end])
        except json.JSONDecodeError:
            pass
    
    # Last resort: try to fix common JSON issues
    try:
        # Replace single quotes with double quotes
        fixed = text.replace("'", '"')
        return json.loads(fixed)
    except json.JSONDecodeError:
        pass
    
    logger.error(f"Failed to parse JSON from: {text[:200]}...")
    raise ValueError(f"Could not parse JSON from AI response: {text[:200]}...")


# ============================================================================
# COMPANY PROFILES - Used for company-specific interview prompts
# ============================================================================

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


# ============================================================================
# INTERVIEW FUNCTIONS
# ============================================================================

async def generate_interview_question(
    job_role: str,
    history: List[Dict[str, Any]],
    company: str = "general",
    difficulty: str = "medium",
) -> Dict[str, Any]:
    """
    Generate the next interview question based on role, company, history, and difficulty.
    
    Args:
        job_role: Target job role (e.g. "Software Engineer", "Data Scientist")
        history: List of previous Q&A dicts with keys: question, answer, score, question_type
        company: Target company (lowercase key into COMPANY_PROFILES or "general")
        difficulty: Target difficulty level (easy, medium, hard)
    
    Returns:
        {question, question_type, tips, difficulty, company, follow_up_expected}
    """
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
        # Adapt difficulty based on performance
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
    
    system_prompt = f"""You are an expert technical interviewer for {job_role} positions.
{company_context}
You must generate interview questions that are realistic, challenging, and appropriate for the target difficulty.

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
    
    # Ensure required fields
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
) -> Dict[str, Any]:
    """
    Evaluate a candidate's answer with company-specific rubrics.
    
    Args:
        question: The interview question asked
        answer: The candidate's answer
        job_role: Target job role
        company: Target company
        question_type: Type of question (technical, behavioral, situational, coding)
    
    Returns:
        {score (1-10), breakdown: {technical, communication, problem_solving, depth},
         strengths, improvements, better_answer, reaction}
    """
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

    system_prompt = f"""You are an expert interviewer evaluating a candidate for {job_role} positions.
{evaluation_context}
{type_guidance}

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
    
    # Ensure required fields and valid score
    parsed.setdefault("score", 5)
    parsed["score"] = max(1, min(10, int(parsed["score"])))
    parsed.setdefault("breakdown", {"technical": 5, "communication": 5, "problem_solving": 5, "depth": 5})
    parsed.setdefault("strengths", ["Attempted the question"])
    parsed.setdefault("improvements", ["Provide more detail and examples"])
    parsed.setdefault("better_answer", "A stronger answer would include more specifics and metrics.")
    
    # Set reaction based on score if not provided
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


# ============================================================================
# CODING CHALLENGES
# ============================================================================

async def generate_coding_challenge(
    difficulty: str,
    topic: str,
    language: str,
) -> Dict[str, Any]:
    """
    Generate a coding challenge with examples, constraints, and test cases.
    
    Args:
        difficulty: easy, medium, or hard
        topic: Topic focus (arrays, trees, graphs, dynamic programming, strings, etc.)
        language: Programming language (python, javascript, java, cpp, etc.)
    
    Returns:
        {title, description, examples, constraints, test_cases, hints, follow_up, time_limit_seconds}
    """
    system_prompt = f"""You are an expert coding challenge designer creating problems for {difficulty} difficulty.
Target topic: {topic}
Solution language: {language}

Generate a unique, well-structured coding challenge. The problem should be:
- Original (not a direct copy of famous problems)
- Clearly defined with unambiguous input/output
- Appropriate difficulty for {difficulty} level
- Related to the topic: {topic}

The output MUST be valid JSON with this exact structure:
{{
    "title": "Problem Title",
    "description": "Full problem description with clear explanation",
    "examples": [
        {{
            "input": "Example input",
            "output": "Example output",
            "explanation": "Step-by-step explanation"
        }}
    ],
    "constraints": [
        "constraint 1 (e.g., 1 <= n <= 10^5)",
        "constraint 2"
    ],
    "test_cases": [
        {{
            "input": "Test input",
            "expected_output": "Expected output",
            "is_hidden": false
        }},
        {{
            "input": "Hidden test input",
            "expected_output": "Hidden expected output",
            "is_hidden": true
        }}
    ],
    "hints": [
        "Hint 1: Think about the approach...",
        "Hint 2: Consider using...",
        "Hint 3: The time complexity should be..."
    ],
    "follow_up": "Can you solve it with O(n) time and O(1) space?",
    "time_limit_seconds": 1800
}}

Generate 2 visible test cases and 3 hidden test cases.
Hints should progressively reveal the approach.
Time limit: 1800 (easy), 2400 (medium), 3600 (hard).

Return ONLY the JSON object. No markdown, no explanation."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Create a {difficulty} coding challenge about {topic} for {language}."},
    ]
    
    result = await chat_completion(messages)
    parsed = parse_json(result)
    
    parsed.setdefault("title", f"{topic.title()} Challenge")
    parsed.setdefault("description", "Solve the given coding problem.")
    parsed.setdefault("examples", [{"input": "[]", "output": "0", "explanation": ""}])
    parsed.setdefault("constraints", ["1 <= n <= 1000"])
    parsed.setdefault("test_cases", [{"input": "[]", "expected_output": "0", "is_hidden": False}])
    parsed.setdefault("hints", ["Think about the approach carefully."])
    parsed.setdefault("follow_up", "Can you optimize your solution?")
    parsed.setdefault("companies", assign_companies())
    
    time_limits = {"easy": 1800, "medium": 2400, "hard": 3600}
    parsed.setdefault("time_limit_seconds", time_limits.get(difficulty, 1800))
    
    return parsed


# ============================================================================
# APTITUDE TEST
# ============================================================================

async def generate_aptitude_questions(
    category: str,
    difficulty: str,
    count: int,
) -> Dict[str, Any]:
    """
    Generate aptitude test MCQs for campus placement preparation.
    
    Args:
        category: quant, logical, verbal, technical, or general
        difficulty: easy, medium, or hard
        count: Number of questions to generate (1-30)
    
    Returns:
        {questions: [{question, options, correct_answer, explanation, topic, difficulty}]}
    """
    system_prompt = f"""You are an expert aptitude test question writer for campus placement preparation.
Category: {category}
Difficulty: {difficulty}
Number of questions: {count}

Generate {count} multiple-choice questions (MCQs) appropriate for campus placement tests.

CATEGORY GUIDELINES:
- quant: Quantitative aptitude (math, percentages, profit/loss, time-speed-distance, probability, permutations)
- logical: Logical reasoning (series, analogies, coding-decoding, blood relations, direction sense, syllogisms)
- verbal: Verbal ability (synonyms, antonyms, sentence correction, reading comprehension, fill in the blanks)
- technical: Programming basics, data structures fundamentals, OS concepts, DBMS, networking
- general: Mixed questions across all categories

Each question must have exactly 4 options (A, B, C, D).
Questions should be realistic and similar to TCS, Infosys, Wipro, Cognizant placement papers.

Each question must include 2-5 company tags from this pool indicating which companies have asked similar questions:
{COMPANY_TAGS}

Mass recruiters (TCS, Infosys, Wipro, Cognizant) should appear more frequently (~30% more often).

The output MUST be valid JSON with this exact structure:
{{
    "questions": [
        {{
            "question": "Question text here?",
            "options": {{
                "A": "Option A",
                "B": "Option B",
                "C": "Option C",
                "D": "Option D"
            }},
            "correct_answer": "B",
            "explanation": "Detailed explanation of the correct answer",
            "topic": "sub-topic name",
            "difficulty": "{difficulty}",
            "companies": ["TCS", "Infosys", "Wipro"]
        }}
    ]
}}

Each question must have exactly 4 options.
Correct answer must be one of "A", "B", "C", "D".
Provide clear explanations for all answers.
Each question must have 2-5 company tags from the pool above.

Return ONLY the JSON object. No markdown, no explanation."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Generate {count} {difficulty} {category} aptitude questions."},
    ]
    
    result = await chat_completion(messages, max_tokens=4000)
    parsed = parse_json(result)
    
    parsed.setdefault("questions", [])
    for q in parsed["questions"]:
        q.setdefault("question", "")
        q.setdefault("options", {"A": "", "B": "", "C": "", "D": ""})
        q.setdefault("correct_answer", "A")
        q.setdefault("explanation", "")
        q.setdefault("topic", category)
        q.setdefault("difficulty", difficulty)
        if not q.get("companies"):
            q["companies"] = assign_companies()
    
    return parsed


async def evaluate_aptitude_answer(
    question: str,
    selected_option: str,
    correct_answer: str,
) -> Dict[str, Any]:
    """
    Evaluate a single aptitude test answer.
    
    Args:
        question: The question text
        selected_option: The option the user selected (A, B, C, or D)
        correct_answer: The correct answer (A, B, C, or D)
    
    Returns:
        {is_correct, correct_answer, explanation}
    """
    is_correct = selected_option.upper().strip() == correct_answer.upper().strip()
    
    system_prompt = f"""You are an aptitude test evaluator.

Question: {question}
Selected Answer: {selected_option}
Correct Answer: {correct_answer}

Generate a brief explanation of why the correct answer is correct.
The output MUST be valid JSON:
{{
    "is_correct": {"true" if is_correct else "false"},
    "correct_answer": "{correct_answer}",
    "explanation": "Brief explanation of why this is the correct answer"
}}

Return ONLY the JSON object."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Evaluate: Selected={selected_option}, Correct={correct_answer}"},
    ]
    
    result = await chat_completion(messages)
    parsed = parse_json(result)
    
    parsed["is_correct"] = is_correct
    parsed.setdefault("correct_answer", correct_answer)
    parsed.setdefault("explanation", f"The correct answer is {correct_answer}.")
    
    return parsed


# ============================================================================
# RESUME FUNCTIONS
# ============================================================================

async def analyze_resume(resume_text: str) -> Dict[str, Any]:
    """
    Analyze a resume and score across 4 dimensions.
    
    Args:
        resume_text: Extracted text from the resume PDF
    
    Returns:
        {score, overall_score, sections: {content, formatting, keywords, impact}, feedback, suggestions}
    """
    system_prompt = """You are an expert resume reviewer and ATS (Applicant Tracking System) specialist.
Analyze the provided resume text thoroughly across 4 dimensions.

SCORING DIMENSIONS (each 1-10):
1. CONTENT: Relevance of experience, achievements quantified, skills listed, education details
2. FORMATTING: Structure, readability, consistent formatting, appropriate length (1-2 pages)
3. KEYWORDS: Industry-relevant keywords, technical terms, action verbs present
4. IMPACT: Strong action verbs, quantified achievements, clear value proposition

The output MUST be valid JSON with this exact structure:
{
    "score": 7,
    "overall_score": 7,
    "sections": {
        "content": {"score": 7, "feedback": "Detailed feedback on content"},
        "formatting": {"score": 6, "feedback": "Detailed feedback on formatting"},
        "keywords": {"score": 8, "feedback": "Detailed feedback on keywords"},
        "impact": {"score": 5, "feedback": "Detailed feedback on impact"}
    },
    "feedback": "Overall assessment paragraph",
    "suggestions": [
        "Specific actionable suggestion 1",
        "Specific actionable suggestion 2",
        "Specific actionable suggestion 3"
    ]
}

Be specific and actionable in your suggestions. Reference actual parts of the resume.

Return ONLY the JSON object. No markdown, no explanation."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Analyze this resume:\n\n{resume_text[:4000]}"},
    ]
    
    result = await chat_completion(messages)
    parsed = parse_json(result)
    
    parsed.setdefault("score", 5)
    parsed.setdefault("overall_score", parsed["score"])
    parsed.setdefault("sections", {
        "content": {"score": 5, "feedback": ""},
        "formatting": {"score": 5, "feedback": ""},
        "keywords": {"score": 5, "feedback": ""},
        "impact": {"score": 5, "feedback": ""},
    })
    parsed.setdefault("feedback", "Resume needs improvement.")
    parsed.setdefault("suggestions", ["Add more quantified achievements", "Include more industry keywords"])
    
    return parsed


async def optimize_ats(resume_text: str, job_description: str) -> Dict[str, Any]:
    """
    Optimize a resume for ATS compatibility against a specific job description.
    
    Args:
        resume_text: Extracted text from the resume PDF
        job_description: The target job description text
    
    Returns:
        {ats_score, missing_keywords, present_keywords, optimized_resume, changes_made}
    """
    system_prompt = """You are an ATS (Applicant Tracking System) optimization expert.
Compare the resume against the job description and optimize it.

STEPS:
1. Extract all important keywords from the job description
2. Check which keywords are present/missing in the resume
3. Rewrite the resume to naturally incorporate missing keywords
4. Keep the original meaning while improving ATS compatibility
5. List all changes made

The output MUST be valid JSON with this exact structure:
{
    "ats_score": 65,
    "missing_keywords": ["keyword1", "keyword2", "keyword3"],
    "present_keywords": ["keyword4", "keyword5"],
    "optimized_resume": "The fully optimized resume text...",
    "changes_made": [
        "Added 'machine learning' to skills section",
        "Rewrote project description to include 'REST API'",
        "Updated job title to match ATS expectations"
    ]
}

Rules:
- ats_score is 0-100 (percentage of keyword match)
- missing_keywords: important terms from JD not in resume (max 15)
- present_keywords: important terms already in resume (max 15)
- optimized_resume: complete rewritten resume incorporating missing keywords naturally
- changes_made: list every modification made

Return ONLY the JSON object. No markdown, no explanation."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"RESUME:\n{resume_text[:3000]}\n\nJOB DESCRIPTION:\n{job_description[:2000]}\n\nOptimize this resume for the job description."},
    ]
    
    result = await chat_completion(messages, max_tokens=4000)
    parsed = parse_json(result)
    
    parsed.setdefault("ats_score", 50)
    parsed.setdefault("missing_keywords", [])
    parsed.setdefault("present_keywords", [])
    parsed.setdefault("optimized_resume", resume_text)
    parsed.setdefault("changes_made", ["General formatting improvements"])
    
    return parsed


async def generate_resume_content(
    name: str,
    email: str,
    target_role: str,
    experience: List[Dict[str, str]],
    education: List[Dict[str, str]],
    skills: List[str],
) -> Dict[str, Any]:
    """
    Generate professional resume content from user details.
    
    Args:
        name: Full name
        email: Email address
        target_role: Target job title
        experience: List of {company, role, duration, description} dicts
        education: List of {school, degree, year, gpa} dicts
        skills: List of skill strings
    
    Returns:
        {content, sections}
    """
    exp_text = ""
    for exp in experience:
        exp_text += f"- {exp.get('role', 'Role')} at {exp.get('company', 'Company')} ({exp.get('duration', 'Duration')})\n  {exp.get('description', '')}\n"
    
    edu_text = ""
    for edu in education:
        edu_text += f"- {edu.get('degree', 'Degree')} from {edu.get('school', 'School')} ({edu.get('year', 'Year')}) GPA: {edu.get('gpa', 'N/A')}\n"
    
    system_prompt = f"""You are an expert resume writer. Generate professional resume content.
Target role: {target_role}
Name: {name}
Email: {email}

The content should:
- Use strong action verbs (Led, Developed, Implemented, Optimized, Architected)
- Quantify achievements where possible
- Be ATS-friendly with relevant keywords
- Be concise and impactful
- Follow a clean, professional format

The output MUST be valid JSON with this exact structure:
{{
    "content": "Full resume text with sections clearly separated",
    "sections": {{
        "summary": "Professional summary paragraph",
        "experience": [
            {{
                "company": "Company Name",
                "role": "Job Title",
                "duration": "Jan 2022 - Present",
                "bullets": ["Achievement 1 with metrics", "Achievement 2"]
            }}
        ],
        "education": [
            {{
                "school": "University Name",
                "degree": "Degree",
                "year": "2020",
                "gpa": "3.8"
            }}
        ],
        "skills": ["Skill 1", "Skill 2"]
    }}
}}

Return ONLY the JSON object. No markdown, no explanation."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Generate resume for {name} targeting {target_role}.\n\nExperience:\n{exp_text}\n\nEducation:\n{edu_text}\n\nSkills: {', '.join(skills)}"},
    ]
    
    result = await chat_completion(messages, max_tokens=3000)
    parsed = parse_json(result)
    
    parsed.setdefault("content", f"{name}\n{email}\n\n{target_role}")
    parsed.setdefault("sections", {
        "summary": "",
        "experience": experience,
        "education": education,
        "skills": skills,
    })
    
    return parsed


# ============================================================================
# COVER LETTER & LINKEDIN
# ============================================================================

async def generate_cover_letter(
    resume_text: str,
    job_description: str,
    company_name: str,
) -> Dict[str, Any]:
    """
    Generate a tailored cover letter.
    
    Args:
        resume_text: Extracted text from the resume
        job_description: The target job description
        company_name: Name of the target company
    
    Returns:
        {cover_letter}
    """
    system_prompt = """You are an expert cover letter writer. Generate a compelling, tailored cover letter.

GUIDELINES:
- Open with a strong hook that connects to the company
- Reference specific skills from the resume that match the JD
- Show knowledge of the company (mission, products, values)
- Keep it to 3-4 paragraphs
- Professional but personable tone
- Close with a clear call to action

The output MUST be valid JSON:
{
    "cover_letter": "The full cover letter text..."
}

Return ONLY the JSON object. No markdown, no explanation."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Write a cover letter for {company_name}.\n\nRESUME:\n{resume_text[:2000]}\n\nJOB DESCRIPTION:\n{job_description[:1500]}"},
    ]
    
    result = await chat_completion(messages)
    parsed = parse_json(result)
    parsed.setdefault("cover_letter", f"Dear Hiring Manager,\n\nI am writing to express my interest in the position at {company_name}...")
    
    return parsed


async def generate_linkedin_about(
    resume_text: str,
    target_role: str,
) -> Dict[str, Any]:
    """
    Generate a LinkedIn About section.
    
    Args:
        resume_text: Extracted text from the resume
        target_role: Target job title/role
    
    Returns:
        {linkedin_about}
    """
    system_prompt = """You are a LinkedIn profile expert. Generate a compelling About section.

GUIDELINES:
- Write in first person
- Start with a hook (who you are, what drives you)
- Highlight key achievements and skills
- Use relevant keywords for recruiter searches
- End with a call to action (open to opportunities, let's connect)
- Keep it to 3-5 short paragraphs (under 2600 characters)
- Professional but personable

The output MUST be valid JSON:
{
    "linkedin_about": "The LinkedIn About section text..."
}

Return ONLY the JSON object. No markdown, no explanation."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Write a LinkedIn About section for someone targeting {target_role} roles.\n\nResume:\n{resume_text[:2000]}"},
    ]
    
    result = await chat_completion(messages)
    parsed = parse_json(result)
    parsed.setdefault("linkedin_about", f"Passionate {target_role} professional with a track record of delivering impactful solutions...")
    
    return parsed


# ============================================================================
# SALARY & NEGOTIATION
# ============================================================================

async def generate_salary_negotiation_tips(
    job_title: str,
    offered_salary: float,
    location: str,
    years_experience: int,
    company_size: str,
    benefits: str,
) -> Dict[str, Any]:
    """
    Generate salary negotiation tips and scripts.
    
    Args:
        job_title: Target job title
        offered_salary: The offered salary amount
        location: Job location
        years_experience: Years of experience
        company_size: small, medium, large, enterprise
        benefits: Description of offered benefits
    
    Returns:
        {market_research, negotiation_points, scripts, dos, donts}
    """
    system_prompt = """You are an expert salary negotiation coach. Provide actionable negotiation advice.

The output MUST be valid JSON:
{
    "market_research": "Summary of market rate for this role/location",
    "negotiation_points": [
        "Point 1: reason to negotiate higher",
        "Point 2: leverage point"
    ],
    "scripts": {
        "opening": "What to say to start the negotiation",
        "counter": "How to present a counter-offer",
        "benefits_fallback": "If they can't increase salary, ask for these benefits",
        "closing": "How to close the negotiation professionally"
    },
    "dos": [
        "Do 1: Specific negotiation best practice"
    ],
    "donts": [
        "Don't 1: Common negotiation mistake to avoid"
    ]
}

Provide at least 5 dos and 5 donts. Scripts should be word-for-word scripts they can use.

Return ONLY the JSON object. No markdown, no explanation."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Negotiate for: {job_title} at offered ${offered_salary:,.0f}/yr\nLocation: {location}\nExperience: {years_experience} years\nCompany size: {company_size}\nBenefits: {benefits}"},
    ]
    
    result = await chat_completion(messages, max_tokens=3000)
    parsed = parse_json(result)
    
    parsed.setdefault("market_research", "Market research data not available.")
    parsed.setdefault("negotiation_points", ["Consider your total compensation package"])
    parsed.setdefault("scripts", {
        "opening": "Thank you for the offer. I'm excited about this opportunity.",
        "counter": "Based on my research and experience, I'd like to discuss a salary of...",
        "benefits_fallback": "If salary flexibility is limited, I'd like to discuss...",
        "closing": "I appreciate the discussion and look forward to finalizing the details.",
    })
    parsed.setdefault("dos", ["Research market rates thoroughly", "Practice your pitch beforehand"])
    parsed.setdefault("donts", ["Don't give a number first", "Don't accept immediately"])
    
    return parsed


async def generate_salary_benchmark(
    job_title: str,
    location: str,
    company: str,
    years_experience: int,
    level: str,
) -> Dict[str, Any]:
    """
    Generate salary benchmark data for a role/location/company.
    
    Args:
        job_title: Job title
        location: City/state/country
        company: Company name (optional)
        years_experience: Years of experience
        level: junior, mid, senior, lead, principal
    
    Returns:
        {market_rate, percentiles, factors_affecting_pay, companies_paying_above_market}
    """
    system_prompt = """You are a compensation data analyst. Provide salary benchmark information.

Use your knowledge of tech industry salaries (2024-2025 data). Be realistic and specific.

The output MUST be valid JSON:
{
    "market_rate": {"min": 80000, "median": 110000, "max": 150000, "currency": "USD"},
    "percentiles": {"p10": 75000, "p25": 90000, "p50": 110000, "p75": 135000, "p90": 160000},
    "factors_affecting_pay": [
        "Factor 1 that influences salary positively",
        "Factor 2"
    ],
    "companies_paying_above_market": [
        {"company": "Company Name", "range": "$120K-$160K", "notes": "Why they pay more"}
    ]
}

Return ONLY the JSON object. No markdown, no explanation."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Benchmark salary for: {job_title} at {level} level\nLocation: {location}\nExperience: {years_experience} years\nCompany: {company}"},
    ]
    
    result = await chat_completion(messages)
    parsed = parse_json(result)
    
    parsed.setdefault("market_rate", {"min": 0, "median": 0, "max": 0, "currency": "USD"})
    parsed.setdefault("percentiles", {"p10": 0, "p25": 0, "p50": 0, "p75": 0, "p90": 0})
    parsed.setdefault("factors_affecting_pay", ["Location", "Experience", "Company size"])
    parsed.setdefault("companies_paying_above_market", [])
    
    return parsed


async def generate_offer_comparison(offers: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Compare multiple job offers and recommend the best one.
    
    Args:
        offers: List of offer dicts with keys like: company, title, salary, location,
                benefits, equity, growth_potential, work_life_balance
    
    Returns:
        {winner, winner_reason, comparison_matrix, recommendation}
    """
    system_prompt = """You are a career advisor helping compare job offers.
Analyze each offer holistically — not just salary, but benefits, growth, culture, and work-life balance.

The output MUST be valid JSON:
{
    "winner": "Company Name",
    "winner_reason": "Detailed explanation of why this offer wins overall",
    "comparison_matrix": {
        "Company1": {
            "salary_score": 8,
            "benefits_score": 7,
            "growth_score": 9,
            "work_life_score": 6,
            "total_score": 30,
            "pros": ["Pro 1", "Pro 2"],
            "cons": ["Con 1"]
        },
        "Company2": {
            "salary_score": 9,
            "benefits_score": 8,
            "growth_score": 6,
            "work_life_score": 7,
            "total_score": 30,
            "pros": ["Pro 1"],
            "cons": ["Con 1", "Con 2"]
        }
    },
    "recommendation": "Personalized recommendation paragraph explaining the trade-offs"
}

Score each dimension 1-10. Total is sum of all dimensions. Consider the full picture.

Return ONLY the JSON object. No markdown, no explanation."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Compare these job offers:\n\n{json.dumps(offers, indent=2)}"},
    ]
    
    result = await chat_completion(messages, max_tokens=3000)
    parsed = parse_json(result)
    
    parsed.setdefault("winner", offers[0].get("company", "Option A") if offers else "N/A")
    parsed.setdefault("winner_reason", "Based on overall compensation and opportunities.")
    parsed.setdefault("comparison_matrix", {})
    parsed.setdefault("recommendation", "Consider both short-term and long-term career goals.")
    
    return parsed


# ============================================================================
# SYSTEM DESIGN
# ============================================================================

async def generate_system_design_question(
    difficulty: str,
    topic: str,
) -> Dict[str, Any]:
    """
    Generate a system design interview question.
    
    Args:
        difficulty: easy, medium, or hard
        topic: Topic area (e.g., social media, e-commerce, chat system, search engine)
    
    Returns:
        {question, hints, expected_components, difficulty, topic}
    """
    system_prompt = f"""You are a system design interview expert. Generate realistic system design questions.

Difficulty: {difficulty}
Topic: {topic}

DIFFICULTY GUIDELINES:
- easy: Design a URL shortener, Pastebin, Rate Limiter (small scale, few components)
- medium: Design a chat system, News Feed, Notification system (moderate scale, multiple services)
- hard: Design Google Search, WhatsApp at scale, Uber, YouTube (massive scale, complex distributed systems)

The output MUST be valid JSON:
{{
    "question": "Design a [system] that [requirements]. Users should be able to [features]. Scale: [expected load].",
    "hints": [
        "Start by clarifying requirements and constraints",
        "Think about the core entities and their relationships",
        "Consider read-heavy vs write-heavy patterns",
        "Think about data storage and caching strategies"
    ],
    "expected_components": [
        "Load Balancer",
        "API Gateway",
        "Application Servers",
        "Database (specify type)",
        "Cache Layer",
        "Message Queue",
        "CDN"
    ],
    "difficulty": "{difficulty}",
    "topic": "{topic}"
}}

Return ONLY the JSON object. No markdown, no explanation."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Generate a {difficulty} system design question about {topic}."},
    ]
    
    result = await chat_completion(messages)
    parsed = parse_json(result)
    
    parsed.setdefault("question", f"Design a scalable {topic} system.")
    parsed.setdefault("hints", ["Start with requirements gathering", "Think about scale and bottlenecks"])
    parsed.setdefault("expected_components", ["Load Balancer", "Application Server", "Database", "Cache"])
    parsed.setdefault("difficulty", difficulty)
    parsed.setdefault("topic", topic)
    
    return parsed


async def evaluate_system_design_answer(
    question: str,
    answer: str,
    diagram_description: str,
) -> Dict[str, Any]:
    """
    Evaluate a system design interview answer.
    
    Args:
        question: The system design question asked
        answer: The candidate's text answer
        diagram_description: Description of the architecture diagram drawn
    
    Returns:
        {score, strengths, improvements, missing_concepts, ideal_design}
    """
    system_prompt = """You are a system design interview evaluator. Score the candidate's response.

EVALUATION CRITERIA (score 1-10):
1. Requirements clarity (functional + non-functional)
2. High-level design correctness
3. Component selection and justification
4. Scalability discussion
5. Trade-off analysis
6. Database design
7. Caching strategy
8. API design
9. Communication clarity
10. Handling bottlenecks

The output MUST be valid JSON:
{
    "score": 7,
    "strengths": ["Strong point 1", "Strong point 2"],
    "improvements": ["Area to improve 1", "Area to improve 2"],
    "missing_concepts": ["Important concept they missed 1", "Concept 2"],
    "ideal_design": "Brief description of what an ideal answer would include..."
}

Return ONLY the JSON object. No markdown, no explanation."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Question: {question}\n\nAnswer: {answer}\n\nDiagram: {diagram_description}\n\nEvaluate this system design response."},
    ]
    
    result = await chat_completion(messages)
    parsed = parse_json(result)
    
    parsed.setdefault("score", 5)
    parsed.setdefault("strengths", ["Attempted to address the problem"])
    parsed.setdefault("improvements", ["Discuss scalability and trade-offs more"])
    parsed.setdefault("missing_concepts", [])
    parsed.setdefault("ideal_design", "A complete answer would cover requirements, high-level design, component details, scalability, and trade-offs.")
    
    return parsed


# ============================================================================
# COMPANY-SPECIFIC PREP
# ============================================================================

async def generate_behavioral_question(
    company: str,
    role: str,
) -> Dict[str, Any]:
    """
    Generate a company-specific behavioral interview question.
    
    Args:
        company: Target company (lowercase)
        role: Target role
    
    Returns:
        {question: {question, category, star_framework, red_flags}}
    """
    company_key = company.lower()
    profile = COMPANY_PROFILES.get(company_key, None)
    
    company_context = ""
    lp_guidance = ""
    if profile:
        company_context = f"This is for a {company.upper()} interview. Interview style: {profile['interview_style']}"
        if profile["leadership_principles"]:
            lp_guidance = f"Focus on these Leadership Principles: {', '.join(profile['leadership_principles'][:5])}"
    
    system_prompt = f"""You are a behavioral interview coach specializing in {company.upper()} interviews.
{company_context}
{lp_guidance}

Generate a realistic behavioral interview question that would be asked at {company.upper()} for a {role} position.

The output MUST be valid JSON:
{{
    "question": {{
        "question": "Tell me about a time when you... (the behavioral question)",
        "category": "leadership|teamwork|conflict|failure|innovation|customer-focus|ownership",
        "star_framework": {{
            "situation": "What context should the candidate set up?",
            "task": "What responsibility should they describe?",
            "action": "What kind of actions should they highlight?",
            "result": "What results should they emphasize?"
        }},
        "red_flags": [
            "Red flag 1: What would make this a weak answer",
            "Red flag 2: Another common mistake"
        ]
    }}
}}

Return ONLY the JSON object. No markdown, no explanation."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Generate a behavioral question for a {role} position at {company}."},
    ]
    
    result = await chat_completion(messages)
    parsed = parse_json(result)
    
    # Handle nested structure
    if "question" in parsed and isinstance(parsed["question"], str):
        parsed = {
            "question": {
                "question": parsed["question"],
                "category": "leadership",
                "star_framework": {
                    "situation": "Describe the context",
                    "task": "Explain your responsibility",
                    "action": "Detail your specific actions",
                    "result": "Share measurable outcomes",
                },
                "red_flags": ["Vague answers without specific examples", "Taking credit for team achievements"],
            }
        }
    
    if "question" not in parsed:
        parsed = {
            "question": {
                "question": f"Tell me about a time you demonstrated leadership at {company}.",
                "category": "leadership",
                "star_framework": {
                    "situation": "Describe the context",
                    "task": "Explain your responsibility",
                    "action": "Detail your specific actions",
                    "result": "Share measurable outcomes",
                },
                "red_flags": ["Vague answers without specific examples"],
            }
        }
    
    return parsed


async def generate_interview_tips(
    company: str,
    role: str,
    round_type: str,
) -> Dict[str, Any]:
    """
    Generate company-specific interview tips for a specific round.
    
    Args:
        company: Target company (lowercase)
        role: Target role
        round_type: coding, behavioral, system_design, aptitude, hr
    
    Returns:
        {tips: {company_overview, key_focus_areas, common_questions}}
    """
    company_key = company.lower()
    profile = COMPANY_PROFILES.get(company_key, None)
    
    company_context = ""
    if profile:
        company_context = f"""
Company: {company.upper()}
Interview Style: {profile['interview_style']}
Evaluation Rubric: {profile['evaluation_rubric']}
{'Leadership Principles: ' + ', '.join(profile['leadership_principles']) if profile['leadership_principles'] else ''}
"""
    
    system_prompt = f"""You are an interview preparation coach providing tips for {company.upper()} interviews.
{company_context}

Generate comprehensive interview tips for the {round_type} round.

The output MUST be valid JSON:
{{
    "tips": {{
        "company_overview": "Brief overview of {company}'s interview process and culture",
        "key_focus_areas": [
            "Area 1: What they specifically look for",
            "Area 2: Another important evaluation criteria",
            "Area 3: Another focus area"
        ],
        "common_questions": [
            "Common question 1 and how to approach it",
            "Common question 2",
            "Common question 3"
        ]
    }}
}}

Include at least 5 key focus areas and 5 common questions.
Be specific to {company.upper()} — not generic advice.

Return ONLY the JSON object. No markdown, no explanation."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Give me tips for the {round_type} round at {company} for a {role} position."},
    ]
    
    result = await chat_completion(messages)
    parsed = parse_json(result)
    
    # Handle flat tips object
    if "tips" not in parsed:
        parsed = {"tips": parsed}
    
    parsed["tips"].setdefault("company_overview", f"{company} has a structured interview process.")
    parsed["tips"].setdefault("key_focus_areas", ["Technical fundamentals", "Problem-solving approach", "Communication skills"])
    parsed["tips"].setdefault("common_questions", [f"Tell me about yourself", "Why {company}?", "Describe a challenging project"])
    
    return parsed
