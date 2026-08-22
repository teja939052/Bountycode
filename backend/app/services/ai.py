"""AI service module — re-exports from domain-specific submodules.

This module provides backward-compatible imports for all AI functions.
Domain-specific logic lives in:
  - ai_core.py: HTTP client, circuit breaker, caching, chat_completion, parse_json
  - ai_interview.py: Interview question generation, answer evaluation, COMPANY_PROFILES
  - ai_coding.py: Coding challenge generation
  - ai_aptitude.py: Aptitude question generation and evaluation
  - ai_resume.py: Resume analysis, ATS optimization, content generation
  - ai_cover_letter.py: Cover letter and LinkedIn About generation
  - ai_salary.py: Salary negotiation tips, benchmarks, offer comparison
  - ai_system_design.py: System design question generation and evaluation
  - ai_behavioral.py: Behavioral questions, interview tips, mentor messages
  - ai_project.py: Project generation, review, code improvement, setup instructions
"""

from app.services.ai_core import (
    chat_completion,
    parse_json,
    close_http_client,
    _get_http_client,
    _call_openrouter,
    _check_circuit_breaker,
    _record_failure,
    _record_success,
    _make_cache_key,
    FALLBACK_MODELS,
    MAX_RETRIES,
    RETRY_DELAY,
    COMPANY_TAGS,
)
from app.services.ai_interview import (
    COMPANY_PROFILES,
    assign_companies,
    generate_interview_question,
    evaluate_answer,
)
from app.services.ai_coding import generate_coding_challenge
from app.services.ai_aptitude import (
    APTITUDE_SUB_CATEGORY_GUIDELINES,
    generate_aptitude_questions,
    evaluate_aptitude_answer,
)
from app.services.ai_resume import (
    analyze_resume,
    optimize_ats,
    generate_resume_content,
)
from app.services.ai_cover_letter import (
    generate_cover_letter,
    generate_linkedin_about,
)
from app.services.ai_salary import (
    generate_salary_negotiation_tips,
    generate_salary_benchmark,
    generate_offer_comparison,
)
from app.services.ai_system_design import (
    generate_system_design_question,
    evaluate_system_design_answer,
)
from app.services.ai_behavioral import (
    generate_behavioral_question,
    generate_interview_tips,
    generate_mentor_message,
)
from app.services.ai_project import (
    generate_project,
    review_project,
    improve_code,
    generate_setup_instructions,
)

__all__ = [
    "chat_completion",
    "parse_json",
    "close_http_client",
    "FALLBACK_MODELS",
    "MAX_RETRIES",
    "RETRY_DELAY",
    "COMPANY_PROFILES",
    "COMPANY_TAGS",
    "assign_companies",
    "generate_interview_question",
    "evaluate_answer",
    "generate_coding_challenge",
    "APTITUDE_SUB_CATEGORY_GUIDELINES",
    "generate_aptitude_questions",
    "evaluate_aptitude_answer",
    "analyze_resume",
    "optimize_ats",
    "generate_resume_content",
    "generate_cover_letter",
    "generate_linkedin_about",
    "generate_salary_negotiation_tips",
    "generate_salary_benchmark",
    "generate_offer_comparison",
    "generate_system_design_question",
    "evaluate_system_design_answer",
    "generate_behavioral_question",
    "generate_interview_tips",
    "generate_mentor_message",
    "generate_project",
    "review_project",
    "improve_code",
    "generate_setup_instructions",
]