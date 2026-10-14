"""Universal World Wrappers
=========================

Converts ALL existing world levels to the full teaching loop format:
  Hook → See → Understand → Touch → Predict → Change → Build → Break →
  Fix → Retrieve → Transfer → Prove → Reward

Every level across all 13 worlds gets:
- Captain Byte authored moments for each phase
- Visual primitive hints
- Full vertical slice structure
- Backward-compatible with existing LessonService
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.data.worlds_data import (
    WORLD_FOUNDATIONS,
    WORLD_SEARCHLANDS,
    WORLD_SORTING,
)
from app.content.worlds_3_to_6 import (
    WORLD_3_BUILD_SYSTEMS,
    WORLD_4_WORK_WITH_DATA,
    WORLD_5_SOFTWARE_ENGINEERING,
    WORLD_6_UNDER_PRESSURE,
)
from app.content.worlds_7_to_9 import (
    WORLD_7_HIRING_ARENA,
    WORLD_8_COMPANY_MISSIONS,
    WORLD_9_AI_ENGINEERING,
)
from app.content.worlds_10_to_12 import (
    WORLD_10_PRODUCTION,
    WORLD_11_PROJECTS,
    WORLD_12_CREATIVE,
)

ALL_WORLDS = [
    WORLD_FOUNDATIONS,
    WORLD_SEARCHLANDS,
    WORLD_SORTING,
    WORLD_3_BUILD_SYSTEMS,
    WORLD_4_WORK_WITH_DATA,
    WORLD_5_SOFTWARE_ENGINEERING,
    WORLD_6_UNDER_PRESSURE,
    WORLD_7_HIRING_ARENA,
    WORLD_8_COMPANY_MISSIONS,
    WORLD_9_AI_ENGINEERING,
    WORLD_10_PRODUCTION,
    WORLD_11_PROJECTS,
    WORLD_12_CREATIVE,
]

_WORLD_THEME_WORDS: Dict[str, List[str]] = {
    "foundations": ["variable", "box", "remember", "name", "label", "store", "value", "print"],
    "search": ["search", "find", "look", "scan", "linear", "binary", "sorted"],
    "sorting": ["sort", "swap", "order", "merge", "bubble", "arrange"],
    "recursion": ["recursive", "base case", "call", "self", "mirror", "stack"],
    "linked": ["linked", "node", "chain", "pointer", "next", "reverse"],
    "stack": ["stack", "push", "pop", "lifo", "tower", "plate"],
    "queue": ["queue", "fifo", "line", "enqueue", "dequeue"],
    "hashing": ["hash", "map", "lookup", "key", "value", "store"],
    "tree": ["tree", "node", "root", "leaf", "branch", "traverse"],
    "graph": ["graph", "node", "edge", "path", "traverse", "bfs", "dfs"],
    "dp": ["dynamic", "memo", "subproblem", "optimal", "recurrence", "bottom-up"],
    "string": ["string", "text", "character", "palindrome", "anagram"],
    "array": ["array", "list", "subarray", "window", "pointer"],
    "system_design": ["system", "scale", "latency", "database", "cache", "load balancer"],
    "behavioral": ["behavioral", "situation", "team", "conflict", "leadership"],
    "ai": ["ai", "model", "prompt", "generation", "embedding", "vector"],
    "project": ["project", "build", "ship", "deploy", "feature", "user"],
    "production": ["production", "incident", "monitor", "alert", "deploy", "rollback"],
}


def _world_theme(world_id: str) -> str:
    return world_id.split("_")[0] if "_" in world_id else world_id


def _visual_primitives_for(world_id: str, canonical_skill: str) -> List[str]:
    theme = _world_theme(world_id)
    skill = (canonical_skill or "").lower()
    title_words = _WORLD_THEME_WORDS.get(theme, [])
    if any(w in skill for w in ["two pointer", "sliding", "window", "array"]):
        return ["move", "compare", "trace"]
    if any(w in skill for w in ["binary", "search"]):
        return ["split", "compare", "trace"]
    if any(w in skill for w in ["hash", "map"]):
        return ["highlight", "compare"]
    if any(w in skill for w in ["tree", "dfs", "bfs", "graph"]):
        return ["trace", "move", "reveal"]
    if any(w in skill for w in ["dp", "memo", "tabulation"]):
        return ["transform", "merge", "highlight"]
    if any(w in skill for w in ["string", "text"]):
        return ["highlight", "compare", "trace"]
    if any(w in skill for w in ["linked", "list"]):
        return ["move", "trace"]
    if any(w in skill for w in ["stack", "queue"]):
        return ["move", "transform"]
    if any(w in skill for w in ["sort", "merge", "bubble"]):
        return ["move", "transform", "compare"]
    if any(w in skill for w in ["recurs"]):
        return ["trace", "split", "reveal"]
    return ["highlight", "trace"]


def _captain_byte_for(world_id: str, level_title: str, canonical_skill: str) -> Dict[str, Any]:
    theme = _world_theme(world_id)
    title_lower = level_title.lower()
    skill = (canonical_skill or "").lower()

    if theme == "foundations" or any(w in skill for w in ["variable", "naming", "assignment"]):
        return {
            "intro": "🧭 **Captain Byte**\n“Welcome to the foundations. Every program starts with a named box. I will show you how to label, update, and compute with them.”",
            "correct": ["🧭 **Captain Byte**\n“Nice. You labeled the box correctly.”", "🧭 **Captain Byte**\n“Clean. The program remembers now.”"],
            "wrong": ["🧭 **Captain Byte**\n“Stop. Don’t guess the final value. Trace the box line by line.”", "🧭 **Captain Byte**\n“You’re missing a label. What does the program need to remember?”"],
            "after_break": "🧭 **Captain Byte**\n“You found the broken assumption. Now repair the trace.”",
            "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Any variable problem.”",
            "retry_prompt": "🧭 **Captain Byte**\n“Try again. Follow each box from top to bottom.”",
        }
    if theme == "search" or any(w in skill for w in ["search", "binary", "linear"]):
        return {
            "intro": "🧭 **Captain Byte**\n“Search is about finding things fast. Start at the beginning, check each item, or cut the space in half.”",
            "correct": ["🧭 **Captain Byte**\n“Nice. You found the target efficiently.”", "🧭 **Captain Byte**\n“Clean. That is how search works.”"],
            "wrong": ["🧭 **Captain Byte**\n“Stop. Don’t scan blindly. What structure helps you skip?”", "🧭 **Captain Byte**\n“You’re checking everything. Use the order.”"],
            "after_break": "🧭 **Captain Byte**\n“You found the bad assumption. Now search correctly.”",
            "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Any search problem.”",
            "retry_prompt": "🧭 **Captain Byte**\n“Try again. Start at the beginning or cut the space in half.”",
        }
    if theme == "sorting" or any(w in skill for w in ["sort", "bubble", "merge", "order"]):
        return {
            "intro": "🧭 **Captain Byte**\n“Sorting puts things in order. Compare neighbors, swap, or divide and merge.”",
            "correct": ["🧭 **Captain Byte**\n“Nice. The list is in order.”", "🧭 **Captain Byte**\n“Clean. Sorting is systematic.”"],
            "wrong": ["🧭 **Captain Byte**\n“Stop. Don’t swap randomly. Compare the right pair.”", "🧭 **Captain Byte**\n“You’re missing a pass. Keep going until no swaps.”"],
            "after_break": "🧭 **Captain Byte**\n“You found the broken assumption. Now sort correctly.”",
            "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Any sorting problem.”",
            "retry_prompt": "🧭 **Captain Byte**\n“Try again. Compare neighbors or divide and conquer.”",
        }
    if theme == "recursion" or any(w in skill for w in ["recurs", "base case", "call stack"]):
        return {
            "intro": "🧭 **Captain Byte**\n“Recursion solves big problems by solving smaller versions of themselves. Every recursive journey needs a base case.”",
            "correct": ["🧭 **Captain Byte**\n“Nice. You found the base case.”", "🧭 **Captain Byte**\n“Clean. The recursion unwinds correctly.”"],
            "wrong": ["🧭 **Captain Byte**\n“Stop. Don’t recurse forever. What is the smallest case?”", "🧭 **Captain Byte**\n“You’re missing the base case. Add it.”"],
            "after_break": "🧭 **Captain Byte**\n“You found the broken assumption. Now recurse correctly.”",
            "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Any recursive problem.”",
            "retry_prompt": "🧭 **Captain Byte**\n“Try again. Base case first, then recurse.”",
        }
    if theme == "linked" or any(w in skill for w in ["linked", "node", "chain", "pointer"]):
        return {
            "intro": "🧭 **Captain Byte**\n“A linked list is a chain of nodes. You can’t jump to index i — you must walk the chain.”",
            "correct": ["🧭 **Captain Byte**\n“Nice. You walked the chain correctly.”", "🧭 **Captain Byte**\n“Clean. The pointers are right.”"],
            "wrong": ["🧭 **Captain Byte**\n“Stop. Don’t treat it like an array. Walk the chain.”", "🧭 **Captain Byte**\n“You lost a node. Track prev before changing next.”"],
            "after_break": "🧭 **Captain Byte**\n“You found the bad assumption. Now track the pointers correctly.”",
            "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Any linked-list problem.”",
            "retry_prompt": "🧭 **Captain Byte**\n“Try again. Track prev, current, next.”",
        }
    if theme == "stack" or any(w in skill for w in ["stack", "push", "pop", "lifo"]):
        return {
            "intro": "🧭 **Captain Byte**\n“A stack is Last In, First Out. Push onto the top, pop from the top.”",
            "correct": ["🧭 **Captain Byte**\n“Nice. The stack behaves correctly.”", "🧭 **Captain Byte**\n“Clean. LIFO is second nature now.”"],
            "wrong": ["🧭 **Captain Byte**\n“Stop. Don’t use a list for everything. What ordering does this need?”", "🧭 **Captain Byte**\n“You’re popping from the wrong end.”"],
            "after_break": "🧭 **Captain Byte**\n“You found the bad assumption. Now use the stack correctly.”",
            "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Any stack problem.”",
            "retry_prompt": "🧭 **Captain Byte**\n“Try again. Push and pop from the same end.”",
        }
    if theme == "queue" or any(w in skill for w in ["queue", "fifo", "dequeue"]):
        return {
            "intro": "🧭 **Captain Byte**\n“A queue is First In, First Out. Enqueue at the back, dequeue from the front.”",
            "correct": ["🧭 **Captain Byte**\n“Nice. The queue behaves correctly.”", "🧭 **Captain Byte**\n“Clean. FIFO is second nature now.”"],
            "wrong": ["🧭 **Captain Byte**\n“Stop. Don’t treat it like a stack. What ordering does this need?”", "🧭 **Captain Byte**\n“You’re removing from the wrong end.”"],
            "after_break": "🧭 **Captain Byte**\n“You found the bad assumption. Now use the queue correctly.”",
            "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Any queue problem.”",
            "retry_prompt": "🧭 **Captain Byte**\n“Try again. Enqueue back, dequeue front.”",
        }
    if theme == "hashing" or any(w in skill for w in ["hash", "map", "lookup"]):
        return {
            "intro": "🧭 **Captain Byte**\n“A hash map gives O(1) lookup. Trade memory for speed.”",
            "correct": ["🧭 **Captain Byte**\n“Nice. You stored the complement and looked it up.”", "🧭 **Captain Byte**\n“Clean. Hash map turns O(n²) into O(n).”"],
            "wrong": ["🧭 **Captain Byte**\n“Stop. Don’t scan the array again. What did you already store?”", "🧭 **Captain Byte**\n“You’re doing nested loops. The hash map removes the inner loop.”"],
            "after_break": "🧭 **Captain Byte**\n“You found the bad assumption. Now use the map correctly.”",
            "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Any lookup problem.”",
            "retry_prompt": "🧭 **Captain Byte**\n“Try again. Store what you need, then look it up in O(1).”",
        }
    if theme == "tree" or any(w in skill for w in ["tree", "dfs", "bfs", "traverse"]):
        return {
            "intro": "🧭 **Captain Byte**\n“Trees are hierarchies. DFS goes deep first. BFS goes level by level.”",
            "correct": ["🧭 **Captain Byte**\n“Nice. You chose the right traversal.”", "🧭 **Captain Byte**\n“Clean. Recursion or queue — both work.”"],
            "wrong": ["🧭 **Captain Byte**\n“Stop. Don’t traverse randomly. What does the question need?”", "🧭 **Captain Byte**\n“You’re missing a subtree. Don’t forget the children.”"],
            "after_break": "🧭 **Captain Byte**\n“You found the bad assumption. Now traverse correctly.”",
            "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Any tree problem.”",
            "retry_prompt": "🧭 **Captain Byte**\n“Try again. Depth or breadth? Recursion or queue?”",
        }
    if theme == "graph" or any(w in skill for w in ["graph", "edge", "node", "path"]):
        return {
            "intro": "🧭 **Captain Byte**\n“Graphs model connections. BFS finds shortest path. DFS explores all paths. Topological sort orders dependencies.”",
            "correct": ["🧭 **Captain Byte**\n“Nice. You chose the right graph algorithm.”", "🧭 **Captain Byte**\n“Clean. Adjacency list + visited set.”"],
            "wrong": ["🧭 **Captain Byte**\n“Stop. Don’t treat it like a tree. Graphs can cycle.”", "🧭 **Captain Byte**\n“You’re revisiting nodes. Track visited.”"],
            "after_break": "🧭 **Captain Byte**\n“You found the bad assumption. Now handle cycles and visited nodes.”",
            "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Any graph problem.”",
            "retry_prompt": "🧭 **Captain Byte**\n“Try again. BFS for shortest path, DFS for all paths, topo for dependencies.”",
        }
    if theme == "dp" or any(w in skill for w in ["dp", "memo", "tabulation", "dynamic"]):
        return {
            "intro": "🧭 **Captain Byte**\n“Dynamic programming is about overlapping subproblems. Memoization stores results. Tabulation builds bottom-up.”",
            "correct": ["🧭 **Captain Byte**\n“Nice. You identified the subproblem and reused the result.”", "🧭 **Captain Byte**\n“Clean. The recurrence is the heart of DP.”"],
            "wrong": ["🧭 **Captain Byte**\n“Stop. Don’t recompute. What did you already solve?”", "🧭 **Captain Byte**\n“You’re doing O(2^n). Cache the subproblem results.”"],
            "after_break": "🧭 **Captain Byte**\n“You found the bad assumption. Now define the recurrence correctly.”",
            "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Any DP problem.”",
            "retry_prompt": "🧭 **Captain Byte**\n“Try again. What’s the smallest subproblem? How does it build up?”",
        }
    if theme == "system_design" or any(w in skill for w in ["system", "design", "scale", "latency"]):
        return {
            "intro": "🧭 **Captain Byte**\n“System design is about trade-offs. Scale, consistency, availability — pick the right balance.”",
            "correct": ["🧭 **Captain Byte**\n“Nice. You balanced the trade-offs correctly.”", "🧭 **Captain Byte**\n“Clean. That is the right architecture.”"],
            "wrong": ["🧭 **Captain Byte**\n“Stop. Don’t over-engineer. What is the actual bottleneck?”", "🧭 **Captain Byte**\n“You’re missing the bottleneck. Identify it first.”"],
            "after_break": "🧭 **Captain Byte**\n“You found the bad assumption. Now design with the right trade-offs.”",
            "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Any system design problem.”",
            "retry_prompt": "🧭 **Captain Byte**\n“Try again. Identify the bottleneck, then choose the right component.”",
        }
    if theme == "behavioral" or any(w in skill for w in ["behavioral", "situation", "team", "conflict"]):
        return {
            "intro": "🧭 **Captain Byte**\n“Behavioral interviews are stories. Use STAR: Situation, Task, Action, Result.”",
            "correct": ["🧭 **Captain Byte**\n“Nice. That is a clear STAR story.”", "🧭 **Captain Byte**\n“Clean. You showed impact.”"],
            "wrong": ["🧭 **Captain Byte**\n“Stop. Don’t list duties. What did YOU do?”", "🧭 **Captain Byte**\n“You’re missing the result. Show impact.”"],
            "after_break": "🧭 **Captain Byte**\n“You found the gap. Now rebuild the story with STAR.”",
            "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Any behavioral question.”",
            "retry_prompt": "🧭 **Captain Byte**\n“Try again. Situation, Task, Action, Result.”",
        }
    if theme == "ai" or any(w in skill for w in ["ai", "model", "prompt", "generation"]):
        return {
            "intro": "🧭 **Captain Byte**\n“AI systems learn patterns from data. Prompt, generate, evaluate — the loop is the same.”",
            "correct": ["🧭 **Captain Byte**\n“Nice. You understand the AI pattern.”", "🧭 **Captain Byte**\n“Clean. That is how the model works.”"],
            "wrong": ["🧭 **Captain Byte**\n“Stop. Don’t guess the output. What does the model actually do?”", "🧭 **Captain Byte**\n“You’re missing the prompt structure.”"],
            "after_break": "🧭 **Captain Byte**\n“You found the gap. Now fix the AI pipeline.”",
            "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Any AI problem.”",
            "retry_prompt": "🧭 **Captain Byte**\n“Try again. What is the input, what is the model, what is the output?”",
        }
    if theme == "production" or any(w in skill for w in ["production", "incident", "monitor", "alert"]):
        return {
            "intro": "🧭 **Captain Byte**\n“Production is where theory meets reality. Incidents happen. You debug, fix, and prevent.”",
            "correct": ["🧭 **Captain Byte**\n“Nice. You handled the incident correctly.”", "🧭 **Captain Byte**\n“Clean. That is how you debug in production.”"],
            "wrong": ["🧭 **Captain Byte**\n“Stop. Don’t restart blindly. Read the logs first.”", "🧭 **Captain Byte**\n“You’re missing the root cause. Dig deeper.”"],
            "after_break": "🧭 **Captain Byte**\n“You found the gap. Now fix the production issue.”",
            "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Any production problem.”",
            "retry_prompt": "🧭 **Captain Byte**\n“Try again. Read the logs, identify the root cause, fix it.”",
        }
    if theme == "project" or any(w in skill for w in ["project", "build", "ship", "deploy"]):
        return {
            "intro": "🧭 **Captain Byte**\n“Projects are where you ship. Plan, build, test, deploy — the full loop.”",
            "correct": ["🧭 **Captain Byte**\n“Nice. You shipped the feature.”", "🧭 **Captain Byte**\n“Clean. That is how projects succeed.”"],
            "wrong": ["🧭 **Captain Byte**\n“Stop. Don’t skip testing. What breaks?”", "🧭 **Captain Byte**\n“You’re missing the user need. Start there.”"],
            "after_break": "🧭 **Captain Byte**\n“You found the gap. Now build with the user in mind.”",
            "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Any project.”",
            "retry_prompt": "🧭 **Captain Byte**\n“Try again. Plan, build, test, ship.”",
        }
    return {
        "intro": "🧭 **Captain Byte**\n“Let’s master this. Follow the steps, and I’ll guide you.”",
        "correct": ["🧭 **Captain Byte**\n“Nice work.”", "🧭 **Captain Byte**\n“Clean execution.”"],
        "wrong": ["🧭 **Captain Byte**\n“Try again. Read the hint carefully.”", "🧭 **Captain Byte**\n“Close. Check your assumption.”"],
        "after_break": "🧭 **Captain Byte**\n“You found the issue. Now fix it.”",
        "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. Next challenge.”",
        "retry_prompt": "🧭 **Captain Byte**\n“Try again. You’re close.”",
    }


def _options_list(opts) -> List[Dict[str, Any]]:
    if not opts:
        return []
    return [
        {
            "id": o.get("id", ""),
            "text": o.get("text", ""),
            "correct": o.get("correct", False),
            "explanation": o.get("explanation", ""),
        }
        for o in opts
    ]


def _keywords_from(text: str, max_words: int = 8) -> List[str]:
    stop = {"the", "a", "an", "is", "are", "was", "were", "to", "of", "and", "or", "in", "on", "at", "for", "by", "with", "from", "as", "that", "this", "it", "be", "have", "has", "had", "will", "would", "could", "should", "may", "might", "can", "do", "does", "did", "not", "no", "yes", "but", "if", "so", "than", "then", "when", "where", "how", "what", "which", "who", "whom", "their", "its", "his", "her", "they", "them", "you", "your", "my", "we", "our"}
    words = []
    for w in text.lower().replace(",", " ").replace(".", " ").replace("!", " ").replace("?", " ").split():
        w = w.strip()
        if not w:
            continue
        if w.isdigit() or (len(w) > 2 and w not in stop):
            words.append(w)
    seen = set()
    out = []
    for w in words:
        if w not in seen:
            seen.add(w)
            out.append(w)
        if len(out) >= max_words:
            break
    return out


def _as_step(step_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"step_type": step_type, **payload}


def convert_level_to_flagship(level) -> Dict[str, Any]:
    """Convert any Level or Boss or LessonDefinition to the full flagship vertical slice dict."""
    is_lesson_def = hasattr(level, "steps") and hasattr(level, "tutor_discover")
    world_id = getattr(level, "world_id", "") or ""
    canonical_skill = getattr(level, "canonical_skill", "") or getattr(level, "concept", "") or ""
    captain_byte = _captain_byte_for(world_id, level.title, canonical_skill)
    visual_primitives = _visual_primitives_for(world_id, canonical_skill)

    if is_lesson_def:
        return _convert_lesson_definition(level, captain_byte, visual_primitives, canonical_skill, world_id)

    story = getattr(level, "story", None) or type("S", (), {"location": "", "npc": "", "line": ""})()
    tutor = getattr(level, "tutor", None) or type("T", (), {"discover": "", "explain": ""})()
    discover = getattr(level, "discover", None) or type("D", (), {"visual": "", "interaction": "", "prompt": "", "answer": "", "values": None})()
    manipulate = getattr(level, "manipulate", None) or type("M", (), {"type": "", "template": "", "answer": "", "blocks": None, "hint": None})()
    predict = getattr(level, "predict", None)
    build = getattr(level, "build", None)
    break_step = getattr(level, "break_step", None)
    debug = getattr(level, "debug", None)
    retrieval = getattr(level, "retrieval", None)
    transfer = getattr(level, "transfer", None)
    code = getattr(level, "code", None) or type("C", (), {"prompt": "", "starter": "", "placeholder": "", "language": "python"})()
    checks = getattr(level, "checks", None) or type("Ch", (), {"required_patterns": [], "forbidden": [], "hint_triggers": []})()
    hints = getattr(level, "hints", []) or []
    success = getattr(level, "success", None) or type("Su", (), {"world_before": "", "world_after": "", "world_reaction": "", "reward_text": "", "byte_line": "", "diamonds": 0})()
    reward = getattr(level, "reward", None) or type("R", (), {"diamonds": success.diamonds, "coins": 0, "badges": [], "unlocks_town": None, "unlocks_world": None, "title": None})()

    return _convert_old_level(level, story, tutor, discover, manipulate, predict, build, break_step, debug, retrieval, transfer, code, checks, hints, success, reward, captain_byte, visual_primitives, canonical_skill, world_id)


def _convert_old_level(level, story, tutor, discover, manipulate, predict, build, break_step, debug, retrieval, transfer, code, checks, hints, success, reward, captain_byte, visual_primitives, canonical_skill, world_id) -> Dict[str, Any]:

    discovery_steps = [
        _as_step("discover", {
            "action": "discover",
            "narration": discover.visual or tutor.discover or "",
            "interaction": {
                "type": discover.interaction or "inspect_code",
                "code": discover.answer or "",
                "expected_output": discover.values[0] if discover.values else "",
                "hint": manipulate.hint or "",
            },
        }),
    ]
    if predict:
        discovery_steps.append(_as_step("predict", {
            "action": "predict",
            "narration": predict.prompt or "",
            "interaction": {
                "type": "choose_outcome",
                "prompt": predict.prompt or "",
                "options": _options_list([
                    {"id": "a", "text": predict.answer or "", "correct": True, "explanation": predict.explanation or ""},
                ]),
                "expected_answer": predict.answer or "",
                "explanation": predict.explanation or "",
            },
        }))

    discovery_section = {
        "title": level.title,
        "visual_primitives": visual_primitives,
        "steps": discovery_steps,
        "conclusion": success.world_reaction or "",
    }

    predict_section = {}
    if predict:
        predict_section = {
            "title": "Predict",
            "captain_byte_intro": captain_byte["intro"],
            "question": predict.prompt or "",
            "options": _options_list([
                {"id": "a", "text": predict.answer or "", "correct": True, "explanation": predict.explanation or ""},
            ]),
            "explanation": predict.explanation or "",
        }

    explain_section = {
        "title": "Understand",
        "captain_byte_intro": captain_byte["intro"],
        "prompt": tutor.explain or tutor.discover or "",
        "answer_format": "short_answer",
        "keywords": _keywords_from(tutor.explain or tutor.discover or ""),
        "min_words": 8,
        "model_answer": tutor.explain or tutor.discover or "",
        "intention": "Explain the concept in your own words.",
    }

    build_steps = []
    if build:
        build_steps.append({
            "step_order": 1,
            "title": level.title,
            "captain_byte_moment": captain_byte["intro"],
            "description": build.prompt or code.prompt or "",
            "starter_code": build.starter or code.starter or "",
            "function_name": "solution",
            "signature": build.placeholder or code.starter or "",
            "test_cases": [],
            "hidden_test_cases": [],
            "diamonds": reward.diamonds // 2,
            "scaffolded_hints": [{"level": i + 1, "text": h} for i, h in enumerate(hints)],
        })

    transfer_section = {}
    if transfer:
        transfer_section = {
            "title": "Transfer",
            "captain_byte_intro": captain_byte["retry_prompt"],
            "description": transfer.prompt or "",
            "function_name": "solution",
            "signature": "",
            "description_full": transfer.context or transfer.prompt or "",
            "test_cases": [],
            "hidden_test_cases": [],
            "time_limit_minutes": 7,
            "diamonds": reward.diamonds // 2,
            "scaffolded_hints": [{"level": 1, "text": transfer.answer or ""}],
        }

    assessment_questions = []
    if predict:
        assessment_questions.append({
            "type": "concept",
            "question": predict.prompt or "",
            "answer_format": "short_answer",
            "keywords": _keywords_from(predict.answer or ""),
            "expected_answer": predict.answer or "",
            "explanation": predict.explanation or "",
        })
    if retrieval:
        assessment_questions.append({
            "type": "concept",
            "question": retrieval.prompt or "",
            "answer_format": "short_answer",
            "keywords": _keywords_from(retrieval.answer or ""),
            "expected_answer": retrieval.answer or "",
            "explanation": retrieval.explanation or "",
        })
    if not assessment_questions:
        assessment_questions.append({
            "type": "concept",
            "question": f"What is the key insight of {level.title}?",
            "answer_format": "short_answer",
            "keywords": _keywords_from(tutor.explain or tutor.discover or ""),
            "expected_answer": "",
            "explanation": tutor.explain or tutor.discover or "",
        })

    assessment_section = {
        "title": f"{level.title} Mastery",
        "captain_byte_intro": captain_byte["after_mastery"],
        "description": tutor.explain or tutor.discover or "",
        "questions": assessment_questions,
        "mastery_threshold": getattr(level, "mastery_threshold", None) or 70,
        "diamonds": reward.diamonds,
    }

    break_section = {
        "title": "What Breaks?",
        "captain_byte_intro": captain_byte["after_break"],
        "story": break_step.prompt if break_step else "",
        "buggy_code": break_step.broken_code if break_step else "",
        "expected_output": "",
        "actual_output": break_step.expected_failure if break_step else "",
        "diagnosis": {
            "question": break_step.prompt if break_step else "Which assumption is wrong?",
            "options": _options_list([
                {"id": "a", "text": "The logic assumes the wrong condition", "correct": True, "why": "The broken code makes an unsafe assumption."},
                {"id": "b", "text": "The input is wrong", "correct": False, "why": "The input is correct; the logic is broken."},
                {"id": "c", "text": "The output format is wrong", "correct": False, "why": "The output format is fine."},
                {"id": "d", "text": "The function name is wrong", "correct": False, "why": "The name is fine."},
            ]),
        },
        "fix": debug.answer if debug else "",
        "fixed_code": debug.answer if debug else "",
        "explanation": debug.prompt if debug else break_step.expected_failure if break_step else "",
    }

    srs_key_points = []
    if tutor.discover:
        srs_key_points.append(tutor.discover)
    if tutor.explain:
        srs_key_points.append(tutor.explain)
    if predict and predict.explanation:
        srs_key_points.append(predict.explanation)
    if not srs_key_points:
        srs_key_points = [level.mental_model or level.title]

    return {
        "lesson_id": level.id,
        "module_id": level.concept or level.id,
        "title": level.title,
        "description": level.mental_model or level.title,
        "difficulty": "medium",
        "est_minutes": getattr(level, "estimated_minutes", None) or 15,
        "xp_reward": reward.diamonds,
        "skills_taught": [canonical_skill] if canonical_skill else [level.concept],
        "srs_concept_tag": canonical_skill or level.concept or level.id,
        "captain_byte": captain_byte,
        "story_context": {
            "title": level.title,
            "narration": story.line or tutor.discover or "",
            "setting": story.location or "",
            "character": story.npc or "Captain Byte",
            "intro_text": tutor.discover or tutor.explain or level.mental_model or "",
        },
        "discovery": discovery_section,
        "prediction": predict_section,
        "explain": explain_section,
        "guided_build": {"steps": build_steps, "captain_byte_intro": captain_byte["intro"]},
        "transfer_challenge": transfer_section,
        "assessment": assessment_section,
        "break": break_section,
        "srs_enrollment": {
            "concept_id": canonical_skill or level.concept or level.id,
            "concept_name": level.title,
            "review_intervals": [1, 3, 7, 14, 30],
            "key_points": srs_key_points,
            "spaced_fields": [level.concept],
        },
        "world_progression": {
            "world_id": world_id,
            "competency_id": level.concept,
            "unlocks_next": [level.unlocks] if getattr(level, "unlocks", None) else [],
            "tower_badge": level.id,
            "world_node": {
                "level": level.order,
                "title": level.title,
                "color": "teal",
                "icon": level.icon,
                "description": level.mental_model or "",
            },
        },
    }


def _convert_old_level(level, story, tutor, discover, manipulate, predict, build, break_step, debug, retrieval, transfer, code, checks, hints, success, reward, captain_byte, visual_primitives, canonical_skill, world_id) -> Dict[str, Any]:
    discovery_steps = [
        _as_step("discover", {
            "action": "discover",
            "narration": discover.visual or tutor.discover or "",
            "interaction": {
                "type": discover.interaction or "inspect_code",
                "code": discover.answer or "",
                "expected_output": discover.values[0] if discover.values else "",
                "hint": manipulate.hint or "",
            },
        }),
    ]
    if predict:
        discovery_steps.append(_as_step("predict", {
            "action": "predict",
            "narration": predict.prompt or "",
            "interaction": {
                "type": "choose_outcome",
                "prompt": predict.prompt or "",
                "options": _options_list([
                    {"id": "a", "text": predict.answer or "", "correct": True, "explanation": predict.explanation or ""},
                ]),
                "expected_answer": predict.answer or "",
                "explanation": predict.explanation or "",
            },
        }))

    discovery_section = {
        "title": level.title,
        "visual_primitives": visual_primitives,
        "steps": discovery_steps,
        "conclusion": success.world_reaction or "",
    }

    predict_section = {}
    if predict:
        predict_section = {
            "title": "Predict",
            "captain_byte_intro": captain_byte["intro"],
            "question": predict.prompt or "",
            "options": _options_list([
                {"id": "a", "text": predict.answer or "", "correct": True, "explanation": predict.explanation or ""},
            ]),
            "explanation": predict.explanation or "",
        }

    explain_section = {
        "title": "Understand",
        "captain_byte_intro": captain_byte["intro"],
        "prompt": tutor.explain or tutor.discover or "",
        "answer_format": "short_answer",
        "keywords": _keywords_from(tutor.explain or tutor.discover or ""),
        "min_words": 8,
        "model_answer": tutor.explain or tutor.discover or "",
        "intention": "Explain the concept in your own words.",
    }

    build_steps = []
    if build:
        build_steps.append({
            "step_order": 1,
            "title": level.title,
            "captain_byte_moment": captain_byte["intro"],
            "description": build.prompt or code.prompt or "",
            "starter_code": build.starter or code.starter or "",
            "function_name": "solution",
            "signature": build.placeholder or code.starter or "",
            "test_cases": [],
            "hidden_test_cases": [],
            "diamonds": reward.diamonds // 2,
            "scaffolded_hints": [{"level": i + 1, "text": h} for i, h in enumerate(hints)],
        })
    else:
        build_steps.append({
            "step_order": 1,
            "title": level.title,
            "captain_byte_moment": captain_byte["intro"],
            "description": code.prompt or "Write the solution.",
            "starter_code": code.starter or "",
            "function_name": "solution",
            "signature": code.starter or "",
            "test_cases": [],
            "hidden_test_cases": [],
            "diamonds": reward.diamonds // 2,
            "scaffolded_hints": [{"level": 1, "text": h} for h in hints],
        })

    transfer_section = {}
    if transfer:
        transfer_section = {
            "title": "Transfer",
            "captain_byte_intro": captain_byte["retry_prompt"],
            "description": transfer.prompt or "",
            "function_name": "solution",
            "signature": "",
            "description_full": transfer.context or transfer.prompt or "",
            "test_cases": [],
            "hidden_test_cases": [],
            "time_limit_minutes": 7,
            "diamonds": reward.diamonds // 2,
            "scaffolded_hints": [{"level": 1, "text": transfer.answer or ""}],
        }

    assessment_questions = []
    if predict:
        assessment_questions.append({
            "type": "concept",
            "question": predict.prompt or "",
            "answer_format": "short_answer",
            "keywords": _keywords_from(predict.answer or ""),
            "expected_answer": predict.answer or "",
            "explanation": predict.explanation or "",
        })
    if retrieval:
        assessment_questions.append({
            "type": "concept",
            "question": retrieval.prompt or "",
            "answer_format": "short_answer",
            "keywords": _keywords_from(retrieval.answer or ""),
            "expected_answer": retrieval.answer or "",
            "explanation": retrieval.explanation or "",
        })
    if not assessment_questions:
        assessment_questions.append({
            "type": "concept",
            "question": f"What is the key insight of {level.title}?",
            "answer_format": "short_answer",
            "keywords": _keywords_from(tutor.explain or tutor.discover or ""),
            "expected_answer": "",
            "explanation": tutor.explain or tutor.discover or "",
        })

    assessment_section = {
        "title": f"{level.title} Mastery",
        "captain_byte_intro": captain_byte["after_mastery"],
        "description": tutor.explain or tutor.discover or "",
        "questions": assessment_questions,
        "mastery_threshold": getattr(level, "mastery_threshold", None) or 70,
        "diamonds": reward.diamonds,
    }

    break_section = {
        "title": "What Breaks?",
        "captain_byte_intro": captain_byte["after_break"],
        "story": break_step.prompt if break_step else "",
        "buggy_code": break_step.broken_code if break_step else "",
        "expected_output": "",
        "actual_output": break_step.expected_failure if break_step else "",
        "diagnosis": {
            "question": break_step.prompt if break_step else "Which assumption is wrong?",
            "options": _options_list([
                {"id": "a", "text": "The logic assumes the wrong condition", "correct": True, "why": "The broken code makes an unsafe assumption."},
                {"id": "b", "text": "The input is wrong", "correct": False, "why": "The input is correct; the logic is broken."},
                {"id": "c", "text": "The output format is wrong", "correct": False, "why": "The output format is fine."},
                {"id": "d", "text": "The function name is wrong", "correct": False, "why": "The name is fine."},
            ]),
        },
        "fix": debug.answer if debug else "",
        "fixed_code": debug.answer if debug else "",
        "explanation": debug.prompt if debug else break_step.expected_failure if break_step else "",
    }

    srs_key_points = []
    if tutor.discover:
        srs_key_points.append(tutor.discover)
    if tutor.explain:
        srs_key_points.append(tutor.explain)
    if predict and predict.explanation:
        srs_key_points.append(predict.explanation)
    if not srs_key_points:
        srs_key_points = [level.mental_model or level.title]

    return {
        "lesson_id": level.id,
        "module_id": level.concept or level.id,
        "title": level.title,
        "description": level.mental_model or level.title,
        "difficulty": "medium",
        "est_minutes": getattr(level, "estimated_minutes", None) or 15,
        "xp_reward": reward.diamonds,
        "skills_taught": [canonical_skill] if canonical_skill else [level.concept],
        "srs_concept_tag": canonical_skill or level.concept or level.id,
        "captain_byte": captain_byte,
        "story_context": {
            "title": level.title,
            "narration": story.line or tutor.discover or "",
            "setting": story.location or "",
            "character": story.npc or "Captain Byte",
            "intro_text": tutor.discover or tutor.explain or level.mental_model or "",
        },
        "discovery": discovery_section,
        "prediction": predict_section,
        "explain": explain_section,
        "guided_build": {"steps": build_steps, "captain_byte_intro": captain_byte["intro"]},
        "transfer_challenge": transfer_section,
        "assessment": assessment_section,
        "break": break_section,
        "srs_enrollment": {
            "concept_id": canonical_skill or level.concept or level.id,
            "concept_name": level.title,
            "review_intervals": [1, 3, 7, 14, 30],
            "key_points": srs_key_points,
            "spaced_fields": [level.concept],
        },
        "world_progression": {
            "world_id": world_id,
            "competency_id": level.concept,
            "unlocks_next": [level.unlocks] if getattr(level, "unlocks", None) else [],
            "tower_badge": level.id,
            "world_node": {
                "level": level.order,
                "title": level.title,
                "color": "teal",
                "icon": level.icon,
                "description": level.mental_model or "",
            },
        },
    }


def _convert_lesson_definition(level, captain_byte: Dict[str, Any], visual_primitives: List[str], canonical_skill: str, world_id: str) -> Dict[str, Any]:
    steps = getattr(level, "steps", []) or []
    discovery_steps: List[Dict[str, Any]] = []
    for step in steps:
        st = str(getattr(step, "step_type", "discover")).lower()
        if st in ("discover", "manipulate", "predict", "build", "break", "debug", "retrieval", "transfer", "mastery"):
            discovery_steps.append(_as_step(st, {
                "action": st,
                "narration": step.content or step.title or "",
                "interaction": {
                    "type": "inspect_code",
                    "code": step.content or "",
                    "expected_output": "",
                    "hint": "",
                },
            }))

    if not discovery_steps:
        discovery_steps.append(_as_step("discover", {
            "action": "discover",
            "narration": level.tutor_discover or level.mental_model or "",
            "interaction": {
                "type": "inspect_code",
                "code": "",
                "expected_output": "",
                "hint": "",
            },
        }))

    discovery_section = {
        "title": level.title,
        "visual_primitives": visual_primitives,
        "steps": discovery_steps,
        "conclusion": level.why_this_matters or "",
    }

    predict_section = {}
    for step in steps:
        if str(getattr(step, "step_type", "")).lower() == "predict":
            predict_section = {
                "title": "Predict",
                "captain_byte_intro": captain_byte["intro"],
                "question": step.content or step.title or "",
                "options": _options_list([
                    {"id": "a", "text": step.content or "", "correct": True, "explanation": ""},
                ]),
                "explanation": "",
            }
            break

    explain_section = {
        "title": "Understand",
        "captain_byte_intro": captain_byte["intro"],
        "prompt": level.tutor_explain or level.tutor_discover or "",
        "answer_format": "short_answer",
        "keywords": _keywords_from(level.tutor_explain or level.tutor_discover or ""),
        "min_words": 8,
        "model_answer": level.tutor_explain or level.tutor_discover or "",
        "intention": "Explain the concept in your own words.",
    }

    build_steps = []
    for i, step in enumerate(steps):
        if str(getattr(step, "step_type", "")).lower() in ("build", "debug", "mastery"):
            build_steps.append({
                "step_order": i + 1,
                "title": step.title or level.title,
                "captain_byte_moment": captain_byte["intro"],
                "description": step.content or "",
                "starter_code": "",
                "function_name": "solution",
                "signature": "",
                "test_cases": [],
                "hidden_test_cases": [],
                "diamonds": level.diamonds // max(len(steps), 1),
                "scaffolded_hints": [{"level": 1, "text": level.tutor_explain or level.tutor_discover or ""}],
            })
    if not build_steps:
        build_steps.append({
            "step_order": 1,
            "title": level.title,
            "captain_byte_moment": captain_byte["intro"],
            "description": level.mental_model or "",
            "starter_code": "",
            "function_name": "solution",
            "signature": "",
            "test_cases": [],
            "hidden_test_cases": [],
            "diamonds": level.diamonds // 2,
            "scaffolded_hints": [{"level": 1, "text": level.tutor_explain or level.tutor_discover or ""}],
        })

    transfer_section = {}
    for step in steps:
        if str(getattr(step, "step_type", "")).lower() == "transfer":
            transfer_section = {
                "title": "Transfer",
                "captain_byte_intro": captain_byte["retry_prompt"],
                "description": step.content or "",
                "function_name": "solution",
                "signature": "",
                "description_full": step.content or "",
                "test_cases": [],
                "hidden_test_cases": [],
                "time_limit_minutes": 7,
                "diamonds": level.diamonds // 2,
                "scaffolded_hints": [{"level": 1, "text": step.content or ""}],
            }
            break

    assessment_questions = []
    for step in steps:
        st = str(getattr(step, "step_type", "")).lower()
        if st in ("retrieval", "mastery", "predict"):
            assessment_questions.append({
                "type": "concept",
                "question": step.title or step.content or f"What is {level.title}?",
                "answer_format": "short_answer",
                "keywords": _keywords_from(step.content or step.title or level.mental_model or ""),
                "expected_answer": "",
                "explanation": step.content or level.tutor_explain or "",
            })
    if not assessment_questions:
        assessment_questions.append({
            "type": "concept",
            "question": f"What is the key insight of {level.title}?",
            "answer_format": "short_answer",
            "keywords": _keywords_from(level.mental_model or level.tutor_discover or ""),
            "expected_answer": "",
            "explanation": level.tutor_explain or level.tutor_discover or "",
        })

    assessment_section = {
        "title": f"{level.title} Mastery",
        "captain_byte_intro": captain_byte["after_mastery"],
        "description": level.mental_model or level.tutor_discover or "",
        "questions": assessment_questions,
        "mastery_threshold": 70,
        "diamonds": level.diamonds,
    }

    break_section = {
        "title": "What Breaks?",
        "captain_byte_intro": captain_byte["after_break"],
        "story": "",
        "buggy_code": "",
        "expected_output": "",
        "actual_output": "",
        "diagnosis": {
            "question": "Which assumption is wrong?",
            "options": _options_list([
                {"id": "a", "text": "The logic assumes the wrong condition", "correct": True, "why": "The broken code makes an unsafe assumption."},
                {"id": "b", "text": "The input is wrong", "correct": False, "why": "The input is correct; the logic is broken."},
                {"id": "c", "text": "The output format is wrong", "correct": False, "why": "The output format is fine."},
                {"id": "d", "text": "The function name is wrong", "correct": False, "why": "The name is fine."},
            ]),
        },
        "fix": "",
        "fixed_code": "",
        "explanation": level.mental_model or "",
    }

    srs_key_points = [level.tutor_discover or "", level.tutor_explain or "", level.mental_model or ""]
    srs_key_points = [k for k in srs_key_points if k]
    if not srs_key_points:
        srs_key_points = [level.title]

    npc_name = getattr(level, "npc", "") or "Captain Byte"
    npc_line = getattr(level, "npc_line", "") or ""
    location = getattr(level, "location", "") or ""

    return {
        "lesson_id": level.id,
        "module_id": level.concept or level.id,
        "title": level.title,
        "description": level.mental_model or level.title,
        "difficulty": "medium",
        "est_minutes": getattr(level, "estimated_minutes", None) or 15,
        "xp_reward": level.diamonds,
        "skills_taught": [canonical_skill] if canonical_skill else [level.concept],
        "srs_concept_tag": canonical_skill or level.concept or level.id,
        "captain_byte": captain_byte,
        "story_context": {
            "title": level.title,
            "narration": npc_line or level.tutor_discover or "",
            "setting": location,
            "character": npc_name,
            "intro_text": level.why_this_matters or level.tutor_discover or level.mental_model or "",
        },
        "discovery": discovery_section,
        "prediction": predict_section,
        "explain": explain_section,
        "guided_build": {"steps": build_steps, "captain_byte_intro": captain_byte["intro"]},
        "transfer_challenge": transfer_section,
        "assessment": assessment_section,
        "break": break_section,
        "srs_enrollment": {
            "concept_id": canonical_skill or level.concept or level.id,
            "concept_name": level.title,
            "review_intervals": [1, 3, 7, 14, 30],
            "key_points": srs_key_points,
            "spaced_fields": [level.concept],
        },
        "world_progression": {
            "world_id": world_id,
            "competency_id": level.concept,
            "unlocks_next": [level.unlocks] if getattr(level, "unlocks", None) else [],
            "tower_badge": level.id,
            "world_node": {
                "level": level.order,
                "title": level.title,
                "color": "teal",
                "icon": getattr(level, "icon", "📘") or "📘",
                "description": level.mental_model or "",
            },
        },
    }


def get_all_world_lessons() -> Dict[str, Dict[str, Any]]:
    """Convert every level in every world to flagship format."""
    out: Dict[str, Dict[str, Any]] = {}
    for world in ALL_WORLDS:
        for town in world.towns:
            levels = getattr(town, "levels", None) or getattr(town, "lessons", None) or []
            for lvl in levels:
                try:
                    out[lvl.id] = convert_level_to_flagship(lvl)
                except Exception:
                    continue
    return out


def get_world_lesson(slug: str) -> Dict[str, Any]:
    """Return one converted world lesson by id."""
    for world in ALL_WORLDS:
        for town in world.towns:
            levels = getattr(town, "levels", None) or getattr(town, "lessons", None) or []
            for lvl in levels:
                if lvl.id == slug:
                    return convert_level_to_flagship(lvl)
    return {}
