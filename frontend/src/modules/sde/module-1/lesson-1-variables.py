{
  "id": "module-1-lesson-1",
  "title": "Variables & Types",
  "step": "learn",
  "concept": "Understand primitive data types, type inference, and mutability in Python.",
  "content": "# Variables & Types\n\n## Primitive Types\nPython has several built-in primitive types:\n\n- **int**: Whole numbers (e.g., `42`, `-7`)\n- **float**: Decimal numbers (e.g., `3.14`, `-0.5`)\n- **bool**: True or False values\n- **str**: Sequences of characters (e.g., `\"hello\"`)\n- **None**: Represents absence of value\n\n## Type Inference\nPython is dynamically typed, meaning you don't need to declare types explicitly:\n\n```python\nx = 42          # Automatically becomes int\ny = 3.14       # Automatically becomes float\nname = \"hello\" # Automatically becomes str\nis_active = True # Automatically becomes bool\n```\n\n## Mutability\n- **Immutable types**: int, float, bool, str (cannot be changed after creation)\n- **Mutable types**: list, dict, set (can be modified in place)\n\n## Exercise\nWrite a program that:\n1. Declares variables for your name, age, and a boolean indicating if you're a student\n2. Prints a formatted introduction using these variables\n3. Changes the age variable and prints the updated introduction",
  "concept_check": [
    {
      "question": "Which of the following is an immutable type?",
      "options": ["list", "dict", "str", "set"],
      "answer": "str"
    },
    {
      "question": "What will `x := 5 // 2` produce in Python?",
      "options": ["2.5", "2", "2.0", "Error"],
      "answer": "2"
    }
  ],
  "exercise": {
    "prompt": "Write your solution in the editor below:",
    "template": "```python\n# Your code here\n```",
    "evaluate": "Your code should declare three variables (name, age, is_student) and print a formatted introduction. The code should work without errors.",
    "sample_solution": "```python\nname = \"Alex\"\nage = 21\nis_student = True\n\nprint(f\"Hello, I'm {name} and I'm {age} years old.\")\nprint(f\"I am a student: {is_student}\")\n```"
  },
  "assessment": {
    "questions": [
      {
        "question": "What will be the output of the following code?\n```python\nx = 5\ny = 2.5\nprint(x + y)\n```",
        "options": ["7.5", "7", "Error", "5.5"],
        "answer": "7.5"
      },
      {
        "question": "Which of the following types is mutable?",
        "options": ["int", "float", "str", "list"],
        "answer": "list"
      }
    ]
  }
]