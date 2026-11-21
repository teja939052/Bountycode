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
SKILL_ID = "coding.javascript_basics"
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
        "title": "What is JavaScript?",
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
        "output": "Clicking the button changes the paragraph text to 'Hello World!'",
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
            "explanation": "document.getElementById() selects a single element by its unique ID attribute.",
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
    "assessment": {"questions": [
        {
            "id": "js_assess_1",
            "type": "mcq",
            "question": "What does document.getElementById('btn') return?",
            "options": ["All button elements", "The element with id='btn'", "All elements", "The first button element"],
            "correct_index": 1,
            "explanation": "getElementById returns the single element with the matching id attribute.",
        },
        {
            "id": "js_assess_2",
            "type": "mcq",
            "question": "Which event fires when a user clicks an element?",
            "options": ["onchange", "onmouseover", "onclick", "onkeydown"],
            "correct_index": 2,
            "explanation": "onclick fires when the user clicks on an element.",
        },
    ]},
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
        "answer": "let isOn = false;\nbtn.onclick = function() {\n  isOn = !isOn;\n  btn.textContent = isOn ? 'ON' : 'OFF';\n};",
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
            "content": "HTML structures content, CSS styles it, and JavaScript makes it interactive. Without JavaScript, web pages are static.",
        },
        {
            "step_id": "manipulate",
            "step_type": "manipulate",
            "content": "Open any website, right-click an element, and select 'Inspect'. In the Console tab, type: document.body.style.backgroundColor = 'lightblue' and press Enter.",
            "predict": "What happens to the page background color?",
        },
        {
            "step_id": "predict",
            "step_type": "predict",
            "content": "What does this print?\n\nfunction greet(name) {\n  return 'Hello, ' + name;\n}\nconsole.log(greet('Alice'));",
            "options": ["Hello, Alice", "Hello, undefined", "Hello, name", "Error"],
            "correct_index": 0,
        },
        {
            "step_id": "break_debug",
            "step_type": "debug",
            "title": "Find the bug",
            "content": "This function should return the sum of two numbers but returns undefined. Find the bug:\n\nfunction add(a, b) {\n  a + b;\n}",
            "checks": ["missing return statement"],
        },
        {
            "step_id": "transfer",
            "step_type": "transfer",
            "title": "Transfer: Toggle button",
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
