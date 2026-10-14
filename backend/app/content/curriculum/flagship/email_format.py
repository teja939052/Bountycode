"""
Flagship Lesson — Email Format Validation
=============================================

Gold-standard interactive lesson for professional email writing.

Full teaching loop with Captain Byte authored mentor moments.
"""
from typing import Dict, Any

SLUG = "email_format"

LESSON: Dict[str, Any] = {
    "lesson_id": "email_format_professional_letter",
    "module_id": "communication:verbal:email_format",
    "title": "The Professional Letter",
    "description": "Write structured, keyword-complete, formally toned emails that satisfy placement rubrics.",
    "difficulty": "beginner",
    "est_minutes": 14,
    "xp_reward": 110,
    "skills_taught": ["email_writing", "formal_tone", "structured_writing", "verbal"],
    "srs_concept_tag": "communication:email_format",
    "captain_byte": {
        "intro": (
            "🧭 **Captain Byte**\n"
            "“Every placement assessment with a written-communication section expects "
            "the same skeleton: subject, greeting, purpose, three prompt keywords, "
            "polite closing. Master the skeleton and the section becomes automatic. "
            "You do not need fancy words. You need structure.”"
        ),
        "correct": [
            "🧭 **Captain Byte**\n“Nice. Structure first, words second.”",
            "🧭 **Captain Byte**\n“That’s the skeleton. Every good email has it.”",
            "🧭 **Captain Byte**\n“Clean. The rubric rewards this every time.”",
        ],
        "wrong": [
            "🧭 **Captain Byte**\n“Stop. Don’t write yet. What does the rubric reward?”",
            "🧭 **Captain Byte**\n“You’re missing a structural element. Check the skeleton.”",
            "🧭 **Captain Byte**\n“Close, but too casual. Placement emails are formal.”",
        ],
        "after_break": "🧭 **Captain Byte**\n“You identified the missing elements. Now rebuild with the full skeleton.”",
        "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Any prompt, any structure.”",
        "retry_prompt": "🧭 **Captain Byte**\n“Try again. Subject, greeting, purpose, keywords, closing — in that order.”",
    },
    "story_context": {
        "title": "The Professional Letter",
        "narration": (
            "Every placement assessment with a written-communication section expects "
            "the same skeleton: subject, greeting, purpose, three prompt keywords, "
            "polite closing. Master the skeleton and the section becomes automatic."
        ),
        "setting": "letter_office",
        "character": "Captain Byte",
        "intro_text": (
            "You do not need fancy words. You need structure. Subject, greeting, "
            "purpose, all prompt keywords, and closing — in 70–100 words."
        ),
    },
    "discovery": {
        "title": "Read the Skeleton",
        "visual_primitives": ["highlight", "compare", "reveal"],
        "steps": [
            {
                "action": "subject_line",
                "narration": "The subject is a crisp noun phrase, not a sentence.",
                "interaction": {
                    "type": "choose_outcome",
                    "prompt": "Which subject fits a request for a joining date?",
                    "options": [
                        {"id": "a", "text": "Joining Date Request", "correct": True},
                        {"id": "b", "text": "I want to know my joining date", "correct": False},
                        {"id": "c", "text": "Hello", "correct": False},
                        {"id": "d", "text": "Request", "correct": False},
                    ],
                    "explanation": "A crisp noun phrase tells the reader the topic immediately.",
                },
            },
            {
                "action": "greeting",
                "narration": "A formal greeting names the recipient or role.",
                "interaction": {
                    "type": "choose_outcome",
                    "prompt": "Choose the formal greeting.",
                    "options": [
                        {"id": "a", "text": "Dear Sir/Madam,", "correct": True},
                        {"id": "b", "text": "Yo,", "correct": False},
                        {"id": "c", "text": "Hey team,", "correct": False},
                        {"id": "d", "text": "Greetings,", "correct": False},
                    ],
                    "explanation": "Dear Sir/Madam is the standard formal opener for placement emails.",
                },
            },
            {
                "action": "purpose_first",
                "narration": "State the purpose in the first sentence.",
                "interaction": {
                    "type": "choose_outcome",
                    "prompt": "Which opening states purpose first?",
                    "options": [
                        {"id": "a", "text": "I am writing to request my joining date.", "correct": True},
                        {"id": "b", "text": "Hope you are well. Could you tell me my joining date?", "correct": False},
                        {"id": "c", "text": "Please tell me my joining date.", "correct": False},
                        {"id": "d", "text": "Joining date?", "correct": False},
                    ],
                    "explanation": "A clear purpose sentence tells the reader what you want immediately.",
                },
            },
            {
                "action": "keyword_coverage",
                "narration": "The prompt usually names three things you must mention.",
                "interaction": {
                    "type": "choose_outcome",
                    "prompt": "The prompt asks for joining date, location, and reporting time. Which sentence covers all three?",
                    "options": [
                        {"id": "a", "text": "I need my joining date, location, and reporting time.", "correct": True},
                        {"id": "b", "text": "I need my joining date.", "correct": False},
                        {"id": "c", "text": "When do I join?", "correct": False},
                        {"id": "d", "text": "Please send details.", "correct": False},
                    ],
                    "explanation": "One clean sentence can cover all prompt keywords without fluff.",
                },
            },
        ],
        "conclusion": (
            "A placement email is not a letter to a friend. It is a structured request: "
            "subject, greeting, purpose, keywords, polite closing — in that order."
        ),
    },
    "prediction": {
        "title": "Before You Write",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Before you write, predict. Which email satisfies the rubric best?”",
        "question": "A prompt asks for joining date, location, and reporting manager. Which email satisfies the rubric best?",
        "options": [
            {"id": "a", "text": "Subject: Joining Details. Dear Sir/Madam, I am writing to request my joining date, location, and reporting manager. Thank you.", "correct": True, "explanation": "Subject, greeting, purpose, all three keywords, polite close."},
            {"id": "b", "text": "Subject: Help. Hi, can you tell me when I join?", "correct": False, "explanation": "Missing keywords and too casual."},
            {"id": "c", "text": "Joining date?", "correct": False, "explanation": "No structure, no keywords, no politeness."},
            {"id": "d", "text": "Dear Sir, I have a query.", "correct": False, "explanation": "Purpose and keywords are missing."},
        ],
        "explanation": "The rubric rewards structure and keyword coverage, not length.",
    },
    "explain": {
        "title": "Explain the Structure",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Why does placing the purpose in the first sentence improve an email?”",
        "prompt": "Why does placing the purpose in the first sentence improve an email?",
        "answer_format": "short_answer",
        "keywords": ["clear", "first", "reader", "immediately", "purpose", "busy", "quickly", "understand"],
        "min_words": 10,
        "model_answer": (
            "Recruiters read fast. A purpose-first sentence tells them immediately what "
            "you want, so they do not hunt through pleasantries. Busy readers reward "
            "clarity."
        ),
        "intention": "The explanation must connect structure to reader behavior.",
    },
    "guided_build": {
        "title": "Write the Email",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Now you write. Skeleton first, words second.”",
        "steps": [
            {
                "step_order": 1,
                "title": "Subject + Greeting",
                "captain_byte_moment": "🧭 **Captain Byte**\n“Subject is a crisp noun phrase. Greeting is formal. Join them with newlines.”",
                "description": "Return the subject and greeting for a joining-date request.",
                "starter_code": "def email_opening(recipient):\n    # return subject and greeting\n    pass",
                "function_name": "email_opening",
                "signature": "def email_opening(recipient: str) -> str:",
                "test_cases": [
                    {"input": ["HR Manager"], "expected": "Subject: Joining Date Request\nDear HR Manager,"},
                    {"input": ["Sir/Madam"], "expected": "Subject: Joining Date Request\nDear Sir/Madam,"},
                ],
                "hidden_test_cases": [
                    {"input": [""], "expected": "Subject: Joining Date Request\nDear Sir/Madam,"},
                ],
                "diamonds": 30,
                "scaffolded_hints": [
                    {"level": 1, "text": "Subject is a crisp noun phrase."},
                    {"level": 2, "text": "Use Dear <role> or Dear Sir/Madam."},
                    {"level": 3, "text": "Join subject and greeting with newlines."},
                ],
            },
            {
                "step_order": 2,
                "title": "Purpose + Keywords",
                "captain_byte_moment": "🧭 **Captain Byte**\n“One sentence. Purpose first. All three keywords.”",
                "description": "Return a sentence stating purpose and covering three keywords.",
                "starter_code": "def purpose_sentence(keywords):\n    # keywords is a list of 3 strings\n    pass",
                "function_name": "purpose_sentence",
                "signature": "def purpose_sentence(keywords: list) -> str:",
                "test_cases": [
                    {"input": [["joining date", "location", "reporting manager"]], "expected": "I am writing to request my joining date, location, and reporting manager."},
                ],
                "hidden_test_cases": [
                    {"input": [["date", "time", "place"]], "expected": "I am writing to request my date, time, and place."},
                ],
                "diamonds": 35,
                "scaffolded_hints": [
                    {"level": 1, "text": "Start with 'I am writing to request ...'"},
                    {"level": 2, "text": "Join the three keywords with commas and 'and' before the last."},
                    {"level": 3, "text": "Keep it to one sentence."},
                ],
            },
            {
                "step_order": 3,
                "title": "Closing",
                "captain_byte_moment": "🧭 **Captain Byte**\n“Short and polite. Thank you, then your name.”",
                "description": "Return a polite closing with name.",
                "starter_code": "def email_closing(name):\n    # polite closing + name\n    pass",
                "function_name": "email_closing",
                "signature": "def email_closing(name: str) -> str:",
                "test_cases": [
                    {"input": ["Asha"], "expected": "Thank you.\nAsha"},
                    {"input": ["Ravi"], "expected": "Thank you.\nRavi"},
                ],
                "hidden_test_cases": [
                    {"input": [""], "expected": "Thank you.\n"},
                ],
                "diamonds": 30,
                "scaffolded_hints": [
                    {"level": 1, "text": "A standard closing is short and polite."},
                    {"level": 2, "text": "Use 'Thank you.' followed by the name."},
                    {"level": 3, "text": "Newline between closing and name."},
                ],
            },
        ],
    },
    "transfer_challenge": {
        "title": "The Complaint Email",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Same skeleton, different situation. Issue, impact, action — three keywords.”",
        "description": "Write a 70–100 word complaint email about a delayed offer letter, covering issue, impact, and requested action.",
        "function_name": "complaint_email",
        "signature": "def complaint_email(name: str, issue: str, impact: str, action: str) -> str:",
        "description_full": (
            "Return a single string with subject, greeting, body, and closing.\n\n"
            "Example:\n"
            "  complaint_email('Asha', 'delayed offer letter', 'I cannot complete my notice period without it', 'Please release the letter by Friday')\n"
            "  -> 'Subject: Delayed Offer Letter\\nDear Sir/Madam,\\nI am writing about a delayed offer letter. This prevents me from completing my notice period. Please release the letter by Friday.\\nThank you.\\nAsha'"
        ),
        "test_cases": [
            {"input": ["Asha", "delayed offer letter", "I cannot complete my notice period without it", "Please release the letter by Friday"], "expected": "Subject: Delayed Offer Letter\nDear Sir/Madam,\nI am writing about a delayed offer letter. This prevents me from completing my notice period. Please release the letter by Friday.\nThank you.\nAsha"},
        ],
        "hidden_test_cases": [
            {"input": ["Ravi", "wrong joining date", "My travel is booked for the old date", "Please correct the joining date"], "expected": "Subject: Wrong Joining Date\nDear Sir/Madam,\nI am writing about a wrong joining date. My travel is booked for the old date. Please correct the joining date.\nThank you.\nRavi"},
        ],
        "time_limit_minutes": 8,
        "diamonds": 70,
        "scaffolded_hints": [
            {"level": 1, "text": "Keep it under 100 words."},
            {"level": 2, "text": "Use the same skeleton: subject, greeting, purpose, keywords, closing."},
            {"level": 3, "text": "Make the tone polite, not angry."},
        ],
    },
    "assessment": {
        "title": "Professional Letter Final Test",
        "captain_byte_intro": "🧭 **Captain Byte**\n“Prove you know the skeleton. Timed.”",
        "description": "Validate structure, keyword coverage, and tone in three emails.",
        "questions": [
            {
                "type": "concept",
                "question": "Which element must appear first in a formal placement email?",
                "answer_format": "short_answer",
                "keywords": ["subject", "subject line", "topic"],
                "explanation": "The subject line is the first thing the reader sees.",
            },
            {
                "type": "concept",
                "question": "Why is 'Dear Sir/Madam' safer than 'Hi team' in placement emails?",
                "answer_format": "short_answer",
                "keywords": ["formal", "professional", "standard", "polite", "safe"],
                "explanation": "Formal greeting matches placement-email rubrics.",
            },
            {
                "type": "debug",
                "code": "def email(prompt):\n    return prompt\n# should return structured email",
                "error": "email('joining date') must return a structured email, not the raw prompt.",
                "question": "Restructure the response.",
                "fix": "return 'Subject: Joining Date Request\\nDear Sir/Madam,\\nI am writing to request my joining date.\\nThank you.'",
                "explanation": "Raw prompt is not an email. Add subject, greeting, purpose, and closing.",
            },
        ],
        "mastery_threshold": 70,
        "diamonds": 100,
    },
    "break": {
        "title": "The Casual Note",
        "captain_byte_intro": "🧭 **Captain Byte**\n“I gave you a broken email. Identify the missing structural elements.”",
        "story": (
            "A student wrote: 'Yo, send my joining date plz.' The rubric gave zero. "
            "Identify the three missing structural elements."
        ),
        "buggy_code": "def email():\n    return 'Yo, send my joining date plz.'",
        "expected_output": "A structured formal email",
        "actual_output": "Casual text message, not an email",
        "diagnosis": {
            "question": "Which structural elements are missing?",
            "options": [
                {"id": "a", "text": "Subject line, formal greeting, polite closing", "correct": True, "why": "All three are required by the rubric."},
                {"id": "b", "text": "Only the subject line", "correct": False, "why": "Greeting and closing are also missing."},
                {"id": "c", "text": "Only the greeting", "correct": False, "why": "Subject and closing are also missing."},
                {"id": "d", "text": "Nothing is missing; the message is fine", "correct": False, "why": "The rubric requires formal structure."},
            ],
        },
        "fix": "return 'Subject: Joining Date Request\\nDear Sir/Madam,\\nI am writing to request my joining date.\\nThank you.'",
        "fixed_code": "def email():\n    return 'Subject: Joining Date Request\\nDear Sir/Madam,\\nI am writing to request my joining date.\\nThank you.'",
        "explanation": (
            "Placement emails are judged on structure first. Add subject, greeting, "
            "purpose, and closing — every time."
        ),
    },
    "srs_enrollment": {
        "concept_id": "communication:email_format",
        "concept_name": "Professional Email Format",
        "review_intervals": [1, 3, 7, 14, 30],
        "key_points": [
            "subject is a crisp noun phrase",
            "greeting is formal",
            "purpose comes first",
            "cover all prompt keywords",
            "polite closing with name",
        ],
        "spaced_fields": [
            "subject_line",
            "formal_greeting",
            "purpose_first",
            "keyword_coverage",
            "polite_closing",
        ],
    },
    "world_progression": {
        "world_id": "communication_world",
        "competency_id": "email_format",
        "unlocks_next": ["professional_communication"],
        "tower_badge": "professional_letter",
        "world_node": {
            "level": 1,
            "title": "The Professional Letter",
            "color": "sky",
            "icon": "✉️",
            "description": "Write structured, keyword-complete, formally toned emails",
        },
    },
}
