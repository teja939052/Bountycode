# Master Curriculum Blueprint — PlacementPro

## Overview

This document is the single source of truth for the PlacementPro curriculum system.
It defines how skills, roles, companies, patterns, assessments, and interviews map
together. All other systems (personalization, readiness, repair, question serving,
mock OA, AI interview) must resolve to IDs defined here.

**Architecture invariant:** ONE canonical curriculum graph. No parallel systems.

## 1. Master Skill Graph

**File:** `backend/app/content/master_skill_graph.py`

The master skill graph is a directed acyclic graph (DAG) of skill nodes. Each node
has the following canonical shape:

```python
@dataclass
class SkillNode:
    skill_id: str          # canonical ID, e.g. "dsa.arrays_hashing"
    name: str              # human-readable name
    parent: Optional[str]  # parent skill_id for tree structure
    prerequisites: List[str]  # transitive prerequisites
    concepts: List[str]    # micro-concepts covered
    difficulty: str        # beginner | intermediate | advanced | expert
    domains: List[str]     # e.g. ["dsa"], ["coding"], ["aptitude"]
    role_relevance: Dict[str, float]  # role_id → 0.0–1.0
    company_relevance: Dict[str, float]  # company_id → 0.0–1.0
    assessment_relevance: Dict[str, float]  # assessment_type → 0.0–1.0
```

### Graph layers

1. **Foundation** (`foundation.*`)
   - programming_basics, control_flow, functions, data_structures_lang, complexity
   - Entry point for all roles. Prerequisites for everything else.

2. **Technical — DSA** (`dsa.*`)
   - arrays_hashing, two_pointers, sliding_window, binary_search, strings,
     linked_list, stack_queue, trees, heaps, graphs, dp, greedy, backtracking,
     tries, sorting, bit_manipulation
   - Core coding interview content.

3. **CS Fundamentals** (`cs_fundamentals.*`)
   - os, networks, dbms, oops, sql, complexity
   - Required for SDE and backend roles.

4. **System Design** (`system_design.*`)
   - scalability, hld, dld, tradeoffs
   - Advanced layer for senior roles.

5. **Aptitude** (`aptitude.*`)
   - quantitative, logical, verbal, data_interpretation, puzzles
   - Indian placement pattern (TCS, Infosys, Wipro, etc.).

6. **Behavioral / Interview** (`behavioral.*`, `interview.*`)
   - communication, leadership, conflict_resolution, teamwork, problem_solving,
     technical_accuracy, depth, system_design_reasoning

7. **Role-specific** (`role.sde.*`, `role.qa.*`, `role.data_analyst.*`, `role.data_scientist.*`)
   - api_design, databases, testing, git, test_strategy, automation, sql, visualization, ml_fundamentals, deep_learning, nlp, mlops

8. **Mock OA** (`oa.*`)
   - aptitude_section, coding_section, cs_section, verbal_section, logical_section

9. **Projects** (`projects.*`)
   - portfolio, architecture

### Graph rules

- No cycles. Every node has at most one parent.
- A skill is blocked if any prerequisite is below threshold (default: score < 60).
- The graph is pure data: no DB calls, no AI, no network I/O.
- Skill IDs are stable. Do not rename existing IDs; add new ones instead.

## 2. Five Role Blueprints

**File:** `backend/app/content/role_blueprints.py`

Five canonical roles are defined:

| Role ID | Display Name | Focus |
|---------|-------------|-------|
| `software_developer` | Software Developer | Full-stack coding, DSA, system design basics |
| `software_engineer` | Software Engineer | Engineering rigor, testing, architecture, design |
| `qa_test_engineer` | QA / Test Engineer | Test strategy, automation, defect management |
| `data_analyst` | Data Analyst | SQL, statistics, visualization, data interpretation |
| `data_scientist` | Data Scientist | ML, statistics, experimentation, deep learning |

### Blueprint shape

```python
@dataclass
class RoleBlueprint:
    role_id: str
    display_name: str
    description: str
    icon: str
    required_skills: List[Dict[str, Any]]   # skill_id, weight, critical flag
    optional_skills: List[Dict[str, Any]]
    prerequisites: List[RolePrerequisite]    # skill_id, min_score
    core_curriculum: List[Dict[str, Any]]   # skill_id, topics, difficulty, hours
    advanced_curriculum: List[Dict[str, Any]]
    assessment_mix: Dict[str, float]         # category → weight
    interview_skills: List[str]              # master graph skill IDs
    project_skills: List[str]
    readiness_requirements: Dict[str, Any]   # min scores, counts
    estimated_weeks: int
    target_companies: List[str]
```

### Integration points

- `readiness_engine.build_target_profile()` reads role blueprints to compute
  target skill weights and criticality.
- `personalization.select_next_mission()` uses role required skills to prioritize
  weak areas that are also role-critical.
- `opportunity_graph` uses role context when computing company fit.

## 3. Service-Based Preparation Blueprint

Preparation is organized around **services** (what the learner does), not pages:

```
LEARN → PRACTICE → ASSESS → REPAIR → RETEST → INTERVIEW → READY
```

| Service | Input | Output | Canonical module |
|---------|-------|--------|------------------|
| Learning | skill_id, lesson_ids | mastery evidence | lesson_runtime, lesson_definitions |
| Practice | skill_id, pattern_id | solves + accuracy | question_store |
| Assessment | category, type | score + trust tier | oa.py, aptitude.py |
| Repair | skill_id, concept | repair mission | repair_service |
| Retest | skill_id, question_id | trust-gated score | repair_service, question_store |
| Interview | role, company | rubric + score | interview.py |
| Readiness | user_id, role, company | 0–100 + next action | readiness_engine |

### Trust policy

Assessment evidence is trust-gated:

| Trust tier | Assessment weight | Learning weight |
|------------|-------------------|-----------------|
| verified | 1.0 | 1.0 |
| reviewed | 0.85 | 0.85 |
| automated_checked | 0.0 (assessment only) | 0.5 |
| needs_review / quarantined / unverified | 0.0 | 0.0 |

## 4. Company Overlay Schema

**File:** `backend/app/content/company_overlays.py`

Each company has a versioned overlay:

```python
@dataclass
class CompanyOverlay:
    company_id: str
    display_name: str
    role: str
    assessment_stages: List[Dict[str, Any]]
    skill_weights: Dict[str, float]
    pattern_relevance: Dict[str, float]  # pattern_id → 0.0–1.0
    question_filters: Dict[str, Any]
    mock_blueprint: Dict[str, Any]
    interview_focus: List[str]
    effective_from: str
    effective_to: str
    version: str
    source: str
    provenance: str
    confidence: float
    min_solved: int
    min_medium: int
    min_hard: int
    min_skills: Dict[str, float]
    focus_topics: List[str]
    interview_rounds: List[str]
    typical_timeline_weeks: int
    match_weights: Dict[str, float]
```

### Versioning

- `effective_from` / `effective_to`: ISO dates. Only active overlays are served.
- `version`: monotonically increasing (e.g. "2025-01").
- `provenance`: who/what produced this profile (e.g. "tcsonly_released_structure").
- `confidence`: 0.0–1.0. Lower confidence profiles are flagged in UI.

### Company registry (12 companies)

| company_id | display_name | confidence |
|------------|-------------|------------|
| tcs | TCS | 0.85 |
| infosys | Infosys | 0.85 |
| wipro | Wipro | 0.80 |
| accenture | Accenture | 0.80 |
| cognizant | Cognizant | 0.80 |
| capgemini | Capgemini | 0.80 |
| hcltech | HCLTech | 0.80 |
| tech_mahindra | Tech Mahindra | 0.75 |
| ltimindtree | LTIMindtree | 0.75 |
| mphasis | Mphasis | 0.70 |
| coforge | Coforge | 0.75 |
| persistent | Persistent | 0.75 |

### Pattern relevance (NOT "most asked")

Pattern relevance is a calibrated 0.0–1.0 score reflecting how much preparation
weight the platform assigns to each pattern for the company. It is derived from:
- Released exam structures
- Known section weightings
- Platform's own historical question tagging

It does **not** claim frequency in the company's actual assessments unless
independently verified and documented in `provenance`.

## 5. Company Pattern Taxonomy

**File:** `backend/app/content/pattern_taxonomy.py`

Patterns are organized by assessment domain:

| Domain | Pattern examples |
|--------|-----------------|
| coding | arrays_hashing, two_pointers, sliding_window, binary_search, dp_1d, dp_2d, greedy, graphs, trees, ... |
| quant | percentages, profit_loss, ratio_proportion, time_work, probability, permutations, data_interpretation, ... |
| reasoning | series, coding_decoding, blood_relations, direction_sense, syllogisms, seating_arrangements, puzzles, ... |
| verbal | reading_comprehension, sentence_correction, para_jumbles, synonyms_antonyms, fill_blanks, ... |
| sql | basic_queries, joins, aggregations, subqueries, window_functions, cte, indexing_optimization, ... |
| cs | os.processes, os.memory, networks.tcp_ip, dbms.acid, dbms.normalization, oops.pillars, ... |

Each pattern has:
- `pattern_id`: canonical stable ID
- `display_name`: human-readable
- `domain`: one of the six domains
- `parent_pattern`: for hierarchical organization
- `concepts`: micro-concepts
- `keywords`: search tokens
- `role_relevance`: role → 0.0–1.0
- `company_relevance`: company → 0.0–1.0
- `assessment_relevance`: assessment type → 0.0–1.0

### Legacy migration

`get_striver_pattern_mapping()` and `map_striver_pattern_to_canonical()` provide
a bridge for questions already tagged with Striver pattern names. New questions
must use canonical `pattern_id`.

## 6. Personalized Recommendation Rules

**File:** `backend/app/services/personalization.py`

The personalization engine selects the next mission using a fixed priority queue:

1. **REQUIRED PREREQUISITE** — A skill is blocked because a graph prerequisite
   is not mastered (score < 60). Must be resolved first.
2. **FAILED CONCEPT / REPAIR** — Open repair missions take priority.
3. **OVERDUE RECALL / SRS** — Due spaced repetition cards.
4. **TARGET-COMPANY REQUIRED SKILL** — A weak skill (score < 70) that is also
   high-relevance for the target company/role (from company_overlays +
   role_blueprints).
5. **LOWEST IMPORTANT MASTERY** — The weakest required skill for the learner's
   role. Falls back to global weak areas.
6. **TRANSFER / INTERLEAVING** — Strong skills practiced in new contexts, or
   misconceptions needing repair.
7. **SESSION-TIME FIT** — If session < 10 minutes, quick SRS review.

### Role-aware personalization

When `role` is provided, the engine:
- Reads `role_blueprints.get_role(role_id)` to get required skills.
- Uses `master_skill_graph.get_skills_for_role(role_id)` for prerequisite checking.
- Prioritizes weak areas that are in the role's `required_skills` list.

### Company-aware personalization

When `company` is provided, the engine:
- Reads `company_overlays.get_company(company_id)` for `min_skills` and
  `pattern_relevance`.
- Cross-references with the learner's weak areas to find company-critical gaps.
- Falls back to `opportunity_graph.get_opportunity()` if overlay is missing.

## 7. Interactive Lesson Grammar

Lessons follow a canonical structure (no second grammar is introduced):

```
Discover → Manipulate → Predict → Build → Break → Debug → Retrieve → Transfer → Mastery
```

Each stage has a trust-gated question or exercise. The lesson engine (`lesson_runtime.py`)
renders stages using question IDs from the bank. Curriculum nodes in `master_skill_graph`
and `role_blueprints` reference `lesson_ids` and `topics` only; they do not contain
lesson content.

## 8. Mock OA Mapping

**File:** `backend/app/routes/oa.py` (existing)

Mock OAs are mapped to curriculum via:
- `oa.*` skill nodes in `master_skill_graph` define OA section skills.
- `company_overlays.mock_blueprint` defines company-specific OA structure
  (sections, question counts, duration, negative marking).
- `company_overlays.assessment_stages` maps to OA stages.

### OA section → skill mapping

| OA section | Master graph skill | Question type |
|------------|-------------------|---------------|
| quantitative_aptitude | aptitude.quantitative | aptitude / quant |
| verbal_ability | aptitude.verbal | verbal |
| reasoning_ability | aptitude.logical | logical |
| advanced_coding | dsa.* (role-dependent) | coding |
| cs_fundamentals | cs_fundamentals.* | cs_fundamentals |

## 9. Interview Mapping

**File:** `backend/app/routes/interview.py` (existing)

Interviews are mapped to curriculum via:
- `interview.*` skill nodes in `master_skill_graph`
- `behavioral.*` skill nodes
- `company_overlays.interview_focus` defines company-specific interview priorities
- `role_blueprints.interview_skills` defines role-specific interview competencies

### Interview question type → skill mapping

| Question type | Master graph skill |
|---------------|-------------------|
| technical | interview.technical_accuracy |
| behavioral | behavioral.communication |
| system_design | system_design.hld |
| coding | dsa.* (role-dependent) |
| sql | cs_fundamentals.sql |
| puzzle | aptitude.puzzles |

## 10. Curriculum-to-Question Mapping

**File:** `backend/app/services/question_store.py` (existing, canonical)

Questions are mapped to the curriculum through:
- `skill_id` → matches `master_skill_graph.skill_id`
- `pattern_id` → matches `pattern_taxonomy.pattern_id`
- `topic` / `sub_topic` → maps to `master_skill_graph.concepts` via
  `pattern_taxonomy` keyword search
- `role` → matches `role_blueprints.role_id`
- `companies` → matches `company_overlays.company_id`
- `type` → maps to OA section / interview question type

### Mapping rules

1. Every served question must have a `trust_status` of `verified` or `reviewed`.
2. Every question must map to at least one `skill_id` from the master graph.
3. Every question must map to exactly one `pattern_id` from the pattern taxonomy.
4. Company-tagged questions use `company_overlays.company_id` values.
5. Role-tagged questions use `role_blueprints.role_id` values.
6. Unmapped questions are quarantined until manually reviewed.

## 11. Content Trust Requirements

The platform enforces a strict trust pipeline:

```
UNVERIFIED → AUTOMATED_CHECKED → HUMAN_REVIEWED → TRUSTED
```

- **UNVERIFIED**: Raw imported content. Never served to students.
- **AUTOMATED_CHECKED**: Passes automated validation (solution executes, tests pass).
- **HUMAN_REVIEWED**: Human verified correctness, relevance, quality.
- **TRUSTED**: Fully verified. Safe to serve as placement-quality.

### Serving gate

Only `trust_status in ("verified", "reviewed")` questions are served.
All others are quarantined.

### Evidence hierarchy

1. Visible test cases (student-facing)
2. Hidden test cases (grading)
3. Independent expected outputs
4. Visible tests + hidden tests + edge cases

### Question bank residency

Question content lives in versioned files under `backend/app/data/`, loaded into
memory at startup by `question_store`. **Never write question content to MongoDB.**

### No-LLM bank rule

No LLM is involved in the question bank — not in authoring, tagging, grading keys,
company attribution, or promotion. LLM-drafted candidates are UNVERIFIED raw material
only.

## 12. Migration Map from Existing Systems

| Existing system | Migration target | Action |
|-----------------|------------------|--------|
| `readiness_engine.COMPANY_PROFILES` | `company_overlays.py` | Replace reads with `company_overlays.get_company()` |
| `company_blueprints.json` | `company_overlays.py` | Merge exam structure into `mock_blueprint` and `assessment_stages` |
| `role_packages.py` | `role_blueprints.py` | Keep learning paths; use `role_blueprints` for capability definitions |
| `role_curriculum.py` | `role_blueprints.py` | Keep phase definitions; use `role_blueprints` for required skills |
| `question_store.STRIVER_PATTERNS` | `pattern_taxonomy.py` | Migrate via `get_striver_pattern_mapping()` |
| `skill_taxonomy.CANONICAL_SKILL_DOMAINS` | `master_skill_graph.py` | Keep as normalization layer; master graph is the richer source |
| `personalization.py` (isolated logic) | `personalization.py` (wired) | Already migrated — reads from master graph, role_blueprints, company_overlays |
| `opportunity_graph.py` (readiness_engine) | `opportunity_graph.py` (company_overlays) | Already migrated — primary source is company_overlays |

### Non-goals

- Do NOT create a new question bank. Reuse `question_store.py`.
- Do NOT create parallel systems. Wire into existing canonical services.
- Do NOT invent URLs. Do NOT call LLMs for curriculum content.
- Do NOT delete existing systems until all callers have migrated.
