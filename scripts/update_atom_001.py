import json

with open("backend/app/data/python_50_atoms.json", "r", encoding="utf-8") as f:
    d = json.load(f)

a = d["atoms"]["python.001"]

new_atom = {
    "id": a["id"],
    "title": a["title"],
    "concept": a["concept"],
    "prerequisites": a.get("prerequisites", []),
    "misconception_codes": a.get("misconception_codes", []),
    "mental_model": a.get("mental_model", ""),
    "why_this_matters": a.get("why_this_matters", ""),
    "engineering_context": a.get("engineering_context", ""),
    "builds_toward": a.get("builds_toward", ""),
    "service_company_relevance": a.get("service_company_relevance", {}),
    "metaphor_key": a.get("metaphor_key", ""),
    "visual_primitive": a.get("visual_primitive", ""),
    "tutor_tree_id": a.get("tutor_tree_id", ""),
    "estimated_minutes": a.get("estimated_minutes", 10),
    "diamonds": a.get("diamonds", 15),
    "connect": {
        "mode": "story",
        "title": "Why instructions matter",
        "teacher_say": "You are a robot operator. Your robot must deliver 3 packages to 3 desks. But the cards are scrambled. If you miss one step, the robot fails.",
        "problem": "Arrange 6 scrambled instruction cards so the robot delivers all packages correctly.",
        "interaction_type": "reorder-cards",
        "correct_answer": ["PICK package", "MOVE to desk", "DROP package", "PICK package", "MOVE to desk", "DROP package"],
        "success_feedback": "Robot delivers all 3 packages. Every step matters.",
        "failure_feedback": "Robot failed. Think about what must happen first before moving."
    },
    "explain": {
        "mode": "direct-teach",
        "title": "What is a program?",
        "steps": [
            {
                "say": "A program is a precise, ordered list of instructions.",
                "visual": "text",
                "content": "A program = ordered instructions"
            },
            {
                "say": "The computer does exactly what you say, in the order you say it.",
                "visual": "text",
                "content": "Computer follows instructions top-to-bottom"
            },
            {
                "say": "If you change one instruction, everything changes.",
                "visual": "text",
                "content": "One change = different result"
            }
        ],
        "teacher_summary": "A program is a precise, ordered list of instructions. The computer does exactly what you say, in the order you say it."
    },
    "show": {
        "mode": "animation",
        "title": "Watch execution order",
        "animation_key": "instruction_sequence",
        "frames": [
            {"scene": "5 scrambled cards: MOVE, PICK, DROP, MOVE, PICK", "duration_ms": 1000},
            {"scene": "Robot fails in wrong order", "duration_ms": 1500},
            {"scene": "Correct order: PICK -> MOVE -> DROP -> PICK -> MOVE -> DROP", "duration_ms": 1000},
            {"scene": "Robot succeeds: all 3 packages delivered", "duration_ms": 1200}
        ]
    },
    "experience": {
        "mode": "interactive",
        "title": "Try it yourself",
        "instruction": "Change the robot instructions and see what happens.",
        "manipulatives": [
            {
                "type": "instruction-cards",
                "initial": ["MOVE", "PICK", "DROP", "MOVE", "PICK", "DROP"],
                "actions": ["reorder"]
            }
        ]
    },
    "guide": {
        "mode": "scaffold",
        "title": "Write your first program",
        "scaffold_level": "partial",
        "prompt": "Complete the program to print the 3 delivery steps.",
        "starter_code": "# Delivery program\nprint(\"PICK package\")\nprint(\"___ to desk\")\nprint(\"___ package\")",
        "solution": 'print("PICK package")\nprint("MOVE to desk")\nprint("DROP package")',
        "blanks": ["MOVE", "DROP"],
        "hints": [
            "Think about what happens between picking and dropping",
            "The robot must move before dropping"
        ]
    },
    "fade": {
        "mode": "gradual-release",
        "title": "Write it independently",
        "stages": [
            {
                "stage": "full-example",
                "show_code": True,
                "prompt": "This is a complete program. Read it carefully."
            },
            {
                "stage": "partial",
                "show_code": False,
                "starter_code": "# Write 3 instructions\nprint(\"PICK package\")\nprint(\"___\")\nprint(\"___\")",
                "blanks": ["MOVE to desk", "DROP package"]
            },
            {
                "stage": "no-help",
                "show_code": False,
                "starter_code": "# Write the full program\n",
                "blanks": []
            }
        ]
    },
    "transfer": {
        "mode": "new-context",
        "title": "ATM withdrawal",
        "context": "atm_withdrawal",
        "story": "An ATM must verify your PIN, check balance, dispense cash, then print a receipt.",
        "task": "Arrange these 4 steps in the correct order:",
        "options": ["Verify PIN", "Check balance", "Dispense cash", "Print receipt"],
        "correct_order": [0, 1, 2, 3]
    },
    "prove": {
        "mode": "assessment",
        "title": "Prove you understand",
        "tasks": [
            {
                "type": "predict",
                "prompt": "If you swap MOVE and DROP in the robot program, what happens?",
                "answer": "Robot drops before moving, fails"
            },
            {
                "type": "code",
                "prompt": "Write a 3-line program for a robot making tea: boil water, add tea, pour cup.",
                "starter_code": "# Tea robot\n",
                "solution": 'print("Boil water")\nprint("Add tea")\nprint("Pour cup")'
            },
            {
                "type": "debug",
                "buggy_code": 'print("Add tea")\nprint("Pour cup")\nprint("Boil water")',
                "question": "What is wrong?",
                "answer": "Water must boil before adding tea"
            }
        ],
        "passing_score": 80
    }
}

d["atoms"]["python.001"] = new_atom

with open("backend/app/data/python_50_atoms.json", "w", encoding="utf-8") as f:
    json.dump(d, f, indent=2, ensure_ascii=False)

print("Updated python.001 with 8-step teaching modes")
