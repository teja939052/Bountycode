"""World 2 wrappers — convert LessonDefinition world2 lessons to the vertical slice
dict format consumed by LessonService and the lesson route.

World2 lessons already exist as rich LessonDefinition objects in
world2_problem_solver.py. Rather than duplicate their content, these wrappers
restructure the step list into the canonical sections:
  discovery, prediction, explain, guided_build, transfer_challenge, assessment,
  break, srs_enrollment, world_progression
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.content.world2_problem_solver import (
    ARRAYS_TOWN,
    TREES_TOWN,
    GRAPHS_TOWN,
    DP_TOWN,
)
from app.content.lesson_definitions import LessonStep


def _step_to_dict(step: LessonStep) -> Dict[str, Any]:
    return step.model_dump()


def _first_step_by_type(steps: List[LessonStep], step_type: str) -> Optional[Dict[str, Any]]:
    for step in steps:
        if step.step_type == step_type:
            return _step_to_dict(step)
    return None


def _all_steps_by_type(steps: List[LessonStep], step_type: str) -> List[Dict[str, Any]]:
    return [_step_to_dict(s) for s in steps if s.step_type == step_type]


def _build_guided_step(step: LessonStep, order: int) -> Dict[str, Any]:
    tc_inputs = [tc.get("input", []) for tc in (step.test_cases or [])]
    return {
        "step_order": order,
        "title": step.title,
        "description": step.description or "",
        "starter_code": step.starter_code or step.starter or "",
        "function_name": step.function_name or "solution",
        "signature": step.signature or "",
        "test_cases": step.test_cases or [],
        "hidden_test_cases": [],
        "diamonds": 50,
        "scaffolded_hints": [
            {"level": i + 1, "text": h} for i, h in enumerate(step.repair_steps or [])
        ],
        "buggy_code": step.buggy_code or "",
        "fix_steps": step.fix_steps or [],
    }


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


def _make_vertical_slice(lesson_def) -> Dict[str, Any]:
    steps: List[LessonStep] = lesson_def.steps or []
    discover_steps = _all_steps_by_type(steps, "discover")
    predict_step = _first_step_by_type(steps, "predict")
    manipulate_steps = _all_steps_by_type(steps, "manipulate")
    build_steps_raw = _all_steps_by_type(steps, "build")
    break_step = _first_step_by_type(steps, "break")
    debug_steps_raw = _all_steps_by_type(steps, "debug")
    retrieve_steps = _all_steps_by_type(steps, "retrieve")
    transfer_step = _first_step_by_type(steps, "transfer")
    mastery_step = _first_step_by_type(steps, "mastery")

    guided: List[Dict[str, Any]] = []
    order = 1
    for raw in build_steps_raw:
        guided.append(_build_guided_step(
            LessonStep(**{**raw, "repair_steps": raw.get("repair_steps", [])}), order
        ))
        order += 1
    for raw in debug_steps_raw:
        guided.append(_build_guided_step(
            LessonStep(**{**raw, "repair_steps": raw.get("repair_steps", [])}), order
        ))
        order += 1
    if mastery_step:
        tc = mastery_step.get("test_cases", [])
        guided.append({
            "step_order": order,
            "title": mastery_step.get("title", "Mastery"),
            "description": mastery_step.get("description", ""),
            "starter_code": mastery_step.get("starter_code", mastery_step.get("starter", "")),
            "function_name": mastery_step.get("function_name", "solution"),
            "signature": mastery_step.get("signature", ""),
            "test_cases": tc,
            "hidden_test_cases": [],
            "diamonds": 100,
            "scaffolded_hints": [],
        })

    discovery_steps = discover_steps + manipulate_steps
    discovery_section: Dict[str, Any] = {
        "title": lesson_def.title,
        "steps": discovery_steps,
        "conclusion": "",
        "visual_primitives": _visual_primitives_for(lesson_def),
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

    assessment_questions: List[Dict[str, Any]] = []
    if predict_step:
        opts = predict_step.get("options", [])
        explanation_text = predict_step.get("explanation", "")
        correct_text = next((o.get("text", "") for o in opts if o.get("correct")), "")
        keywords_text = explanation_text or correct_text
        assessment_questions.append({
            "type": "concept",
            "question": predict_step.get("question", predict_step.get("prompt", "")),
            "answer_format": "single_choice",
            "options": _options_list(opts),
            "expected_answer": next((o.get("id", "") for o in opts if o.get("correct")), ""),
            "keywords": _keywords_from(keywords_text),
            "explanation": explanation_text,
        })
    if retrieve_steps:
        for rs in retrieve_steps:
            answer_text = rs.get("answer", "")
            assessment_questions.append({
                "type": "concept",
                "question": rs.get("prompt", rs.get("title", "")),
                "answer_format": "short_answer",
                "keywords": _keywords_from(answer_text) if answer_text else [],
                "explanation": answer_text,
            })
    if not assessment_questions:
        assessment_questions.append({
            "type": "concept",
            "question": f"What is the key insight of {lesson_def.title}?",
            "answer_format": "short_answer",
            "keywords": [],
            "explanation": lesson_def.mental_model,
        })

    assessment_section = {
        "title": f"{lesson_def.title} Mastery",
        "description": lesson_def.mental_model,
        "questions": assessment_questions,
        "mastery_threshold": 70,
        "diamonds": lesson_def.diamonds,
    }

    break_fix_steps = break_step.get("fix_steps", []) if break_step else []
    break_fix = ""
    if break_fix_steps:
        break_fix = break_fix_steps[0] if isinstance(break_fix_steps[0], str) else str(break_fix_steps[0])
    break_fixed_code = ""
    if break_step and break_step.get("buggy_code"):
        break_fixed_code = break_step.get("buggy_code", "").replace(break_fix, f"# FIXED: {break_fix}") if break_fix else ""
    break_section: Dict[str, Any] = {
        "title": "What Breaks?",
        "story": break_step.get("content", "") if break_step else "",
        "buggy_code": break_step.get("buggy_code", "") if break_step else "",
        "expected_output": "",
        "actual_output": "",
        "diagnosis": {
            "question": break_step.get("question", "") if break_step else "",
            "options": _options_list(break_step.get("options", [])) if break_step else [],
        },
        "fix": break_fix,
        "fixed_code": break_fixed_code,
        "explanation": break_step.get("explanation", "") if break_step else "",
    }

    transfer_section: Dict[str, Any] = {}
    if transfer_step:
        transfer_section = {
            "title": transfer_step.get("title", "Transfer"),
            "description": transfer_step.get("description", transfer_step.get("content", "")),
            "function_name": transfer_step.get("function_name", "solution"),
            "signature": transfer_step.get("signature", ""),
            "description_full": transfer_step.get("description", ""),
            "test_cases": transfer_step.get("test_cases", []),
            "hidden_test_cases": [],
            "time_limit_minutes": 7,
            "diamonds": lesson_def.diamonds,
            "scaffolded_hints": [],
        }

    explain_section: Dict[str, Any] = {
        "title": f"Explain {lesson_def.title}",
        "captain_byte_intro": f"🧭 **Captain Byte**\n\"Why does {lesson_def.title} work? Explain the core idea in your own words.\"",
        "prompt": f"Why does {lesson_def.title} work? Explain the core idea in your own words.",
        "answer_format": "short_answer",
        "keywords": _keywords_from(lesson_def.mental_model or lesson_def.title, max_words=8),
        "min_words": 10,
        "model_answer": lesson_def.mental_model or "",
        "intention": f"Explain the core idea behind {lesson_def.title}.",
    }

    result: Dict[str, Any] = {
        "lesson_id": lesson_def.id,
        "module_id": lesson_def.concept,
        "title": lesson_def.title,
        "description": lesson_def.mental_model,
        "difficulty": "medium",
        "est_minutes": lesson_def.estimated_minutes,
        "xp_reward": lesson_def.diamonds,
        "skills_taught": [lesson_def.canonical_skill] if lesson_def.canonical_skill else [],
        "srs_concept_tag": lesson_def.canonical_skill or lesson_def.id,
        "captain_byte": _captain_byte_for(lesson_def),
        "story_context": {
            "title": lesson_def.title,
            "narration": lesson_def.mental_model,
            "setting": lesson_def.id,
            "character": "Captain Byte",
            "intro_text": lesson_def.why_this_matters or lesson_def.mental_model,
        },
        "discovery": discovery_section,
        "explain": explain_section,
        "guided_build": {"steps": guided},
        "transfer_challenge": transfer_section,
        "assessment": assessment_section,
        "break": break_section,
        "srs_enrollment": {
            "concept_id": lesson_def.canonical_skill or lesson_def.id,
            "concept_name": lesson_def.title,
            "review_intervals": [1, 3, 7, 14, 30],
            "key_points": lesson_def.mastery_evidence or [lesson_def.mental_model],
            "spaced_fields": [lesson_def.concept],
        },
        "world_progression": {
            "world_id": "code_foundations",
            "competency_id": lesson_def.concept,
            "unlocks_next": [lesson_def.unlocks] if lesson_def.unlocks else [],
            "tower_badge": lesson_def.id,
            "world_node": {
                "level": lesson_def.order,
                "title": lesson_def.title,
                "color": "teal",
                "icon": lesson_def.icon,
                "description": lesson_def.mental_model,
            },
        },
    }
    if predict_step:
        step_explanation = predict_step.get("explanation", "")
        enriched_opts = []
        for o in (predict_step.get("options") or []):
            enriched_opts.append({
                "id": o.get("id", ""),
                "text": o.get("text", ""),
                "correct": o.get("correct", False),
                "explanation": o.get("explanation", step_explanation),
            })
        captain_byte = _captain_byte_for(lesson_def)
        result["prediction"] = {
            "title": predict_step.get("title", "Predict"),
            "captain_byte_intro": captain_byte.get("intro", ""),
            "question": predict_step.get("question", predict_step.get("prompt", "")),
            "options": enriched_opts,
            "explanation": step_explanation,
        }
    return result


def _captain_byte_for(lesson_def) -> Dict[str, Any]:
    skill_id = lesson_def.canonical_skill or lesson_def.id
    title = lesson_def.title
    if skill_id == "dsa.two_pointers" or "two pointer" in title.lower():
        return {
            "intro": "🧭 **Captain Byte**\n“Two pointers let you walk a sorted array from both ends. Left moves right, right moves left — and the answer often appears when they meet.”",
            "correct": ["🧭 **Captain Byte**\n“Nice. You moved both pointers with purpose.”", "🧭 **Captain Byte**\n“Clean. The two-pointer move is second nature now.”"],
            "wrong": ["🧭 **Captain Byte**\n“Stop. Don’t brute-force. Ask: what does moving each pointer buy me?”", "🧭 **Captain Byte**\n“You’re checking every pair. Two pointers means O(n), not O(n²).”"],
            "after_break": "🧭 **Captain Byte**\n“You found the bad assumption. Now move the pointers correctly.”",
            "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Any sorted-array pair problem.”",
            "retry_prompt": "🧭 **Captain Byte**\n“Try again. Move L and R toward each other. What’s the invariant?”",
        }
    if skill_id == "dsa.sliding_window" or "sliding" in title.lower():
        return {
            "intro": "🧭 **Captain Byte**\n“A sliding window is a moving frame. Expand until the condition breaks, then shrink from the left. The frame slides — you never restart.”",
            "correct": ["🧭 **Captain Byte**\n“Nice. You expanded, then shrank — the window is doing the work.”", "🧭 **Captain Byte**\n“Clean. The frame slides, the invariant holds.”"],
            "wrong": ["🧭 **Captain Byte**\n“Stop. Don’t restart for every right index. Keep the window.”", "🧭 **Captain Byte**\n“You’re losing O(n). The window must slide, not reset.”"],
            "after_break": "🧭 **Captain Byte**\n“You found the bad assumption. Now keep the window state correct.”",
            "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Any subarray problem.”",
            "retry_prompt": "🧭 **Captain Byte**\n“Try again. Expand right, then shrink left while the condition breaks.”",
        }
    if skill_id == "dsa.arrays_hashing" or "hash" in title.lower():
        return {
            "intro": "🧭 **Captain Byte**\n“A hash map gives you O(1) lookup. Trade memory for speed — remember the complement, not the whole array.”",
            "correct": ["🧭 **Captain Byte**\n“Nice. You stored the complement and looked it up instantly.”", "🧭 **Captain Byte**\n“Clean. Hash map turns O(n²) into O(n).”"],
            "wrong": ["🧭 **Captain Byte**\n“Stop. Don’t scan the array again. What did you already store?”", "🧭 **Captain Byte**\n“You’re doing nested loops. The hash map removes the inner loop.”"],
            "after_break": "🧭 **Captain Byte**\n“You found the bad assumption. Now use the map correctly.”",
            "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Any lookup problem.”",
            "retry_prompt": "🧭 **Captain Byte**\n“Try again. Store what you need, then look it up in O(1).”",
        }
    if skill_id == "dsa.binary_search" or "binary search" in title.lower():
        return {
            "intro": "🧭 **Captain Byte**\n“Binary search halves the search space each step. lo, mid, hi — cut, decide, repeat.”",
            "correct": ["🧭 **Captain Byte**\n“Nice. You halved the space and found the target.”", "🧭 **Captain Byte**\n“Clean. O(log n) beats O(n) every time.”"],
            "wrong": ["🧭 **Captain Byte**\n“Stop. Don’t scan linearly. What does sorted data buy you?”", "🧭 **Captain Byte**\n“You’re checking every element. Use the middle.”"],
            "after_break": "🧭 **Captain Byte**\n“You found the bad assumption. Now halve correctly.”",
            "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Any sorted-search problem.”",
            "retry_prompt": "🧭 **Captain Byte**\n“Try again. Check the middle. Discard half. Repeat.”",
        }
    if skill_id == "dsa.strings" or "string" in title.lower():
        return {
            "intro": "🧭 **Captain Byte**\n“Strings are arrays of characters. The same array tricks apply — plus character-specific patterns like palindrome and anagram.”",
            "correct": ["🧭 **Captain Byte**\n“Nice. You treated the string like an array with extra structure.”", "🧭 **Captain Byte**\n“Clean. Character counts or two pointers — both work.”"],
            "wrong": ["🧭 **Captain Byte**\n“Stop. Don’t rebuild the whole string. What’s the invariant?”", "🧭 **Captain Byte**\n“You’re doing O(n²). Character counts make it O(n).”"],
            "after_break": "🧭 **Captain Byte**\n“You found the bad assumption. Now use the right invariant.”",
            "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Any string problem.”",
            "retry_prompt": "🧭 **Captain Byte**\n“Try again. What’s the smallest state you need to track?”",
        }
    if skill_id == "dsa.linked_list" or "linked list" in title.lower():
        return {
            "intro": "🧭 **Captain Byte**\n“A linked list is a chain of nodes. You can’t jump to index i — you must walk the chain. Pointers are your only tool.”",
            "correct": ["🧭 **Captain Byte**\n“Nice. You walked the chain with the right pointer moves.”", "🧭 **Captain Byte**\n“Clean. Prev, current, next — the three-pointer dance.”"],
            "wrong": ["🧭 **Captain Byte**\n“Stop. Don’t treat it like an array. You can’t jump. Walk the chain.”", "🧭 **Captain Byte**\n“You lost a node. Track prev before you change current.next.”"],
            "after_break": "🧭 **Captain Byte**\n“You found the bad assumption. Now track the pointers correctly.”",
            "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Any linked-list problem.”",
            "retry_prompt": "🧭 **Captain Byte**\n“Try again. Track prev, current, next. Don’t lose the chain.”",
        }
    if skill_id == "dsa.stack_queue" or "stack" in title.lower() or "queue" in title.lower():
        return {
            "intro": "🧭 **Captain Byte**\n“Stacks reverse order (LIFO). Queues preserve order (FIFO). Choose the structure that matches the problem.”",
            "correct": ["🧭 **Captain Byte**\n“Nice. You chose the right structure for the job.”", "🧭 **Captain Byte**\n“Clean. Stack for undo, queue for order.”"],
            "wrong": ["🧭 **Captain Byte**\n“Stop. Don’t use a list for everything. What ordering does the problem need?”", "🧭 **Captain Byte**\n“You’re mixing LIFO and FIFO. Pick one.”"],
            "after_break": "🧭 **Captain Byte**\n“You found the bad assumption. Now use the right structure.”",
            "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Any stack/queue problem.”",
            "retry_prompt": "🧭 **Captain Byte**\n“Try again. Does this need LIFO or FIFO?”",
        }
    if skill_id == "dsa.trees" or "tree" in title.lower() or "dfs" in title.lower() or "bfs" in title.lower():
        return {
            "intro": "🧭 **Captain Byte**\n“Trees are hierarchies. DFS goes deep first. BFS goes level by level. Choose the traversal that matches the question.”",
            "correct": ["🧭 **Captain Byte**\n“Nice. You chose the right traversal for the problem.”", "🧭 **Captain Byte**\n“Clean. Recursion or queue — both have their place.”"],
            "wrong": ["🧭 **Captain Byte**\n“Stop. Don’t traverse randomly. What does the question need: depth or breadth?”", "🧭 **Captain Byte**\n“You’re missing a subtree. Don’t forget the children.”"],
            "after_break": "🧭 **Captain Byte**\n“You found the bad assumption. Now traverse correctly.”",
            "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Any tree/graph problem.”",
            "retry_prompt": "🧭 **Captain Byte**\n“Try again. Depth or breadth? Recursion or queue?”",
        }
    if skill_id == "dsa.graphs" or "graph" in title.lower():
        return {
            "intro": "🧭 **Captain Byte**\n“Graphs model connections. BFS finds shortest path. DFS explores all paths. Topological sort orders dependencies.”",
            "correct": ["🧭 **Captain Byte**\n“Nice. You chose the right graph algorithm.”", "🧭 **Captain Byte**\n“Clean. Adjacency list + visited set — the standard toolkit.”"],
            "wrong": ["🧭 **Captain Byte**\n“Stop. Don’t treat it like a tree. Graphs can cycle.”", "🧭 **Captain Byte**\n“You’re revisiting nodes. Track visited.”"],
            "after_break": "🧭 **Captain Byte**\n“You found the bad assumption. Now handle cycles and visited nodes.”",
            "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Any graph problem.”",
            "retry_prompt": "🧭 **Captain Byte**\n“Try again. BFS for shortest path, DFS for all paths, topo for dependencies.”",
        }
    if skill_id == "dsa.dp" or "dp" in title.lower() or "memoization" in title.lower() or "tabulation" in title.lower():
        return {
            "intro": "🧭 **Captain Byte**\n“Dynamic programming is about overlapping subproblems. Memoization stores results. Tabulation builds bottom-up. Both turn exponential into polynomial.”",
            "correct": ["🧭 **Captain Byte**\n“Nice. You identified the subproblem and reused the result.”", "🧭 **Captain Byte**\n“Clean. The recurrence is the heart of DP.”"],
            "wrong": ["🧭 **Captain Byte**\n“Stop. Don’t recompute. What did you already solve?”", "🧭 **Captain Byte**\n“You’re doing O(2^n). Cache the subproblem results.”"],
            "after_break": "🧭 **Captain Byte**\n“You found the bad assumption. Now define the recurrence correctly.”",
            "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. I’m removing the training wheels. Any DP problem.”",
            "retry_prompt": "🧭 **Captain Byte**\n“Try again. What’s the smallest subproblem? How does it build up?”",
        }
    return {
        "intro": "🧭 **Captain Byte**\n“Let’s master this pattern. Follow the steps, and I’ll guide you.”",
        "correct": ["🧭 **Captain Byte**\n“Nice work.”", "🧭 **Captain Byte**\n“Clean execution.”"],
        "wrong": ["🧭 **Captain Byte**\n“Try again. Read the hint carefully.”", "🧭 **Captain Byte**\n“Close. Check your assumption.”"],
        "after_break": "🧭 **Captain Byte**\n“You found the issue. Now fix it.”",
        "after_mastery": "🧭 **Captain Byte**\n“You’ve got it. Next challenge.”",
        "retry_prompt": "🧭 **Captain Byte**\n“Try again. You’re close.”",
    }


def _visual_primitives_for(lesson_def) -> List[str]:
    skill_id = lesson_def.canonical_skill or lesson_def.id
    title = lesson_def.title.lower()
    if "two pointer" in title or skill_id == "dsa.two_pointers":
        return ["move", "compare", "trace"]
    if "sliding" in title or skill_id == "dsa.sliding_window":
        return ["move", "transform", "highlight"]
    if "hash" in title or skill_id == "dsa.arrays_hashing":
        return ["highlight", "compare"]
    if "binary search" in title or skill_id == "dsa.binary_search":
        return ["split", "compare", "trace"]
    if "string" in title or skill_id == "dsa.strings":
        return ["highlight", "compare", "trace"]
    if "linked list" in title or skill_id == "dsa.linked_list":
        return ["move", "trace"]
    if "stack" in title or "queue" in title or skill_id == "dsa.stack_queue":
        return ["move", "transform"]
    if "tree" in title or "dfs" in title or "bfs" in title or skill_id in ("dsa.trees", "dsa.graphs"):
        return ["trace", "move", "reveal"]
    if "graph" in title or skill_id == "dsa.graphs":
        return ["trace", "move", "compare"]
    if "dp" in title or "memo" in title or "tabulation" in title or skill_id == "dsa.dp":
        return ["transform", "merge", "highlight"]
    return ["highlight", "trace"]


def get_two_pointers_lesson() -> Dict[str, Any]:
    arrays_1 = next((l for l in ARRAYS_TOWN.lessons if l.id == "arrays-1"), None)
    if arrays_1 is None:
        return {}
    return _make_vertical_slice(arrays_1)


def get_sliding_window_lesson() -> Dict[str, Any]:
    arrays_2 = next((l for l in ARRAYS_TOWN.lessons if l.id == "arrays-2"), None)
    if arrays_2 is None:
        return {}
    return _make_vertical_slice(arrays_2)


def get_hash_map_lesson() -> Dict[str, Any]:
    arrays_3 = next((l for l in ARRAYS_TOWN.lessons if l.id == "arrays-3"), None)
    if arrays_3 is None:
        return {}
    return _make_vertical_slice(arrays_3)


def get_binary_search_lesson() -> Dict[str, Any]:
    arrays_4 = next((l for l in ARRAYS_TOWN.lessons if l.id == "arrays-4"), None)
    if arrays_4 is None:
        return {}
    return _make_vertical_slice(arrays_4)


def get_prefix_sum_lesson() -> Dict[str, Any]:
    arrays_5 = next((l for l in ARRAYS_TOWN.lessons if l.id == "arrays-5"), None)
    if arrays_5 is None:
        return {}
    return _make_vertical_slice(arrays_5)


def get_dfs_lesson() -> Dict[str, Any]:
    trees_1 = next((l for l in TREES_TOWN.lessons if l.id == "trees-1"), None)
    if trees_1 is None:
        return {}
    return _make_vertical_slice(trees_1)


def get_bfs_lesson() -> Dict[str, Any]:
    trees_2 = next((l for l in TREES_TOWN.lessons if l.id == "trees-2"), None)
    if trees_2 is None:
        return {}
    return _make_vertical_slice(trees_2)


def get_graph_traversal_lesson() -> Dict[str, Any]:
    graphs_1 = next((l for l in GRAPHS_TOWN.lessons if l.id == "graphs-1"), None)
    if graphs_1 is None:
        return {}
    return _make_vertical_slice(graphs_1)


def get_topological_sort_lesson() -> Dict[str, Any]:
    graphs_2 = next((l for l in GRAPHS_TOWN.lessons if l.id == "graphs-2"), None)
    if graphs_2 is None:
        return {}
    return _make_vertical_slice(graphs_2)


def get_memoization_lesson() -> Dict[str, Any]:
    dp_1 = next((l for l in DP_TOWN.lessons if l.id == "dp-1"), None)
    if dp_1 is None:
        return {}
    return _make_vertical_slice(dp_1)


def get_tabulation_lesson() -> Dict[str, Any]:
    dp_2 = next((l for l in DP_TOWN.lessons if l.id == "dp-2"), None)
    if dp_2 is None:
        return {}
    return _make_vertical_slice(dp_2)
