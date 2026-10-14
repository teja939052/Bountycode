"""Scrimba-style interactive slide lessons.

Each lesson is a sequence of slides.  A slide can mix:
  - narrative text
  - live code snippet
  - interactive prompt (multiple choice / fill-in / run)
  - instant feedback / explanation

This is the canonical source for slide-based depth content.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional


Slide = Dict[str, Any]


def _slide(
    title: str,
    content: str,
    code: str = "",
    language: str = "",
    interaction: Optional[Dict[str, Any]] = None,
    explanation: str = "",
    challenge: str = "",
) -> Slide:
    return {
        "title": title,
        "content": content,
        "code": code,
        "language": language,
        "interaction": interaction,
        "explanation": explanation,
        "challenge": challenge,
    }


def _mcq(question: str, options: List[Dict[str, Any]], explanation: str = "") -> Dict[str, Any]:
    return {"type": "mcq", "question": question, "options": options, "explanation": explanation}


def _fill(question: str, answer: str, hint: str = "") -> Dict[str, Any]:
    return {"type": "fill", "question": question, "answer": answer, "hint": hint}


def _run(description: str, starter: str, expected_output: str, hint: str = "") -> Dict[str, Any]:
    return {
        "type": "run",
        "description": description,
        "starter": starter,
        "expected_output": expected_output,
        "hint": hint,
    }


LANGUAGES = [
    {
        "id": "python",
        "name": "Python",
        "icon": "🐍",
        "version": "3.10+",
        "welcome": "Python is one of the most popular programming languages in the world. It is readable, powerful, and fun.",
        "snippets": {
            "welcome": 'print("Hello, world!")',
            "strings": 'print("Python")',
            "comments": "# This is a comment\nprint(1 + 1)",
            "numbers": "print(2 + 3)\nprint(10 // 3)",
            "variables": 'x = 10\nprint(x)',
            "naming": 'my_score = 95\nprint(my_score)',
            "reassign": 'x = 5\nx = x + 1\nprint(x)',
            "fstrings": 'name = "Ada"\nprint(f"Hello, {name}")',
            "input": 'name = input("Name? ")\nprint(name)',
            "int_cast": 'age = int(input("Age? "))\nprint(age + 1)',
            "boolean": 'is_ready = True\nprint(is_ready)',
            "comparisons": 'print(5 > 3)\nprint(5 == 3)',
            "if": "x = 7\nif x > 5:\n    print('big')",
            "else": "x = 3\nif x > 5:\n    print('big')\nelse:\n    print('small')",
            "elif": "x = 5\nif x < 4:\n    print('low')\nelif x < 7:\n    print('mid')\nelse:\n    print('high')",
            "nested_if": "x = 8\nif x > 5:\n    if x > 7:\n        print('very big')",
            "and_or": 'print(True and False)\nprint(True or False)',
            "not": 'print(not True)\nprint(not False)',
            "for_loop": "for i in range(3):\n    print(i)",
            "range": "for i in range(1, 4):\n    print(i)",
            "while_loop": "i = 0\nwhile i < 3:\n    print(i)\n    i += 1",
            "break": "for i in range(10):\n    if i == 3:\n        break\n    print(i)",
            "continue": "for i in range(5):\n    if i == 2:\n        continue\n    print(i)",
            "list": 'fruits = ["apple", "banana"]\nprint(fruits[0])',
            "list_methods": 'nums = [1, 2]\nnums.append(3)\nprint(nums)',
            "dict": 'student = {"name": "Ada", "age": 20}\nprint(student["name"])',
            "tuple": 'rgb = (255, 0, 0)\nprint(rgb[0])',
            "set": 'values = {1, 2, 2, 3}\nprint(values)',
            "function": "def greet():\n    print('Hello!')\ngreet()",
            "params": "def greet(name):\n    print(f'Hi, {name}')\ngreet('Ada')",
            "return": "def square(x):\n    return x * x\nprint(square(4))",
            "multiple_returns": "def minmax(a, b):\n    return min(a,b), max(a,b)\nprint(minmax(3, 7))",
            "defaults": "def greet(name='friend'):\n    print(f'Hi, {name}')\ngreet()\ngreet('Ada')",
            "lambda": "square = lambda x: x * x\nprint(square(5))",
            "map": "nums = [1, 2, 3]\ndoubled = list(map(lambda x: x*2, nums))\nprint(doubled)",
            "filter": "nums = [1, 2, 3, 4]\nevens = list(filter(lambda x: x % 2 == 0, nums))\nprint(evens)",
            "try_except": "try:\n    x = int('abc')\nexcept ValueError:\n    print('not a number')",
            "raise": "def check(age):\n    if age < 0:\n        raise ValueError('age cannot be negative')",
            "import": "import math\nprint(math.sqrt(16))",
            "from_import": "from math import sqrt\nprint(sqrt(9))",
            "pip": "# Run in terminal:\n# pip install requests",
            "file_read": 'with open("notes.txt", "w") as f:\n    f.write("hello")',
            "file_write": 'with open("notes.txt", "r") as f:\n    print(f.read())',
            "capstone": 'todos = []\nfor i in range(3):\n    todos.append(input("Task? "))\nprint(todos)',
        },
    },
    {
        "id": "javascript",
        "name": "JavaScript",
        "icon": "🟨",
        "version": "ES2022+",
        "welcome": "JavaScript runs in browsers and on servers. It is the language of the web and everywhere else today.",
        "snippets": {
            "welcome": 'console.log("Hello, world!");',
            "strings": 'console.log("JavaScript");',
            "comments": "// This is a comment\nconsole.log(1 + 1);",
            "numbers": "console.log(2 + 3);\nconsole.log(10 / 3);",
            "variables": "let x = 10;\nconsole.log(x);",
            "naming": "let myScore = 95;\nconsole.log(myScore);",
            "reassign": "let x = 5;\nx = x + 1;\nconsole.log(x);",
            "fstrings": "let name = 'Ada';\nconsole.log(`Hello, ${name}`);",
            "input": "// In browser: let name = prompt('Name?');\nconsole.log(name);",
            "int_cast": "let age = parseInt(prompt('Age?'), 10);\nconsole.log(age + 1);",
            "boolean": "let isReady = true;\nconsole.log(isReady);",
            "comparisons": "console.log(5 > 3);\nconsole.log(5 == '5');",
            "if": "let x = 7;\nif (x > 5) {\n  console.log('big');\n}",
            "else": "let x = 3;\nif (x > 5) {\n  console.log('big');\n} else {\n  console.log('small');\n}",
            "elif": "let x = 5;\nif (x < 4) {\n  console.log('low');\n} else if (x < 7) {\n  console.log('mid');\n} else {\n  console.log('high');\n}",
            "nested_if": "let x = 8;\nif (x > 5) {\n  if (x > 7) {\n    console.log('very big');\n  }\n}",
            "and_or": "console.log(true && false);\nconsole.log(true || false);",
            "not": "console.log(!true);\nconsole.log(!false);",
            "for_loop": "for (let i = 0; i < 3; i++) {\n  console.log(i);\n}",
            "range": "for (let i = 1; i < 4; i++) {\n  console.log(i);\n}",
            "while_loop": "let i = 0;\nwhile (i < 3) {\n  console.log(i);\n  i++;\n}",
            "break": "for (let i = 0; i < 10; i++) {\n  if (i === 3) break;\n  console.log(i);\n}",
            "continue": "for (let i = 0; i < 5; i++) {\n  if (i === 2) continue;\n  console.log(i);\n}",
            "list": "let fruits = ['apple', 'banana'];\nconsole.log(fruits[0]);",
            "list_methods": "let nums = [1, 2];\nnums.push(3);\nconsole.log(nums);",
            "dict": "let student = { name: 'Ada', age: 20 };\nconsole.log(student.name);",
            "tuple": "let rgb = [255, 0, 0];\nconsole.log(rgb[0]);",
            "set": "let values = new Set([1, 2, 2, 3]);\nconsole.log(values.size);",
            "function": "function greet() {\n  console.log('Hello!');\n}\ngreet();",
            "params": "function greet(name) {\n  console.log(`Hi, ${name}`);\n}\ngreet('Ada');",
            "return": "function square(x) {\n  return x * x;\n}\nconsole.log(square(4));",
            "multiple_returns": "function minmax(a, b) {\n  return [Math.min(a,b), Math.max(a,b)];\n}\nconsole.log(minmax(3, 7));",
            "defaults": "function greet(name = 'friend') {\n  console.log(`Hi, ${name}`);\n}\ngreet();\ngreet('Ada');",
            "lambda": "const square = x => x * x;\nconsole.log(square(5));",
            "map": "const nums = [1, 2, 3];\nconst doubled = nums.map(x => x * 2);\nconsole.log(doubled);",
            "filter": "const nums = [1, 2, 3, 4];\nconst evens = nums.filter(x => x % 2 === 0);\nconsole.log(evens);",
            "try_except": "try {\n  x = parseInt('abc');\n} catch (e) {\n  console.log('not a number');\n}",
            "raise": "function check(age) {\n  if (age < 0) throw new Error('age cannot be negative');\n}",
            "import": "import _ from 'lodash';\nconsole.log(_.join(['a','b'], '-'));",
            "from_import": "import { sqrt } from 'math';\nconsole.log(sqrt(9));",
            "pip": "# Run in terminal:\n# npm install lodash",
            "file_read": "const fs = require('fs');\nfs.writeFileSync('notes.txt', 'hello');",
            "file_write": "const fs = require('fs');\nconsole.log(fs.readFileSync('notes.txt', 'utf8'));",
            "capstone": "let todos = [];\nfor (let i = 0; i < 3; i++) {\n  todos.push(prompt('Task?'));\n}\nconsole.log(todos);",
        },
    },
    {
        "id": "typescript",
        "name": "TypeScript",
        "icon": "🔷",
        "version": "5.x",
        "welcome": "TypeScript adds optional static types to JavaScript. It catches mistakes before runtime and makes large codebases maintainable.",
        "snippets": {
            "welcome": 'let message: string = "Hello, TypeScript!";\nconsole.log(message);',
            "strings": 'let greeting: string = "TypeScript";\nconsole.log(greeting);',
            "comments": "// This is a comment\nlet x: number = 1 + 1;\nconsole.log(x);",
            "numbers": "let count: number = 2 + 3;\nlet divide: number = 10 / 3;\nconsole.log(count, divide);",
            "variables": 'let score: number = 10;\nconsole.log(score);',
            "naming": 'let myScore: number = 95;\nconsole.log(myScore);',
            "reassign": 'let x: number = 5;\nx = x + 1;\nconsole.log(x);',
            "fstrings": 'let name: string = "Ada";\nconsole.log(`Hello, ${name}`);',
            "input": "// TypeScript is compile-time typed\nlet input: string = 'test';\nconsole.log(input);",
            "int_cast": "let age: number = parseInt('25', 10);\nconsole.log(age + 1);",
            "boolean": "let isReady: boolean = true;\nconsole.log(isReady);",
            "comparisons": "console.log(5 > 3);\nconsole.log(5 === '5');",
            "if": "let x: number = 7;\nif (x > 5) {\n  console.log('big');\n}",
            "else": "let x: number = 3;\nif (x > 5) {\n  console.log('big');\n} else {\n  console.log('small');\n}",
            "elif": "let x: number = 5;\nif (x < 4) {\n  console.log('low');\n} else if (x < 7) {\n  console.log('mid');\n} else {\n  console.log('high');\n}",
            "nested_if": "let x: number = 8;\nif (x > 5) {\n  if (x > 7) {\n    console.log('very big');\n  }\n}",
            "and_or": "console.log(true && false);\nconsole.log(true || false);",
            "not": "console.log(!true);\nconsole.log(!false);",
            "for_loop": "for (let i: number = 0; i < 3; i++) {\n  console.log(i);\n}",
            "range": "for (let i: number = 1; i < 4; i++) {\n  console.log(i);\n}",
            "while_loop": "let i: number = 0;\nwhile (i < 3) {\n  console.log(i);\n  i++;\n}",
            "break": "for (let i: number = 0; i < 10; i++) {\n  if (i === 3) break;\n  console.log(i);\n}",
            "continue": "for (let i: number = 0; i < 5; i++) {\n  if (i === 2) continue;\n  console.log(i);\n}",
            "list": "let fruits: string[] = ['apple', 'banana'];\nconsole.log(fruits[0]);",
            "list_methods": "let nums: number[] = [1, 2];\nnums.push(3);\nconsole.log(nums);",
            "dict": "interface User { name: string; age: number; }\nlet student: User = { name: 'Ada', age: 20 };\nconsole.log(student.name);",
            "tuple": "let rgb: [number, number, number] = [255, 0, 0];\nconsole.log(rgb[0]);",
            "set": "let values: Set<number> = new Set([1, 2, 2, 3]);\nconsole.log(values.size);",
            "function": "function greet(): void {\n  console.log('Hello!');\n}\ngreet();",
            "params": "function greet(name: string): void {\n  console.log(`Hi, ${name}`);\n}\ngreet('Ada');",
            "return": "function square(x: number): number {\n  return x * x;\n}\nconsole.log(square(4));",
            "multiple_returns": "function minmax(a: number, b: number): [number, number] {\n  return [Math.min(a,b), Math.max(a,b)];\n}\nconsole.log(minmax(3, 7));",
            "defaults": "function greet(name: string = 'friend'): void {\n  console.log(`Hi, ${name}`);\n}\ngreet();\ngreet('Ada');",
            "lambda": "const square = (x: number): number => x * x;\nconsole.log(square(5));",
            "map": "const nums: number[] = [1, 2, 3];\nconst doubled: number[] = nums.map(x => x * 2);\nconsole.log(doubled);",
            "filter": "const nums: number[] = [1, 2, 3, 4];\nconst evens: number[] = nums.filter(x => x % 2 === 0);\nconsole.log(evens);",
            "try_except": "try {\n  x = parseInt('abc');\n} catch (e) {\n  console.log('not a number');\n}",
            "raise": "function check(age: number): void {\n  if (age < 0) throw new Error('age cannot be negative');\n}",
            "import": "import _ from 'lodash';\nconsole.log(_.join(['a','b'], '-'));",
            "from_import": "import { sqrt } from 'math';\nconsole.log(sqrt(9));",
            "pip": "# Run in terminal:\n# npm install --save-dev typescript",
            "file_read": "import * as fs from 'fs';\nfs.writeFileSync('notes.txt', 'hello');",
            "file_write": "import * as fs from 'fs';\nconsole.log(fs.readFileSync('notes.txt', 'utf8'));",
            "capstone": "let todos: string[] = [];\nfor (let i = 0; i < 3; i++) {\n  todos.push(prompt('Task?') || '');\n}\nconsole.log(todos);",
        },
    },
    {
        "id": "react",
        "name": "React",
        "icon": "⚛️",
        "version": "18+",
        "welcome": "React is a component-driven UI library. You build small reusable pieces and compose them into full interfaces.",
        "snippets": {
            "welcome": "function App() {\n  return <h1>Hello, React!</h1>;\n}",
            "strings": "function Greeting() {\n  return <p>Hello, React!</p>;\n}",
            "comments": "// JSX comments use {/* */}\nfunction App() {\n  return (\n    <div>\n      {/* comment */}\n      <h1>Hello</h1>\n    </div>\n  );\n}",
            "numbers": "function Counter() {\n  const [count, setCount] = useState(0);\n  return <button onClick={() => setCount(count + 1)}>{count}</button>;\n}",
            "variables": "function App() {\n  const name = 'React';\n  return <h1>Hello, {name}</h1>;\n}",
            "naming": "const UserProfile = ({ user }) => {\n  return <div>{user.name}</div>;\n};",
            "reassign": "function Counter() {\n  const [count, setCount] = useState(0);\n  return <button onClick={() => setCount(count + 1)}>{count}</button>;\n}",
            "fstrings": "function Greeting({ name }) {\n  return <p>Hello, {name}!</p>;\n}",
            "input": "function Search() {\n  const [query, setQuery] = useState('');\n  return <input value={query} onChange={e => setQuery(e.target.value)} />;\n}",
            "int_cast": "function AgeInput() {\n  const [age, setAge] = useState(0);\n  return <input type='number' onChange={e => setAge(Number(e.target.value))} />;\n}",
            "boolean": "function Toggle() {\n  const [on, setOn] = useState(false);\n  return <button onClick={() => setOn(!on)}>{on ? 'ON' : 'OFF'}</button>;\n}",
            "comparisons": "function Status({ score }) {\n  return <p>{score >= 60 ? 'Pass' : 'Fail'}</p>;\n}",
            "if": "function Message({ type }) {\n  if (type === 'error') {\n    return <div className='error'>Error</div>;\n  }\n  return <div>OK</div>;\n}",
            "else": "function Message({ type }) {\n  if (type === 'error') {\n    return <div className='error'>Error</div>;\n  } else {\n    return <div>OK</div>;\n  }\n}",
            "elif": "function Grade({ score }) {\n  if (score >= 90) {\n    return <span>A</span>;\n  } else if (score >= 80) {\n    return <span>B</span>;\n  } else {\n    return <span>C</span>;\n  }\n}",
            "nested_if": "function UserBadge({ user }) {\n  if (user.isActive) {\n    if (user.isAdmin) {\n      return <span>Admin</span>;\n    }\n    return <span>Active</span>;\n  }\n  return <span>Inactive</span>;\n}",
            "and_or": "function Alert({ type, show }) {\n  return show && (type === 'error' || type === 'warning') && <div>Alert</div>;\n}",
            "not": "function Hidden({ visible, children }) {\n  return !visible ? null : <div>{children}</div>;\n}",
            "for_loop": "function List({ items }) {\n  return (\n    <ul>\n      {items.map((item, i) => <li key={i}>{item}</li>)}\n    </ul>\n  );\n}",
            "range": "function List({ items }) {\n  return (\n    <ul>\n      {items.map((item, i) => <li key={i}>{item}</li>)}\n    </ul>\n  );\n}",
            "while_loop": "// React uses map instead of while loops",
            "break": "function List({ items }) {\n  return (\n    <ul>\n      {items.filter(item => item).map((item, i) => <li key={i}>{item}</li>)}\n    </ul>\n  );\n}",
            "continue": "function List({ items }) {\n  return (\n    <ul>\n      {items.filter(item => item).map((item, i) => <li key={i}>{item}</li>)}\n    </ul>\n  );\n}",
            "list": "function FruitList() {\n  const fruits = ['apple', 'banana'];\n  return <p>First: {fruits[0]}</p>;\n}",
            "list_methods": "function List() {\n  const nums = [1, 2];\n  nums.push(3);\n  return <p>{nums.join(', ')}</p>;\n}",
            "dict": "function User() {\n  const user = { name: 'Ada', age: 20 };\n  return <p>{user.name}</p>;\n}",
            "tuple": "function Color() {\n  const rgb = [255, 0, 0];\n  return <p>R: {rgb[0]}</p>;\n}",
            "set": "function Unique() {\n  const values = new Set([1, 2, 2, 3]);\n  return <p>Count: {values.size}</p>;\n}",
            "function": "function Greeting() {\n  return <h1>Hello!</h1>;\n}",
            "params": "function Greeting({ name }) {\n  return <h1>Hello, {name}</h1>;\n}",
            "return": "function Square({ x }) {\n  return <p>{x * x}</p>;\n}",
            "multiple_returns": "function MinMax({ a, b }) {\n  return <p>Min: {Math.min(a,b)}, Max: {Math.max(a,b)}</p>;\n}",
            "defaults": "function Greeting({ name = 'friend' }) {\n  return <p>Hello, {name}</p>;\n}",
            "lambda": "const Square = ({ x }) => <p>{x * x}</p>;",
            "map": "function List({ items }) {\n  return <ul>{items.map(i => <li key={i}>{i}</li>)}</ul>;\n}",
            "filter": "function DoneList({ items }) {\n  return <ul>{items.filter(i => i.done).map(i => <li key={i.id}>{i.text}</li>)}</ul>;\n}",
            "try_except": "// React error boundaries are class components",
            "raise": "// React handles errors with error boundaries",
            "import": "import React from 'react';\nimport ReactDOM from 'react-dom';\nconsole.log('React loaded');",
            "from_import": "import { useState } from 'react';\nconsole.log('useState imported');",
            "pip": "# Create React App:\n# npx create-react-app my-app",
            "file_read": "// In React, use fetch or axios for file reads",
            "file_write": "// In React, state updates trigger re-renders",
            "capstone": "function TodoApp() {\n  const [todos, setTodos] = useState<string[]>([]);\n  const add = () => setTodos([...todos, prompt('Task?') || '']);\n  return (\n    <div>\n      <button onClick={add}>Add</button>\n      <ul>{todos.map((t, i) => <li key={i}>{t}</li>)}</ul>\n    </div>\n  );\n}",
        },
    },
    {
        "id": "node",
        "name": "Node.js",
        "icon": "🟢",
        "version": "20+",
        "welcome": "Node.js brings JavaScript to the server. Build APIs, handle files, and manage databases with the same language you use in the browser.",
        "snippets": {
            "welcome": "console.log('Hello from Node.js!');",
            "strings": "console.log('Node.js');",
            "comments": "// This is a comment\nconsole.log(1 + 1);",
            "numbers": "console.log(2 + 3);\nconsole.log(Math.floor(10 / 3));",
            "variables": "const port = 3000;\nconsole.log(port);",
            "naming": "const PORT = 3000;\nconsole.log(PORT);",
            "reassign": "let count = 0;\ncount = count + 1;\nconsole.log(count);",
            "fstrings": "const name = 'Ada';\nconsole.log(`Hello, ${name}`);",
            "input": "const readline = require('readline');\nconst rl = readline.createInterface({ input: process.stdin });\nrl.question('Name? ', (answer) => {\n  console.log(answer);\n  rl.close();\n});",
            "int_cast": "const age = parseInt(process.argv[2], 10);\nconsole.log(age + 1);",
            "boolean": "const isReady = true;\nconsole.log(isReady);",
            "comparisons": "console.log(5 > 3);\nconsole.log(5 == '5');",
            "if": "const x = 7;\nif (x > 5) {\n  console.log('big');\n}",
            "else": "const x = 3;\nif (x > 5) {\n  console.log('big');\n} else {\n  console.log('small');\n}",
            "elif": "const x = 5;\nif (x < 4) {\n  console.log('low');\n} else if (x < 7) {\n  console.log('mid');\n} else {\n  console.log('high');\n}",
            "nested_if": "const x = 8;\nif (x > 5) {\n  if (x > 7) {\n    console.log('very big');\n  }\n}",
            "and_or": "console.log(true && false);\nconsole.log(true || false);",
            "not": "console.log(!true);\nconsole.log(!false);",
            "for_loop": "for (let i = 0; i < 3; i++) {\n  console.log(i);\n}",
            "range": "for (let i = 1; i < 4; i++) {\n  console.log(i);\n}",
            "while_loop": "let i = 0;\nwhile (i < 3) {\n  console.log(i);\n  i++;\n}",
            "break": "for (let i = 0; i < 10; i++) {\n  if (i === 3) break;\n  console.log(i);\n}",
            "continue": "for (let i = 0; i < 5; i++) {\n  if (i === 2) continue;\n  console.log(i);\n}",
            "list": "const fruits = ['apple', 'banana'];\nconsole.log(fruits[0]);",
            "list_methods": "const nums = [1, 2];\nnums.push(3);\nconsole.log(nums);",
            "dict": "const user = { name: 'Ada', age: 20 };\nconsole.log(user.name);",
            "tuple": "const rgb = [255, 0, 0];\nconsole.log(rgb[0]);",
            "set": "const values = new Set([1, 2, 2, 3]);\nconsole.log(values.size);",
            "function": "function greet() {\n  console.log('Hello!');\n}\ngreet();",
            "params": "function greet(name) {\n  console.log(`Hi, ${name}`);\n}\ngreet('Ada');",
            "return": "function square(x) {\n  return x * x;\n}\nconsole.log(square(4));",
            "multiple_returns": "function minmax(a, b) {\n  return [Math.min(a,b), Math.max(a,b)];\n}\nconsole.log(minmax(3, 7));",
            "defaults": "function greet(name = 'friend') {\n  console.log(`Hi, ${name}`);\n}\ngreet();\ngreet('Ada');",
            "lambda": "const square = x => x * x;\nconsole.log(square(5));",
            "map": "const nums = [1, 2, 3];\nconst doubled = nums.map(x => x * 2);\nconsole.log(doubled);",
            "filter": "const nums = [1, 2, 3, 4];\nconst evens = nums.filter(x => x % 2 === 0);\nconsole.log(evens);",
            "try_except": "try {\n  x = parseInt('abc');\n} catch (e) {\n  console.log('not a number');\n}",
            "raise": "function check(age) {\n  if (age < 0) throw new Error('age cannot be negative');\n}",
            "import": "import _ from 'lodash';\nconsole.log(_.join(['a','b'], '-'));",
            "from_import": "import { sqrt } from 'math';\nconsole.log(sqrt(9));",
            "pip": "# Run in terminal:\n# npm install express",
            "file_read": "const fs = require('fs');\nconst content = fs.readFileSync('notes.txt', 'utf8');\nconsole.log(content);",
            "file_write": "const fs = require('fs');\nfs.writeFileSync('notes.txt', 'hello');\nconsole.log('written');",
            "capstone": "const http = require('http');\nconst todos = [];\nconst server = http.createServer((req, res) => {\n  if (req.url === '/todos') {\n    res.end(JSON.stringify(todos));\n  }\n});\nserver.listen(3000, () => console.log('Server running'));",
        },
    },
    {
        "id": "sql",
        "name": "SQL",
        "icon": "🗄️",
        "version": "ANSI SQL",
        "welcome": "SQL is the language of data. Learn to model, query, and transform data with SELECT, JOINs, and aggregates.",
        "snippets": {
            "welcome": "SELECT 'Hello, SQL!' AS greeting;",
            "strings": "SELECT 'SQL' AS language;",
            "comments": "-- This is a comment\nSELECT 1 + 1;",
            "numbers": "SELECT 2 + 3;\nSELECT 10 / 3;",
            "variables": "-- SQL uses DECLARE or WITH for variables\nWITH x AS (SELECT 10 AS val)\nSELECT * FROM x;",
            "naming": "SELECT \n  10 AS my_score\n;",
            "reassign": "-- SQL does not have variables in basic SELECT\nSELECT 5 AS a, 5 AS b;",
            "fstrings": "SELECT 'Hello, ' || 'SQL' AS greeting;",
            "input": "-- Parameters in prepared statements\nSELECT * FROM users WHERE id = ?;",
            "int_cast": "SELECT CAST('25' AS INTEGER) + 1;",
            "boolean": "SELECT true AS is_ready;",
            "comparisons": "SELECT 5 > 3;\nSELECT 5 = '5';",
            "if": "SELECT CASE WHEN 5 > 3 THEN 'big' END;",
            "else": "SELECT CASE WHEN 5 > 3 THEN 'big' ELSE 'small' END;",
            "elif": "SELECT CASE WHEN 5 < 4 THEN 'low' WHEN 5 < 7 THEN 'mid' ELSE 'high' END;",
            "nested_if": "SELECT CASE WHEN 5 > 3 THEN CASE WHEN 5 > 4 THEN 'very big' END END;",
            "and_or": "SELECT true AND false;\nSELECT true OR false;",
            "not": "SELECT NOT true;\nSELECT NOT false;",
            "for_loop": "-- SQL uses set operations instead of loops\nSELECT generate_series(1, 3) AS i;",
            "range": "SELECT generate_series(1, 3) AS i;",
            "while_loop": "-- SQL is set-based, not loop-based",
            "break": "-- SQL filters with WHERE instead of break",
            "continue": "-- SQL filters with WHERE instead of continue",
            "list": "SELECT ARRAY['apple', 'banana'] AS fruits;\nSELECT fruits[1] FROM ARRAY['apple', 'banana'] AS fruits;",
            "list_methods": "SELECT ARRAY[1, 2] || 3 AS nums;",
            "dict": "SELECT json_build_object('name', 'Ada', 'age', 20) AS student;",
            "tuple": "SELECT (255, 0, 0) AS rgb;",
            "set": "SELECT ARRAY[1, 2, 2, 3] AS values;",
            "function": "CREATE FUNCTION greet() RETURNS text AS $$\nBEGIN\n  RETURN 'Hello!';\nEND;\n$$ LANGUAGE plpgsql;",
            "params": "CREATE FUNCTION greet(name text) RETURNS text AS $$\nBEGIN\n  RETURN 'Hi, ' || name;\nEND;\n$$ LANGUAGE plpgsql;",
            "return": "CREATE FUNCTION square(x int) RETURNS int AS $$\nBEGIN\n  RETURN x * x;\nEND;\n$$ LANGUAGE plpgsql;",
            "multiple_returns": "SELECT LEAST(3, 7) AS min, GREATEST(3, 7) AS max;",
            "defaults": "CREATE FUNCTION greet(name text DEFAULT 'friend') RETURNS text AS $$\nBEGIN\n  RETURN 'Hi, ' || name;\nEND;\n$$ LANGUAGE plpgsql;",
            "lambda": "-- SQL uses inline expressions\nSELECT (x => x * x)(5);",
            "map": "SELECT array_agg(x * 2) FROM (SELECT 1 AS x UNION ALL SELECT 2 UNION ALL SELECT 3) t;",
            "filter": "SELECT * FROM (SELECT 1 AS x UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4) t WHERE x % 2 = 0;",
            "try_except": "BEGIN;\n  -- transaction\nEXCEPTION\n  WHEN division_by_zero THEN\n    ROLLBACK;\nEND;",
            "raise": "RAISE EXCEPTION 'age cannot be negative';",
            "import": "CREATE EXTENSION IF NOT EXISTS pg_trgm;",
            "from_import": "SELECT sqrt(9);",
            "pip": "-- Install PostgreSQL client:\n-- npm install pg",
            "file_read": "SELECT pg_read_file('notes.txt');",
            "file_write": "-- COPY loads data from files\nCOPY users FROM '/path/to/users.csv' CSV HEADER;",
            "capstone": "CREATE TABLE todos (id serial PRIMARY KEY, task text);\nINSERT INTO todos (task) VALUES ('Learn SQL');\nSELECT * FROM todos;",
        },
    },
    {
        "id": "c",
        "name": "C Programming",
        "icon": "⚙️",
        "version": "C11",
        "welcome": "C is the foundation of modern systems programming. Learn pointers, memory management, and how computers really work.",
        "snippets": {
            "welcome": r'#include <stdio.h>\nint main() {\n  printf("Hello, world!\\n");\n  return 0;\n}',
            "strings": r'#include <stdio.h>\nint main() {\n  char lang[] = "C";\n  printf("%s\\n", lang);\n  return 0;\n}',
            "comments": "// This is a comment\\n#include <stdio.h>\\nint main() {\\n  printf(\"%d\\\\n\", 1 + 1);\\n  return 0;\\n}",
            "numbers": r"#include <stdio.h>\nint main() {\n  printf(\"%d\\n\", 2 + 3);\n  printf(\"%d\\n\", 10 / 3);\n  return 0;\n}",
            "variables": r"int x = 10;\nprintf(\"%d\\n\", x);",
            "naming": r"int my_score = 95;\nprintf(\"%d\\n\", my_score);",
            "reassign": r"int x = 5;\nx = x + 1;\nprintf(\"%d\\n\", x);",
            "fstrings": r"char name[] = \"Ada\";\nprintf(\"Hello, %s\\n\", name);",
            "input": r"char name[50];\nprintf(\"Name? \");\nscanf(\"%s\", name);\nprintf(\"%s\\n\", name);",
            "int_cast": r"int age;\nprintf(\"Age? \");\nscanf(\"%d\", &age);\nprintf(\"%d\\n\", age + 1);",
            "boolean": r"#include <stdbool.h>\nbool isReady = true;\nprintf(\"%s\\n\", isReady ? \"true\" : \"false\");",
            "comparisons": r"printf(\"%d\\n\", 5 > 3);\nprintf(\"%d\\n\", 5 == 3);",
            "if": r"int x = 7;\nif (x > 5) {\n  printf(\"big\\n\");\n}",
            "else": r"int x = 3;\nif (x > 5) {\n  printf(\"big\\n\");\n} else {\n  printf(\"small\\n\");\n}",
            "elif": r"int x = 5;\nif (x < 4) {\n  printf(\"low\\n\");\n} else if (x < 7) {\n  printf(\"mid\\n\");\n} else {\n  printf(\"high\\n\");\n}",
            "nested_if": r"int x = 8;\nif (x > 5) {\n  if (x > 7) {\n    printf(\"very big\\n\");\n  }\n}",
            "and_or": r"printf(\"%d\\n\", true && false);\nprintf(\"%d\\n\", true || false);",
            "not": r"printf(\"%d\\n\", !true);\nprintf(\"%d\\n\", !false);",
            "for_loop": r"for (int i = 0; i < 3; i++) {\n  printf(\"%d\\n\", i);\n}",
            "range": r"for (int i = 1; i < 4; i++) {\n  printf(\"%d\\n\", i);\n}",
            "while_loop": r"int i = 0;\nwhile (i < 3) {\n  printf(\"%d\\n\", i);\n  i++;\n}",
            "break": r"for (int i = 0; i < 10; i++) {\n  if (i == 3) break;\n  printf(\"%d\\n\", i);\n}",
            "continue": r"for (int i = 0; i < 5; i++) {\n  if (i == 2) continue;\n  printf(\"%d\\n\", i);\n}",
            "list": r"int fruits[] = {1, 2};\nprintf(\"%d\\n\", fruits[0]);",
            "list_methods": r"int nums[] = {1, 2};\n// C arrays have fixed size; use memcpy or loops to 'append'\nprintf(\"%d\\n\", nums[0]);",
            "dict": r"// C has no built-in dictionaries; use structs or implement hash tables",
            "tuple": r"int rgb[] = {255, 0, 0};\nprintf(\"%d\\n\", rgb[0]);",
            "set": r"// C has no built-in sets; implement with arrays or linked lists",
            "function": r"void greet() {\n  printf(\"Hello!\\n\");\n}\nint main() {\n  greet();\n  return 0;\n}",
            "params": r"void greet(char name[]) {\n  printf(\"Hi, %s\\n\", name);\n}\nint main() {\n  greet(\"Ada\");\n  return 0;\n}",
            "return": r"int square(int x) {\n  return x * x;\n}\nint main() {\n  printf(\"%d\\n\", square(4));\n  return 0;\n}",
            "multiple_returns": r"// C does not have native multiple returns; use struct or pointers\nvoid minmax(int a, int b, int *min, int *max) {\n  *min = a < b ? a : b;\n  *max = a > b ? a : b;\n}",
            "defaults": r"// C does not support default parameters natively; use macros or overloading",
            "lambda": r"// C does not have lambdas natively (C11 has generic selections)",
            "map": r"// C uses loops for mapping\nint nums[] = {1, 2, 3};\nfor (int i = 0; i < 3; i++) nums[i] *= 2;",
            "filter": r"// C uses loops for filtering\nint nums[] = {1, 2, 3, 4};\nfor (int i = 0; i < 4; i++) {\n  if (nums[i] % 2 == 0) printf(\"%d\\n\", nums[i]);\n}",
            "try_except": r"// C has no built-in exceptions; use error codes or setjmp/longjmp",
            "raise": r"// C uses error codes or abort() for fatal errors",
            "import": r"#include <math.h>\nprintf(\"%f\\n\", sqrt(16.0));",
            "from_import": r"#include <stdio.h>\nprintf(\"%d\\n\", abs(-5));",
            "pip": r"# Compile C files:\n# gcc program.c -o program",
            "file_read": r'FILE *f = fopen("notes.txt", "r");\nchar buf[100];\nfgets(buf, sizeof(buf), f);\nprintf("%s", buf);\nfclose(f);',
            "file_write": r'FILE *f = fopen("notes.txt", "w");\nfprintf(f, "hello");\nfclose(f);',
            "capstone": r'#include <stdio.h>\n#include <string.h>\n\nint main() {\n  char todos[3][50];\n  for (int i = 0; i < 3; i++) {\n    printf("Task? ");\n    scanf("%s", todos[i]);\n  }\n  for (int i = 0; i < 3; i++) {\n    printf("%d: %s\\n", i+1, todos[i]);\n  }\n  return 0;\n}',
        },
    },
]


def _interaction_for_slide(
    key: str,
    title: str,
    snippet: str,
    language: str,
) -> Optional[Dict[str, Any]]:
    """Attach a context-aware interaction to a slide."""
    if not snippet and key != "welcome":
        return None

    py_snippet = snippet
    js_snippet = snippet
    ts_snippet = snippet
    c_snippet = snippet
    for lang in LANGUAGES:
        if lang["id"] == "python":
            py_snippet = lang["snippets"].get(key, "")
        elif lang["id"] == "javascript":
            js_snippet = lang["snippets"].get(key, "")
        elif lang["id"] == "typescript":
            ts_snippet = lang["snippets"].get(key, "")
        elif lang["id"] == "c":
            c_snippet = lang["snippets"].get(key, "")

    if key == "welcome":
        return _run(
            description="Run the code to see the output",
            starter=snippet,
            expected_output="Hello, world!",
            hint="Click the play button to execute the code.",
        )
    if key == "strings":
        return _mcq(
            question="How do you create a string?",
            options=[
                {"label": "my_str = 42", "correct": False},
                {"label": "my_str = 'hello'", "correct": True},
                {"label": "my_str = True", "correct": False},
                {"label": "my_str = [1, 2]", "correct": False},
            ],
            explanation="Strings are created using quotes.",
        )
    if key == "comments":
        return _mcq(
            question="What does a comment do?",
            options=[
                {"label": "Runs code", "correct": False},
                {"label": "Explains code to humans", "correct": True},
                {"label": "Compiles code", "correct": False},
                {"label": "Saves files", "correct": False},
            ],
            explanation="Comments explain why, not what.",
        )
    if key == "numbers":
        return _mcq(
            question="What is 10 // 3 in Python?",
            options=[
                {"label": "3.33", "correct": False},
                {"label": "3", "correct": True},
                {"label": "1", "correct": False},
                {"label": "33", "correct": False},
            ],
            explanation="// is integer division (floor division).",
        )
    if key == "variables":
        return _fill(
            question="Complete: x = ____",
            answer="10",
            hint="Variables store values.",
        )
    if key == "naming":
        return _mcq(
            question="Which is a good variable name?",
            options=[
                {"label": "x", "correct": False},
                {"label": "my_score", "correct": True},
                {"label": "a", "correct": False},
                {"label": "xx1", "correct": False},
            ],
            explanation="Use descriptive names like snake_case.",
        )
    if key == "reassign":
        return _mcq(
            question="Can a variable be reassigned?",
            options=[
                {"label": "No, never", "correct": False},
                {"label": "Yes, variables can change", "correct": True},
                {"label": "Only once", "correct": False},
                {"label": "Only in functions", "correct": False},
            ],
            explanation="Most variables can be reassigned.",
        )
    if key == "fstrings":
        return _fill(
            question="Complete: f'Hello, {____}'",
            answer="name",
            hint="Use curly braces to embed expressions.",
        )
    if key == "input":
        return _fill(
            question="Complete: name = ____('Name? ')",
            answer="input",
            hint="input() reads from the user.",
        )
    if key == "int_cast":
        return _fill(
            question="Complete: age = ____(input('Age? '))",
            answer="int",
            hint="int() converts a string to an integer.",
        )
    if key == "boolean":
        return _mcq(
            question="What are boolean values?",
            options=[
                {"label": "0 and 1", "correct": False},
                {"label": "True and False", "correct": True},
                {"label": "yes and no", "correct": False},
                {"label": "on and off", "correct": False},
            ],
            explanation="Booleans have two values: True and False.",
        )
    if key == "comparisons":
        return _mcq(
            question="What does 5 > 3 return?",
            options=[
                {"label": "False", "correct": False},
                {"label": "True", "correct": True},
                {"label": "None", "correct": False},
                {"label": "Error", "correct": False},
            ],
            explanation="5 is greater than 3, so it returns True.",
        )
    if key == "if":
        return _mcq(
            question="When does the if body run?",
            options=[
                {"label": "Always", "correct": False},
                {"label": "When the condition is True", "correct": True},
                {"label": "Never", "correct": False},
                {"label": "Only in loops", "correct": False},
            ],
            explanation="The if body runs when its condition is True.",
        )
    if key == "else":
        return _fill(
            question="Complete: else: ____",
            answer="print('small')",
            hint="else runs when the if condition is False.",
        )
    if key == "elif":
        return _fill(
            question="Complete: ____ x < 7:",
            answer="elif",
            hint="elif is short for else if.",
        )
    if key == "nested_if":
        return _mcq(
            question="What is nested if?",
            options=[
                {"label": "An if inside another if", "correct": True},
                {"label": "A loop", "correct": False},
                {"label": "A function", "correct": False},
                {"label": "A string", "correct": False},
            ],
            explanation="Nested if means an if inside another if.",
        )
    if key == "and_or":
        return _mcq(
            question="What does 'and' need?",
            options=[
                {"label": "At least one side true", "correct": False},
                {"label": "Both sides true", "correct": True},
                {"label": "Neither side true", "correct": False},
                {"label": "Any value", "correct": False},
            ],
            explanation="AND needs both sides true.",
        )
    if key == "not":
        return _mcq(
            question="What does 'not True' return?",
            options=[
                {"label": "True", "correct": False},
                {"label": "False", "correct": True},
                {"label": "None", "correct": False},
                {"label": "0", "correct": False},
            ],
            explanation="NOT flips a boolean.",
        )
    if key == "for_loop":
        return _mcq(
            question="What does a for loop do?",
            options=[
                {"label": "Runs forever", "correct": False},
                {"label": "Repeats a fixed number of times", "correct": True},
                {"label": "Only once", "correct": False},
                {"label": "Only in functions", "correct": False},
            ],
            explanation="For loops repeat a fixed number of times.",
        )
    if key == "range":
        return _fill(
            question="Complete: for i in ____(3):",
            answer="range",
            hint="range() generates a sequence.",
        )
    if key == "while_loop":
        return _mcq(
            question="When does a while loop stop?",
            options=[
                {"label": "After 10 iterations", "correct": False},
                {"label": "When the condition becomes False", "correct": True},
                {"label": "Never", "correct": False},
                {"label": "On error", "correct": False},
            ],
            explanation="While loops stop when the condition becomes False.",
        )
    if key == "break":
        return _fill(
            question="Complete: ____",
            answer="break",
            hint="break stops the loop early.",
        )
    if key == "continue":
        return _mcq(
            question="What does continue do?",
            options=[
                {"label": "Stops the loop", "correct": False},
                {"label": "Skips to the next iteration", "correct": True},
                {"label": "Reverses the loop", "correct": False},
                {"label": "Ends the program", "correct": False},
            ],
            explanation="Continue skips to the next iteration.",
        )
    if key == "list":
        return _mcq(
            question="How do you access the first element?",
            options=[
                {"label": "list[1]", "correct": False},
                {"label": "list[0]", "correct": True},
                {"label": "list.first()", "correct": False},
                {"label": "list[-1]", "correct": False},
            ],
            explanation="Index 0 is the first element.",
        )
    if key == "list_methods":
        return _fill(
            question="Complete: nums.____(3)",
            answer="append",
            hint="append() adds an element to the end.",
        )
    if key == "dict":
        return _mcq(
            question="How do you access a dict value?",
            options=[
                {"label": "dict.key", "correct": False},
                {"label": "dict['key']", "correct": True},
                {"label": "dict(0)", "correct": False},
                {"label": "dict.key()", "correct": False},
            ],
            explanation="Use dict['key'] to access values.",
        )
    if key == "tuple":
        return _fill(
            question="Complete: rgb[____]",
            answer="0",
            hint="Index 0 is the first element.",
        )
    if key == "set":
        return _mcq(
            question="What does a set store?",
            options=[
                {"label": "Duplicate values", "correct": False},
                {"label": "Unique values", "correct": True},
                {"label": "Key-value pairs", "correct": False},
                {"label": "Functions", "correct": False},
            ],
            explanation="Sets store unique values.",
        )
    if key == "function":
        return _fill(
            question="Complete: def ____():",
            answer="greet",
            hint="def defines a function.",
        )
    if key == "params":
        return _fill(
            question="Complete: def greet(____):",
            answer="name",
            hint="Parameters are the inputs a function accepts.",
        )
    if key == "return":
        return _mcq(
            question="What does return do?",
            options=[
                {"label": "Prints to console", "correct": False},
                {"label": "Sends a value back to the caller", "correct": True},
                {"label": "Stops the program", "correct": False},
                {"label": "Deletes a variable", "correct": False},
            ],
            explanation="Return sends a value back to the caller.",
        )
    if key == "multiple_returns":
        return _mcq(
            question="Can a function return multiple values?",
            options=[
                {"label": "No, never", "correct": False},
                {"label": "Yes, as a tuple", "correct": True},
                {"label": "Only in C", "correct": False},
                {"label": "Only with lists", "correct": False},
            ],
            explanation="Functions can return multiple values as a tuple.",
        )
    if key == "defaults":
        return _fill(
            question="Complete: def greet(name=____):",
            answer="friend",
            hint="Default parameter values make functions easier to call.",
        )
    if key == "lambda":
        return _fill(
            question="Complete: square = lambda x: ____",
            answer="x * x",
            hint="Lambda is an anonymous inline function.",
        )
    if key == "map":
        return _mcq(
            question="What does map do?",
            options=[
                {"label": "Filters items", "correct": False},
                {"label": "Transforms every item", "correct": True},
                {"label": "Sorts items", "correct": False},
                {"label": "Searches items", "correct": False},
            ],
            explanation="Map transforms every item in a collection.",
        )
    if key == "filter":
        return _mcq(
            question="What does filter do?",
            options=[
                {"label": "Transforms every item", "correct": False},
                {"label": "Keeps items matching a condition", "correct": True},
                {"label": "Sorts items", "correct": False},
                {"label": "Reverses items", "correct": False},
            ],
            explanation="Filter keeps only items matching a condition.",
        )
    if key == "try_except":
        return _fill(
            question="Complete: except ____:",
            answer="ValueError",
            hint="except catches specific error types.",
        )
    if key == "raise":
        return _fill(
            question="Complete: raise ____('age cannot be negative')",
            answer="ValueError",
            hint="raise throws an exception.",
        )
    if key == "import":
        return _mcq(
            question="What does import do?",
            options=[
                {"label": "Deletes code", "correct": False},
                {"label": "Brings code from other modules", "correct": True},
                {"label": "Compiles code", "correct": False},
                {"label": "Runs code", "correct": False},
            ],
            explanation="Import brings code from other modules.",
        )
    if key == "from_import":
        return _fill(
            question="Complete: from ____ import sqrt",
            answer="math",
            hint="from module import name imports a specific name.",
        )
    if key == "pip":
        return _mcq(
            question="What is pip?",
            options=[
                {"label": "A database", "correct": False},
                {"label": "A package manager", "correct": True},
                {"label": "A web server", "correct": False},
                {"label": "A compiler", "correct": False},
            ],
            explanation="pip installs external libraries.",
        )
    if key == "file_read":
        return _fill(
            question="Complete: open('notes.txt', '____')",
            answer="r",
            hint="'r' opens for reading.",
        )
    if key == "file_write":
        return _fill(
            question="Complete: open('notes.txt', '____')",
            answer="w",
            hint="'w' opens for writing (overwrites).",
        )
    if key == "capstone":
        return _run(
            description="Run the capstone program",
            starter=snippet,
            expected_output="[]",
            hint="Combine loops, input, and lists.",
        )
    return None


def _build_lesson(language: dict) -> dict:
    """Build a Scrimba-style lesson from language snippets."""
    slide_defs = [
        ("welcome", "Welcome", language["welcome"]),
        ("strings", "Strings", "Strings are sequences of characters. In most languages you wrap them in quotes and concatenate with + or interpolation."),
        ("comments", "Comments", "Comments explain code to humans. The compiler ignores them. Use them for why, not what."),
        ("numbers", "Numbers", "Numbers are the most basic data type. Addition, subtraction, multiplication, and division work as expected. Watch out for integer division."),
        ("variables", "Variables", "Variables are named containers for values. Declare them, assign them, and read them back. Choose names that describe the value."),
        ("naming", "Naming", "Good names make code readable. Use snake_case or camelCase consistently. Avoid single letters except for trivial loop counters."),
        ("reassign", "Reassignment", "Most variables can be reassigned. Constants and immutable bindings cannot. Know the difference."),
        ("fstrings", "String Interpolation", "Interpolation embeds expressions inside strings. It is cleaner and less error-prone than concatenation."),
        ("input", "Input", "Programs become interactive when they read input. Convert strings to numbers when needed and validate before using."),
        ("int_cast", "Type Conversion", "Convert between types explicitly. Implicit conversion is convenient but hides bugs."),
        ("boolean", "Booleans", "Booleans have two values: true and false. They drive conditions, loops, and logic."),
        ("comparisons", "Comparisons", "Comparisons produce booleans. Equality, inequality, greater-than, and less-than are the building blocks of conditions."),
        ("if", "If Statement", "If statements run code conditionally. The condition must evaluate to a boolean."),
        ("else", "Else Clause", "Else runs when the if condition is false. Together they cover both branches."),
        ("elif", "Else If", "Else if chains let you handle multiple exclusive cases in order."),
        ("nested_if", "Nested Conditions", "Conditions can be nested. Deep nesting is hard to read — flatten with guards or early returns when possible."),
        ("and_or", "AND / OR", "AND needs both sides true. OR needs at least one side true. They combine conditions."),
        ("not", "NOT", "NOT flips a boolean. It is the simplest way to invert a condition."),
        ("for_loop", "For Loop", "For loops repeat a block a fixed number of times. The loop variable changes each iteration."),
        ("range", "Ranges", "Ranges generate sequences of numbers. They are the backbone of counted loops."),
        ("while_loop", "While Loop", "While loops repeat while a condition stays true. Make sure the condition eventually becomes false."),
        ("break", "Break", "Break stops the loop early. Use it when you have found what you need."),
        ("continue", "Continue", "Continue skips the rest of the current iteration and moves to the next one."),
        ("list", "Lists / Arrays", "Lists store multiple values in order. Access by index, iterate with loops, and grow or shrink as needed."),
        ("list_methods", "List Methods", "Common operations: append, insert, remove, pop, length, slice, sort. Each language names them slightly differently."),
        ("dict", "Dictionaries / Maps", "Dictionaries map keys to values. They are the go-to structure for lookups and grouping."),
        ("tuple", "Tuples", "Tuples group a few values together. They are often used for returning multiple values from a function."),
        ("set", "Sets", "Sets store unique values. They are useful for membership tests and removing duplicates."),
        ("function", "Functions", "Functions are reusable blocks of code. They take inputs, do work, and optionally return a result."),
        ("params", "Parameters", "Parameters are the inputs a function accepts. Arguments are the actual values you pass in."),
        ("return", "Return", "Return sends a value back to the caller. A function without return returns None / void / undefined."),
        ("multiple_returns", "Multiple Values", "Some languages allow returning multiple values directly. Others use arrays, objects, or out parameters."),
        ("defaults", "Default Values", "Default parameter values make functions easier to call. The caller can omit them when the default is fine."),
        ("lambda", "Anonymous Functions", "Short inline functions are useful for one-off transformations in map, filter, and sort."),
        ("map", "Map", "Map transforms every item in a collection. The output collection has the same length as the input."),
        ("filter", "Filter", "Filter keeps only the items that match a condition. The output can be shorter than the input."),
        ("try_except", "Error Handling", "Errors are inevitable. Catch them so the program can respond instead of crashing."),
        ("raise", "Raising Errors", "Raise an error when something is wrong and the caller should know about it."),
        ("import", "Imports", "Imports bring code from other modules into the current file. They keep files small and focused."),
        ("from_import", "Selective Imports", "Import only what you need. It reduces namespace clutter and makes dependencies clearer."),
        ("pip", "Package Managers", "Package managers install external libraries. They make sharing and reusing code easy."),
        ("file_read", "File Read", "Reading files is how programs persist data between runs. Always close the file when done."),
        ("file_write", "File Write", "Writing files creates artifacts, logs, and saved data. Choose the right mode: overwrite, append, or binary."),
        ("capstone", "Capstone", "Combine variables, loops, functions, and files into a small program. Capstones turn isolated concepts into real skill."),
    ]

    slides: List[Slide] = []
    for key, title, content in slide_defs:
        snippet = language["snippets"].get(key, "")
        interaction = _interaction_for_slide(key, title, snippet, language["id"])
        slides.append(
            _slide(
                title=title,
                content=content,
                code=snippet,
                language=language["id"],
                interaction=interaction,
            )
        )

    return {
        "lesson_id": f"{language['id']}-first-program",
        "language_id": language["id"],
        "level_id": "scrimba",
        "title": f"Scrimba-style {language['name']}",
        "description": language["welcome"],
        "slides": slides,
    }


LESSONS: List[Dict[str, Any]] = [_build_lesson(lang) for lang in LANGUAGES]
LESSON_INDEX: Dict[str, dict] = {lesson["lesson_id"]: lesson for lesson in LESSONS}


def get_scrimba_lesson(lesson_id: str) -> Optional[Dict[str, Any]]:
    return LESSON_INDEX.get(lesson_id)


def all_scrimba_lessons() -> List[Dict[str, Any]]:
    return list(LESSONS)
