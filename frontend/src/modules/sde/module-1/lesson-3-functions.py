{
  "id": "module-1-lesson-3",
  "title": "Functions",
  "step": "learn",
  "concept": "Define reusable functions with parameters and return values.",
  "content": "# Functions\n\n## Function Definition\nA function is a reusable block of code that performs a specific task.\n\n```python\ndef greet(name):\n    return f\"Hello, {name}!\"\n\nresult = greet(\"Alice\")\nprint(result)  # Output: Hello, Alice!\n```\n\n## Parameters & Arguments\nFunctions can accept inputs called parameters.\n\n```python\ndef add(a, b):\n    return a + b\n\nresult = add(3, 5)\nprint(result)  # Output: 8\n```\n\n## Default Parameters\nFunctions can have parameters with default values.\n\n```python\ndef greet(name=\"Guest\"):\n    return f\"Hello, {name}!\"\n\nprint(greet())        # Output: Hello, Guest!\nprint(greet(\"Alice\"))  # Output: Hello, Alice!\n```\n\n## Keyword Arguments\nFunctions can be called with keyword arguments.\n\n```python\ndef power(base, exp=2):\n    return base ** exp\n\nprint(power(2))       # Output: 4 (uses default exp=2)\nprint(power(2, 3))    # Output: 8 (uses exp=3)\n```\n\n## Exercise\nWrite a function that calculates the area of a rectangle given its length and width.\n\n```python\ndef rectangle_area(length, width):\n    return length * width\n\n# Example usage:\nprint(rectangle_area(5, 3))  # Output: 15\n```",
  "concept_check": [
    {
      "question": "What will the following code print?\n```python\ndef greet(name):\n    return f\"Hello, {name}!\"\n\nprint(greet(\"Bob\"))\n```",
      "options": ["Hello, Bob!", \"Error\", \"Hello, \", None],
      "answer": "Hello, Bob!"
    },
    {
      "question": "What is the purpose of a default parameter?",
      "options": ["To make a function required", "To provide a fallback value if no argument is passed", "To delete a parameter", "To rename a parameter"],
      "answer": "To provide a fallback value if no argument is passed"
    }
  ],
  "exercise": {
    "prompt": "Write your solution in the editor below:",
    "template": "```python\n# Your code here\n```",
    "evaluate": "Your function should calculate the area of a rectangle given its length and width. The code should work without errors.",
    "sample_solution": "```python\ndef rectangle_area(length, width):\n    return length * width\n\nprint(rectangle_area(5, 3))  # Output: 15\n```"
  },
  "assessment": {
    "questions": [
      {
        "question": "What will the following code print?\n```python\ndef power(base, exp=2):\n    return base ** exp\n\nprint(power(3))\n```",
      "options": ["3", "6", "9", "Error"],
      "answer": "9"
    },
    {
      "question": "Which of the following is a correct function definition?",
      "options": ["def my_function():", "def my_function: ", "def my_function", "def my_function("],
      "answer": "def my_function():"
    }
  ]
}