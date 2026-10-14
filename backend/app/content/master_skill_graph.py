"""Master skill graph — ONE canonical skill/capability graph.

This module is the single source of truth for the platform's skill taxonomy.
It covers:
- foundation skills (programming basics, language-agnostic)
- technical skills (DSA patterns, coding, CS fundamentals, system design, SQL)
- role skills (SDE, software_engineer, qa_test_engineer, data_analyst, data_scientist)
- interview skills (behavioral, communication, problem-solving)

Every other system (personalization, readiness, repair, question mapping, OA)
must resolve to skill IDs from this graph. No second graph may be introduced.

Design constraints:
- Pure data — no network, no DB access, no AI.
- Importable at module load time (no lazy singleton).
- Each node is deterministic: same inputs always produce same output.
- Content trust: this module defines taxonomy only; no question content lives here.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class SkillNode:
    """A single node in the master skill graph."""
    skill_id: str
    name: str
    parent: Optional[str]
    prerequisites: List[str] = field(default_factory=list)
    concepts: List[str] = field(default_factory=list)
    difficulty: str = "beginner"
    domains: List[str] = field(default_factory=list)
    role_relevance: Dict[str, float] = field(default_factory=dict)
    company_relevance: Dict[str, float] = field(default_factory=dict)
    assessment_relevance: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "name": self.name,
            "parent": self.parent,
            "prerequisites": self.prerequisites,
            "concepts": self.concepts,
            "difficulty": self.difficulty,
            "domains": self.domains,
            "role_relevance": self.role_relevance,
            "company_relevance": self.company_relevance,
            "assessment_relevance": self.assessment_relevance,
        }


# ---------------------------------------------------------------------------
# Canonical skill definitions
# ---------------------------------------------------------------------------
# Difficulty ladder:
#   beginner < intermediate < advanced < expert
# Domains mirror CANONICAL_SKILL_DOMAINS from skill_taxonomy.py plus a few
# placement-specific buckets used by OA / aptitude.
#
# Role relevance: 0.0–1.0, how central the skill is to that role.
# Company relevance: 0.0–1.0, how often the skill appears in that company's
#   assessment / interview (NOT "most asked" — just calibrated relative weight).
# Assessment relevance: which assessment types use this skill and with what weight.

_GRAPH: Dict[str, SkillNode] = {}

def _node(
    skill_id: str,
    name: str,
    parent: Optional[str],
    *,
    prerequisites: Optional[List[str]] = None,
    concepts: Optional[List[str]] = None,
    difficulty: str = "beginner",
    domains: Optional[List[str]] = None,
    role_relevance: Optional[Dict[str, float]] = None,
    company_relevance: Optional[Dict[str, float]] = None,
    assessment_relevance: Optional[Dict[str, float]] = None,
) -> SkillNode:
    return SkillNode(
        skill_id=skill_id,
        name=name,
        parent=parent,
        prerequisites=prerequisites or [],
        concepts=concepts or [],
        difficulty=difficulty,
        domains=domains or [],
        role_relevance=role_relevance or {},
        company_relevance=company_relevance or {},
        assessment_relevance=assessment_relevance or {},
    )


def _build_graph() -> Dict[str, SkillNode]:
    """Build and return the canonical master skill graph."""
    g: Dict[str, SkillNode] = {}

    # ── 1. Foundation layer ───────────────────────────────────────────────
    g["foundation.programming_basics"] = _node(
        "foundation.programming_basics", "Programming Basics", None,
        difficulty="beginner",
        domains=["coding"],
        concepts=["variables", "data_types", "operators", "input_output", "debugging"],
        role_relevance={"software_developer": 0.9, "software_engineer": 0.9, "qa_test_engineer": 0.8, "data_analyst": 0.7, "data_scientist": 0.7},
        company_relevance={"tcs": 0.9, "infosys": 0.9, "wipro": 0.9, "accenture": 0.9, "cognizant": 0.9, "capgemini": 0.9, "hcltech": 0.9, "tech_mahindra": 0.9, "ltimindtree": 0.9, "mphasis": 0.9, "coforge": 0.9, "persistent": 0.9},
        assessment_relevance={"aptitude": 0.3, "coding": 0.8, "interview": 0.2},
    )
    g["foundation.control_flow"] = _node(
        "foundation.control_flow", "Control Flow", "foundation.programming_basics",
        prerequisites=["foundation.programming_basics"],
        difficulty="beginner",
        domains=["coding"],
        concepts=["conditions", "if_else", "switch", "loops", "for", "while", "break_continue"],
        role_relevance={"software_developer": 0.9, "software_engineer": 0.9, "qa_test_engineer": 0.8, "data_analyst": 0.7, "data_scientist": 0.7},
        company_relevance={"tcs": 0.9, "infosys": 0.9, "wipro": 0.9, "accenture": 0.9, "cognizant": 0.9, "capgemini": 0.9, "hcltech": 0.9, "tech_mahindra": 0.9, "ltimindtree": 0.9, "mphasis": 0.9, "coforge": 0.9, "persistent": 0.9},
        assessment_relevance={"coding": 0.8, "aptitude": 0.2},
    )
    g["foundation.functions"] = _node(
        "foundation.functions", "Functions & Scope", "foundation.control_flow",
        prerequisites=["foundation.control_flow"],
        difficulty="beginner",
        domains=["coding"],
        concepts=["parameters", "return_values", "scope", "recursion_intro", "lambda"],
        role_relevance={"software_developer": 0.9, "software_engineer": 0.9, "qa_test_engineer": 0.8, "data_analyst": 0.7, "data_scientist": 0.7},
        company_relevance={"tcs": 0.9, "infosys": 0.9, "wipro": 0.9, "accenture": 0.9, "cognizant": 0.9, "capgemini": 0.9, "hcltech": 0.9, "tech_mahindra": 0.9, "ltimindtree": 0.9, "mphasis": 0.9, "coforge": 0.9, "persistent": 0.9},
        assessment_relevance={"coding": 0.8, "interview": 0.2},
    )
    g["foundation.data_structures_lang"] = _node(
        "foundation.data_structures_lang", "Language Data Structures", "foundation.functions",
        prerequisites=["foundation.functions"],
        difficulty="beginner",
        domains=["coding"],
        concepts=["arrays", "lists", "strings", "dictionaries", "sets", "tuples"],
        role_relevance={"software_developer": 0.9, "software_engineer": 0.9, "qa_test_engineer": 0.7, "data_analyst": 0.8, "data_scientist": 0.8},
        company_relevance={"tcs": 0.9, "infosys": 0.9, "wipro": 0.9, "accenture": 0.9, "cognizant": 0.9, "capgemini": 0.9, "hcltech": 0.9, "tech_mahindra": 0.9, "ltimindtree": 0.9, "mphasis": 0.9, "coforge": 0.9, "persistent": 0.9},
        assessment_relevance={"coding": 0.9, "dsa": 0.6},
    )
    g["foundation.complexity"] = _node(
        "foundation.complexity", "Complexity Analysis", "foundation.data_structures_lang",
        prerequisites=["foundation.data_structures_lang"],
        difficulty="intermediate",
        domains=["coding", "cs_fundamentals"],
        concepts=["big_o", "time_complexity", "space_complexity", "best_avg_worst", "amortized"],
        role_relevance={"software_developer": 0.9, "software_engineer": 0.9, "qa_test_engineer": 0.6, "data_analyst": 0.6, "data_scientist": 0.6},
        company_relevance={"tcs": 0.8, "infosys": 0.8, "wipro": 0.8, "accenture": 0.8, "cognizant": 0.8, "capgemini": 0.8, "hcltech": 0.8, "tech_mahindra": 0.8, "ltimindtree": 0.8, "mphasis": 0.8, "coforge": 0.8, "persistent": 0.8},
        assessment_relevance={"dsa": 0.9, "coding": 0.7, "interview": 0.4},
    )

    # ── 2. Technical / DSA layer ──────────────────────────────────────────
    dsa_nodes = [
        ("dsa.arrays_hashing", "Arrays & Hashing", "foundation.data_structures_lang",
         ["arrays", "hash_maps", "frequency_count", "two_sum", "anagram"],
         "intermediate", 0.9),
        ("dsa.two_pointers", "Two Pointers", "dsa.arrays_hashing",
         ["two_pointers", "sorted_array", "three_sum", "container_water"],
         "intermediate", 0.85),
        ("dsa.sliding_window", "Sliding Window", "dsa.two_pointers",
         ["fixed_window", "variable_window", "longest_subarray", "minimum_window"],
         "intermediate", 0.85),
        ("dsa.binary_search", "Binary Search", "foundation.complexity",
         ["binary_search", "search_space", "sorted_array", "upper_lower_bound"],
         "intermediate", 0.9),
        ("dsa.strings", "Strings", "foundation.data_structures_lang",
         ["palindrome", "substrings", "anagram", "string_manipulation"],
         "intermediate", 0.85),
        ("dsa.linked_list", "Linked Lists", "foundation.data_structures_lang",
         ["singly_linked", "doubly_linked", "cycle_detection", "merge_lists"],
         "intermediate", 0.8),
        ("dsa.stack_queue", "Stacks & Queues", "foundation.data_structures_lang",
         ["stack", "queue", "monotonic_stack", "valid_parentheses"],
         "intermediate", 0.8),
        ("dsa.trees", "Trees", "foundation.data_structures_lang",
         ["binary_tree", "traversals", "bst", "height_depth"],
         "intermediate", 0.85),
        ("dsa.heaps", "Heaps / Priority Queue", "foundation.data_structures_lang",
         ["min_heap", "max_heap", "top_k", "merge_k_sorted"],
         "intermediate", 0.75),
        ("dsa.graphs", "Graphs", "foundation.data_structures_lang",
         ["bfs", "dfs", "adjacency_list", "connected_components"],
         "intermediate", 0.8),
        ("dsa.dp", "Dynamic Programming", "foundation.complexity",
         ["memoization", "tabulation", "knapsack", "longest_common_subsequence"],
         "advanced", 0.9),
        ("dsa.greedy", "Greedy", "foundation.complexity",
         ["greedy_choice", "local_optimum", "interval_scheduling", "jump_game"],
         "advanced", 0.8),
        ("dsa.backtracking", "Backtracking", "dsa.dp",
         ["recursion", "state_space", "permutations", "combinations", "n_queens"],
         "advanced", 0.75),
        ("dsa.tries", "Tries", "dsa.strings",
         ["prefix_tree", "autocomplete", "word_search"],
         "advanced", 0.7),
        ("dsa.sorting", "Sorting", "foundation.complexity",
         ["quick_sort", "merge_sort", "heap_sort", "counting_sort", "radix_sort"],
         "intermediate", 0.85),
        ("dsa.bit_manipulation", "Bit Manipulation", "foundation.complexity",
         ["xor", "bitwise_and_or", "masking", "power_of_two"],
         "intermediate", 0.7),
    ]
    for sid, name, parent, concepts, diff, rel in dsa_nodes:
        g[sid] = _node(
            sid, name, parent,
            prerequisites=[parent] if parent else [],
            concepts=concepts,
            difficulty=diff,
            domains=["dsa"],
            role_relevance={"software_developer": rel, "software_engineer": rel, "qa_test_engineer": rel * 0.6, "data_analyst": rel * 0.5, "data_scientist": rel * 0.5},
            company_relevance={"tcs": 0.7, "infosys": 0.7, "wipro": 0.7, "accenture": 0.6, "cognizant": 0.7, "capgemini": 0.6, "hcltech": 0.7, "tech_mahindra": 0.7, "ltimindtree": 0.7, "mphasis": 0.6, "coforge": 0.7, "persistent": 0.7},
            assessment_relevance={"dsa": 0.9, "coding": 0.7, "interview": 0.3},
        )

    # ── 3. CS fundamentals layer ─────────────────────────────────────────
    cs_nodes = [
        ("cs_fundamentals.os", "Operating Systems", None,
         ["processes", "threads", "scheduling", "memory_management", "deadlocks"], "intermediate"),
        ("cs_fundamentals.networks", "Computer Networks", None,
         ["osi_model", "tcp_ip", "http_https", "dns", "socket_programming"], "intermediate"),
        ("cs_fundamentals.dbms", "DBMS & Databases", None,
         ["rdbms", "normalization", "acid", "indexes", "transactions"], "intermediate"),
        ("cs_fundamentals.oops", "OOP", None,
         ["classes_objects", "inheritance", "polymorphism", "encapsulation", "abstraction"], "beginner"),
        ("cs_fundamentals.sql", "SQL", "cs_fundamentals.dbms",
         ["joins", "aggregations", "subqueries", "window_functions", "query_optimization"], "intermediate"),
        ("cs_fundamentals.complexity", "Complexity Analysis", "foundation.complexity",
         ["big_o", "np_completeness", "approximation"], "advanced"),
    ]
    for sid, name, parent, concepts, diff in cs_nodes:
        g[sid] = _node(
            sid, name, parent,
            prerequisites=[parent] if parent else [],
            concepts=concepts,
            difficulty=diff,
            domains=["cs_fundamentals"],
            role_relevance={"software_developer": 0.7, "software_engineer": 0.7, "qa_test_engineer": 0.6, "data_analyst": 0.8, "data_scientist": 0.8},
            company_relevance={"tcs": 0.6, "infosys": 0.6, "wipro": 0.6, "accenture": 0.7, "cognizant": 0.6, "capgemini": 0.7, "hcltech": 0.6, "tech_mahindra": 0.6, "ltimindtree": 0.6, "mphasis": 0.6, "coforge": 0.7, "persistent": 0.6},
            assessment_relevance={"cs_fundamentals": 0.9, "interview": 0.4, "coding": 0.3},
        )

    # ── 4. System design layer ────────────────────────────────────────────
    sd_nodes = [
        ("system_design.scalability", "Scalability", None,
         ["horizontal_scaling", "vertical_scaling", "load_balancing", "caching", "cdn"], "advanced"),
        ("system_design.hld", "High-Level Design", "system_design.scalability",
         ["requirements", "api_design", "data_modeling", "traffic_analysis"], "advanced"),
        ("system_design.dld", "Detailed Design", "system_design.hld",
         ["database_choice", "microservices", "message_queues", "rate_limiting"], "expert"),
        ("system_design.tradeoffs", "Trade-off Analysis", "system_design.dld",
         ["consistency_availability", "latency_throughput", "cost_performance"], "expert"),
    ]
    for sid, name, parent, concepts, diff in sd_nodes:
        g[sid] = _node(
            sid, name, parent,
            prerequisites=[parent] if parent else [],
            concepts=concepts,
            difficulty=diff,
            domains=["system_design"],
            role_relevance={"software_developer": 0.7, "software_engineer": 0.9, "qa_test_engineer": 0.3, "data_analyst": 0.4, "data_scientist": 0.4},
            company_relevance={"tcs": 0.4, "infosys": 0.4, "wipro": 0.4, "accenture": 0.5, "cognizant": 0.4, "capgemini": 0.6, "hcltech": 0.4, "tech_mahindra": 0.4, "ltimindtree": 0.4, "mphasis": 0.4, "coforge": 0.5, "persistent": 0.5},
            assessment_relevance={"system_design": 0.9, "interview": 0.5, "coding": 0.2},
        )

    # ── 5. Aptitude layer (Indian placement pattern) ──────────────────────
    apt_nodes = [
        ("aptitude.quantitative", "Quantitative Ability", None,
         ["percentages", "profit_loss", "ratio_proportion", "time_work", "probability", "permutations"], "intermediate"),
        ("aptitude.logical", "Logical Reasoning", None,
         ["series", "coding_decoding", "blood_relation", "syllogisms", "seating_arrangements"], "intermediate"),
        ("aptitude.verbal", "Verbal Ability", None,
         ["reading_comprehension", "sentence_correction", "para_jumbles", "synonyms_antonyms"], "intermediate"),
        ("aptitude.data_interpretation", "Data Interpretation", "aptitude.quantitative",
         ["graphs", "tables", "pie_charts", "caselets"], "intermediate"),
        ("aptitude.puzzles", "Puzzle Solving", "aptitude.logical",
         ["logic_grids", "constraint_satisfaction", "analytical_puzzles"], "advanced"),
    ]
    for sid, name, parent, concepts, diff in apt_nodes:
        g[sid] = _node(
            sid, name, parent,
            prerequisites=[parent] if parent else [],
            concepts=concepts,
            difficulty=diff,
            domains=["aptitude"],
            role_relevance={"software_developer": 0.5, "software_engineer": 0.5, "qa_test_engineer": 0.6, "data_analyst": 0.7, "data_scientist": 0.6},
            company_relevance={"tcs": 0.9, "infosys": 0.9, "wipro": 0.9, "accenture": 0.8, "cognizant": 0.9, "capgemini": 0.8, "hcltech": 0.9, "tech_mahindra": 0.9, "ltimindtree": 0.9, "mphasis": 0.9, "coforge": 0.8, "persistent": 0.8},
            assessment_relevance={"aptitude": 0.9, "interview": 0.1},
        )

    # ── 6. Behavioral / interview layer ──────────────────────────────────
    beh_nodes = [
        ("behavioral.communication", "Communication", None,
         ["clarity", "structured_answers", "storytelling"], "intermediate"),
        ("behavioral.leadership", "Leadership", "behavioral.communication",
         ["ownership", "bias_for_action", "decision_making"], "intermediate"),
        ("behavioral.conflict_resolution", "Conflict Resolution", "behavioral.communication",
         ["disagreement", "negotiation", "empathy"], "intermediate"),
        ("behavioral.teamwork", "Teamwork", "behavioral.communication",
         ["collaboration", "diversity", "mentoring"], "intermediate"),
        ("behavioral.problem_solving", "Problem Solving (Behavioral)", "behavioral.communication",
         ["star_method", "root_cause", "ambiguity"], "intermediate"),
        ("behavioral.adaptability", "Adaptability", "behavioral.communication",
         ["change_management", "learning_agility", "resilience"], "intermediate"),
    ]
    for sid, name, parent, concepts, diff in beh_nodes:
        g[sid] = _node(
            sid, name, parent,
            prerequisites=[parent] if parent else [],
            concepts=concepts,
            difficulty=diff,
            domains=["behavioral", "interview"],
            role_relevance={"software_developer": 0.6, "software_engineer": 0.6, "qa_test_engineer": 0.6, "data_analyst": 0.6, "data_scientist": 0.6},
            company_relevance={"tcs": 0.7, "infosys": 0.7, "wipro": 0.7, "accenture": 0.8, "cognizant": 0.7, "capgemini": 0.8, "hcltech": 0.7, "tech_mahindra": 0.7, "ltimindtree": 0.7, "mphasis": 0.7, "coforge": 0.8, "persistent": 0.8},
            assessment_relevance={"interview": 0.9, "behavioral": 0.9},
        )

    # ── 7. Role-specific skills ──────────────────────────────────────────
    role_nodes = [
        # Software Developer / Engineer shared
        ("role.sde.api_design", "API Design", "system_design.hld",
         ["rest", "graphql", "versioning", "authentication"], "advanced"),
        ("role.sde.databases", "Database Design", "cs_fundamentals.dbms",
         ["schema_design", "normalization", "indexing", "query_optimization"], "intermediate"),
        ("role.sde.testing", "Testing", "foundation.functions",
         ["unit_testing", "integration_testing", "tdd", "test_automation"], "intermediate"),
        ("role.sde.git", "Version Control", "foundation.programming_basics",
         ["git_workflow", "branching", "pull_requests", "conflict_resolution"], "beginner"),
        # QA / Test Engineer
        ("role.qa.test_strategy", "Test Strategy", "role.sde.testing",
         ["test_planning", "test_cases", "test_data", "traceability_matrix"], "intermediate"),
        ("role.qa.automation", "Test Automation", "role.qa.test_strategy",
         ["selenium", "playwright", "api_testing", "ci_cd_integration"], "advanced"),
        ("role.qa.performance", "Performance Testing", "role.qa.test_strategy",
         ["load_testing", "stress_testing", "jmeter", "benchmarking"], "advanced"),
        ("role.qa.defect_management", "Defect Management", "role.qa.test_strategy",
         ["bug_lifecycle", "severity_priority", "root_cause_analysis"], "intermediate"),
        # Data Analyst
        ("role.data_analyst.sql", "Advanced SQL", "cs_fundamentals.sql",
         ["window_functions", "cte", "pivot", "query_optimization"], "intermediate"),
        ("role.data_analyst.visualization", "Data Visualization", None,
         ["matplotlib", "seaborn", "powerbi", "tableau", "storytelling"], "intermediate"),
        ("role.data_analyst.statistics", "Statistics for Analysis", None,
         ["descriptive_stats", "hypothesis_testing", "ab_testing", "probability"], "intermediate"),
        ("role.data_analyst.etl", "ETL & Data Pipelines", None,
         ["extract_transform_load", "data_quality", "scheduling"], "intermediate"),
        # Data Scientist
        ("role.data_scientist.ml_fundamentals", "ML Fundamentals", None,
         ["supervised", "unsupervised", "evaluation_metrics", "train_test_split"], "intermediate"),
        ("role.data_scientist.deep_learning", "Deep Learning", "role.data_scientist.ml_fundamentals",
         ["neural_networks", "cnn", "rnn", "transformers", "backpropagation"], "advanced"),
        ("role.data_scientist.nlp", "NLP", "role.data_scientist.deep_learning",
         ["tokenization", "embeddings", "llms", "rag", "fine_tuning"], "advanced"),
        ("role.data_scientist.mlops", "MLOps", "role.data_scientist.ml_fundamentals",
         ["model_deployment", "monitoring", "feature_store", "experiment_tracking"], "advanced"),
    ]
    for sid, name, parent, concepts, diff in role_nodes:
        # Determine base role relevance by prefix
        base_role_relevance = {
            "software_developer": 0.5, "software_engineer": 0.5, "qa_test_engineer": 0.5,
            "data_analyst": 0.5, "data_scientist": 0.5,
        }
        if sid.startswith("role.sde."):
            base_role_relevance = {"software_developer": 0.9, "software_engineer": 0.9, "qa_test_engineer": 0.5, "data_analyst": 0.4, "data_scientist": 0.4}
        elif sid.startswith("role.qa."):
            base_role_relevance = {"software_developer": 0.4, "software_engineer": 0.4, "qa_test_engineer": 0.95, "data_analyst": 0.3, "data_scientist": 0.3}
        elif sid.startswith("role.data_analyst."):
            base_role_relevance = {"software_developer": 0.3, "software_engineer": 0.3, "qa_test_engineer": 0.3, "data_analyst": 0.95, "data_scientist": 0.6}
        elif sid.startswith("role.data_scientist."):
            base_role_relevance = {"software_developer": 0.3, "software_engineer": 0.3, "qa_test_engineer": 0.2, "data_analyst": 0.6, "data_scientist": 0.95}

        g[sid] = _node(
            sid, name, parent,
            prerequisites=[parent] if parent else [],
            concepts=concepts,
            difficulty=diff,
            domains=["coding"] if "api" in sid or "git" in sid else (
                ["cs_fundamentals"] if "sql" in sid or "db" in sid else (
                    ["dsa"] if "testing" in sid and "automation" not in sid else (
                        ["system_design"] if "api_design" in sid else ["coding"]
                    )
                )
            ),
            role_relevance=base_role_relevance,
            company_relevance={"tcs": 0.6, "infosys": 0.6, "wipro": 0.6, "accenture": 0.6, "cognizant": 0.6, "capgemini": 0.6, "hcltech": 0.6, "tech_mahindra": 0.6, "ltimindtree": 0.6, "mphasis": 0.6, "coforge": 0.6, "persistent": 0.6},
            assessment_relevance={"coding": 0.6, "dsa": 0.4, "interview": 0.3},
        )

    # ── 8. Interview competency layer ────────────────────────────────────
    interview_nodes = [
        ("interview.technical_accuracy", "Technical Accuracy", None,
         ["correctness", "depth", "edge_cases"], "intermediate"),
        ("interview.communication", "Communication & Delivery", None,
         ["clarity", "pace", "structure", "listening"], "intermediate"),
        ("interview.problem_solving", "Problem Solving Approach", None,
         ["clarification", "bruteforce_first", "optimization", "tradeoffs"], "intermediate"),
        ("interview.depth", "Answer Depth", "interview.problem_solving",
         ["time_space", "alternatives", "scalability"], "advanced"),
        ("interview.system_design_reasoning", "System Design Reasoning", "system_design.hld",
         ["requirements", "components", "bottlenecks", "evolution"], "advanced"),
    ]
    for sid, name, parent, concepts, diff in interview_nodes:
        g[sid] = _node(
            sid, name, parent,
            prerequisites=[parent] if parent else [],
            concepts=concepts,
            difficulty=diff,
            domains=["interview"],
            role_relevance={"software_developer": 0.8, "software_engineer": 0.9, "qa_test_engineer": 0.7, "data_analyst": 0.7, "data_scientist": 0.8},
            company_relevance={"tcs": 0.7, "infosys": 0.7, "wipro": 0.7, "accenture": 0.8, "cognizant": 0.7, "capgemini": 0.8, "hcltech": 0.7, "tech_mahindra": 0.7, "ltimindtree": 0.7, "mphasis": 0.7, "coforge": 0.8, "persistent": 0.8},
            assessment_relevance={"interview": 0.95, "behavioral": 0.4},
        )

    # ── 9. Mock OA / assessment layer ────────────────────────────────────
    oa_nodes = [
        ("oa.aptitude_section", "Aptitude Section", None,
         ["quantitative", "logical", "verbal", "time_pressure"], "intermediate"),
        ("oa.coding_section", "Coding Section", None,
         ["problem_solving", "test_cases", "debugging", "time_pressure"], "intermediate"),
        ("oa.cs_section", "CS Section", None,
         ["os", "networks", "dbms", "oops", "sql"], "intermediate"),
        ("oa.verbal_section", "Verbal Section", None,
         ["grammar", "comprehension", "vocabulary"], "intermediate"),
        ("oa.logical_section", "Logical Section", None,
         ["reasoning", "puzzles", "data_interpretation"], "intermediate"),
    ]
    for sid, name, parent, concepts, diff in oa_nodes:
        g[sid] = _node(
            sid, name, parent,
            prerequisites=[parent] if parent else [],
            concepts=concepts,
            difficulty=diff,
            domains=["aptitude", "cs_fundamentals", "coding", "interview"],
            role_relevance={"software_developer": 0.7, "software_engineer": 0.7, "qa_test_engineer": 0.8, "data_analyst": 0.7, "data_scientist": 0.6},
            company_relevance={"tcs": 0.9, "infosys": 0.9, "wipro": 0.9, "accenture": 0.9, "cognizant": 0.9, "capgemini": 0.9, "hcltech": 0.9, "tech_mahindra": 0.9, "ltimindtree": 0.9, "mphasis": 0.9, "coforge": 0.9, "persistent": 0.9},
            assessment_relevance={"aptitude": 0.8, "cs_fundamentals": 0.6, "coding": 0.7, "interview": 0.2},
        )

    # ── 10. Project layer ────────────────────────────────────────────────
    g["projects.portfolio"] = _node(
        "projects.portfolio", "Portfolio Projects", None,
        difficulty="intermediate",
        domains=["projects"],
        concepts=["real_world_problem", "documentation", "deployment", "demo"],
        role_relevance={"software_developer": 0.8, "software_engineer": 0.8, "qa_test_engineer": 0.7, "data_analyst": 0.8, "data_scientist": 0.9},
        company_relevance={"tcs": 0.5, "infosys": 0.5, "wipro": 0.5, "accenture": 0.6, "cognizant": 0.5, "capgemini": 0.6, "hcltech": 0.5, "tech_mahindra": 0.5, "ltimindtree": 0.5, "mphasis": 0.5, "coforge": 0.6, "persistent": 0.6},
        assessment_relevance={"interview": 0.6, "projects": 0.9},
    )
    g["projects.architecture"] = _node(
        "projects.architecture", "Project Architecture", "projects.portfolio",
        prerequisites=["projects.portfolio"],
        difficulty="advanced",
        domains=["projects", "system_design"],
        concepts=["system_design", "scalability", "reliability", "tech_stack"],
        role_relevance={"software_developer": 0.8, "software_engineer": 0.9, "qa_test_engineer": 0.5, "data_analyst": 0.5, "data_scientist": 0.6},
        company_relevance={"tcs": 0.5, "infosys": 0.5, "wipro": 0.5, "accenture": 0.6, "cognizant": 0.5, "capgemini": 0.6, "hcltech": 0.5, "tech_mahindra": 0.5, "ltimindtree": 0.5, "mphasis": 0.5, "coforge": 0.6, "persistent": 0.6},
        assessment_relevance={"interview": 0.5, "projects": 0.8},
    )

    return g


def _ensure_graph() -> Dict[str, SkillNode]:
    global _GRAPH
    if not _GRAPH:
        _GRAPH = _build_graph()
    return _GRAPH


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_skill(skill_id: str) -> Optional[SkillNode]:
    """Return a skill node by canonical skill_id, or None."""
    return _ensure_graph().get(skill_id)


def get_all_skills() -> Dict[str, SkillNode]:
    """Return the entire canonical skill graph (read-only copy)."""
    return dict(_ensure_graph())


def get_skills_by_domain(domain: str) -> List[SkillNode]:
    """Return all skills whose domains list contains the given domain."""
    return [n for n in _ensure_graph().values() if domain in n.domains]


def get_skills_for_role(role_id: str) -> List[SkillNode]:
    """Return skills ranked by role_relevance for the given role."""
    role_id = role_id.lower().strip()
    graph = _ensure_graph()
    scored = []
    for node in graph.values():
        rel = node.role_relevance.get(role_id, 0.0)
        if rel > 0:
            scored.append((rel, node))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [n for _, n in scored]


def get_prerequisites(skill_id: str) -> List[str]:
    """Return transitive prerequisites for a skill."""
    node = get_skill(skill_id)
    if not node:
        return []
    result: List[str] = []
    queue = list(node.prerequisites)
    seen: Set[str] = set()
    while queue:
        pid = queue.pop(0)
        if pid in seen:
            continue
        seen.add(pid)
        result.append(pid)
        parent = get_skill(pid)
        if parent:
            queue.extend(parent.prerequisites)
    return result


def get_children(skill_id: str) -> List[SkillNode]:
    """Return direct children of a skill."""
    return [n for n in _ensure_graph().values() if n.parent == skill_id]


def resolve_skill_chain(skill_id: str) -> Dict[str, Any]:
    """Return a skill plus all its prerequisites and children, for debugging."""
    node = get_skill(skill_id)
    if not node:
        return {}
    return {
        "skill": node.to_dict(),
        "prerequisites": [get_skill(p).to_dict() for p in node.prerequisites if get_skill(p)],
        "children": [c.to_dict() for c in get_children(skill_id)],
    }


def is_prerequisite_met(skill_id: str, mastered: Set[str]) -> bool:
    """Return True if all prerequisites for skill_id are in the mastered set."""
    prereqs = get_prerequisites(skill_id)
    return all(p in mastered for p in prereqs)


# ---------------------------------------------------------------------------
# Integration helpers (map external names to canonical IDs)
# ---------------------------------------------------------------------------

def map_oa_section_to_skill(section: str) -> Optional[str]:
    """Map an OA section name to a master graph skill_id."""
    mapping = {
        "aptitude": "aptitude.quantitative",
        "quantitative": "aptitude.quantitative",
        "logical": "aptitude.logical",
        "verbal": "aptitude.verbal",
        "coding": "dsa.arrays_hashing",
        "cs_fundamentals": "cs_fundamentals.oops",
        "reasoning": "aptitude.logical",
        "data_interpretation": "aptitude.data_interpretation",
    }
    return mapping.get(section.lower())


def map_company_focus_to_skill(focus: str) -> Optional[str]:
    """Map a company focus area to a master graph skill_id."""
    mapping = {
        "arrays": "dsa.arrays_hashing",
        "strings": "dsa.strings",
        "trees": "dsa.trees",
        "dp": "dsa.dp",
        "graphs": "dsa.graphs",
        "system_design": "system_design.hld",
        "sql": "cs_fundamentals.sql",
        "aptitude": "aptitude.quantitative",
        "verbal": "aptitude.verbal",
        "logical": "aptitude.logical",
        "oops": "cs_fundamentals.oops",
        "os": "cs_fundamentals.os",
        "networks": "cs_fundamentals.networks",
        "pseudo_code": "foundation.control_flow",
    }
    return mapping.get(focus.lower())


def map_interview_question_type_to_skill(qtype: str) -> Optional[str]:
    """Map an interview question type to a master graph skill_id."""
    mapping = {
        "technical": "interview.technical_accuracy",
        "behavioral": "behavioral.communication",
        "system_design": "system_design.hld",
        "coding": "dsa.arrays_hashing",
        "sql": "cs_fundamentals.sql",
        "puzzle": "aptitude.puzzles",
    }
    return mapping.get(qtype.lower())


# ---------------------------------------------------------------------------
# Graph integrity helpers
# ---------------------------------------------------------------------------

def validate_graph() -> Dict[str, Any]:
    """Return a validation report for the master skill graph."""
    graph = _ensure_graph()
    issues: List[str] = []
    orphans = []
    missing_parents = []
    for sid, node in graph.items():
        if node.parent and node.parent not in graph:
            missing_parents.append((sid, node.parent))
        if not node.parent and not node.prerequisites:
            orphans.append(sid)
    if missing_parents:
        issues.append(f"{len(missing_parents)} nodes have missing parents")
    if orphans:
        issues.append(f"Root nodes: {orphans}")
    return {
        "total_nodes": len(graph),
        "issues": issues,
        "valid": len(issues) == 0,
    }
