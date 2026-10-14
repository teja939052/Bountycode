"""CFIC — Correctness-First Interactive Curriculum.

Additive curriculum system that teaches coding fundamentals through an
interactive concept graph:
    predict → visualize → manipulate → break → transfer

This module is completely independent from the existing world/lesson
curriculum. It lives under:
    backend/app/content/cfic_*
    backend/app/services/concept_engine.py
    backend/app/routes/concepts.py
    frontend/src/pages/ConceptGraph.tsx
    frontend/src/pages/ConceptFrame.tsx

No existing curriculum file is modified.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# ─── Concept graph nodes and edges ─────────────────────────────────────

class ConceptNode(BaseModel):
    """One concept in the CFIC knowledge graph."""
    concept_id: str
    title: str
    domain: str  # e.g. "fundamentals", "data", "control", "functions"
    difficulty: int = 1  # 1–5
    estimated_minutes: int = 8
    one_liner: str = ""
    mental_model: str = ""
    prerequisite_ids: List[str] = Field(default_factory=list)
    mastery_threshold: float = 0.8  # BKT probability required to unlock
    xp_reward: int = 25
    diamonds_reward: int = 10
    why_it_matters: str = ""
    engineering_context: str = ""
    unlocks: List[str] = Field(default_factory=list)


class ConceptEdge(BaseModel):
    """Prerequisite relationship between two concepts."""
    from_concept: str  # prerequisite
    to_concept: str    # dependent
    weight: float = 1.0


class ConceptGraph(BaseModel):
    """The full CFIC knowledge graph."""
    nodes: List[ConceptNode] = Field(default_factory=list)
    edges: List[ConceptEdge] = Field(default_factory=list)


# ─── Concept frame interaction types ──────────────────────────────────

class PredictFrame(BaseModel):
    """Prediction before execution."""
    prompt: str = ""
    code: str = ""
    options: List[Dict[str, Any]] = Field(default_factory=list)
    correct_index: int = 0
    explanation: str = ""


class VisualizeFrame(BaseModel):
    """Step-by-step execution visualization guide."""
    trace_description: str = ""
    key_state_changes: List[Dict[str, str]] = Field(default_factory=list)
    animation_hints: List[str] = Field(default_factory=list)


class ManipulateFrame(BaseModel):
    """Change one value, rerun, observe the change."""
    starter_code: str = ""
    language: str = "python"
    scaffold_prompt: str = ""
    target_variable: str = ""
    hint: str = ""
    success_condition: str = ""


class BreakFrame(BaseModel):
    """Introdu a bug, observe the failure, then diagnose it."""
    buggy_code: str = ""
    language: str = "python"
    failure_description: str = ""
    diagnosis_options: List[Dict[str, Any]] = Field(default_factory=list)
    correct_diagnosis: str = ""
    fix_code: str = ""
    fix_steps: List[str] = Field(default_factory=list)


class TransferFrame(BaseModel):
    """Apply the concept in a new context."""
    prompt: str = ""
    starter_code: str = ""
    language: str = "python"
    test_cases: List[Dict[str, Any]] = Field(default_factory=list)
    hidden_tests: int = 0
    success_condition: str = ""


class ConceptFrame(BaseModel):
    """One interactive concept frame."""
    concept_id: str
    frame_order: int
    frame_type: str  # predict | visualize | manipulate | break | transfer
    predict: Optional[PredictFrame] = None
    visualize: Optional[VisualizeFrame] = None
    manipulate: Optional[ManipulateFrame] = None
    break_frame: Optional[BreakFrame] = None
    transfer: Optional[TransferFrame] = None
    xp_reward: int = 0
    diamonds_reward: int = 0


class ConceptContent(BaseModel):
    """Complete authored content for a concept."""
    concept: ConceptNode
    frames: List[ConceptFrame] = Field(default_factory=list)


# ─── Mastery state ─────────────────────────────────────────────────────

class ConceptMastery(BaseModel):
    """Per-user, per-concept mastery state."""
    user_id: str
    concept_id: str
    mastered: bool = False
    mastery_probability: float = 0.0  # BKT estimate 0–1
    attempts: int = 0
    successes: int = 0
    first_seen_at: Optional[str] = None
    last_practiced_at: Optional[str] = None
    frame_results: List[Dict[str, Any]] = Field(default_factory=list)
    unlocked: bool = False


# ─── Session state ─────────────────────────────────────────────────────

class ConceptSession(BaseModel):
    """An active concept session."""
    user_id: str
    concept_id: str
    current_frame_index: int = 0
    frame_results: List[Dict[str, Any]] = Field(default_factory=list)
    total_xp_earned: int = 0
    total_diamonds_earned: int = 0
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


# ─── API response models ───────────────────────────────────────────────

class ConceptGraphResponse(BaseModel):
    graph: ConceptGraph
    mastery: Dict[str, ConceptMastery] = Field(default_factory=dict)


class ConceptFrameResponse(BaseModel):
    session_id: str
    frame: ConceptFrame
    total_frames: int
    current_index: int
    concept: ConceptNode
    mastery: ConceptMastery


class ConceptFrameResultResponse(BaseModel):
    mastery: ConceptMastery
    session: ConceptSession
    xp_awarded: int
    diamonds_awarded: int
    unlocked_concepts: List[str] = Field(default_factory=list)


# ─── CFIC curriculum: the additive graph content ────────────────────────

_CFIC_NODES: List[ConceptNode] = [
    # ── Domain 1: Fundamentals ────────────────────────────────────────
    ConceptNode(
        concept_id="print_hello",
        title="Print & Output",
        domain="fundamentals",
        difficulty=1,
        estimated_minutes=8,
        one_liner="The program's way of speaking to you.",
        mental_model="print() is the program saying something out loud.",
        prerequisite_ids=[],
        mastery_threshold=0.8,
        xp_reward=25,
        diamonds_reward=10,
        why_it_matters="Output is how every program communicates.",
        engineering_context="Engineers debug by printing state.",
        unlocks=["variables"],
    ),
    ConceptNode(
        concept_id="variables",
        title="Variables & Names",
        domain="fundamentals",
        difficulty=1,
        estimated_minutes=10,
        one_liner="Named boxes that hold values.",
        mental_model="name = value puts a value into a named box.",
        prerequisite_ids=["print_hello"],
        mastery_threshold=0.8,
        xp_reward=30,
        diamonds_reward=12,
        why_it_matters="Variables are the program's memory.",
        engineering_context="Naming is how code stays understandable.",
        unlocks=["types", "expressions"],
    ),
    ConceptNode(
        concept_id="types",
        title="Types & Values",
        domain="fundamentals",
        difficulty=1,
        estimated_minutes=10,
        one_liner="Not all values are the same kind.",
        mental_model="int, float, str, bool — the program keeps different kinds apart.",
        prerequisite_ids=["variables"],
        mastery_threshold=0.8,
        xp_reward=30,
        diamonds_reward=12,
        why_it_matters="Type errors are the most common beginner bug.",
        engineering_context="Static types prevent whole categories of bugs.",
        unlocks=["conditionals"],
    ),
    ConceptNode(
        concept_id="expressions",
        title="Expressions & Operators",
        domain="fundamentals",
        difficulty=1,
        estimated_minutes=10,
        one_liner="Combining values into new values.",
        mental_model="x + 1 produces a new value without changing x.",
        prerequisite_ids=["variables", "types"],
        mastery_threshold=0.8,
        xp_reward=30,
        diamonds_reward=12,
        why_it_matters="Every computation is built from expressions.",
        engineering_context="Arithmetic, comparison, and logical operators form computation.",
        unlocks=["conditionals"],
    ),
    # ── Domain 2: Control ──────────────────────────────────────────────
    ConceptNode(
        concept_id="conditionals",
        title="Conditionals & Branching",
        domain="control",
        difficulty=2,
        estimated_minutes=12,
        one_liner="The program making a decision.",
        mental_model="if / elif / else — different paths for different truths.",
        prerequisite_ids=["types", "expressions", "variables"],
        mastery_threshold=0.8,
        xp_reward=40,
        diamonds_reward=15,
        why_it_matters="Programs without branching can only do one thing.",
        engineering_context="Business logic is just conditionals composed.",
        unlocks=["loops", "match"],
    ),
    ConceptNode(
        concept_id="loops",
        title="Loops & Repetition",
        domain="control",
        difficulty=2,
        estimated_minutes=14,
        one_liner="Repeating without repeating yourself.",
        mental_model="while condition: and for x in y: — control repetition.",
        prerequisite_ids=["conditionals"],
        mastery_threshold=0.8,
        xp_reward=50,
        diamonds_reward=18,
        why_it_matters="Loops turn one-step programs into batch processors.",
        engineering_context="Off-by-one is the most famous loop bug.",
        unlocks=["functions", "list_comprehension"],
    ),
    ConceptNode(
        concept_id="list_comprehension",
        title="List Comprehensions",
        domain="data",
        difficulty=2,
        estimated_minutes=12,
        one_liner="A loop and a filter squeezed into one line.",
        mental_model="[f(x) for x in items if cond] is a transformation recipe.",
        prerequisite_ids=["loops", "conditionals"],
        mastery_threshold=0.8,
        xp_reward=45,
        diamonds_reward=16,
        why_it_matters="Comprehensions are the idiomatic Python transform.",
        engineering_context="Data pipelines are just nested comprehensions.",
        unlocks=["dictionaries"],
    ),
    # ── Domain 3: Data ─────────────────────────────────────────────────
    ConceptNode(
        concept_id="lists",
        title="Lists & Sequences",
        domain="data",
        difficulty=2,
        estimated_minutes=12,
        one_liner="Ordered collections you can grow and shrink.",
        mental_model="A list is an ordered bag of values addressed by index.",
        prerequisite_ids=["variables", "types"],
        mastery_threshold=0.8,
        xp_reward=40,
        diamonds_reward=15,
        why_it_matters="Lists are the primary data structure for ordered data.",
        engineering_context="Array-backed structures dominate real code.",
        unlocks=["list_comprehension", "strings"],
    ),
    ConceptNode(
        concept_id="dictionaries",
        title="Dictionaries & Maps",
        domain="data",
        difficulty=2,
        estimated_minutes=12,
        one_liner="Lookup tables keyed by anything.",
        mental_model="d[key] looks up a value by its key.",
        prerequisite_ids=["lists", "conditionals"],
        mastery_threshold=0.8,
        xp_reward=45,
        diamonds_reward=16,
        why_it_matters="Dicts give O(1) lookup where lists need O(n).",
        engineering_context="Caches, configs, and JSON all become dicts.",
        unlocks=["sets"],
    ),
    ConceptNode(
        concept_id="strings",
        title="Strings & Text",
        domain="data",
        difficulty=2,
        estimated_minutes=10,
        one_liner="Immutable sequences of characters.",
        mental_model="A string is read-only; slicing returns new strings.",
        prerequisite_ids=["variables", "types"],
        mastery_threshold=0.8,
        xp_reward=35,
        diamonds_reward=13,
        why_it_matters="Strings are the program's primary user interface.",
        engineering_context="Parsing, formatting, and validation are all string work.",
        unlocks=["string_methods"],
    ),
    # ── Domain 4: Abstraction ──────────────────────────────────────────
    ConceptNode(
        concept_id="functions",
        title="Functions & Reuse",
        domain="abstraction",
        difficulty=3,
        estimated_minutes=14,
        one_liner="Named chunks of behavior you can call.",
        mental_model="def name(params): return value — reuse by name.",
        prerequisite_ids=["conditionals", "loops", "variables"],
        mastery_threshold=0.8,
        xp_reward=55,
        diamonds_reward=20,
        why_it_matters="Functions turn one-off scripts into libraries.",
        engineering_context="Pure functions are the backbone of testing.",
        unlocks=["scope", "args_kwargs", "recursion"],
    ),
    ConceptNode(
        concept_id="scope",
        title="Scope & Lifetime",
        domain="abstraction",
        difficulty=3,
        estimated_minutes=12,
        one_liner="Where a name is visible and for how long.",
        mental_model="Names live in namespaces; LEGB resolves visibility.",
        prerequisite_ids=["functions"],
        mastery_threshold=0.8,
        xp_reward=45,
        diamonds_reward=16,
        why_it_matters="Scope bugs show up as confusing name errors.",
        engineering_context="Modules and classes exist to control scope.",
        unlocks=["recursion", "classes"],
    ),
    ConceptNode(
        concept_id="recursion",
        title="Recursion & Self-Reference",
        domain="abstraction",
        difficulty=3,
        estimated_minutes=14,
        one_liner="A function that calls a smaller version of itself.",
        mental_model="Base case + recursive case — smaller and smaller.",
        prerequisite_ids=["functions", "conditionals"],
        mastery_threshold=0.8,
        xp_reward=55,
        diamonds_reward=20,
        why_it_matters="Recursion turns divide-and-conquer into code.",
        engineering_context="DFS, tree traversals, and DP are all recursive.",
        unlocks=["classes", "algorithms"],
    ),
    # ── Domain 5: Error & Debug ────────────────────────────────────────
    ConceptNode(
        concept_id="errors",
        title="Errors & Stack Traces",
        domain="debug",
        difficulty=2,
        estimated_minutes=10,
        one_liner="The program's way of saying what went wrong.",
        mental_model="Syntax errors stop execution; exceptions halt a running program.",
        prerequisite_ids=["variables", "conditionals", "functions"],
        mastery_threshold=0.8,
        xp_reward=40,
        diamonds_reward=15,
        why_it_matters="Reading stack traces is the first debugging skill.",
        engineering_context="Engineers spend more time reading errors than writing code.",
        unlocks=["debugging", "try_except"],
    ),
    ConceptNode(
        concept_id="debugging",
        title="Debugging & Observation",
        domain="debug",
        difficulty=2,
        estimated_minutes=12,
        one_liner="Finding why code does not do what you expect.",
        mental_model="Observe, hypothesize, test, repeat.",
        prerequisite_ids=["errors", "print_hello", "variables"],
        mastery_threshold=0.8,
        xp_reward=45,
        diamonds_reward=16,
        why_it_matters="Debugging is where programmers spend most of their time.",
        engineering_context="Print debugging is still the fastest path to a fix.",
        unlocks=["try_except", "tests"],
    ),
    ConceptNode(
        concept_id="try_except",
        title="Exceptions & Recovery",
        domain="debug",
        difficulty=3,
        estimated_minutes=12,
        one_liner="Catching failures so the program can continue.",
        mental_model="try / except / else / finally — program robustness.",
        prerequisite_ids=["errors", "functions"],
        mastery_threshold=0.8,
        xp_reward=45,
        diamonds_reward=16,
        why_it_matters="Uncaught exceptions crash programs.",
        engineering_context="Services catch exceptions to avoid user-facing crashes.",
        unlocks=["tests"],
    ),
    ConceptNode(
        concept_id="tests",
        title="Testing & Assertion",
        domain="debug",
        difficulty=3,
        estimated_minutes=12,
        one_liner="Code that proves other code works.",
        mental_model="assert statement fails when behavior is wrong.",
        prerequisite_ids=["functions", "conditionals", "try_except"],
        mastery_threshold=0.8,
        xp_reward=50,
        diamonds_reward=18,
        why_it_matters="Tests prevent regressions.",
        engineering_context="CI runs tests on every push.",
        unlocks=[],
    ),
]

_CFIC_EDGES: List[ConceptEdge] = [
    ConceptEdge(from_concept="print_hello", to_concept="variables"),
    ConceptEdge(from_concept="variables", to_concept="types"),
    ConceptEdge(from_concept="variables", to_concept="expressions"),
    ConceptEdge(from_concept="types", to_concept="conditionals"),
    ConceptEdge(from_concept="expressions", to_concept="conditionals"),
    ConceptEdge(from_concept="variables", to_concept="lists"),
    ConceptEdge(from_concept="variables", to_concept="strings"),
    ConceptEdge(from_concept="conditionals", to_concept="loops"),
    ConceptEdge(from_concept="conditionals", to_concept="list_comprehension"),
    ConceptEdge(from_concept="loops", to_concept="functions"),
    ConceptEdge(from_concept="loops", to_concept="list_comprehension"),
    ConceptEdge(from_concept="lists", to_concept="list_comprehension"),
    ConceptEdge(from_concept="lists", to_concept="dictionaries"),
    ConceptEdge(from_concept="conditionals", to_concept="dictionaries"),
    ConceptEdge(from_concept="functions", to_concept="scope"),
    ConceptEdge(from_concept="functions", to_concept="recursion"),
    ConceptEdge(from_concept="conditionals", to_concept="recursion"),
    ConceptEdge(from_concept="functions", to_concept="classes"),
    ConceptEdge(from_concept="scope", to_concept="recursion"),
    ConceptEdge(from_concept="variables", to_concept="errors"),
    ConceptEdge(from_concept="conditionals", to_concept="errors"),
    ConceptEdge(from_concept="functions", to_concept="errors"),
    ConceptEdge(from_concept="print_hello", to_concept="debugging"),
    ConceptEdge(from_concept="variables", to_concept="debugging"),
    ConceptEdge(from_concept="errors", to_concept="debugging"),
    ConceptEdge(from_concept="errors", to_concept="try_except"),
    ConceptEdge(from_concept="functions", to_concept="try_except"),
    ConceptEdge(from_concept="functions", to_concept="tests"),
    ConceptEdge(from_concept="conditionals", to_concept="tests"),
    ConceptEdge(from_concept="try_except", to_concept="tests"),
]


# ─── CFIC additive content — concept frames ─────────────────────────────

_CFIC_FRAMES: Dict[str, List[ConceptFrame]] = {
    "print_hello": [
        ConceptFrame(
            concept_id="print_hello",
            frame_order=0,
            frame_type="predict",
            predict=PredictFrame(
                prompt="What will this program print?",
                code='print("Hello, World!")',
                options=[
                    {"id": "a", "text": "Hello, World!"},
                    {"id": "b", "text": "print(\"Hello, World!\")"},
                    {"id": "c", "text": "Nothing, it is a syntax error."},
                ],
                correct_index=0,
                explanation="print() outputs the string value, not the source code.",
            ),
            xp_reward=5,
            diamonds_reward=2,
        ),
        ConceptFrame(
            concept_id="print_hello",
            frame_order=1,
            frame_type="visualize",
            visualize=VisualizeFrame(
                trace_description="print() receives the string value, then writes it to stdout.",
                key_state_changes=[
                    {"step": "evaluate", "change": "Value 'Hello, World!' is formed from the string literal."},
                    {"step": "output", "change": "Value is written to stdout for the user to read."},
                ],
                animation_hints=["Highlight the string literal, then highlight stdout."],
            ),
            xp_reward=5,
            diamonds_reward=2,
        ),
        ConceptFrame(
            concept_id="print_hello",
            frame_order=2,
            frame_type="manipulate",
            manipulate=ManipulateFrame(
                starter_code='print("Hello, World!")\n# Change the greeting below\nname = "World"\n',
                language="python",
                scaffold_prompt="Change the greeting to use the name variable.",
                target_variable="name",
                hint="Use an f-string or string concatenation with the variable.",
                success_condition="printed value contains the name variable",
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
        ConceptFrame(
            concept_id="print_hello",
            frame_order=3,
            frame_type="break",
            break_frame=BreakFrame(
                buggy_code='name = "World"\nprint(name)\nprint("Hello, " + 5)\n',
                language="python",
                failure_description="The program crashes before printing the second line.",
                diagnosis_options=[
                    {"id": "a", "text": "name is undefined."},
                    {"id": "b", "text": "Cannot add str and int."},
                    {"id": "c", "text": "print() needs quotes."},
                ],
                correct_diagnosis="b",
                fix_code='name = "World"\nprint(name)\nprint("Hello, " + str(5))\n',
                fix_steps=["Convert the number to string before concatenation."],
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
        ConceptFrame(
            concept_id="print_hello",
            frame_order=4,
            frame_type="transfer",
            transfer=TransferFrame(
                prompt="Write a program that prints a 3-line poem.",
                starter_code="# Your poem here\n",
                language="python",
                test_cases=[
                    {"type": "contains", "expected": "\n", "count": 2},
                ],
                hidden_tests=1,
                success_condition="output contains at least 2 newline characters",
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
    ],
    "variables": [
        ConceptFrame(
            concept_id="variables",
            frame_order=0,
            frame_type="predict",
            predict=PredictFrame(
                prompt="What is the final value of x?",
                code="x = 10\nx = x + 5\n",
                options=[
                    {"id": "a", "text": "10"},
                    {"id": "b", "text": "15"},
                    {"id": "c", "text": "x + 5"},
                ],
                correct_index=1,
                explanation="x = x + 5 reads the current x, adds 5, and writes it back.",
            ),
            xp_reward=5,
            diamonds_reward=2,
        ),
        ConceptFrame(
            concept_id="variables",
            frame_order=1,
            frame_type="manipulate",
            manipulate=ManipulateFrame(
                starter_code="radius = 5\n# Compute the area below\n# area = ?\n",
                language="python",
                scaffold_prompt="Compute the area of a circle. Use math.pi or 3.14.",
                target_variable="area",
                hint="area = pi * radius ** 2",
                success_condition="area ≈ 78.54",
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
        ConceptFrame(
            concept_id="variables",
            frame_order=2,
            frame_type="break",
            break_frame=BreakFrame(
                buggy_code="height = 170\nwidth = 3\narea = height + width\n",
                language="python",
                failure_description="The variable area contains the wrong value.",
                diagnosis_options=[
                    {"id": "a", "text": "Variable names cannot be English words."},
                    {"id": "b", "text": "+ adds; area requires multiplication."},
                    {"id": "c", "text": "width is too large."},
                ],
                correct_diagnosis="b",
                fix_code="height = 170\nwidth = 3\narea = height * width\n",
                fix_steps=["Use * for multiplication instead of +."],
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
        ConceptFrame(
            concept_id="variables",
            frame_order=3,
            frame_type="transfer",
            transfer=TransferFrame(
                prompt="Swap two variables without a temporary variable.",
                starter_code="a = 10\nb = 20\n# swap here\nprint(a, b)\n",
                language="python",
                test_cases=[
                    {"type": "contains", "expected": "20 10", "count": 1},
                ],
                hidden_tests=2,
                success_condition="printed values are swapped",
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
    ],
    "types": [
        ConceptFrame(
            concept_id="types",
            frame_order=0,
            frame_type="predict",
            predict=PredictFrame(
                prompt="What type is the result of 3 / 2 in Python?",
                code="result = 3 / 2\nprint(type(result))\n",
                options=[
                    {"id": "a", "text": "<class 'int'>"},
                    {"id": "b", "text": "<class 'float'>"},
                    {"id": "c", "text": "<class 'str'>"},
                ],
                correct_index=1,
                explanation="/ always returns float in Python 3.",
            ),
            xp_reward=5,
            diamonds_reward=2,
        ),
        ConceptFrame(
            concept_id="types",
            frame_order=1,
            frame_type="manipulate",
            manipulate=ManipulateFrame(
                starter_code="x = \"42\"\ny = 42\n# convert x to int below\n",
                language="python",
                scaffold_prompt="Convert x to an integer and compare with y.",
                target_variable="x",
                hint="int(x) == y",
                success_condition="x equals y as integers",
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
        ConceptFrame(
            concept_id="types",
            frame_order=2,
            frame_type="break",
            break_frame=BreakFrame(
                buggy_code='name = input("Age: ")\nage = name + 1\nprint(age)\n',
                language="python",
                failure_description="The program crashes before printing.",
                diagnosis_options=[
                    {"id": "a", "text": "input() is deprecated."},
                    {"id": "b", "text": "Cannot add str and int."},
                    {"id": "c", "text": "age needs quotes."},
                ],
                correct_diagnosis="b",
                fix_code='name = input("Age: ")\nage = int(name) + 1\nprint(age)\n',
                fix_steps=["Convert input string to int before adding."],
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
        ConceptFrame(
            concept_id="types",
            frame_order=3,
            frame_type="transfer",
            transfer=TransferFrame(
                prompt="Round a float to the nearest cent without using round().",
                starter_code="price = 19.999\n# cents = ?\nprint(cents)\n",
                language="python",
                test_cases=[
                    {"type": "contains", "expected": "20.0", "count": 1},
                ],
                hidden_tests=3,
                success_condition="rounded value equals 20.0",
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
    ],
    "expressions": [
        ConceptFrame(
            concept_id="expressions",
            frame_order=0,
            frame_type="predict",
            predict=PredictFrame(
                prompt="What is the result?",
                code="x = 5\nprint(x > 3 and x < 10)\n",
                options=[
                    {"id": "a", "text": "True"},
                    {"id": "b", "text": "False"},
                    {"id": "c", "text": "Error"},
                ],
                correct_index=0,
                explanation="Both comparisons are true, so and is true.",
            ),
            xp_reward=5,
            diamonds_reward=2,
        ),
        ConceptFrame(
            concept_id="expressions",
            frame_order=1,
            frame_type="manipulate",
            manipulate=ManipulateFrame(
                starter_code="# Negate a boolean using only not\nflag = True\n# result = ?\n",
                language="python",
                scaffold_prompt="Produce the opposite of flag without if.",
                target_variable="result",
                hint="not flag",
                success_condition="result is False",
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
        ConceptFrame(
            concept_id="expressions",
            frame_order=2,
            frame_type="break",
            break_frame=BreakFrame(
                buggy_code="score = 75\npassed = score >= 60 or score < 0\n",
                language="python",
                failure_description="passed is True when it should be False.",
                diagnosis_options=[
                    {"id": "a", "text": "or requires both sides to be true."},
                    {"id": "b", "text": "score < 0 makes passed True."},
                    {"id": "c", "text": "score cannot be negative."},
                ],
                correct_diagnosis="b",
                fix_code="score = 75\npassed = score >= 60 and score < 100\n",
                fix_steps=["Use and for valid range checks."],
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
        ConceptFrame(
            concept_id="expressions",
            frame_order=3,
            frame_type="transfer",
            transfer=TransferFrame(
                prompt="Check if a year is a leap year using boolean expressions.",
                starter_code="year = 2000\n# is_leap = ?\n",
                language="python",
                test_cases=[
                    {"type": "contains", "expected": "True", "count": 1},
                ],
                hidden_tests=3,
                success_condition="leap year logic holds",
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
    ],
    "conditionals": [
        ConceptFrame(
            concept_id="conditionals",
            frame_order=0,
            frame_type="predict",
            predict=PredictFrame(
                prompt="What is printed?",
                code="x = 10\nif x > 10:\n    print('big')\nelse:\n    print('small')\n",
                options=[
                    {"id": "a", "text": "big"},
                    {"id": "b", "text": "small"},
                    {"id": "c", "text": "Error"},
                ],
                correct_index=1,
                explanation="x is 10, not greater than 10, so else runs.",
            ),
            xp_reward=5,
            diamonds_reward=2,
        ),
        ConceptFrame(
            concept_id="conditionals",
            frame_order=1,
            frame_type="manipulate",
            manipulate=ManipulateFrame(
                starter_code="# Grade to letter using elif\nscore = 85\n# letter = ?\n",
                language="python",
                scaffold_prompt="A → 90+, B → 80+, C → 70+, else F.",
                target_variable="letter",
                hint="elif chain from highest to lowest",
                success_condition="letter == 'B'",
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
        ConceptFrame(
            concept_id="conditionals",
            frame_order=2,
            frame_type="break",
            break_frame=BreakFrame(
                buggy_code="age = 20\nif age < 18:\n    print('minor')\nelif age < 60:\n    print('adult')\nelif age < 120:\n    print('senior')\nelse:\n    print('invalid')\n",
                language="python",
                failure_description="Senior citizens see 'invalid'.",
                diagnosis_options=[
                    {"id": "a", "text": "Missing brackets."},
                    {"id": "b", "text": "Final else catches valid senior ages."},
                    {"id": "c", "text": "elif cannot be nested."},
                ],
                correct_diagnosis="b",
                fix_code="age = 20\nif age < 18:\n    print('minor')\nelif age < 60:\n    print('adult')\nelif age < 120:\n    print('senior')\n# else removed or covers invalid only\n",
                fix_steps=["Remove or adjust the final else clause."],
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
        ConceptFrame(
            concept_id="conditionals",
            frame_order=3,
            frame_type="transfer",
            transfer=TransferFrame(
                prompt="Return the maximum of three numbers using only if.",
                starter_code="a, b, c = 3, 1, 2\n# max3 = ?\nprint(max3)\n",
                language="python",
                test_cases=[
                    {"type": "contains", "expected": "3", "count": 1},
                ],
                hidden_tests=4,
                success_condition="max3 equals maximum",
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
    ],
    "loops": [
        ConceptFrame(
            concept_id="loops",
            frame_order=0,
            frame_type="predict",
            predict=PredictFrame(
                prompt="How many times does this loop run?",
                code="for i in range(5):\n    print(i)\n",
                options=[
                    {"id": "a", "text": "4"},
                    {"id": "b", "text": "5"},
                    {"id": "c", "text": "6"},
                ],
                correct_index=1,
                explanation="range(5) produces 0,1,2,3,4 — five values.",
            ),
            xp_reward=5,
            diamonds_reward=2,
        ),
        ConceptFrame(
            concept_id="loops",
            frame_order=1,
            frame_type="manipulate",
            manipulate=ManipulateFrame(
                starter_code="# Print even numbers from 0 to 10\nfor i in range(11):\n    if i % 2 == 0:\n        print(i)\n",
                language="python",
                scaffold_prompt="Change the range so the loop prints 0 through 20.",
                target_variable="range",
                hint="range(21)",
                success_condition="output contains 20",
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
        ConceptFrame(
            concept_id="loops",
            frame_order=2,
            frame_type="break",
            break_frame=BreakFrame(
                buggy_code="total = 0\nfor i in range(1, 6):\n    total = total + i\nprint(total)\n",
                language="python",
                failure_description="total is 10 instead of 15.",
                diagnosis_options=[
                    {"id": "a", "text": "range stops before the end value."},
                    {"id": "b", "text": "total starts at wrong value."},
                    {"id": "c", "text": "+ is wrong."},
                ],
                correct_diagnosis="a",
                fix_code="total = 0\nfor i in range(1, 7):\n    total = total + i\nprint(total)\n",
                fix_steps=["Use range(1, 7) to include 6."],
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
        ConceptFrame(
            concept_id="loops",
            frame_order=3,
            frame_type="transfer",
            transfer=TransferFrame(
                prompt="Compute factorial using a while loop.",
                starter_code="n = 5\nfact = 1\n# your loop here\nprint(fact)\n",
                language="python",
                test_cases=[
                    {"type": "contains", "expected": "120", "count": 1},
                ],
                hidden_tests=3,
                success_condition="fact equals n!",
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
    ],
    "functions": [
        ConceptFrame(
            concept_id="functions",
            frame_order=0,
            frame_type="predict",
            predict=PredictFrame(
                prompt="What does this return?",
                code="def add(a, b):\n    return a + b\nprint(add(2, 3))\n",
                options=[
                    {"id": "a", "text": "5"},
                    {"id": "b", "text": "23"},
                    {"id": "c", "text": "Error"},
                ],
                correct_index=0,
                explanation="add(2, 3) returns 2 + 3 = 5.",
            ),
            xp_reward=5,
            diamonds_reward=2,
        ),
        ConceptFrame(
            concept_id="functions",
            frame_order=1,
            frame_type="manipulate",
            manipulate=ManipulateFrame(
                starter_code="def is_even(n):\n    # your code here\n    pass\n",
                language="python",
                scaffold_prompt="Return True when n is even.",
                target_variable="is_even",
                hint="return n % 2 == 0",
                success_condition="is_even(4) returns True",
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
        ConceptFrame(
            concept_id="functions",
            frame_order=2,
            frame_type="break",
            break_frame=BreakFrame(
                buggy_code="def area(r):\n    return 3.14 * r ** r\n",
                language="python",
                failure_description="area(3) gives a wrong answer.",
                diagnosis_options=[
                    {"id": "a", "text": "3.14 is not precise enough."},
                    {"id": "b", "text": "Exponent should be 2, not r."},
                    {"id": "c", "text": "Function needs two parameters."},
                ],
                correct_diagnosis="b",
                fix_code="def area(r):\n    return 3.14 * r ** 2\n",
                fix_steps=["Use r ** 2 for circle area."],
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
        ConceptFrame(
            concept_id="functions",
            frame_order=3,
            frame_type="transfer",
            transfer=TransferFrame(
                prompt="Write a function that counts vowels in a string.",
                starter_code="def count_vowels(s):\n    # your code\n    pass\n",
                language="python",
                test_cases=[
                    {"type": "contains", "expected": "5", "count": 1},
                ],
                hidden_tests=4,
                success_condition="counts vowels correctly",
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
    ],
    "errors": [
        ConceptFrame(
            concept_id="errors",
            frame_order=0,
            frame_type="predict",
            predict=PredictFrame(
                prompt="What kind of error is this?",
                code='print("Hello")\n',
                options=[
                    {"id": "a", "text": "SyntaxError"},
                    {"id": "b", "text": "NameError"},
                    {"id": "c", "text": "TypeError"},
                ],
                correct_index=1,
                explanation="The unclosed string triggers a SyntaxError.",
            ),
            xp_reward=5,
            diamonds_reward=2,
        ),
        ConceptFrame(
            concept_id="errors",
            frame_order=1,
            frame_type="manipulate",
            manipulate=ManipulateFrame(
                starter_code="# Trigger a NameError, then fix it\nx = 5\nprint(y)\n",
                language="python",
                scaffold_prompt="Fix the NameError.",
                target_variable="y",
                hint="Define y before printing",
                success_condition="no NameError raised",
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
        ConceptFrame(
            concept_id="errors",
            frame_order=2,
            frame_type="break",
            break_frame=BreakFrame(
                buggy_code="def greet(name):\n    return 'Hello ' + name\nprint(greet())\n",
                language="python",
                failure_description="The program raises an exception.",
                diagnosis_options=[
                    {"id": "a", "text": "name is undefined."},
                    {"id": "b", "text": "Missing required positional argument."},
                    {"id": "c", "text": "Cannot add str and None."},
                ],
                correct_diagnosis="b",
                fix_code="def greet(name):\n    return 'Hello ' + name\nprint(greet('World')\n",
                fix_steps=["Pass the required argument."],
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
        ConceptFrame(
            concept_id="errors",
            frame_order=3,
            frame_type="transfer",
            transfer=TransferFrame(
                prompt="Add try/except to catch a ZeroDivisionError.",
                starter_code="def safe_div(a, b):\n    # your code\n    pass\nprint(safe_div(1, 0))\n",
                language="python",
                test_cases=[
                    {"type": "contains", "expected": "None", "count": 1},
                ],
                hidden_tests=2,
                success_condition="returns None for zero division",
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
    ],
    "lists": [
        ConceptFrame(
            concept_id="lists",
            frame_order=0,
            frame_type="predict",
            predict=PredictFrame(
                prompt="What is the last element?",
                code="items = [10, 20, 30]\nprint(items[2])\n",
                options=[
                    {"id": "a", "text": "10"},
                    {"id": "b", "text": "20"},
                    {"id": "c", "text": "30"},
                ],
                correct_index=2,
                explanation="Lists are 0-indexed, so [2] is the third element.",
            ),
            xp_reward=5,
            diamonds_reward=2,
        ),
        ConceptFrame(
            concept_id="lists",
            frame_order=1,
            frame_type="manipulate",
            manipulate=ManipulateFrame(
                starter_code="nums = [1, 2, 3]\n# append 4 below\n",
                language="python",
                scaffold_prompt="Add 4 to the end of nums.",
                target_variable="nums",
                hint="nums.append(4)",
                success_condition="nums length equals 4",
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
        ConceptFrame(
            concept_id="lists",
            frame_order=2,
            frame_type="break",
            break_frame=BreakFrame(
                buggy_code="nums = [1, 2, 3]\nlast = nums[3]\n",
                language="python",
                failure_description="Program crashes on the last line.",
                diagnosis_options=[
                    {"id": "a", "text": "IndexError: index out of range."},
                    {"id": "b", "text": "TypeError: list index must be int."},
                    {"id": "c", "text": "SyntaxError: missing bracket."},
                ],
                correct_diagnosis="a",
                fix_code="nums = [1, 2, 3]\nlast = nums[2]\n",
                fix_steps=["Use index 2 for the third element."],
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
        ConceptFrame(
            concept_id="lists",
            frame_order=3,
            frame_type="transfer",
            transfer=TransferFrame(
                prompt="Return the sum of a list using a loop.",
                starter_code="def total(values):\n    # your code\n    pass\nprint(total([1,2,3]))\n",
                language="python",
                test_cases=[
                    {"type": "contains", "expected": "6", "count": 1},
                ],
                hidden_tests=3,
                success_condition="returns sum of values",
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
    ],
    "strings": [
        ConceptFrame(
            concept_id="strings",
            frame_order=0,
            frame_type="predict",
            predict=PredictFrame(
                prompt="What is the result?",
                code='s = "abc"\nprint(s.upper())\n',
                options=[
                    {"id": "a", "text": "ABC"},
                    {"id": "b", "text": "abc"},
                    {"id": "c", "text": "Error"},
                ],
                correct_index=0,
                explanation="upper() returns an uppercase copy.",
            ),
            xp_reward=5,
            diamonds_reward=2,
        ),
        ConceptFrame(
            concept_id="strings",
            frame_order=1,
            frame_type="manipulate",
            manipulate=ManipulateFrame(
                starter_code="text = 'hello world'\n# reverse below\n",
                language="python",
                scaffold_prompt="Reverse the string using slicing.",
                target_variable="reversed_text",
                hint="text[::-1]",
                success_condition="reversed_text equals 'dlrow olleh'",
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
        ConceptFrame(
            concept_id="strings",
            frame_order=2,
            frame_type="break",
            break_frame=BreakFrame(
                buggy_code='name = "Alice"\ninitial = name[0]\ninitial = initial + "e"\n',
                language="python",
                failure_description="initial becomes 'Aie' instead of 'A'.",
                diagnosis_options=[
                    {"id": "a", "text": "Strings are immutable."},
                    {"id": "b", "text": "Slicing includes the end index."},
                    {"id": "c", "text": "initial is reassigned."},
                ],
                correct_diagnosis="c",
                fix_code="name = 'Alice'\ninitial = name[0]\n# do not reassign if immutability matters\n",
                fix_steps=["Avoid treating strings as mutable if correctness requires immutability."],
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
        ConceptFrame(
            concept_id="strings",
            frame_order=3,
            frame_type="transfer",
            transfer=TransferFrame(
                prompt="Check if a string is a palindrome.",
                starter_code="def palindrome(s):\n    # your code\n    pass\nprint(palindrome('level'))\n",
                language="python",
                test_cases=[
                    {"type": "contains", "expected": "True", "count": 1},
                ],
                hidden_tests=4,
                success_condition="returns True for palindrome",
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
    ],
    "dictionaries": [
        ConceptFrame(
            concept_id="dictionaries",
            frame_order=0,
            frame_type="predict",
            predict=PredictFrame(
                prompt="What is the output?",
                code="d = {'a': 1, 'b': 2}\nd['a'] = 10\nprint(d['a'])\n",
                options=[
                    {"id": "a", "text": "1"},
                    {"id": "b", "text": "10"},
                    {"id": "c", "text": "Error"},
                ],
                correct_index=1,
                explanation="Dict values are overwritten by key assignment.",
            ),
            xp_reward=5,
            diamonds_reward=2,
        ),
        ConceptFrame(
            concept_id="dictionaries",
            frame_order=1,
            frame_type="manipulate",
            manipulate=ManipulateFrame(
                starter_code="# Count frequencies using a dict\nitems = ['a', 'b', 'a']\nfreq = {}\n# your code below\n",
                language="python",
                scaffold_prompt="Use freq[item] = freq.get(item, 0) + 1.",
                target_variable="freq",
                hint="freq.get(item, 0) + 1",
                success_condition="freq['a'] equals 2",
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
        ConceptFrame(
            concept_id="dictionaries",
            frame_order=2,
            frame_type="break",
            break_frame=BreakFrame(
                buggy_code="d = {}\nd['x'] = 1\nprint(d['y'])\n",
                language="python",
                failure_description="Program crashes on the last line.",
                diagnosis_options=[
                    {"id": "a", "text": "KeyError: y is missing."},
                    {"id": "b", "text": "TypeError: string required."},
                    {"id": "c", "text": "SyntaxError: missing colon."},
                ],
                correct_diagnosis="a",
                fix_code="d = {}\nd['x'] = 1\nprint(d.get('y', 'missing'))\n",
                fix_steps=["Use get() with a default instead of direct access."],
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
        ConceptFrame(
            concept_id="dictionaries",
            frame_order=3,
            frame_type="transfer",
            transfer=TransferFrame(
                prompt="Group strings by their length.",
                starter_code="words = ['hi', 'hello', 'a', 'world']\ngroups = {}\n# your code\n",
                language="python",
                test_cases=[
                    {"type": "contains", "expected": "5", "count": 1},
                ],
                hidden_tests=3,
                success_condition="groups keyed by length",
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
    ],
    "list_comprehension": [
        ConceptFrame(
            concept_id="list_comprehension",
            frame_order=0,
            frame_type="predict",
            predict=PredictFrame(
                prompt="What does this produce?",
                code="squares = [x**2 for x in range(4)]\nprint(squares)\n",
                options=[
                    {"id": "a", "text": "[0, 1, 4, 9]"},
                    {"id": "b", "text": "[1, 4, 9, 16]"},
                    {"id": "c", "text": "Error"},
                ],
                correct_index=1,
                explanation="range(4) yields 0–3; squares produce [1,4,9,16].",
            ),
            xp_reward=5,
            diamonds_reward=2,
        ),
        ConceptFrame(
            concept_id="list_comprehension",
            frame_order=1,
            frame_type="manipulate",
            manipulate=ManipulateFrame(
                starter_code="# Filter odd numbers from 0..9\n# evens = ?\n",
                language="python",
                scaffold_prompt="Use a comprehension with an if.",
                target_variable="evens",
                hint="[x for x in range(10) if x % 2 == 0]",
                success_condition="evens equals [0,2,4,6,8]",
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
        ConceptFrame(
            concept_id="list_comprehension",
            frame_order=2,
            frame_type="break",
            break_frame=BreakFrame(
                buggy_code="nums = [1, 2, 3]\nsquares = [x ** 2 for x in range(3)]\n",
                language="python",
                failure_description="squares is [0, 1, 4] instead of [1, 4, 9].",
                diagnosis_options=[
                    {"id": "a", "text": "range starts at 1."},
                    {"id": "b", "text": "range(3) ignores nums entirely."},
                    {"id": "c", "text": "x ** 2 is wrong."},
                ],
                correct_diagnosis="b",
                fix_code="nums = [1, 2, 3]\nsquares = [x ** 2 for x in nums]\n",
                fix_steps=["Iterate over nums, not range(3)."],
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
        ConceptFrame(
            concept_id="list_comprehension",
            frame_order=3,
            frame_type="transfer",
            transfer=TransferFrame(
                prompt="Flatten a list of lists using comprehension.",
                starter_code="pairs = [[1, 2], [3, 4]]\n# flat = ?\n",
                language="python",
                test_cases=[
                    {"type": "contains", "expected": "4", "count": 1},
                ],
                hidden_tests=2,
                success_condition="flat equals [1,2,3,4]",
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
    ],
    "debugging": [
        ConceptFrame(
            concept_id="debugging",
            frame_order=0,
            frame_type="predict",
            predict=PredictFrame(
                prompt="Where is the first broken line?",
                code="total = 0\nfor i in range(5)\n    total = total + i\nprint(total)\n",
                options=[
                    {"id": "a", "text": "Line 1"},
                    {"id": "b", "text": "Line 3"},
                    {"id": "c", "text": "Line 4"},
                ],
                correct_index=1,
                explanation="Missing colon after for triggers SyntaxError.",
            ),
            xp_reward=5,
            diamonds_reward=2,
        ),
        ConceptFrame(
            concept_id="debugging",
            frame_order=1,
            frame_type="manipulate",
            manipulate=ManipulateFrame(
                starter_code="def add(a, b):\n    s = a + b\nprint(add(1, 2))\n",
                language="python",
                scaffold_prompt="Use print to inspect the sum before returning.",
                target_variable="s",
                hint="print('sum=', s) before return",
                success_condition="printed output contains 'sum= 3'",
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
        ConceptFrame(
            concept_id="debugging",
            frame_order=2,
            frame_type="break",
            break_frame=BreakFrame(
                buggy_code="def average(values):\n    return sum(values) / len(values)\nprint(average([]))\n",
                language="python",
                failure_description="Program crashes on empty list.",
                diagnosis_options=[
                    {"id": "a", "text": "sum([]) is wrong."},
                    {"id": "b", "text": "len([]) is 0, division by zero."},
                    {"id": "c", "text": "average needs a default."},
                ],
                correct_diagnosis="b",
                fix_code="def average(values):\n    if not values:\n        return 0\n    return sum(values) / len(values)\n",
                fix_steps=["Guard against empty input before dividing."],
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
        ConceptFrame(
            concept_id="debugging",
            frame_order=3,
            frame_type="transfer",
            transfer=TransferFrame(
                prompt="Find and fix the bug in this countdown loop.",
                starter_code="i = 5\nwhile i > 0:\n    print(i)\n# missing decrement\n",
                language="python",
                test_cases=[
                    {"type": "contains", "expected": "0", "count": 1},
                ],
                hidden_tests=2,
                success_condition="output contains 0 and no infinite loop",
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
    ],
    "functions": [
        ConceptFrame(
            concept_id="functions",
            frame_order=0,
            frame_type="predict",
            predict=PredictFrame(
                prompt="What is returned?",
                code="def double(x):\n    return x * 2\nprint(double(double(2)))\n",
                options=[
                    {"id": "a", "text": "4"},
                    {"id": "b", "text": "6"},
                    {"id": "c", "text": "8"},
                ],
                correct_index=1,
                explanation="double(2) is 4; double(4) is 8.",
            ),
            xp_reward=5,
            diamonds_reward=2,
        ),
        ConceptFrame(
            concept_id="functions",
            frame_order=1,
            frame_type="manipulate",
            manipulate=ManipulateFrame(
                starter_code="def greet(name, greeting='Hello'):\n    # your code\n    pass\n",
                language="python",
                scaffold_prompt="Return '{greeting}, {name}!' using default parameter.",
                target_variable="greet",
                hint="return f'{greeting}, {name}!'",
                success_condition="greet('Ada') returns 'Hello, Ada!'",
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
        ConceptFrame(
            concept_id="functions",
            frame_order=2,
            frame_type="break",
            break_frame=BreakFrame(
                buggy_code="def add(a, b=0):\n    return a + b\nprint(add(5))\n",
                language="python",
                failure_description="Result is 5 instead of 10.",
                diagnosis_options=[
                    {"id": "a", "text": "Default arguments must come first."},
                    {"id": "b", "text": "b was not passed; default is 0."},
                    {"id": "c", "text": "Return value must be printed."},
                ],
                correct_diagnosis="b",
                fix_code="def add(a, b=0):\n    return a + b\nprint(add(5, 5))\n",
                fix_steps=["Pass both arguments or use a meaningful default."],
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
        ConceptFrame(
            concept_id="functions",
            frame_order=3,
            frame_type="transfer",
            transfer=TransferFrame(
                prompt="Write a function that filters positive numbers.",
                starter_code="def positives(values):\n    # your code\n    pass\nprint(positives([-1, 0, 1, 2]))\n",
                language="python",
                test_cases=[
                    {"type": "contains", "expected": "1", "count": 1},
                ],
                hidden_tests=4,
                success_condition="returns only positive values",
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
    ],
    "errors": [
        ConceptFrame(
            concept_id="errors",
            frame_order=0,
            frame_type="predict",
            predict=PredictFrame(
                prompt="Which traceback message appears?",
                code="x = 1 / 0\n",
                options=[
                    {"id": "a", "text": "ZeroDivisionError"},
                    {"id": "b", "text": "ValueError"},
                    {"id": "c", "text": "NameError"},
                ],
                correct_index=0,
                explanation="Integer division by zero raises ZeroDivisionError.",
            ),
            xp_reward=5,
            diamonds_reward=2,
        ),
        ConceptFrame(
            concept_id="errors",
            frame_order=1,
            frame_type="manipulate",
            manipulate=ManipulateFrame(
                starter_code="# Catch a ZeroDivisionError\n# Your code below\n",
                language="python",
                scaffold_prompt="Wrap 1 / 0 in try/except ZeroDivisionError.",
                target_variable="result",
                hint="try: result = 1/0\nexcept ZeroDivisionError: result = None",
                success_condition="no unhandled exception",
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
        ConceptFrame(
            concept_id="errors",
            frame_order=2,
            frame_type="break",
            break_frame=BreakFrame(
                buggy_code="try:\n    1 / 0\nexcept:\n    pass\nprint('done')\n",
                language="python",
                failure_description="The program silently ignores the error.",
                diagnosis_options=[
                    {"id": "a", "text": "Bare except hides the real exception."},
                    {"id": "b", "text": "pass is deprecated."},
                    {"id": "c", "text": "try needs finally."},
                ],
                correct_diagnosis="a",
                fix_code="try:\n    1 / 0\nexcept ZeroDivisionError:\n    print('caught')\n",
                fix_steps=["Catch specific exceptions and handle them."],
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
        ConceptFrame(
            concept_id="errors",
            frame_order=3,
            frame_type="transfer",
            transfer=TransferFrame(
                prompt="Write a safe integer conversion with fallback.",
                starter_code="def to_int(s):\n    # your code\n    pass\nprint(to_int('abc'))\n",
                language="python",
                test_cases=[
                    {"type": "contains", "expected": "None", "count": 1},
                ],
                hidden_tests=3,
                success_condition="returns None for bad input",
            ),
            xp_reward=8,
            diamonds_reward=3,
        ),
    ],
}


def get_cfic_graph() -> ConceptGraph:
    """Return the additive CFIC concept graph (no side effects)."""
    return ConceptGraph(nodes=list(_CFIC_NODES), edges=list(_CFIC_EDGES))


def get_cfic_frames(concept_id: str) -> List[ConceptFrame]:
    """Return frames for one concept, or [] if concept is not in the additive graph."""
    return list(_CFIC_FRAMES.get(concept_id, []))


def get_cfic_content(concept_id: str) -> Optional[ConceptContent]:
    """Return additive content for one concept, or None."""
    node = next((n for n in _CFIC_NODES if n.concept_id == concept_id), None)
    if node is None:
        return None
    return ConceptContent(concept=node, frames=get_cfic_frames(concept_id))
