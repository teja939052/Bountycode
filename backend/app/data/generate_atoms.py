"""Generate the remaining 40 Python atoms for the Concept Clarity Curriculum."""

import json

BASE_ATOMS = {
    "python.001": {
        "id": "python.001",
        "title": "A Computer Follows Instructions",
        "concept": "programs_are_instructions",
        "prerequisites": [],
        "misconception_codes": ["program_is_magic", "computer_guesses"],
        "mental_model": "A program is a precise, ordered list of instructions. The computer does exactly what you say, in the order you say it.",
        "why_this_matters": "Every program is instructions. Understanding this removes fear.",
        "engineering_context": "Production code executes these instructions millions of times. Precision matters.",
        "builds_toward": "All programming",
        "service_company_relevance": {
            "tcs_nqt": {"weight": 10, "intuition_hint": "Flowchart questions"},
            "infosys_infytq": {"weight": 9, "intuition_hint": "Logical sequencing"},
            "wipro_nlth": {"weight": 9, "intuition_hint": "Algorithm tracing"}
        },
        "hook": {"scene": "robot_delivery", "question": "Robot must deliver 3 packages. Cards are scrambled. What first?", "interaction": "reorder-cards"},
        "see": {"animation": "instruction_sequence", "steps": [
            {"scene": "5 scrambled cards: MOVE, PICK, DROP, MOVE, PICK", "duration_ms": 1000},
            {"scene": "Robot fails in wrong order", "duration_ms": 1500},
            {"scene": "Correct order: PICK → MOVE → DROP → PICK → MOVE → DROP", "duration_ms": 1000},
            {"scene": "Robot succeeds: all 3 packages delivered", "duration_ms": 1200}
        ]},
        "interact": [{"type": "drag-reorder", "prompt": "Arrange instructions so robot delivers all 3 packages:", "options": ["PICK package", "MOVE to desk", "DROP package", "PICK package", "MOVE to desk", "DROP package"], "correct": "PICK package", "feedback_correct": "Robot now knows the sequence!", "feedback_wrong": "Robot got confused. Think about what must happen first."}],
        "predict": {"prompt": "If you change 'MOVE' to 'MOVE twice', what happens?", "answer": "Robot overshoots and drops in wrong place", "explanation": "Changing one instruction changes everything."},
        "build": {"language": "python", "starter_code": "# Three instructions\n", "solution": "print('Pick package')\nprint('Move to desk')\nprint('Drop package')", "test_cases": [{"input": [], "expected": "Pick package\nMove to desk\nDrop package"}]},
        "break": {"buggy_code": "print('Pick package')\nprint('Drop package')\nprint('Move to desk')", "expected_failure": "Robot drops before moving", "question": "What's wrong?"},
        "debug": {"fix_steps": ["Move must happen before Drop", "Swap lines 2 and 3"], "answer": "Swap last two lines"},
        "retrieve": {"delay_days": [1, 3, 7], "prompt": "A computer program is...", "answer": "a precise, ordered list of instructions"},
        "transfer": {"context": "atm_withdrawal", "prompt": "ATM must: verify PIN, check balance, dispense cash, print receipt. Arrange correctly.", "answer": "verify PIN → check balance → dispense cash → print receipt"},
        "prove": {"type": "reorder", "passing_score": 80, "requires_explanation": False},
        "mastery": {"prediction": 0.8, "build": 0.8, "transfer": 0.75, "debug": 0.7},
        "estimated_minutes": 8, "diamonds": 15
    },
    "python.002": {
        "id": "python.002",
        "title": "Program vs Result",
        "concept": "instructions_vs_output",
        "prerequisites": ["python.001"],
        "misconception_codes": ["code_is_result", "same_input_same_output"],
        "mental_model": "Same input + different instructions = different output. Code is the recipe; result is the dish.",
        "why_this_matters": "Beginners think code does something magically. The instruction→result chain is foundational.",
        "engineering_context": "Two functions with same name but different logic produce different results. The code IS the difference.",
        "builds_toward": "Functions, debugging, code review",
        "service_company_relevance": {
            "tcs_nqt": {"weight": 8, "intuition_hint": "Output prediction"},
            "infosys_infytq": {"weight": 8, "intuition_hint": "Code snippet output"},
            "wipro_nlth": {"weight": 8, "intuition_hint": "Basic programming logic"}
        },
        "hook": {"scene": "recipe_vs_dish", "question": "Two chefs, same ingredients, different recipes. Same dish?", "interaction": "select-answer"},
        "see": {"animation": "recipe_execution", "steps": [
            {"scene": "Recipe A: boil water. Recipe B: freeze water", "duration_ms": 1200},
            {"scene": "Same ingredient (water) into both", "duration_ms": 800},
            {"scene": "Recipe A produces: hot water", "duration_ms": 800},
            {"scene": "Recipe B produces: ice", "duration_ms": 800}
        ]},
        "interact": [{"type": "predict-output", "prompt": "Change print('Hello') to print('Goodbye'). What changes?", "options": [
            {"id": "a", "text": "Output changes to 'Goodbye'", "correct": True},
            {"id": "b", "text": "Code runs faster", "correct": False},
            {"id": "c", "text": "Nothing changes", "correct": False}
        ], "correct": "a", "feedback_correct": "The instruction changed, so output changed.", "feedback_wrong": "Change the instruction, change the output."}],
        "predict": {"prompt": "What will this output?\nprint(2 + 3)\nprint(2 * 3)", "answer": "5 then 6", "explanation": "Each line executes in order."},
        "build": {"language": "python", "starter_code": "print('Result A:')\n", "solution": "print('Result A:')\nprint(2 + 3)\nprint('Result B:')\nprint(2 * 3)", "test_cases": [{"input": [], "expected": "Result A:\n5\nResult B:\n6"}]},
        "break": {"buggy_code": "print(2 + 3)\nprint('2 * 3')", "expected_failure": "Second line prints text, not 6", "question": "Why doesn't this print 6?"},
        "debug": {"fix_steps": ["Second line is a string, not math", "Remove quotes"], "answer": "Remove quotes to make it calculation"},
        "retrieve": {"delay_days": [1, 3, 7], "prompt": "Code is to output as...", "answer": "recipe is to dish"},
        "transfer": {"context": "shopping_cart", "prompt": "Two discount codes produce different totals from same cart. Why?", "answer": "Different instructions produce different results"},
        "prove": {"type": "output-prediction", "passing_score": 80, "requires_explanation": False},
        "mastery": {"prediction": 0.8, "build": 0.8, "transfer": 0.75, "debug": 0.7},
        "estimated_minutes": 7, "diamonds": 12
    }
}

if __name__ == "__main__":
    with open(r"D:\Project-Fremen\backend\app\data\python_50_atoms.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    data["atoms"].update(BASE_ATOMS)
    with open(r"D:\Project-Fremen\backend\app\data\python_50_atoms.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Updated atoms:", len(data["atoms"]))
