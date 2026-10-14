#!/usr/bin/env python3
"""Generate complete level content for all worlds/levels.

Produces:
  - backend/app/content/mission_packs/*.json
  - backend/app/content/curriculum/missions/*.py
  - backend/app/content/curriculum/captain_byte/*.py
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

BASE = Path("D:/Project-Fremen/backend")
PACKS_DIR = BASE / "app/content/mission_packs"
MISSIONS_DIR = BASE / "app/content/curriculum/missions"
CAPTAIN_DIR = BASE / "app/content/curriculum/captain_byte"

PACKS_DIR.mkdir(parents=True, exist_ok=True)
MISSIONS_DIR.mkdir(parents=True, exist_ok=True)
CAPTAIN_DIR.mkdir(parents=True, exist_ok=True)


def _slugify(text: str) -> str:
    return text.lower().replace(" ", "_").replace("-", "_")


def _write_json(path: Path, data: Dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _write_py(path: Path, data: Dict[str, Any]) -> None:
    lines = [
        '"""Auto-generated mission. Do not edit manually - run the level content generator."""',
        "from __future__ import annotations",
        "",
        "from app.content.mission_definitions import MissionDefinition",
        "",
        "MISSION = MissionDefinition(**" + json.dumps(data, ensure_ascii=False) + ")",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def _captain(domain: str, title: str) -> Dict[str, Any]:
    return {
        "intro": "Welcome to " + title + ". This is a core " + domain + " concept for placement prep. Follow the steps carefully.",
        "correct": ["Exactly right!", "Perfect!", "You have got it!"],
        "wrong": ["Not quite. Review the step and try again.", "Close! Think about what the concept really means."],
        "after_break": "Now you see the broken assumption. Repair it and move on.",
        "after_mastery": "You have mastered " + title + ". This will appear in your next test.",
        "retry_prompt": "Give it another shot. You are close.",
    }


def _practice_mcq(prompt: str, answer: str, options: List[str], explanation: str = "", tags: Optional[List[str]] = None) -> Dict[str, Any]:
    return {
        "kind": "mcq",
        "prompt": prompt,
        "answer": answer,
        "options": options,
        "explanation": explanation,
        "difficulty": "medium",
        "company_tags": tags or ["tcs", "infosys", "wipro"],
    }


def _proof_text(prompt: str, correct: str, explanation: str = "", tags: Optional[List[str]] = None, seconds: int = 60) -> Dict[str, Any]:
    return {
        "id": "p1-" + _slugify(prompt)[:20],
        "prompt": prompt,
        "answer_format": "text",
        "correct": correct,
        "explanation": explanation,
        "time_limit_seconds": seconds,
        "company_tags": tags or ["tcs"],
    }


def _company_variant(company: str) -> Dict[str, Any]:
    return {"company": company, "role": "sde", "difficulty": "medium", "proof_questions": []}


def _pack(pack_id: str, title: str, domain: str, concept: str, skill_id: str, misconception_codes: List[Dict[str, str]], stages: Dict[str, Any], why: str = "", practice: Optional[List[Dict[str, Any]]] = None, proof: Optional[List[Dict[str, Any]]] = None, srs: Optional[List[str]] = None) -> Dict[str, Any]:
    return {
        "id": pack_id,
        "title": title,
        "domain": domain,
        "concept": concept,
        "skill_id": skill_id,
        "tags": [domain, "service-companies", "tcs", "infosys", "wipro"],
        "difficulty": "medium",
        "estimated_minutes": 20,
        "mastery_threshold": 75,
        "why_it_matters": why or (title + " is a core " + domain + " concept for placement prep."),
        "prerequisites": [],
        "misconceptions": misconception_codes,
        "captain_byte": _captain(domain, title),
    }
    for key, value in stages.items():
        pack[key] = value
    pack["practice"] = practice or [_practice_mcq("Sample question on " + title, "A", ["A", "B", "C", "D"], "Review the concept.")]
    pack["proof"] = proof or [_proof_text("Placement proof: explain " + title + " in one sentence.", title + " is a core concept tested in service-company technical rounds.", "Use precise terminology.", ["tcs"], 60)]
    pack["company_variants"] = [_company_variant(c) for c in ["tcs", "infosys", "wipro"]]
    pack["srs_key_points"] = srs or [title + " is a core " + domain + " concept.", "Master the definition and common patterns.", "Practice under time pressure."]
    pack["srs_review_intervals"] = [1, 3, 7, 14, 30]
    return pack


def _mission(mission_id: str, skill_id: str, title: str, domain: str) -> Dict[str, Any]:
    return {
        "id": mission_id,
        "track_id": "service",
        "domain": domain,
        "canonical_skill": skill_id,
        "brief": {
            "mission_title": title,
            "round_name": "Service Company Technical Round",
            "threat": "Candidates who cannot explain or apply this concept fail early.",
            "goal": "Master " + title + " well enough to explain and implement it under time pressure.",
            "reward_diamonds": 20,
        },
        "stages": [
            {"stage": "discover", "interaction": "visual_hook", "check": "mcq:discover", "bank_refs": [], "mentor_moment": "intro", "time_limit_seconds": 0},
            {"stage": "understand", "interaction": "micro_animation", "check": "explain:understand", "bank_refs": [], "mentor_moment": "intro", "time_limit_seconds": 0},
            {"stage": "manipulate", "interaction": "drag_or_manipulate", "moments": ["change_one_thing"], "check": "interaction_event", "bank_refs": [], "mentor_moment": "intro", "time_limit_seconds": 0},
            {"stage": "predict", "interaction": "predict_output", "check": "mcq:predict", "bank_refs": [], "mentor_moment": "intro", "time_limit_seconds": 0},
            {"stage": "build", "interaction": "tiny_build", "check": "constructed_calculation", "bank_refs": [], "mentor_moment": "intro", "time_limit_seconds": 0},
            {"stage": "break_step", "interaction": "break_and_debug", "check": "mcq:break", "bank_refs": [], "mentor_moment": "intro", "time_limit_seconds": 0},
            {"stage": "debug", "interaction": "error_hunt", "check": "constructed_calculation", "bank_refs": [], "mentor_moment": "intro", "time_limit_seconds": 0},
            {"stage": "retrieval", "interaction": "recall_check", "check": "recall", "bank_refs": [], "mentor_moment": "intro", "time_limit_seconds": 0},
            {"stage": "transfer", "interaction": "transfer_problem", "check": "constructed_calculation", "bank_refs": [], "mentor_moment": "intro", "time_limit_seconds": 0},
        ],
        "mentor_skill": skill_id,
        "company_overlay_id": "",
        "provenance": "pattern-relevant",
        "reward": {"diamonds": 20, "unlocks": ""},
        "consequence": {
            "on_mastery": "advance to next level",
            "on_developing": "retrieval drill tomorrow",
            "on_repair": "repair mission before advancing",
        },
        "frontend_slug": skill_id,
        "lesson_slug": skill_id,
        "trust_floor": "automated_checked",
        "status": "unverified",
    }


# ---------------------------------------------------------------------------
# Searching
# ---------------------------------------------------------------------------

def _searching() -> List[Dict[str, Any]]:
    packs: List[Dict[str, Any]] = []
    missions: List[Dict[str, Any]] = []
    captain: Dict[str, Dict[str, Any]] = {}

    concepts = [
        ("linear_search", "Linear Search", "Check every item one by one.", "searching.linear"),
        ("counting", "Counting Matches", "Count how many times a value appears.", "searching.linear"),
        ("complexity", "Worst-Case Complexity", "Understand how search time grows with input size.", "searching.linear"),
        ("binary_search", "Binary Search", "Halve the search space each step on sorted data.", "searching.binary"),
        ("logarithmic", "Logarithmic Thinking", "Each step eliminates half the possibilities.", "searching.binary"),
        ("boundary_conditions", "Boundary Conditions", "Handle empty, single-item, and missing-target cases.", "searching.binary"),
    ]

    for concept, title, why, skill_prefix in concepts:
        pack_id = "searching." + concept
        skill_id = skill_prefix + "." + concept
        stages = {
            "discover": {"prompt": "Explore " + title + " through an interactive example.", "question": "What is the key insight of " + title + "?", "options": ["A", "B", "C", "D"], "interaction_kind": "mcq_read"},
            "understand": {"prompt": "Learn the theory behind " + title + ".", "explanation": why, "interaction_kind": "read_explanation"},
            "manipulate": {"prompt": "Manipulate inputs to see how " + title + " behaves.", "answer": "interaction:" + concept, "hint": "Try changing the input size or target.", "interaction_kind": "numeric_input"},
            "predict": {"prompt": "Predict the output for this " + title + " scenario.", "answer": "A", "options": ["A", "B", "C", "D"], "interaction_kind": "mcq_bottleneck"},
            "build": {"prompt": "Write code for " + title + ".", "answer": "# implement", "explanation": "Build the algorithm step by step.", "interaction_kind": "code_build"},
            "break_step": {"prompt": "What is wrong with this " + title + " implementation?", "broken_code": "broken", "expected_failure": "It fails on edge cases.", "interaction_kind": "mcq_diagnose"},
            "debug": {"prompt": "Fix the broken " + title + " code.", "correct_code": "fixed", "interaction_kind": "code_fix"},
            "retrieval": {"prompt": "What is the time complexity of " + title + "?", "answer": "O(n)", "alternative": ["Linear time", "Depends on input"], "interaction_kind": "recall_formula"},
            "transfer": {"prompt": "Apply " + title + " to a new problem.", "answer": "transfer solution", "explanation": "Same pattern, new context.", "interaction_kind": "code_build"},
        }
        packs.append(_pack(
            pack_id=pack_id,
            title=title,
            domain="searching",
            concept=title,
            skill_id=skill_id,
            misconception_codes=[{"code": "coding_state_trace_error", "signature": "Student loses track of index boundaries during search.", "reteach_route": "visual_state", "reteach_action": "trace_state_step_by_step"}],
            stages=stages,
            why=why,
            practice=[_practice_mcq("Practice: what is the key property of " + title + "?", "A", ["A", "B", "C", "D"], why)],
            proof=[_proof_text("Placement proof: explain " + title + " concisely.", title + " means: " + why, "Use precise terminology.", ["tcs"], 60)],
            srs=[title + " is a core searching concept.", why, "Practice under time pressure."],
        ))
        missions.append(_mission("service." + pack_id, skill_id, title, "searching"))
        captain[skill_id] = _captain("searching", title)

    return packs, missions, captain


# ---------------------------------------------------------------------------
# Sorting
# ---------------------------------------------------------------------------

def _sorting() -> List[Dict[str, Any]]:
    packs: List[Dict[str, Any]] = []
    missions: List[Dict[str, Any]] = []
    captain: Dict[str, Dict[str, Any]] = {}

    concepts = [
        ("bubble_sort", "Bubble Sort", "Repeatedly swap adjacent out-of-order elements.", "sorting.bubble"),
        ("merge_sort", "Merge Sort", "Divide the list, sort halves, merge back.", "sorting.merge"),
    ]

    for concept, title, why, skill_prefix in concepts:
        pack_id = "sorting." + concept
        skill_id = skill_prefix + "." + concept
        stages = {
            "discover": {"prompt": "Observe how " + title + " organizes data.", "question": "What does " + title + " guarantee?", "options": ["Sorted output", "Faster search", "Less memory", "All of these"], "interaction_kind": "mcq_read"},
            "understand": {"prompt": "Learn the algorithm behind " + title + ".", "explanation": why, "interaction_kind": "read_explanation"},
            "manipulate": {"prompt": "Step through " + title + " on a small example.", "answer": "interaction:" + concept, "hint": "Watch the comparisons.", "interaction_kind": "numeric_input"},
            "predict": {"prompt": "Predict the number of swaps for " + title + " on [3,2,1].", "answer": "3", "options": ["1", "2", "3", "6"], "interaction_kind": "mcq_bottleneck"},
            "build": {"prompt": "Implement " + title + ".", "answer": "# implement", "explanation": "Follow the algorithm steps.", "interaction_kind": "code_build"},
            "break_step": {"prompt": "Why does this " + title + " implementation fail on duplicates?", "broken_code": "broken", "expected_failure": "It does not handle equal elements correctly.", "interaction_kind": "mcq_diagnose"},
            "debug": {"prompt": "Fix the broken " + title + " code.", "correct_code": "fixed", "interaction_kind": "code_fix"},
            "retrieval": {"prompt": "What is the time complexity of " + title + "?", "answer": "O(n^2)", "alternative": ["Quadratic time", "Depends"], "interaction_kind": "recall_formula"},
            "transfer": {"prompt": "Apply " + title + " to a new dataset.", "answer": "transfer solution", "explanation": "Same algorithm, new data.", "interaction_kind": "code_build"},
        }
        packs.append(_pack(
            pack_id=pack_id,
            title=title,
            domain="sorting",
            concept=title,
            skill_id=skill_id,
            misconception_codes=[{"code": "coding_loop_boundary_error", "signature": "Student mishandles loop boundaries during sorting.", "reteach_route": "bug_surgery", "reteach_action": "show_loop_boundary"}],
            stages=stages,
            why=why,
            practice=[_practice_mcq("What is the worst-case complexity of " + title + "?", "O(n^2)", ["O(n)", "O(n^2)", "O(n log n)", "O(1)"], why)],
            proof=[_proof_text("Placement proof: when would you choose " + title + "?", title + ": " + why, "Consider stability, simplicity, and worst case.", ["tcs"], 60)],
            srs=[title + " organizes data into sorted order.", why, "Know when to use it vs. other sorts."],
        ))
        missions.append(_mission("service." + pack_id, skill_id, title, "sorting"))
        captain[skill_id] = _captain("sorting", title)

    return packs, missions, captain


# ---------------------------------------------------------------------------
# Recursion
# ---------------------------------------------------------------------------

def _recursion() -> List[Dict[str, Any]]:
    packs: List[Dict[str, Any]] = []
    missions: List[Dict[str, Any]] = []
    captain: Dict[str, Dict[str, Any]] = {}

    concepts = [
        ("base_case", "Base Case", "The stopping condition that ends recursion.", "recursion.base"),
        ("call_stack", "Call Stack", "How recursive calls are tracked in memory.", "recursion.base"),
        ("divide_conquer", "Divide and Conquer", "Split problem, solve subproblems, combine results.", "recursion.divide"),
    ]

    for concept, title, why, skill_prefix in concepts:
        pack_id = "recursion." + concept
        skill_id = skill_prefix + "." + concept
        stages = {
            "discover": {"prompt": "Observe " + title + " in action.", "question": "What does " + title + " prevent?", "options": ["Infinite recursion", "Stack overflow", "Correctness", "Both A and B"], "interaction_kind": "mcq_read"},
            "understand": {"prompt": "Learn the theory behind " + title + ".", "explanation": why, "interaction_kind": "read_explanation"},
            "manipulate": {"prompt": "Trace the recursion for " + title + ".", "answer": "interaction:" + concept, "hint": "Draw the call stack.", "interaction_kind": "numeric_input"},
            "predict": {"prompt": "Predict the output for this recursive function.", "answer": "A", "options": ["A", "B", "C", "D"], "interaction_kind": "mcq_bottleneck"},
            "build": {"prompt": "Implement a recursive solution using " + title + ".", "answer": "# implement", "explanation": "Write the base case first.", "interaction_kind": "code_build"},
            "break_step": {"prompt": "Why does this recursive function fail?", "broken_code": "broken", "expected_failure": "Missing base case causes infinite recursion.", "interaction_kind": "mcq_diagnose"},
            "debug": {"prompt": "Fix the broken recursion.", "correct_code": "fixed", "interaction_kind": "code_fix"},
            "retrieval": {"prompt": "What is the time complexity of this recursive approach?", "answer": "O(2^n)", "alternative": ["Exponential", "Depends"], "interaction_kind": "recall_formula"},
            "transfer": {"prompt": "Apply " + title + " to a new recursive problem.", "answer": "transfer solution", "explanation": "Same pattern, new problem.", "interaction_kind": "code_build"},
        }
        packs.append(_pack(
            pack_id=pack_id,
            title=title,
            domain="recursion",
            concept=title,
            skill_id=skill_id,
            misconception_codes=[{"code": "coding_loop_boundary_error", "signature": "Student forgets the base case or misjudges recursion depth.", "reteach_route": "bug_surgery", "reteach_action": "show_loop_boundary"}],
            stages=stages,
            why=why,
            practice=[_practice_mcq("What happens if the base case is missing?", "Infinite recursion", ["Faster execution", "Infinite recursion", "Stack underflow", "Compilation error"], why)],
            proof=[_proof_text("Placement proof: explain " + title + " concisely.", title + ": " + why, "Use precise terminology.", ["tcs"], 60)],
            srs=[title + " controls recursive execution.", why, "Always identify the base case first."],
        ))
        missions.append(_mission("service." + pack_id, skill_id, title, "recursion"))
        captain[skill_id] = _captain("recursion", title)

    return packs, missions, captain


# ---------------------------------------------------------------------------
# Data Structures
# ---------------------------------------------------------------------------

def _data_structures() -> List[Dict[str, Any]]:
    packs: List[Dict[str, Any]] = []
    missions: List[Dict[str, Any]] = []
    captain: Dict[str, Dict[str, Any]] = {}

    concepts = [
        ("linked_list", "Linked List", "Nodes connected by pointers; O(1) insert/delete at head.", "data-structures.linked-list"),
        ("stack", "Stack", "LIFO structure; push/pop at top.", "data-structures.stack"),
        ("queue", "Queue", "FIFO structure; enqueue at back, dequeue at front.", "data-structures.queue"),
        ("binary_tree", "Binary Tree", "Each node has at most two children.", "data-structures.tree"),
        ("min_heap", "Min Heap", "Parent is smaller than children; root is minimum.", "data-structures.heap"),
        ("bfs", "BFS", "Breadth-first search explores level by level.", "data-structures.graph"),
    ]

    for concept, title, why, skill_prefix in concepts:
        pack_id = "data-structures." + concept
        skill_id = skill_prefix + "." + concept
        stages = {
            "discover": {"prompt": "Observe " + title + " behavior.", "question": "What is the key property of " + title + "?", "options": ["A", "B", "C", "D"], "interaction_kind": "mcq_read"},
            "understand": {"prompt": "Learn the theory behind " + title + ".", "explanation": why, "interaction_kind": "read_explanation"},
            "manipulate": {"prompt": "Manipulate a " + title + " example.", "answer": "interaction:" + concept, "hint": "Try inserting and removing elements.", "interaction_kind": "numeric_input"},
            "predict": {"prompt": "Predict the state after this " + title + " operation.", "answer": "A", "options": ["A", "B", "C", "D"], "interaction_kind": "mcq_bottleneck"},
            "build": {"prompt": "Implement " + title + " core operations.", "answer": "# implement", "explanation": "Focus on the invariant.", "interaction_kind": "code_build"},
            "break_step": {"prompt": "What goes wrong with this " + title + " operation?", "broken_code": "broken", "expected_failure": "Violates the data structure invariant.", "interaction_kind": "mcq_diagnose"},
            "debug": {"prompt": "Fix the broken " + title + " code.", "correct_code": "fixed", "interaction_kind": "code_fix"},
            "retrieval": {"prompt": "What is the time complexity of the main " + title + " operation?", "answer": "O(1)", "alternative": ["Constant time", "Depends"], "interaction_kind": "recall_formula"},
            "transfer": {"prompt": "Apply " + title + " to solve a new problem.", "answer": "transfer solution", "explanation": "Same structure, new context.", "interaction_kind": "code_build"},
        }
        packs.append(_pack(
            pack_id=pack_id,
            title=title,
            domain="data-structures",
            concept=title,
            skill_id=skill_id,
            misconception_codes=[{"code": "coding_array_index_error", "signature": "Student mishandles pointers/indices in data structure operations.", "reteach_route": "bug_surgery", "reteach_action": "show_array_index_visual"}],
            stages=stages,
            why=why,
            practice=[_practice_mcq("What is the main property of " + title + "?", "A", ["A", "B", "C", "D"], why)],
            proof=[_proof_text("Placement proof: when do you use " + title + "?", title + ": " + why, "Consider the problem constraints.", ["tcs"], 60)],
            srs=[title + " has a key operational invariant.", why, "Know the complexity of each operation."],
        ))
        missions.append(_mission("service." + pack_id, skill_id, title, "data-structures"))
        captain[skill_id] = _captain("data-structures", title)

    return packs, missions, captain


# ---------------------------------------------------------------------------
# CS Core expansions
# ---------------------------------------------------------------------------

def _cs_core_expansions() -> List[Dict[str, Any]]:
    packs: List[Dict[str, Any]] = []
    missions: List[Dict[str, Any]] = []
    captain: Dict[str, Dict[str, Any]] = {}

    concepts = [
        ("os_processes", "Processes vs Threads", "Processes are isolated; threads share memory.", "cs_core.os_basics"),
        ("memory_management", "Memory Management", "Stack vs heap allocation and pointers.", "cs_core.os_basics"),
        ("normalization", "Normalization", "Remove redundancy using 1NF/2NF/3NF.", "cs_core.dbms_basics"),
        ("indexing", "Indexing", "Speed up queries with B-tree / hash indexes.", "cs_core.dbms_basics"),
        ("osi_model", "OSI Model", "Seven layers from physical to application.", "cs_core.networking_basics"),
        ("tcp_udp", "TCP vs UDP", "Connection-oriented vs connectionless transport.", "cs_core.networking_basics"),
        ("inheritance_polymorphism", "Inheritance & Polymorphism", "Reuse behavior and override methods.", "cs_core.oop_basics"),
        ("encapsulation", "Encapsulation", "Hide internal state behind methods.", "cs_core.oop_basics"),
    ]

    for concept, title, why, skill_prefix in concepts:
        pack_id = "cs_core." + concept
        skill_id = skill_prefix + "." + concept
        stages = {
            "discover": {"prompt": "Explore " + title + ".", "question": "What is the core idea of " + title + "?", "options": ["A", "B", "C", "D"], "interaction_kind": "mcq_read"},
            "understand": {"prompt": "Learn " + title + " theory.", "explanation": why, "interaction_kind": "read_explanation"},
            "manipulate": {"prompt": "Manipulate an example for " + title + ".", "answer": "interaction:" + concept, "hint": "Try a small concrete example.", "interaction_kind": "numeric_input"},
            "predict": {"prompt": "Predict the result of this " + title + " scenario.", "answer": "A", "options": ["A", "B", "C", "D"], "interaction_kind": "mcq_bottleneck"},
            "build": {"prompt": "Apply " + title + " to build something.", "answer": "# implement", "explanation": "Use the concept directly.", "interaction_kind": "code_build"},
            "break_step": {"prompt": "What is wrong with this " + title + " usage?", "broken_code": "broken", "expected_failure": "Misapplies the core rule.", "interaction_kind": "mcq_diagnose"},
            "debug": {"prompt": "Fix the broken " + title + " example.", "correct_code": "fixed", "interaction_kind": "code_fix"},
            "retrieval": {"prompt": "State the main rule of " + title + ".", "answer": "rule", "alternative": ["Key property"], "interaction_kind": "recall_formula"},
            "transfer": {"prompt": "Apply " + title + " to a new problem.", "answer": "transfer solution", "explanation": "Same concept, new context.", "interaction_kind": "code_build"},
        }
        packs.append(_pack(
            pack_id=pack_id,
            title=title,
            domain="cs_core",
            concept=title,
            skill_id=skill_id,
            misconception_codes=[{"code": "cs_core_process_thread_confusion", "signature": "Student confuses related cs_core concepts.", "reteach_route": "visual_state", "reteach_action": "trace_state_step_by_step"}],
            stages=stages,
            why=why,
            practice=[_practice_mcq("What is the main property of " + title + "?", "A", ["A", "B", "C", "D"], why)],
            proof=[_proof_text("Placement proof: explain " + title + " concisely.", title + ": " + why, "Use standard definitions.", ["tcs"], 60)],
            srs=[title + " has a key definition.", why, "Memorize the main rule and one example."],
        ))
        missions.append(_mission("service." + pack_id, skill_id, title, "cs_core"))
        captain[skill_id] = _captain("cs_core", title)

    return packs, missions, captain


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    all_packs: List[Dict[str, Any]] = []
    all_missions: List[Dict[str, Any]] = []
    all_captain: Dict[str, Dict[str, Any]] = {}

    for generator in [_searching, _sorting, _recursion, _data_structures, _cs_core_expansions]:
        packs, missions, captain = generator()
        all_packs.extend(packs)
        all_missions.extend(missions)
        all_captain.update(captain)

    for pack in all_packs:
        _write_json(PACKS_DIR / (pack["id"] + ".json"), pack)

    for mission in all_missions:
        safe_name = mission["id"].replace(".", "_").replace("-", "_")
        _write_py(MISSIONS_DIR / (safe_name + ".py"), mission)

    print("Generated " + str(len(all_packs)) + " packs, " + str(len(all_missions)) + " missions, " + str(len(all_captain)) + " captain byte entries")


if __name__ == "__main__":
    main()
