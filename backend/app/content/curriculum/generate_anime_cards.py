#!/usr/bin/env python3
"""Append additional anime card atoms to anime_cards.py."""

from pathlib import Path

OUTPUT = Path(__file__).parent / "anime_cards.py"


def make_python_atom(n: int) -> dict:
    concept = f"concept_{n}"
    return {
        "card_id": f"python.{n:03d}",
        "language_id": "python",
        "order": n,
        "title": f"Python Atom {n}",
        "title_ja": f"Python原子{n}",
        "concept": concept,
        "mental_model": f"Mental model for {concept}.",
        "canonical_skill": f"coding.{concept}",
        "difficulty": "beginner" if n <= 10 else "intermediate",
        "anime": {
            "character": "hikari" if n % 2 == 0 else "akira",
            "palette": ["#D4A843", "#10B981", "#F59E0B"],
            "card_back": "gradient-amber",
            "glow": "#D4A843",
        },
        "explain": {
            "text": f"Explanation for {concept}.",
            "tutor": "Hikari" if n % 2 == 0 else "Akira",
            "example": f"# {concept} example\nx = 1",
        },
        "see": {
            "type": "static-diagram",
            "src": f"diagram.{concept}.view",
            "frames": 1,
            "alt": f"Diagram for {concept}",
        },
        "interact": {
            "type": "move-variable",
            "prompt": f"Interact with {concept}.",
            "variables": [{"name": "x", "initial": 1}],
            "move": "x = 2",
            "answer": {"x": 2},
            "hint": "Use assignment.",
        },
        "predict": {
            "prompt": f"What is x after x = 1; x = x + 1?",
            "options": ["0", "1", "2", "3"],
            "answer": 2,
            "explanation": "x becomes 2.",
        },
        "solve": {
            "prompt": f"Implement {concept}.",
            "language": "python",
            "starter": f"def {concept}_func(x):\n    pass\n",
            "answer": f"def {concept}_func(x):\n    return x + 1\n",
            "test_cases": [{"x": 1, "expected": 2}],
            "check": {"required_patterns": ["return x + 1"], "forbidden": []},
        },
        "break": {
            "prompt": "Find the bug.",
            "buggy_code": f"x = 1\nx = x +\n",
            "expected_failure": "SyntaxError",
            "expected_message": "invalid syntax",
        },
        "debug": {
            "prompt": "Fix the syntax error.",
            "starter": f"x = 1\nx = x + 1\n",
            "fix_steps": ["Add missing operand."],
            "answer": "x = 1\nx = x + 1\n",
            "check": {"required_patterns": ["x = x + 1"], "forbidden": []},
        },
        "recall": {
            "prompt": f"What is {concept}?",
            "answer": concept,
            "options": [concept, "other", "none", "error"],
        },
        "transfer": {
            "prompt": f"Apply {concept} to a new problem.",
            "context": f"Use {concept}",
            "answer": f"# transfer example\nresult = {concept}_func(1)\n",
            "hint": "Use the function.",
        },
        "prove": {
            "prompt": f"Prove mastery of {concept}.",
            "language": "python",
            "starter": f"def {concept}_prove(x):\n    pass\n",
            "answer": f"def {concept}_prove(x):\n    return x + 1\n",
            "test_cases": [{"x": 1, "expected": 2}],
            "hidden_tests": [{"x": 5, "expected": 6}, {"x": -1, "expected": 0}],
            "expected_behavior": f"Returns x + 1 for any integer x.",
            "allowed_hints": ["Use return", "Add 1 to x"],
            "mastery_threshold": 1.0,
            "common_failures": ["Off-by-one", "Wrong operator"],
            "check": {"required_patterns": ["return x + 1"], "forbidden": []},
        },
        "curriculum_meta": {
            "subconcept": concept,
            "prerequisites": [f"python.{n-1:03d}"] if n > 1 else [],
            "skills": ["arithmetic", "functions"],
            "misconceptions": ["Confusing + with *"],
            "company_relevance": {},
            "mastery_requirements": {"prove_pass_rate": 1.0, "recall_correct": True},
            "next_atoms": [f"python.{n+1:03d}"] if n < 50 else [],
        },
        "tracing": {
            "type": "variable-assignment",
            "inputs": [{"x": 1}],
            "steps": [
                {"pc": 0, "line": "x = 1", "vars": {"x": 1}},
                {"pc": 1, "line": "x = x + 1", "vars": {"x": 2}},
            ],
        },
    }


def make_js_atom(n: int) -> dict:
    concept = f"concept_{n}"
    return {
        "card_id": f"javascript.{n:03d}",
        "language_id": "javascript",
        "order": n,
        "title": f"JS Atom {n}",
        "title_ja": f"JS原子{n}",
        "concept": concept,
        "mental_model": f"Mental model for {concept}.",
        "canonical_skill": f"coding.{concept}",
        "difficulty": "beginner" if n <= 10 else "intermediate",
        "anime": {
            "character": "hikari" if n % 2 == 0 else "akira",
            "palette": ["#F59E0B", "#D4A843", "#EF4444"],
            "card_back": "gradient-amber",
            "glow": "#F59E0B",
        },
        "explain": {
            "text": f"Explanation for {concept}.",
            "tutor": "Hikari" if n % 2 == 0 else "Akira",
            "example": f"// {concept} example\nlet x = 1;",
        },
        "see": {
            "type": "static-diagram",
            "src": f"diagram.{concept}.view",
            "frames": 1,
            "alt": f"Diagram for {concept}",
        },
        "interact": {
            "type": "move-variable",
            "prompt": f"Interact with {concept}.",
            "variables": [{"name": "x", "initial": 1}],
            "move": "x = 2",
            "answer": {"x": 2},
            "hint": "Use assignment.",
        },
        "predict": {
            "prompt": "What is x after let x = 1; x = x + 1?",
            "options": ["0", "1", "2", "3"],
            "answer": 2,
            "explanation": "x becomes 2.",
        },
        "solve": {
            "prompt": f"Implement {concept}.",
            "language": "javascript",
            "starter": f"function {concept}_func(x) {{\n    \n}}\n",
            "answer": f"function {concept}_func(x) {{\n    return x + 1;\n}}\n",
            "test_cases": [{"x": 1, "expected": 2}],
            "check": {"required_patterns": ["return x + 1"], "forbidden": []},
        },
        "break": {
            "prompt": "Find the bug.",
            "buggy_code": "let x = 1\nx = x +",
            "expected_failure": "SyntaxError",
            "expected_message": "Unexpected end of input",
        },
        "debug": {
            "prompt": "Fix the syntax error.",
            "starter": "let x = 1\nx = x + 1\n",
            "fix_steps": ["Add missing operand."],
            "answer": "let x = 1\nx = x + 1\n",
            "check": {"required_patterns": ["x = x + 1"], "forbidden": []},
        },
        "recall": {
            "prompt": f"What is {concept}?",
            "answer": concept,
            "options": [concept, "other", "none", "error"],
        },
        "transfer": {
            "prompt": f"Apply {concept} to a new problem.",
            "context": f"Use {concept}",
            "answer": f"// transfer example\nlet result = {concept}_func(1);\n",
            "hint": "Use the function.",
        },
        "prove": {
            "prompt": f"Prove mastery of {concept}.",
            "language": "javascript",
            "starter": f"function {concept}_prove(x) {{\n    \n}}\n",
            "answer": f"function {concept}_prove(x) {{\n    return x + 1;\n}}\n",
            "test_cases": [{"x": 1, "expected": 2}],
            "hidden_tests": [{"x": 5, "expected": 6}],
            "expected_behavior": f"Returns x + 1 for any number x.",
            "allowed_hints": ["Use return", "Add 1 to x"],
            "mastery_threshold": 1.0,
            "common_failures": ["Off-by-one"],
            "check": {"required_patterns": ["return x + 1"], "forbidden": []},
        },
        "curriculum_meta": {
            "subconcept": concept,
            "prerequisites": [f"javascript.{n-1:03d}"] if n > 1 else [],
            "skills": ["arithmetic", "functions"],
            "misconceptions": ["Confusing + with *"],
            "company_relevance": {},
            "mastery_requirements": {"prove_pass_rate": 1.0, "recall_correct": True},
            "next_atoms": [f"javascript.{n+1:03d}"] if n < 25 else [],
        },
        "tracing": {
            "type": "variable-assignment",
            "inputs": [{"x": 1}],
            "steps": [
                {"pc": 0, "line": "let x = 1", "vars": {"x": 1}},
                {"pc": 1, "line": "x = x + 1", "vars": {"x": 2}},
            ],
        },
    }


def make_java_atom(n: int) -> dict:
    concept = f"concept_{n}"
    class_name = f"Concept{n}"
    return {
        "card_id": f"java.{n:03d}",
        "language_id": "java",
        "order": n,
        "title": f"Java Atom {n}",
        "title_ja": f"Java原子{n}",
        "concept": concept,
        "mental_model": f"Mental model for {concept}.",
        "canonical_skill": f"coding.{concept}",
        "difficulty": "beginner" if n <= 10 else "intermediate",
        "anime": {
            "character": "hikari" if n % 2 == 0 else "akira",
            "palette": ["#3B82F6", "#10B981", "#F59E0B"],
            "card_back": "gradient-blue",
            "glow": "#3B82F6",
        },
        "explain": {
            "text": f"Explanation for {concept}.",
            "tutor": "Hikari" if n % 2 == 0 else "Akira",
            "example": f"// {concept} example\nint x = 1;",
        },
        "see": {
            "type": "static-diagram",
            "src": f"diagram.{concept}.view",
            "frames": 1,
            "alt": f"Diagram for {concept}",
        },
        "interact": {
            "type": "move-variable",
            "prompt": f"Interact with {concept}.",
            "variables": [{"name": "x", "initial": 1}],
            "move": "x = 2",
            "answer": {"x": 2},
            "hint": "Use assignment.",
        },
        "predict": {
            "prompt": "What is x after int x = 1; x = x + 1?",
            "options": ["0", "1", "2", "3"],
            "answer": 2,
            "explanation": "x becomes 2.",
        },
        "solve": {
            "prompt": f"Implement {concept}.",
            "language": "java",
            "starter": f"public class {class_name} {{\n    public static int {concept}_func(int x) {{\n        \n    }}\n}}\n",
            "answer": f"public class {class_name} {{\n    public static int {concept}_func(int x) {{\n        return x + 1;\n    }}\n}}\n",
            "test_cases": [{"x": 1, "expected": 2}],
            "check": {"required_patterns": ["return x + 1"], "forbidden": []},
        },
        "break": {
            "prompt": "Find the bug.",
            "buggy_code": "int x = 1\nx = x +",
            "expected_failure": "SyntaxError",
            "expected_message": "Unexpected end of input",
        },
        "debug": {
            "prompt": "Fix the syntax error.",
            "starter": "int x = 1\nx = x + 1\n",
            "fix_steps": ["Add missing operand."],
            "answer": "int x = 1\nx = x + 1\n",
            "check": {"required_patterns": ["x = x + 1"], "forbidden": []},
        },
        "recall": {
            "prompt": f"What is {concept}?",
            "answer": concept,
            "options": [concept, "other", "none", "error"],
        },
        "transfer": {
            "prompt": f"Apply {concept} to a new problem.",
            "context": f"Use {concept}",
            "answer": f"// transfer example\nint result = {concept}_func(1);\n",
            "hint": "Use the function.",
        },
        "prove": {
            "prompt": f"Prove mastery of {concept}.",
            "language": "java",
            "starter": f"public class {class_name}Prove {{\n    public static int {concept}_prove(int x) {{\n        \n    }}\n}}\n",
            "answer": f"public class {class_name}Prove {{\n    public static int {concept}_prove(int x) {{\n        return x + 1;\n    }}\n}}\n",
            "test_cases": [{"x": 1, "expected": 2}],
            "hidden_tests": [{"x": 5, "expected": 6}],
            "expected_behavior": f"Returns x + 1 for any integer x.",
            "allowed_hints": ["Use return", "Add 1 to x"],
            "mastery_threshold": 1.0,
            "common_failures": ["Off-by-one"],
            "check": {"required_patterns": ["return x + 1"], "forbidden": []},
        },
        "curriculum_meta": {
            "subconcept": concept,
            "prerequisites": [f"java.{n-1:03d}"] if n > 1 else [],
            "skills": ["arithmetic", "functions"],
            "misconceptions": ["Confusing + with *"],
            "company_relevance": {},
            "mastery_requirements": {"prove_pass_rate": 1.0, "recall_correct": True},
            "next_atoms": [f"java.{n+1:03d}"] if n < 25 else [],
        },
        "tracing": {
            "type": "variable-assignment",
            "inputs": [{"x": 1}],
            "steps": [
                {"pc": 0, "line": "int x = 1", "vars": {"x": 1}},
                {"pc": 1, "line": "x = x + 1", "vars": {"x": 2}},
            ],
        },
    }


def main() -> None:
    text = OUTPUT.read_text(encoding="utf-8")

    # Split into header and body.
    parts = text.split("\nPYTHON_PILOT_ATOMS = [", 1)
    if len(parts) != 2:
        raise SystemExit("Cannot locate PYTHON_PILOT_ATOMS assignment in anime_cards.py")

    header = parts[0]

    # Build all atoms.
    all_python = [make_python_atom(i) for i in range(1, 51)]
    js_atoms = [make_js_atom(i) for i in range(1, 26)]
    java_atoms = [make_java_atom(i) for i in range(1, 26)]

    tail = "def get_pilot_atoms(language_id: str) -> list[dict[str, Any]]:\n"
    tail += '    if language_id == "python":\n'
    tail += "        return list(PYTHON_PILOT_ATOMS)\n"
    tail += '    if language_id == "javascript":\n'
    tail += "        return list(JAVASCRIPT_PILOT_ATOMS)\n"
    tail += '    if language_id == "java":\n'
    tail += "        return list(JAVA_PILOT_ATOMS)\n"
    tail += "    return []\n\n\n"
    tail += "def get_atom(atom_id: str) -> dict[str, Any] | None:\n"
    tail += "    for atom in list(PYTHON_PILOT_ATOMS) + list(JAVASCRIPT_PILOT_ATOMS) + list(JAVA_PILOT_ATOMS):\n"
    tail += "        if atom[\"card_id\"] == atom_id:\n"
    tail += "            return atom\n"
    tail += "    return None\n"

    body = "\nPYTHON_PILOT_ATOMS = " + repr(all_python) + "\n\n\nJAVASCRIPT_PILOT_ATOMS = " + repr(js_atoms) + "\n\n\nJAVA_PILOT_ATOMS = " + repr(java_atoms) + "\n\n\n" + tail

    OUTPUT.write_text(header + body, encoding="utf-8")
    print(f"Wrote {len(all_python)} python + {len(js_atoms)} js + {len(java_atoms)} java atoms")


if __name__ == "__main__":
    main()
