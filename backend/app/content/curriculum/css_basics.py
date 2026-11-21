"""
Promoted Lesson: CSS Basics
=======================================

Service-company web development foundation. Follows the full content contract:

- Stable lesson ID, version, canonical skill ID
- Company relevance classification
- Learning objectives, prerequisites
- Concept explanation, worked example
- Interactive practice, misconception-specific feedback
- Assessment, transfer task, deterministic answer key
- Source/provenance metadata, review state, accessibility metadata
- Estimated time, spaced-repetition metadata

Provenance: Pattern-relevant for service-company technical aptitude (TCS, Infosys,
Wipro, Cognizant, Capgemini, Accenture). Not a claim about any private employer
question bank.
"""
from typing import Dict, List, Any

LESSON_ID = "css_basics_01"
VERSION = "1.0.0"
SKILL_ID = "css_selectors"
COMPANY_RELEVANCE = ["tcs", "infosys", "wipro", "cognizant", "capgemini", "accenture"]
EST_MINUTES = 15
XP_REWARD = 120

CSS_BASICS_LESSON: Dict[str, Any] = {
    "lesson_id": LESSON_ID,
    "version": VERSION,
    "module_id": "computer_science:css_basics",
    "title": "CSS Basics",
    "description": "Master CSS fundamentals: selectors, box model, layout, responsive design.",
    "difficulty": "beginner",
    "est_minutes": EST_MINUTES,
    "xp_reward": XP_REWARD,
    "skills_taught": ["css_selectors", "box_model", "flexbox", "responsive_design"],
    "srs_concept_tag": SKILL_ID,
    "company_relevance": COMPANY_RELEVANCE,
    "learning_objectives": [
        "Write CSS selectors to target HTML elements.",
        "Apply CSS properties for color, font, spacing, and layout.",
        "Use the CSS box model (margin, border, padding, content).",
        "Create responsive layouts with Flexbox.",
        "Debug common CSS layout issues.",
    ],
    "prerequisites": ["cs_html_basics"],
    "concept_explanation": {
        "title": "CSS Fundamentals",
        "text": (
            "CSS (Cascading Style Sheets) styles HTML elements. A CSS rule has a "
            "selector that picks elements, and a declaration block with "
            "property:value pairs that define how those elements look."
        ),
        "key_formula": "selector { property: value; }",
    },
    "worked_example": {
        "title": "Style a paragraph",
        "problem": "Make all paragraphs blue with 16px font.",
        "code": "p {\n  color: blue;\n  font-size: 16px;\n}",
        "expected_output": "All paragraph text turns blue with 16px font size.",
        "explanation": "The selector p targets all paragraph elements. The declaration block sets color to blue and font-size to 16px.",
    },
    "interactive_practice": [
        {
            "id": "css_practice_1",
            "type": "mcq",
            "question": "Which CSS property changes text color?",
            "options": ["font-color", "text-color", "color", "text-color-code"],
            "correct_index": 2,
            "explanation": "The CSS property for text color is color, not font-color or text-color.",
        },
        {
            "id": "css_practice_2",
            "type": "mcq",
            "question": "Which selector targets elements with class=\"highlight\"?",
            "options": ["highlight", ".highlight", "#highlight", "element.highlight"],
            "correct_index": 1,
            "explanation": "The dot (.) prefix selects elements by class name: .highlight selects all elements with class=\"highlight\".",
        },
    ],
    "misconception_feedback": {
        "id_vs_class": {
            "title": "Common mistake: Confusing ID and class selectors",
            "text": "Use #id for unique elements and .class for reusable groups. Mixing them up causes styles to not apply as expected.",
        },
        "box_model_confusion": {
            "title": "Common mistake: Margin vs padding",
            "text": "margin creates space outside the border; padding creates space inside the border between content and border.",
        },
    },
    "assessment": {
        "questions": [
            {
                "id": "css_assess_1",
                "type": "mcq",
                "question": "Which property controls the space outside an element's border?",
                "options": ["padding", "margin", "border-spacing", "outline"],
                "correct_index": 1,
                "explanation": "margin creates space outside the border; padding creates space inside the border.",
            },
            {
                "id": "css_assess_2",
                "type": "mcq",
                "question": "What does display: flex do?",
                "options": ["Makes text bold", "Enables flexbox layout", "Changes font to flex", "Hides the element"],
                "correct_index": 1,
                "explanation": "display: flex enables Flexbox layout, a modern CSS layout model for arranging items in a container.",
            },
        ],
    },
    "transfer_task": {
        "title": "Real-world: Style a card component",
        "problem": (
            "Style a card component with: a light gray background, rounded corners, "
            "20px padding, and a subtle shadow. Center the content horizontally."
        ),
        "steps": [
            "Use background-color for the light gray background.",
            "Use border-radius for rounded corners.",
            "Use padding: 20px for internal spacing.",
            "Use box-shadow for the subtle shadow.",
            "Use display: flex with justify-content: center to center horizontally.",
        ],
        "code": ".card {\n  background-color: #f5f5f5;\n  border-radius: 8px;\n  padding: 20px;\n  box-shadow: 0 2px 4px rgba(0,0,0,0.1);\n  display: flex;\n  justify-content: center;\n}",
    },
    "deterministic_answer_key": {
        "css_practice_1": 2,
        "css_practice_2": 1,
        "css_assess_1": 1,
        "css_assess_2": 1,
        "transfer_task": ".card {\n  background-color: #f5f5f5;\n  border-radius: 8px;\n  padding: 20px;\n  box-shadow: 0 2px 4px rgba(0,0,0,0.1);\n  display: flex;\n  justify-content: center;\n}",
    },
    "source_provenance": {
        "source": "pattern-relevant",
        "source_urls": [
            "https://developer.mozilla.org/en-US/docs/Web/CSS",
            "https://www.w3schools.com/css/",
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
    "steps": [
        {
            "id": "discovery",
            "step_type": "discover",
            "title": "Why CSS?",
            "content": "HTML structures content; CSS styles it. Without CSS, every webpage looks like a plain text document from the 1990s.",
        },
        {
            "step_id": "manipulate",
            "step_type": "manipulate",
            "title": "Inspect an element",
            "content": "Open any webpage, right-click an element, and select 'Inspect' to see its HTML and applied CSS styles.",
            "predict": "What happens when you change an element's color in DevTools?",
        },
        {
            "step_id": "predict",
            "step_type": "predict",
            "content": "What does this CSS do?\n\np {\n  color: blue;\n  font-size: 16px;\n}",
            "options": ["Makes all paragraphs blue with 16px font", "Makes the page background blue", "Changes the page title", "Hides paragraphs"],
            "correct_index": 0,
        },
        {
            "step_id": "break_debug",
            "step_type": "debug",
            "title": "Find the bug",
            "content": "This code should make text red but doesn't work. Why?\n\np {\n  colr: red;\n}",
            "bug": "colr is not a valid CSS property name. The correct property name is color.",
            "fix": "Change colr to color",
            "explanation": "CSS property names are case-sensitive and must be spelled exactly correctly.",
        },
        {
            "step_id": "transfer",
            "step_type": "transfer",
            "title": "Real-world: Style a card component",
            "problem": (
                "Style a card component with: a light gray background, rounded corners, "
                "20px padding, and a subtle shadow. Center the content horizontally."
            ),
            "steps": [
                "Use background-color for the light gray background.",
                "Use border-radius for rounded corners.",
                "Use padding: 20px for internal spacing.",
                "Use box-shadow for the subtle shadow.",
                "Use display: flex with justify-content: center to center horizontally.",
            ],
            "code": ".card {\n  background-color: #f5f5f5;\n  border-radius: 8px;\n  padding: 20px;\n  box-shadow: 0 2px 4px rgba(0,0,0,0.1);\n  display: flex;\n  justify-content: center;\n}",
        },
    ],
}
