"""
Promoted Lesson: HTTP/API Reasoning
===================================

Service-company technical foundation. Follows the full content contract.

Provenance: Pattern-relevant for service-company technical aptitude.
Not a claim about any private employer question bank.
"""
from typing import Dict, List, Any

LESSON_ID = "cs_http_api_01"
VERSION = "1.0.0"
SKILL_ID = "cs.http_api_reasoning"
COMPANY_RELEVANCE = ["tcs", "infosys", "wipro", "cognizant", "capgemini", "accenture"]
EST_MINUTES = 12
XP_REWARD = 100

HTTP_API_LESSON: Dict[str, Any] = {
    "lesson_id": LESSON_ID,
    "version": VERSION,
    "module_id": "computer_science:http_api_reasoning",
    "title": "HTTP and API Reasoning",
    "description": "Master web fundamentals — HTTP methods, status codes, REST principles, JSON.",
    "difficulty": "beginner",
    "est_minutes": EST_MINUTES,
    "xp_reward": XP_REWARD,
    "skills_taught": ["http_methods", "status_codes", "rest_principles", "json_format"],
    "srs_concept_tag": SKILL_ID,
    "company_relevance": COMPANY_RELEVANCE,
    "learning_objectives": [
        "Identify GET, POST, PUT, DELETE use cases.",
        "Interpret HTTP status codes (200, 201, 400, 404, 500).",
        "Explain REST principles (stateless, resource-based).",
        "Read and write basic JSON.",
    ],
    "prerequisites": [],
    "concept_explanation": {
        "title": "HTTP and APIs",
        "text": (
            "HTTP is the protocol of the web. Methods define actions: GET retrieves, POST creates, "
            "PUT updates, DELETE removes. Status codes indicate results: 2xx success, 4xx client error, 5xx server error. "
            "REST APIs expose resources via URLs and use JSON for data exchange."
        ),
        "key_formula": "GET /users → retrieve list. POST /users → create new user.",
    },
    "worked_example": {
        "title": "GET request",
        "problem": "What happens when a browser requests GET /api/users/42?",
        "steps": [
            "Browser sends GET request to /api/users/42.",
            "Server looks up user with ID 42.",
            "If found, returns 200 with user JSON.",
            "If not found, returns 404.",
        ],
        "answer": "Returns user data (200) or not found (404).",
    },
    "interactive_practice": [
        {
            "id": "http_practice_1",
            "type": "mcq",
            "question": "Which HTTP method creates a new resource?",
            "options": ["GET", "POST", "PUT", "DELETE"],
            "correct_index": 1,
            "explanation": "POST is used to create new resources on the server.",
        },
        {
            "id": "http_practice_2",
            "type": "mcq",
            "question": "What does 404 mean?",
            "options": ["Server error", "Not found", "Unauthorized", "Bad request"],
            "correct_index": 1,
            "explanation": "404 Not Found means the requested resource doesn't exist.",
        },
    ],
    "misconception_feedback": {
        "put_vs_post": {
            "title": "Common mistake: Confusing PUT and POST",
            "text": "POST creates a new resource. PUT updates/replaces an existing resource at a known URL.",
        },
    },
    "assessment": [
        {
            "id": "http_assess_1",
            "type": "mcq",
            "question": "Which status code means success?",
            "options": ["200", "400", "404", "500"],
            "correct_index": 0,
            "explanation": "200 OK means the request succeeded.",
        },
        {
            "id": "http_assess_2",
            "type": "mcq",
            "question": "JSON stands for?",
            "options": ["JavaScript Object Notation", "Java Structured Query Language", "Just Simple Objects", "JavaScript Simple Output"],
            "correct_index": 0,
            "explanation": "JSON = JavaScript Object Notation, a lightweight data format.",
        },
    ],
    "transfer_task": {
        "title": "Real-world: API error handling",
        "problem": (
            "A frontend calls POST /api/login and gets 401. What should the app do?"
        ),
        "steps": [
            "401 = Unauthorized (invalid credentials).",
            "Show error message: 'Invalid email or password'.",
            "Do not retry automatically — ask user to re-enter credentials.",
        ],
        "answer": "Show 'Invalid email or password' and prompt user to retry.",
    },
    "deterministic_answer_key": {
        "http_practice_1": 1,
        "http_practice_2": 1,
        "http_assess_1": 0,
        "http_assess_2": 0,
        "transfer_task": "Show 'Invalid email or password' and prompt user to retry.",
    },
    "source_provenance": {
        "source": "pattern-relevant",
        "source_urls": [
            "https://developer.mozilla.org/en-US/docs/Web/HTTP",
            "https://restfulapi.net/",
        ],
        "note": (
            "This preparation path targets commonly reported patterns and role expectations. "
            "It is not a claim about a private employer question bank."
        ),
    },
    "review_state": "human_reviewed",
    "accessibility_metadata": {
        "color_blind_safe": True,
        "screen_reader_friendly": True,
        "font_scale_support": True,
    },
    "spaced_repetition_metadata": {
        "initial_interval_days": 2,
        "ease_factor": 2.5,
        "retention_target": 0.85,
    },
}
