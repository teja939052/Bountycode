# 03 SKILL GRAPH AND CONTENT CATALOGUE

**BountyCode — Phase 2 Design Freeze**
**Status: Design-only document**
**No application code written**

---

## 1. Purpose

Define the skill graph, content catalogue, and content contract for BountyCode.
This document maps the existing `skill_taxonomy.py` canonical ID system to
learning content, establishes content trust gates, and defines how skills relate
to prerequisites and lessons.

This is a design document. No implementation is authorized.

---

## 2. Canonical Skill ID System

### 2.1 Existing Asset

`app/services/skill_taxonomy.py` provides a canonical `domain.subskill` namespace
with 11 domains and ~160 canonical skill IDs. It already maps 9 incompatible
naming schemes:

| Source | Example Name | Canonical ID |
|--------|-------------|--------------|
| adaptive_learning | `arrays_hashing` | `dsa.arrays` |
| skill_assessment | `arrays` | `dsa.arrays` |
| readiness_engine | `dsa` | `dsa.arrays` |
| OA section | `coding` | `dsa.arrays` |
| interview dimension | `technical` | `interview.technical` |
| spaced_repetition | `linked-lists` | `dsa.linked_list` |

### 2.2 Canonical Domains

| Domain | Description |
|--------|-------------|
| `dsa` | Data Structures & Algorithms patterns |
| `coding` | Programming foundations |
| `aptitude` | Quantitative, logical, verbal |
| `system_design` | Architecture and scalability |
| `behavioral` | Soft skills and interview behavior |
| `interview` | Interview-specific competencies |
| `resume` | Resume and career materials |
| `projects` | Project work |
| `cs_fundamentals` | Computer Science fundamentals |
| `sdlc` | Software Development Life Cycle |

### 2.3 Skill ID Format

`domain.subskill` (e.g., `dsa.two_pointers`, `aptitude.quantitative`,
`coding.loops`, `cs_fundamentals.databases`)

---

## 4. Content Trust Pipeline

Content must pass through four trust levels before being served in graded flows:

| Level | Meaning | Servable in Graded Flow? |
|-------|---------|--------------------------|
| `UNVERIFIED` | Raw imported content | No |
| `AUTOMATED_CHECKED` | Passes automated validation | No |
| `HUMAN_REVIEWED` | Human verified correctness and relevance | Yes (with restrictions) |
| `TRUSTED` | Fully verified with independent expected outputs and reasoning verification | Yes |

### 4.1 Content Trust Rules (Binding)

- **Never serve UNVERIFIED content to students.**
- **Never serve AUTOMATED_CHECKED content as placement-quality.**
- **`HUMAN_REVIEWED` content may be served only with restrictions and explicit disclosure.**
- **Only `TRUSTED` content may be used in graded flows, placement-quality assessments, or mastery determination.**
- **Human review is not automatically equivalent to TRUSTED.**
- **Question content lives in versioned files under `backend/app/data/` and `backend/app/content/`.**
- **Never write question content to MongoDB.**
- **No LLM involvement in question bank** — not in authoring, tagging, grading keys, company attribution, or promotion.
- **Company attribution**: Only explicit `companies` tags + `provenance` already in data. Topic-to-company alignment without explicit tag is labeled `pattern-relevant`, never "asked at X".

### 4.2 Servable Question Requirements

A question is servable only when ALL of the following are true:

| Requirement | Description |
|-------------|-------------|
| trust_status | `"TRUSTED"` |
| content_review_status | not `"quarantined"` |
| has_answer_key | For MCQ: `correct_index` is valid; For coding: `test_cases` present |
| has_explanation | `explanation` field present and >= 35 chars |
| executable | For coding: has runnable test cases |

---

## 5. Content Contract

### 5.1 Common Content Contract

All content types share this base schema:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique content identifier |
| `skill_id` | string | Canonical skill ID (`domain.subskill`) |
| `title` | string | Human-readable title |
| `description` | string | What the content teaches |
| `difficulty` | string | `"easy"` / `"medium"` / `"hard"` |
| `estimated_minutes` | number | Estimated time to complete |
| `interaction_template` | string | Template ID from Section 7 |
| `learning_objective` | string | What student should be able to do |
| `trust_status` | string | `"TRUSTED"` / `"HUMAN_REVIEWED"` / `"AUTOMATED_CHECKED"` / `"UNVERIFIED"` |
| `content_version` | string | Content version for change tracking |
| `evidence_eligible` | boolean | Whether completion generates evidence events |
| `prerequisite_skill_ids` | array | Canonical skill IDs that must be met first |
| `misconception_mappings` | array | Misconception IDs this content addresses |
| `companies` | array | Explicit company tags (provenance only) |
| `provenance` | string | Source attribution |

### 5.2 Content Type Contracts

#### 5.2.1 Interactive Lesson

| Field | Type | Description |
|-------|------|-------------|
| `stages` | array | Seven-beat stages (discover → manipulate → predict → build → break → debug → retrieve → transfer) |
| `stage_type` | string | Per-stage interaction type |
| `worked_examples` | array | Fully worked examples with annotations |
| `common_mistakes` | array | Mistake → fix pairs |
| `exercise` | object | Starter code, expected output, hints |
| `quiz` | array | Quiz questions with answer keys (server-side only) |
| `transfer_task` | object | Changed-context application task |
| `mastery_threshold` | number | Score required to mark complete |

#### 5.2.2 Coding Question

| Field | Type | Description |
|-------|------|-------------|
| `test_cases` | array | Visible and hidden test cases with expected outputs |
| `function_name` | string | Expected function name |
| `language` | string | Supported language |
| `starter_code` | string | Initial code in editor |
| `solution` | object | Server-side only — never sent to client |
| `complexity` | object | Time and space complexity |
| `edge_cases` | array | Edge cases the solution handles |

#### 5.2.3 Aptitude Question (MCQ)

| Field | Type | Description |
|-------|------|-------------|
| `options` | array | At least 2 options |
| `correct_index` | integer | Index of correct option |
| `explanation` | string | Why the answer is correct |
| `common_mistakes` | array | Typical wrong answers and why |

#### 5.2.4 Transfer Task

| Field | Type | Description |
|-------|------|-------------|
| `original_context` | string | The context the skill was learned in |
| `new_context` | string | The changed context for application |
| `adaptation_required` | string | What must change in the student's approach |
| `rubric` | object | Grading rubric for transfer response |

#### 5.2.5 Repair Activity

| Field | Type | Description |
|-------|------|-------------|
| `misconception_id` | string | Which misconception this repairs |
| `defective_code` | string | Code with the misconception embedded |
| `fix_prompt` | string | What the student must fix |
| `test_cases` | array | Cases that expose the defect |
| `explanation` | string | Why the defect is wrong |

---

## 6. Skill Graph

### 6.1 Existing Asset

`app/services/prerequisite_graph.py` provides:

- `SKILL_PREREQUISITES` dict with 21 skills and explicit prerequisite lists
- `validate_prerequisite_graph()` — cycle detection and unknown reference detection
- `build_prerequisite_plan()` — evaluates whether a target can be taught
- `aggregate_prerequisite_evidence()` — aggregates evidence per skill
- `get_user_prerequisite_learning_step()` — determines teach/diagnose/reassess

### 6.2 Skill Graph Rules

| Rule | Description |
|------|-------------|
| Explicit prerequisites | Every skill lists its prerequisites explicitly |
| No silent mastery | Missing evidence is `not_assessed`, never treated as mastery |
| Cycle detection | Graph validation rejects cycles |
| Unknown reference detection | Graph validation rejects references to non-existent skills |
| Minimum independent attempts | 3 attempts before a skill is assessed |
| Mastery threshold | 70.0 score prerequisite for "ready" status |

### 6.3 Sample Skill Graph Subset

```
coding.variables          → (leaf)
coding.types              → (leaf)
coding.conditions         → (leaf)
coding.functions          → coding.variables, coding.types, coding.conditions
coding.parameters         → coding.variables, coding.types
coding.return             → coding.functions, coding.conditions
coding.loops              → coding.variables, coding.conditions
coding.lists              → coding.loops, coding.variables
dsa.arrays                → coding.loops, coding.variables
dsa.two_pointers          → dsa.arrays
dsa.recursion             → coding.functions, coding.parameters, coding.return, coding.conditions
dsa.backtracking          → dsa.recursion, coding.conditions
dsa.trees                 → dsa.recursion, dsa.arrays
dsa.graph                 → dsa.trees, dsa.arrays
dsa.dp                    → dsa.recursion, dsa.arrays
cs_fundamentals.databases → (leaf)
system_design.caching     → (leaf)
system_design.scalability → cs_fundamentals.databases, system_design.caching
```

### 6.4 World / Level Mapping

The `app/data/worlds_data.py` WORLD_REGISTRY contains 5+ worlds with towns and
levels. Each level maps to a canonical skill ID:

| World | Town | Level | Canonical Skill |
|-------|------|-------|-----------------|
| Foundations | Coding Basics | Variables | `coding.variables` |
| Foundations | Coding Basics | Loops | `coding.loops` |
| Foundations | Arrays | Arrays | `dsa.arrays` |
| Searchlands | Two Pointers | Two Sum | `dsa.two_pointers` |
| Searchlands | Binary Search | Search | `dsa.binary_search` |

**Note**: No dedicated Two Pointers town exists yet in the current registry.
Phase 3 may add one.

---

## 7. Interaction Template Contract

### 7.1 Template Registry

| Template ID | Name | Student Action | Validation | Supported Skill Types |
|-------------|------|---------------|------------|----------------------|
| `select` | Select | Choose a value or operation | Deterministic answer rule | All |
| `manipulate` | Manipulate | Change parameter or variable | Expected state transition | dsa, coding |
| `predict` | Predict | Commit expected outcome | Compare with trusted answer | All |
| `trace` | Trace | Follow algorithm execution | Compare with canonical trace | dsa, cs_fundamentals |
| `arrange` | Arrange | Put shuffled steps/code in order | Structural + semantic validation | dsa, coding |
| `fill` | Fill | Complete missing code/reasoning | Exact or rubric-backed validation | coding, aptitude |
| `debug` | Debug | Identify and fix defect | Verified test cases | coding |
| `explain` | Explain | Explain why approach works | Structured review evaluation | All |
| `transfer` | Transfer | Solve changed-context task | Independent assessment | All |

### 7.2 Template Schema

```json
{
  "template_id": "manipulate",
  "name": "Array Pointer Manipulation",
  "input_schema": {
    "initial_state": "array representation",
    "allowed_operations": ["move_left", "move_right", "swap"],
    "target_condition": "pointers meet at target"
  },
  "expected_response": {
    "final_state": "array state after operations",
    "operation_sequence": ["move_right", "move_left"]
  },
  "validation_strategy": "Compare final state to expected; verify each operation is legal",
  "feedback_contract": "Show current state after each operation; highlight invalid moves",
  "hint_levels": [
    "Which pointer should move first?",
    "The left pointer is too small — move it right.",
    "Both pointers now point to the answer."
  ],
  "accessibility_behavior": "Keyboard navigable; screen reader announces pointer positions",
  "evidence_emitted": ["interaction_type:manipulate", "correct:bool", "hints_used:int"],
  "supported_skill_types": ["dsa.arrays", "dsa.two_pointers", "dsa.sliding_window"]
}
```

---

## 8. Content Loading Path

### 8.1 Current State (from Phase 1 audit)

| Component | File | Status |
|-----------|------|--------|
| `content_loader.py` | Real file-loading from `app/data/content/` JSON | Unused by question_store |
| `question_store.py` | Empty `_questions = []`, stubs for `find()`/`find_one()` | Broken serving |
| `quiz_service.py` | Calls missing `find_one_verified()` | Broken integration |

### 8.2 Design Fix

1. `question_store.py` loads content from versioned JSON files at startup
   (adopting `content_loader.py` patterns or replacing with direct file reads).
2. `find_one_verified()` is added to `question_store.py` — returns only
   `trust_status == "TRUSTED"` questions.
3. `load_all()` becomes async or is called with `await`.
4. `quiz_service.py` uses `question_store.find_one_verified()` for
   `get_question_by_id()`.
5. No fallback bypasses trust governance.

### 8.3 Content File Format

```json
{
  "id": "qs_two_sum_001",
  "skill_id": "dsa.two_pointers",
  "title": "Two Sum on Sorted Array",
  "description": "Find two numbers that add to target using two pointers.",
  "difficulty": "medium",
  "estimated_minutes": 15,
  "interaction_template": "manipulate",
  "learning_objective": "Apply convergent two-pointer technique to find a pair summing to target",
  "trust_status": "TRUSTED",
  "content_version": "1.0",
  "evidence_eligible": true,
  "prerequisite_skill_ids": ["coding.loops", "dsa.arrays"],
  "misconception_mappings": ["POINTER_MOVEMENT_REVERSED", "ZERO_BASED_INDEX_CONFUSION"],
  "companies": ["tcs", "infosys"],
  "provenance": "curated_pattern-relevant",
  "test_cases": [
    {"input": {"nums": [1,2,4,6,8], "target": 10}, "expected": [1,4]},
    {"input": {"nums": [1,2,4,8], "target": 20}, "expected": null}
  ],
  "function_name": "two_sum",
  "language": "python",
  "starter_code": "def two_sum(nums, target):\n    # your code here\n    pass",
  "solution": { ... },
  "complexity": {"time": "O(n)", "space": "O(1)"},
  "edge_cases": ["empty array", "single element", "no pair exists"],
  "common_mistakes": [
    {"mistake": "Moving both pointers when sum equals target", "fix": "Return immediately when sum matches"}
  ],
  "hints": [
    "If the sum is too small, move the left pointer right.",
    "If the sum is too large, move the right pointer left.",
    "The array must be sorted for this technique to work."
  ],
  "why_this_matters": "Two pointers is the foundation of sliding window and many array problems.",
  "real_world_use": "Finding pairs in sorted data — prices, scores, timestamps.",
  "pattern_recognition": "Convergent pointers on sorted data.",
  "anti_patterns": ["Using nested loops O(n²)", "Assuming unsorted input works"],
  "common_mistakes_detail": [...],
  "prerequisite_concepts": ["array indexing", "while loops"],
  "estimated_time": "15-25 minutes",
  "xp_reward": 10
}
```

---

## 9. Content Trust Pipeline Integration

| Stage | Gate | Who Decides | Evidence Required |
|-------|------|-------------|-------------------|
| UNVERIFIED → AUTOMATED_CHECKED | Automated validation (solution executes, tests pass, no ambiguity) | System | Solution runs, visible tests pass |
| AUTOMATED_CHECKED → HUMAN_REVIEWED | Correctness, relevance, quality | Human reviewer | Reviewer sign-off |
| HUMAN_REVIEWED → TRUSTED | Fully verified, placement-quality | Human + independent expected outputs | Independent answer verification + reasoning verification |

---

## 10. Design Review Checklist

| # | Question | Status |
|---|----------|--------|
| 1 | Canonical skill ID system defined? | Yes (skill_taxonomy.py) |
| 2 | Content trust pipeline defined? | Yes (4 levels) |
| 3 | Only verified content served? | Yes |
| 4 | Content contract covers all types? | Yes (lesson, coding, aptitude, transfer, repair) |
| 5 | Interaction templates defined? | Yes (9 templates) |
| 6 | Skill graph has prerequisites? | Yes (21 skills with explicit deps) |
| 7 | World/level mapping defined? | Yes (sample mapping) |
| 8 | Content loading path fixed? | Yes (adopt content_loader patterns) |
| 9 | No MongoDB for content? | Yes (file-backed only) |
| 10 | Aligned with Vision Lock Question Bank Residency Rule? | Yes |

---

**End of 03 Skill Graph and Content Catalogue**
