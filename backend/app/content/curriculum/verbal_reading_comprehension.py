"""
Promoted Lesson: Reading Comprehension
======================================

Service-company verbal ability foundation. Follows the full content contract.

Provenance: Pattern-relevant for service-company verbal ability sections.
Not a claim about any private employer question bank.
"""
from typing import Dict, List, Any

LESSON_ID = "verbal_reading_comprehension_01"
VERSION = "1.0.0"
SKILL_ID = "verbal.reading_comprehension"
COMPANY_RELEVANCE = ["tcs", "infosys", "wipro", "cognizant", "capgemini", "accenture"]
EST_MINUTES = 15
XP_REWARD = 120

READING_COMPREHENSION_LESSON: Dict[str, Any] = {
    "lesson_id": LESSON_ID,
    "version": VERSION,
    "module_id": "verbal_ability:reading_comprehension",
    "title": "Reading Comprehension",
    "description": "Master reading comprehension — identify main idea, inference, tone, and vocabulary in context.",
    "difficulty": "beginner",
    "est_minutes": EST_MINUTES,
    "xp_reward": XP_REWARD,
    "skills_taught": ["main_idea", "inference", "tone_attitude", "vocabulary_context"],
    "srs_concept_tag": SKILL_ID,
    "company_relevance": COMPANY_RELEVANCE,
    "learning_objectives": [
        "Identify the main idea of a passage.",
        "Make logical inferences from stated information.",
        "Determine author's tone and attitude.",
        "Determine word meaning from context.",
    ],
    "prerequisites": [],
    "concept_explanation": {
        "title": "Reading Comprehension",
        "text": (
            "Read the passage first, then the questions. Main idea = what the passage is "
            "mostly about. Inference = what must be true based on the text (not stated directly). "
            "Tone = author's attitude (positive, negative, neutral, critical). Context clues "
            "help determine unfamiliar word meanings."
        ),
        "key_formula": "Read → Identify main idea → Answer from text only → Eliminate wrong options.",
    },
    "worked_example": {
        "title": "Main idea identification",
        "passage": (
            "Regular exercise improves cardiovascular health, strengthens muscles, "
            "and reduces stress. Even 30 minutes of walking daily can significantly "
            "lower the risk of heart disease and diabetes."
        ),
        "question": "What is the main idea?",
        "options": [
            "Walking is the only good exercise.",
            "Exercise has multiple health benefits.",
            "Heart disease is dangerous.",
            "Stress causes diabetes.",
        ],
        "correct_index": 1,
        "explanation": "The passage lists multiple benefits of exercise — cardiovascular health, muscles, stress reduction.",
    },
    "interactive_practice": [
        {
            "id": "rc_practice_1",
            "type": "mcq",
            "question": "Which is an inference (not directly stated)?",
            "options": [
                "The passage mentions walking.",
                "Exercise reduces heart disease risk.",
                "Everyone should exercise daily.",
                "30 minutes is mentioned.",
            ],
            "correct_index": 2,
            "explanation": "'Everyone should' is a recommendation/inference beyond what's stated.",
        },
        {
            "id": "rc_practice_2",
            "type": "mcq",
            "question": "Tone of the passage?",
            "options": ["Critical", "Positive", "Neutral", "Humorous"],
            "correct_index": 1,
            "explanation": "Words like 'improves', 'strengthens', 'reduces stress' show a positive tone.",
        },
    ],
    "misconception_feedback": {
        "outside_knowledge": {
            "title": "Common mistake: Using outside knowledge",
            "text": "Answer only from the passage, not from what you know about the topic in real life.",
        },
    },
    "assessment": [
        {
            "id": "rc_assess_1",
            "type": "mcq",
            "question": "According to the passage, how much walking is recommended?",
            "options": ["10 minutes", "30 minutes", "60 minutes", "Not mentioned"],
            "correct_index": 1,
            "explanation": "The passage states 'Even 30 minutes of walking daily'.",
        },
        {
            "id": "rc_assess_2",
            "type": "mcq",
            "question": "Which condition is NOT mentioned as reduced by exercise?",
            "options": ["Heart disease", "Diabetes", "Cancer", "Stress"],
            "correct_index": 2,
            "explanation": "The passage mentions heart disease, diabetes, and stress — not cancer.",
        },
    ],
    "transfer_task": {
        "title": "Real-world: Email comprehension",
        "problem": (
            "Your manager writes: 'The project deadline is moved to Friday. "
            "Please prioritize the login module first.' What should you do first?"
        ),
        "steps": [
            "Identify the action item: prioritize the login module.",
            "Note the new deadline: Friday.",
            "Start work on the login module immediately.",
        ],
        "answer": "Prioritize and start work on the login module first.",
    },
    "deterministic_answer_key": {
        "rc_practice_1": 2,
        "rc_practice_2": 1,
        "rc_assess_1": 1,
        "rc_assess_2": 2,
        "transfer_task": "Prioritize and start work on the login module first.",
    },
    "source_provenance": {
        "source": "pattern-relevant",
        "source_urls": [
            "https://www.prepinsta.com/verbal-ability/reading-comprehension/",
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
        "initial_interval_days": 1,
        "ease_factor": 2.5,
        "retention_target": 0.85,
    },
}
