{
  "id": "module-1-lesson-4",
  "title": "Debugging Basics",
  "step": "learn",
  "concept": "Identify and fix common programming errors.",
  "content": "# Debugging Basics\n\n## Common Runtime Errors\n### Type Error\nOccurs when an operation is applied to an inappropriate type.\n\n```python\nx = \"hello\"\nprint(x + 5)  # TypeError: cannot concatenate str and int\n```\n\n### Name Error\nOccurs when a variable is not defined.\n\n```python\nprint(undefined_variable)  # NameError: name 'undefined_variable' is not defined\n```\n\n### Index Error\nOccurs when accessing an invalid index in a list.\n\n```python\nmy_list = [1, 2, 3]\nprint(my_list[5])  # IndexError: list index out of range\n```\n\n## Debugging Techniques\n### Print Debugging\nAdd `print()` statements to track variable values.\n\n```python\nx = 5\nprint(f\"x is {x}\")\nx = x + 1\nprint(f\"x is now {x}\")\n```\n\n### IDE Debugger\nUse step-over, step-into, and step-out features.\n\n### Console Errors\nRead error messages carefully – they tell you exactly what went wrong and where.\n\n## Exercise\nFind and fix the error in the following code:\n\n```python\nx = 10\ny = \"hello\"\nresult = x + y\nprint(result)\n```\n\n**Fix**: Convert `y` to a string or perform the operation on compatible types.",
  "concept_check": [
    {
      "question": "What type of error occurs when trying to add a string and an integer?",
      "options": ["Type Error", "Name Error", "Index Error", "Value Error"],
      "answer": "Type Error"
    },
    {
      "question": "What will happen if you try to print an undefined variable?",
      "options": ["Nothing", "The program will crash with a Name Error", "The variable will be created", "The program will pause"],
      "answer": "The program will crash with a Name Error"
    }
  ],
  "exercise": {
    "prompt": "Find and fix the error:",
    "template": "```python\n# Broken code\nx = 10\ny = \"hello\"\nresult = x + y\nprint(result)\n```\n\n**Fix**:",
    "sample_fix": "```python\nx = 10\ny = \"hello\"\nresult = x + str(y)  # Convert y to string\nprint(result)  # Output: 10hello\n```"
  },
  "assessment": {
    "questions": [
      {
        "question": "What type of error is shown when accessing an index out of range?",
        "options": ["Type Error", "Name Error", "Index Error", "Key Error"],
      "answer": "Index Error"
    },
    {
      "question": "Which technique involves adding print statements to track variable values?",
      "options": ["Print Debugging", "IDE Debugger", "Console Errors", "Static Analysis"],
      "answer": "Print Debugging"
    }
  ]
}