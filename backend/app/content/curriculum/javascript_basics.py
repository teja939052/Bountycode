"""
Promoted Lesson: JavaScript Basics
==================================

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

LESSON_ID = "javascript_basics_01"
VERSION = "1.0.0"
SKILL_ID = "javascript_variables"
COMPANY_RELEVANCE = ["tcs", "infosys", "wipro", "cognizant", "capgemini", "accenture"]
EST_MINUTES = 18
XP_REWARD = 140

JAVASCRIPT_BASICS_LESSON: Dict[str, Any] = {
    "lesson_id": LESSON_ID,
    "version": VERSION,
    "module_id": "computer_science:javascript_basics",
    "title": "JavaScript Basics",
    "description": "Master JavaScript fundamentals: variables, functions, DOM manipulation, and event handling.",
    "difficulty": "beginner",
    "est_minutes": EST_MINUTES,
    "xp_reward": XP_REWARD,
    "skills_taught": ["javascript_variables", "javascript_functions", "dom_manipulation", "event_handling"],
    "srs_concept_tag": SKILL_ID,
    "company_relevance": COMPANY_RELEVANCE,
    "learning_objectives": [
        "Declare and use variables with var, let, and const.",
        "Write functions with parameters and return values.",
        "Select and manipulate DOM elements.",
        "Handle user events like clicks and input changes.",
        "Read and write JSON data.",
    ],
    "prerequisites": ["cs_html_basics", "cs_css_basics"],
    "concept_explanation": {
        "title": "JavaScript Basics",
        "text": (
            "JavaScript is the programming language of the web. It makes pages interactive: "
            "responding to clicks, updating content without reloading, validating forms, "
            "and fetching data from servers. HTML provides structure, CSS provides style, "
            "and JavaScript provides behavior."
        ),
        "key_formula": "document.getElementById('id').innerHTML = 'new text';",
    },
    "worked_example": {
        "title": "Change text on button click",
        "problem": "Change the text of a paragraph when a button is clicked.",
        "code": "document.getElementById('myBtn').onclick = function() {\n  document.getElementById('demo').innerHTML = 'Hello World!';\n};",
        "expected_output": "Clicking the button changes the paragraph text to 'Hello World!'",
        "explanation": "The onclick event handler runs the function when the button is clicked. document.getElementById finds the element by its ID, and innerHTML changes its content.",
    },
    "interactive_practice": [
        {
            "id": "js_practice_1",
            "type": "mcq",
            "question": "Which keyword declares a variable that cannot be reassigned?",
            "options": ["var", "let", "const", "all of the above"],
            "correct_index": 2,
            "explanation": "const declares a constant that cannot be reassigned. var and let allow reassignment.",
        },
        {
            "id": "js_practice_2",
            "type": "mcq",
            "question": "Which method selects an element by its ID?",
            "options": ["getElementsByClassName", "getElementById", "getElementsByTagName", "querySelectorAll"],
            "correct_index": 1,
            "explanation": "document.getElementById() selects a single element with the matching id attribute.",
        },
    ],
    "misconception_feedback": {
        "var_vs_let": {
            "title": "Common mistake: Confusing var, let, and const",
            "text": "var is function-scoped and hoisted. let and const are block-scoped. const cannot be reassigned.",
        },
        "this_keyword": {
            "title": "Common mistake: Misunderstanding 'this'",
            "text": "The value of 'this' depends on how a function is called, not where it's defined.",
        },
    },
    "assessment": {
        "questions": [
            {
                "id": "js_assess_1",
                "type": "mcq",
                "question": "What does document.getElementById('btn') return?",
                "options": ["All button elements", "The element with id='btn'", "All elements", "The first button element"],
                "correct_index": 1,
                "explanation": "document.getElementById() selects a single element with the matching id attribute.",
            },
            {
                "id": "js_assess_2",
                "type": "mcq",
                "question": "Which event fires when a user clicks an element?",
                "options": ["onchange", "onmouseover", "onclick", "onkeydown"],
                "correct_index": 2,
                "explanation": "onclick fires when the user clicks on an element.",
            },
        ],
    },
    "transfer_task": {
        "title": "Real-world: Toggle button",
        "problem": (
            "Create a button that toggles text between 'ON' and 'OFF' each time it's clicked. "
            "Use a boolean variable to track the current state."
        ),
        "steps": [
            "Create a button element with an id.",
            "Create a boolean variable isOn initialized to false.",
            "Add an onclick handler to the button.",
            "In the handler, toggle isOn and update the button text accordingly.",
        ],
        "code": "let isOn = false;\nbtn.onclick = function() {\n  isOn = !isOn;\n  btn.textContent = isOn ? 'ON' : 'OFF';\n};",
    },
    "deterministic_answer_key": {
        "js_practice_1": 2,
        "js_practice_2": 1,
        "js_assess_1": 1,
        "js_assess_2": 1,
        "transfer_task": "let isOn = false;\nbtn.onclick = function() {\n  isOn = !isOn;\n  btn.textContent = isOn ? 'ON' : 'OFF';\n};",
    },
    "source_provenance": {
        "source": "pattern-relevant",
        "source_urls": [
            "https://developer.mozilla.org/en-US/docs/Web/JavaScript",
            "https://www.w3schools.com/js/",
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
            "step_id": "discovery",
            "step_type": "discover",
            "title": "Why JavaScript?",
            "content": "JavaScript is the programming language of the web. It makes pages interactive: responding to clicks, updating content without reloading, validating forms, and fetching data from servers.",
        },
        {
            "step_id": "manipulate",
            "step_type": "manipulate",
            "content": "Open any webpage, right-click an element, and select 'Inspect' to see its HTML and applied CSS styles.",
            "predict": "What happens when you change an element's color in DevTools?",
        },
        {
            "step_id": "predict",
            "step_type": "predict",
            "content": "What does this JavaScript do?\n\nconst btn = document.getElementById('myBtn');\nbtn.onclick = function() {\n  alert('Hello!');\n};",
            "options": ["Shows an alert when btn is clicked", "Changes the button text", "Refreshes the page", "Does nothing"],
            "correct_index": 0,
        },
        {
            "step_id": "break_debug",
            "step_type": "debug",
            "title": "Find the bug",
            "content": "This code should show an alert when the button is clicked but doesn't work. Why?\n\nbtn.onclick = function() {\n  alert('Hello!');\n};\n\n// Missing: document.getElementById('btn').onclick = ...",
            "bug": "The code tries to use 'btn' variable that is never defined. It needs document.getElementById('btn').",
            "fix": "Add document.getElementById('btn').onclick = before the function assignment.",
            "explanation": "You must first get a reference to the button element using document.getElementById(), then assign the onclick handler to it.",
        },
        {
            "step_id": "transfer",
            "step_type": "transfer",
            "title": "Real-world: Toggle button",
            "problem": (
                "Create a button that toggles text between 'ON' and 'OFF' each time it's clicked. "
                "Use a boolean variable to track the current state."
            ),
            "steps": [
                "Create a button element with an id.",
                "Create a boolean variable isOn initialized to false.",
                "Add an onclick handler to the button.",
                "In the handler, toggle isOn and update the button text accordingly.",
            ],
            "code": "let isOn = false;\nbtn.onclick = function() {\n  isOn = !isOn;\n  btn.textContent = isOn ? 'ON' : 'OFF';\n};",
        },
    ],
}
