{
  "id": "module-1-lesson-2",
  "title": "Control Flow",
  "step": "learn",
  "concept": "Master if-else statements, loops, and ternary operators for decision making.",
  "content": "# Control Flow\n\n## If-Else Statements\nPython uses standard comparison and logical operators to make decisions.\n\n```python\nx = 10\nif x > 5:\n    print(\"x is greater than 5\")\nelif x == 5:\n    print(\"x is equal to 5\")\nelse:\n    print(\"x is less than 5\")\n```\n\n## Loops\n### For Loops\nIterate over a sequence (list, tuple, string, etc.):\n\n```python\nfruits = [\"apple\", \"banana\", \"cherry\"]\nfor fruit in fruits:\n    print(fruit)\n```\n\n### While Loops\nExecute as long as a condition is true:\n\n```python\ncount = 0\nwhile count < 5:\n    print(count)\n    count += 1\n```\n\n## Ternary Operator\nA concise way to write if-else in a single line:\n\n```python\nage = 18\nstatus = \"adult\" if age >= 18 else \"minor\"\nprint(status)\n```\n\n## Exercise\nWrite a program that:\n1. Asks the user for their age\n2. Determines if they are eligible to vote (age >= 18)\n3. Prints an appropriate message",
  "concept_check": [
    {
      "question": "What will the following code print?\n```python\nx = 5\nif x > 3:\n    print(\"greater\")\nelse:\n    print(\"not greater\")\n```",
      "options": [\"greater\", \"not greater\", \"error\", \"nothing\"],
      "answer": "greater"
    },
    {
      "question": "Which loop will execute as long as a condition is true?",
      "options": ["for loop", "while loop", "foreach loop", "down loop"],
      "answer": "while loop"
    }
  ],
  "exercise": {
    "prompt": "Write your solution in the editor below:",
    "template": "```python\n# Your code here\n```",
    "evaluate": "Your program should ask the user for their age and print whether they are eligible to vote (age >= 18). The code should work without errors.",
    "sample_solution": "```python\nage = int(input(\"Enter your age: \"))\nif age >= 18:\n    print(\"You are eligible to vote.\")\nelse:\n    print(\"You are not eligible to vote yet.\")\n```"
  },
  "assessment": {
    "questions": [
      {
        "question": "What will the following code print?\n```python\nfor i in range(3):\n    print(i)\n```",
      "options": ["0 1 2", "1 2 3", \"Error\", "0 1 2 3"],
      "answer": "0 1 2"
    },
    {
      "question": "What does the ternary operator do?",
      "options": ["Ternary operator is used for looping", "Ternary operator is used for decision making in a single line", "Ternary operator is used for defining functions", "Ternary operator is used for error handling"],
      "answer": "Ternary operator is used for decision making in a single line"
    }
  ]
}