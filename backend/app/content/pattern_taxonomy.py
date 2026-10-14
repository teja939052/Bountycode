"""Pattern taxonomy — canonical question patterns by assessment domain.

This module is the single source of truth for question pattern taxonomy.
It unifies:
- Coding patterns (Striver-style, already partially in question_store.py)
- Quant aptitude patterns
- Logical reasoning patterns
- Verbal ability patterns
- SQL patterns
- CS fundamentals patterns

Pattern IDs are stable and canonical. Every question in the bank should
reference exactly one pattern_id from this taxonomy.

Design constraints:
- Pure data — no network, no DB access, no AI.
- Importable at module load time.
- Deterministic: same inputs always produce same outputs.
- Content trust: this module defines taxonomy only; no question content lives here.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class PatternDefinition:
    """A canonical question pattern."""
    pattern_id: str
    display_name: str
    domain: str  # coding, quant, reasoning, verbal, sql, cs
    parent_pattern: Optional[str] = None
    concepts: List[str] = field(default_factory=list)
    difficulty: str = "intermediate"
    role_relevance: Dict[str, float] = field(default_factory=dict)
    company_relevance: Dict[str, float] = field(default_factory=dict)
    assessment_relevance: Dict[str, float] = field(default_factory=dict)
    keywords: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pattern_id": self.pattern_id,
            "display_name": self.display_name,
            "domain": self.domain,
            "parent_pattern": self.parent_pattern,
            "concepts": self.concepts,
            "difficulty": self.difficulty,
            "role_relevance": self.role_relevance,
            "company_relevance": self.company_relevance,
            "assessment_relevance": self.assessment_relevance,
            "keywords": self.keywords,
        }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _pat(
    pattern_id: str,
    display_name: str,
    domain: str,
    *,
    parent: Optional[str] = None,
    concepts: Optional[List[str]] = None,
    difficulty: str = "intermediate",
    role_relevance: Optional[Dict[str, float]] = None,
    company_relevance: Optional[Dict[str, float]] = None,
    assessment_relevance: Optional[Dict[str, float]] = None,
    keywords: Optional[List[str]] = None,
) -> PatternDefinition:
    return PatternDefinition(
        pattern_id=pattern_id,
        display_name=display_name,
        domain=domain,
        parent_pattern=parent,
        concepts=concepts or [],
        difficulty=difficulty,
        role_relevance=role_relevance or {},
        company_relevance=company_relevance or {},
        assessment_relevance=assessment_relevance or {},
        keywords=keywords or [],
    )


# ---------------------------------------------------------------------------
# Canonical pattern registry
# ---------------------------------------------------------------------------

_TAXONOMY: Dict[str, PatternDefinition] = {}

def _build_taxonomy() -> Dict[str, PatternDefinition]:
    t: Dict[str, PatternDefinition] = {}

    # ── Coding patterns (aligned with Striver sheet + platform needs) ─────
    coding_patterns = [
        {"pattern_id": "coding.arrays_hashing", "display_name": "Arrays & Hashing", "domain": "coding", "concepts": ["arrays", "hash_map", "frequency_count", "two_sum", "anagram"], "keywords": ["two sum", "anagram", "group anagram", "subarray", "majority element"]},
        {"pattern_id": "coding.two_pointers", "display_name": "Two Pointers", "domain": "coding", "parent_pattern": "coding.arrays_hashing", "concepts": ["two_pointers", "sorted_array", "three_sum", "container_water"], "keywords": ["two pointers", "three sum", "sorted array", "trapping rain"]},
        {"pattern_id": "coding.sliding_window", "display_name": "Sliding Window", "domain": "coding", "parent_pattern": "coding.two_pointers", "concepts": ["fixed_window", "variable_window", "longest_subarray", "minimum_window"], "keywords": ["sliding window", "maximum sum subarray", "longest subarray", "minimum window"]},
        {"pattern_id": "coding.binary_search", "display_name": "Binary Search", "domain": "coding", "concepts": ["binary_search", "search_space", "upper_lower_bound", "rotated_array"], "keywords": ["binary search", "search in rotated", "peak element", "kth"]},
        {"pattern_id": "coding.strings", "display_name": "Strings", "domain": "coding", "concepts": ["palindrome", "substrings", "anagram", "string_manipulation"], "keywords": ["palindrome", "valid anagram", "longest palindromic", "group anagram"]},
        {"pattern_id": "coding.linked_list", "display_name": "Linked Lists", "domain": "coding", "concepts": ["singly_linked", "doubly_linked", "cycle_detection", "merge_lists"], "keywords": ["linked list", "reverse list", "detect cycle", "merge two sorted lists"]},
        {"pattern_id": "coding.stack_queue", "display_name": "Stacks & Queues", "domain": "coding", "concepts": ["stack", "queue", "monotonic_stack", "valid_parentheses"], "keywords": ["stack", "queue", "valid parentheses", "min stack", "daily temperatures"]},
        {"pattern_id": "coding.trees", "display_name": "Trees", "domain": "coding", "concepts": ["binary_tree", "traversals", "bst", "height_depth"], "keywords": ["binary tree", "traversal", "lowest common ancestor", "invert tree", "path sum"]},
        {"pattern_id": "coding.heaps", "display_name": "Heaps / Priority Queue", "domain": "coding", "concepts": ["min_heap", "max_heap", "top_k", "merge_k_sorted"], "keywords": ["heap", "priority queue", "top k", "kth largest", "merge k sorted lists"]},
        {"pattern_id": "coding.graphs", "display_name": "Graphs", "domain": "coding", "concepts": ["bfs", "dfs", "adjacency_list", "connected_components"], "keywords": ["graph", "number of islands", "course schedule", "alien dictionary"]},
        {"pattern_id": "coding.dp_1d", "display_name": "Dynamic Programming 1D", "domain": "coding", "concepts": ["memoization", "tabulation", "climbing_stairs", "house_robber"], "keywords": ["climbing stairs", "house robber", "longest increasing", "decode ways", "word break", "coin change"]},
        {"pattern_id": "coding.dp_2d", "display_name": "Dynamic Programming 2D", "domain": "coding", "parent_pattern": "coding.dp_1d", "concepts": ["grid", "unique_paths", "minimum_path_sum", "edit_distance"], "keywords": ["unique paths", "minimum path sum", "triangle", "edit distance", "grid"]},
        {"pattern_id": "coding.dp_strings", "display_name": "Dynamic Programming on Strings", "domain": "coding", "parent_pattern": "coding.dp_1d", "concepts": ["lcs", "edit_distance", "palindromic_subsequence"], "keywords": ["lcs", "edit distance", "longest common subsequence", "palindromic subsequence"]},
        {"pattern_id": "coding.dp_subsequences", "display_name": "DP on Subsequences", "domain": "coding", "parent_pattern": "coding.dp_1d", "concepts": ["subset_sum", "knapsack", "partition_equal"], "keywords": ["coin change", "subset sum", "partition equal subset", "0/1 knapsack", "target sum"]},
        {"pattern_id": "coding.dp_trees", "display_name": "DP on Trees", "domain": "coding", "parent_pattern": "coding.dp_1d", "concepts": ["binary_tree_max_path", "diameter", "house_robber_iii"], "keywords": ["binary tree maximum path", "house robber iii", "diameter of binary tree"]},
        {"pattern_id": "coding.greedy", "display_name": "Greedy", "domain": "coding", "concepts": ["greedy_choice", "local_optimum", "interval_scheduling", "jump_game"], "keywords": ["greedy", "jump game", "gas station", "assign cookies", "minimum number of arrows"]},
        {"pattern_id": "coding.intervals", "display_name": "Intervals", "domain": "coding", "concepts": ["merge_intervals", "meeting_rooms", "insert_interval", "non_overlapping"], "keywords": ["merge intervals", "meeting rooms", "insert interval", "non-overlapping intervals"]},
        {"pattern_id": "coding.bit_manipulation", "display_name": "Bit Manipulation", "domain": "coding", "concepts": ["xor", "bitwise_and_or", "masking", "power_of_two"], "keywords": ["single number", "missing number", "power of two", "hamming weight"]},
        {"pattern_id": "coding.math_number_theory", "display_name": "Math & Number Theory", "domain": "coding", "concepts": ["prime", "gcd", "modulo", "factorial", "palindrome_number"], "keywords": ["prime", "gcd", "modulo", "factorial", "palindrome number", "reverse integer"]},
        {"pattern_id": "coding.recursion_backtracking", "display_name": "Recursion & Backtracking", "domain": "coding", "concepts": ["recursion", "state_space", "permutations", "combinations", "n_queens"], "keywords": ["permutations", "combination sum", "subsets", "n-queens", "word break", "generate parentheses"]},
        {"pattern_id": "coding.sorting", "display_name": "Sorting", "domain": "coding", "concepts": ["quick_sort", "merge_sort", "heap_sort", "counting_sort"], "keywords": ["sort", "sorting", "merge sorted"]},
        {"pattern_id": "coding.searching", "display_name": "Searching", "domain": "coding", "concepts": ["linear_search", "binary_search", "search_space"], "keywords": ["searching", "binary search", "search in rotated"]},
        {"pattern_id": "coding.tries", "display_name": "Tries", "domain": "coding", "concepts": ["prefix_tree", "autocomplete", "word_search"], "keywords": ["trie", "prefix", "dictionary", "autocomplete", "word search ii"]},
        {"pattern_id": "coding.union_find", "display_name": "Union Find", "domain": "coding", "concepts": ["disjoint_set", "connected_components", "redundant_connection"], "keywords": ["union find", "connected components", "number of islands", "redundant connection", "accounts merge"]},
        {"pattern_id": "coding.shortest_path", "display_name": "Shortest Path", "domain": "coding", "concepts": ["dijkstra", "bellman_ford", "floyd_warshall"], "keywords": ["shortest path", "dijkstra", "bellman", "floyd", "network delay"]},
        {"pattern_id": "coding.design_oop", "display_name": "Design / OOP", "domain": "coding", "concepts": ["class_design", "lru_cache", "min_stack", "deque"], "keywords": ["design", "lru cache", "min stack", "deque", "lfu cache"]},
        {"pattern_id": "coding.string_matching", "display_name": "String Matching", "domain": "coding", "concepts": ["kmp", "rabin_karp", "z_algorithm"], "keywords": ["kmp", "rabin-karp", "pattern", "substring search", "z-algorithm"]},
    ]
    for pat in coding_patterns:
        t[pat["pattern_id"]] = _pat(
            pat["pattern_id"], pat["display_name"], pat["domain"],
            parent=pat.get("parent_pattern"),
            concepts=pat.get("concepts", []),
            keywords=pat.get("keywords", []),
            role_relevance={"software_developer": 0.9, "software_engineer": 0.9, "qa_test_engineer": 0.5, "data_analyst": 0.4, "data_scientist": 0.4},
            company_relevance={"tcs": 0.6, "infosys": 0.6, "wipro": 0.6, "accenture": 0.5, "cognizant": 0.6, "capgemini": 0.5, "hcltech": 0.6, "tech_mahindra": 0.6, "ltimindtree": 0.6, "mphasis": 0.5, "coforge": 0.5, "persistent": 0.5},
            assessment_relevance={"dsa": 0.9, "coding": 0.8, "interview": 0.3},
        )

    # ── Quant aptitude patterns ──────────────────────────────────────────
    quant_patterns = [
        {"pattern_id": "quant.percentages", "display_name": "Percentages", "domain": "quant", "concepts": ["percentage_change", "successive_percent", "net_percentage"], "keywords": ["percentage", "profit loss", "discount", "markup"]},
        {"pattern_id": "quant.profit_loss", "display_name": "Profit & Loss", "domain": "quant", "concepts": ["cost_price", "selling_price", "margin"], "keywords": ["profit", "loss", "cost price", "selling price"]},
        {"pattern_id": "quant.ratio_proportion", "display_name": "Ratio & Proportion", "domain": "quant", "concepts": ["ratio", "proportion", "division", "mixtures"], "keywords": ["ratio", "proportion", "a:b", "mixture"]},
        {"pattern_id": "quant.averages", "display_name": "Averages", "domain": "quant", "concepts": ["mean", "median", "mode", "weighted_average"], "keywords": ["average", "mean", "weighted average"]},
        {"pattern_id": "quant.time_work", "display_name": "Time & Work", "domain": "quant", "concepts": ["efficiency", "man_days", "pipes_cisterns"], "keywords": ["time and work", "efficiency", "man days", "pipes and cisterns"]},
        {"pattern_id": "quant.time_distance", "display_name": "Time, Speed & Distance", "domain": "quant", "concepts": ["speed", "relative_speed", "trains", "boats"], "keywords": ["time speed distance", "relative speed", "train", "boat stream"]},
        {"pattern_id": "quant.probability", "display_name": "Probability", "domain": "quant", "concepts": ["experiment", "favorable_cases", "conditional_probability"], "keywords": ["probability", "chance", "dice", "cards"]},
        {"pattern_id": "quant.permutations_combinations", "display_name": "Permutations & Combinations", "domain": "quant", "concepts": ["arrangements", "selections", "factorial"], "keywords": ["permutation", "combination", "arrangement", "selection"]},
        {"pattern_id": "quant.number_systems", "display_name": "Number Systems", "domain": "quant", "concepts": ["divisibility", "remainders", "factors", "base_conversion"], "keywords": ["number system", "divisibility", "remainder", "factors", "hcf", "lcm"]},
        {"pattern_id": "quant.data_interpretation", "display_name": "Data Interpretation", "domain": "quant", "concepts": ["graphs", "tables", "pie_charts", "caselets"], "keywords": ["data interpretation", "graph", "table", "pie chart", "caselet"]},
        {"pattern_id": "quant.simplification", "display_name": "Simplification", "domain": "quant", "concepts": ["bodmas", "approximations", "surds_indices"], "keywords": ["simplification", "bodmas", "approximation"]},
        {"pattern_id": "quant.interest", "display_name": "Interest", "domain": "quant", "concepts": ["simple_interest", "compound_interest"], "keywords": ["simple interest", "compound interest", "si", "ci"]},
    ]
    for pat in quant_patterns:
        t[pat["pattern_id"]] = _pat(pat["pattern_id"], pat["display_name"], pat["domain"], concepts=pat.get("concepts", []), keywords=pat.get("keywords", []),
            role_relevance={"software_developer": 0.5, "software_engineer": 0.5, "qa_test_engineer": 0.6, "data_analyst": 0.8, "data_scientist": 0.8},
            company_relevance={"tcs": 0.8, "infosys": 0.8, "wipro": 0.8, "accenture": 0.7, "cognizant": 0.8, "capgemini": 0.7, "hcltech": 0.8, "tech_mahindra": 0.8, "ltimindtree": 0.8, "mphasis": 0.8, "coforge": 0.7, "persistent": 0.7},
            assessment_relevance={"aptitude": 0.9, "quant": 0.9},
        )

    # ── Logical reasoning patterns ───────────────────────────────────────
    reasoning_patterns = [
        {"pattern_id": "reasoning.series", "display_name": "Series", "domain": "reasoning", "concepts": ["number_series", "letter_series", "mixed_series"], "keywords": ["series", "number series", "letter series", "missing number"]},
        {"pattern_id": "reasoning.coding_decoding", "display_name": "Coding-Decoding", "domain": "reasoning", "concepts": ["letter_shifting", "reverse_coding", "pattern_coding"], "keywords": ["coding decoding", "code language", "shift"]},
        {"pattern_id": "reasoning.blood_relations", "display_name": "Blood Relations", "domain": "reasoning", "concepts": ["family_tree", "relationships"], "keywords": ["blood relation", "family", "relation"]},
        {"pattern_id": "reasoning.direction_sense", "display_name": "Direction Sense", "domain": "reasoning", "concepts": ["compass", "turns", "shadow"], "keywords": ["direction", "compass", "north south"]},
        {"pattern_id": "reasoning.analogy", "display_name": "Analogy", "domain": "reasoning", "concepts": ["word_analogy", "number_analogy"], "keywords": ["analogy", "similarity", "relation"]},
        {"pattern_id": "reasoning.odd_one_out", "display_name": "Odd One Out", "domain": "reasoning", "concepts": ["classification", "odd_item"], "keywords": ["odd one out", "odd man out", "classification"]},
        {"pattern_id": "reasoning.sequence", "display_name": "Sequence & Order", "domain": "reasoning", "concepts": ["ranking", "arrangement", "order"], "keywords": ["sequence", "order", "ranking", "arrangement"]},
        {"pattern_id": "reasoning.seating_arrangements", "display_name": "Seating Arrangements", "domain": "reasoning", "concepts": ["linear_arrangement", "circular_arrangement", "conditions"], "keywords": ["seating arrangement", "linear", "circular"]},
        {"pattern_id": "reasoning.syllogisms", "display_name": "Syllogisms", "domain": "reasoning", "concepts": ["premises", "conclusion", "deduction"], "keywords": ["syllogism", "conclusion", "premise", "deduction"]},
        {"pattern_id": "reasoning.data_sufficiency", "display_name": "Data Sufficiency", "domain": "reasoning", "concepts": ["sufficient_data", "statements"], "keywords": ["data sufficiency", "sufficient", "statement"]},
        {"pattern_id": "reasoning.puzzles", "display_name": "Puzzles", "domain": "reasoning", "concepts": ["logic_grids", "constraints"], "keywords": ["puzzle", "logic puzzle", "constraint"]},
    ]
    for pat in reasoning_patterns:
        t[pat["pattern_id"]] = _pat(pat["pattern_id"], pat["display_name"], pat["domain"], concepts=pat.get("concepts", []), keywords=pat.get("keywords", []),
            role_relevance={"software_developer": 0.5, "software_engineer": 0.5, "qa_test_engineer": 0.7, "data_analyst": 0.6, "data_scientist": 0.6},
            company_relevance={"tcs": 0.8, "infosys": 0.8, "wipro": 0.8, "accenture": 0.7, "cognizant": 0.8, "capgemini": 0.7, "hcltech": 0.8, "tech_mahindra": 0.8, "ltimindtree": 0.8, "mphasis": 0.8, "coforge": 0.7, "persistent": 0.7},
            assessment_relevance={"aptitude": 0.9, "logical": 0.9},
        )

    # ── Verbal ability patterns ──────────────────────────────────────────
    verbal_patterns = [
        {"pattern_id": "verbal.reading_comprehension", "display_name": "Reading Comprehension", "domain": "verbal", "concepts": ["passage", "inference", "main_idea"], "keywords": ["reading comprehension", "passage", "inference"]},
        {"pattern_id": "verbal.sentence_correction", "display_name": "Sentence Correction", "domain": "verbal", "concepts": ["grammar", "subject_verb_agreement", "tenses"], "keywords": ["sentence correction", "grammar", "error"]},
        {"pattern_id": "verbal.para_jumbles", "display_name": "Para Jumbles", "domain": "verbal", "concepts": ["coherence", "logical_flow"], "keywords": ["para jumble", "sentence rearrangement", "jumbled sentences"]},
        {"pattern_id": "verbal.synonyms_antonyms", "display_name": "Synonyms & Antonyms", "domain": "verbal", "concepts": ["vocabulary", "word_meaning"], "keywords": ["synonym", "antonym", "vocabulary", "meaning"]},
        {"pattern_id": "verbal.fill_blanks", "display_name": "Fill in the Blanks", "domain": "verbal", "concepts": ["prepositions", "articles", "conjunctions"], "keywords": ["fill in the blanks", "fill the blanks", "blank"]},
        {"pattern_id": "verbal.error_detection", "display_name": "Error Detection", "domain": "verbal", "concepts": ["grammar_errors", "spelling_errors"], "keywords": ["error detection", "spot the error", "error"]},
        {"pattern_id": "verbal.spelling", "display_name": "Spelling", "domain": "verbal", "concepts": ["correct_spelling", "misspelled_words"], "keywords": ["spelling", "correctly spelt", "misspelled"]},
    ]
    for pat in verbal_patterns:
        t[pat["pattern_id"]] = _pat(pat["pattern_id"], pat["display_name"], pat["domain"], concepts=pat.get("concepts", []), keywords=pat.get("keywords", []),
            role_relevance={"software_developer": 0.4, "software_engineer": 0.4, "qa_test_engineer": 0.5, "data_analyst": 0.5, "data_scientist": 0.5},
            company_relevance={"tcs": 0.7, "infosys": 0.7, "wipro": 0.7, "accenture": 0.8, "cognizant": 0.7, "capgemini": 0.8, "hcltech": 0.7, "tech_mahindra": 0.7, "ltimindtree": 0.7, "mphasis": 0.7, "coforge": 0.8, "persistent": 0.8},
            assessment_relevance={"aptitude": 0.9, "verbal": 0.9},
        )

    # ── SQL patterns ─────────────────────────────────────────────────────
    sql_patterns = [
        {"pattern_id": "sql.basic_queries", "display_name": "Basic Queries", "domain": "sql", "concepts": ["select", "where", "order_by", "limit"], "keywords": ["select", "where", "order by", "limit"]},
        {"pattern_id": "sql.joins", "display_name": "Joins", "domain": "sql", "concepts": ["inner_join", "left_join", "right_join", "full_join", "cross_join"], "keywords": ["join", "inner join", "left join", "right join", "full outer join"]},
        {"pattern_id": "sql.aggregations", "display_name": "Aggregations", "domain": "sql", "concepts": ["group_by", "having", "count_sum_avg_min_max"], "keywords": ["group by", "having", "count", "sum", "avg", "min", "max"]},
        {"pattern_id": "sql.subqueries", "display_name": "Subqueries", "domain": "sql", "concepts": ["nested_select", "correlated_subquery", "exists"], "keywords": ["subquery", "nested", "exists", "not exists", "in"]},
        {"pattern_id": "sql.window_functions", "display_name": "Window Functions", "domain": "sql", "concepts": ["rank", "dense_rank", "row_number", "lead_lag", "ntile"], "keywords": ["rank", "dense rank", "row number", "lead", "lag", "partition by"]},
        {"pattern_id": "sql.cte", "display_name": "Common Table Expressions", "domain": "sql", "concepts": ["with_clause", "recursive_cte"], "keywords": ["cte", "with", "recursive", "common table expression"]},
        {"pattern_id": "sql.indexing_optimization", "display_name": "Indexing & Optimization", "domain": "sql", "concepts": ["indexes", "execution_plan", "query_optimization"], "keywords": ["index", "execution plan", "optimize", "query optimization"]},
        {"pattern_id": "sql.schema_design", "display_name": "Schema Design", "domain": "sql", "concepts": ["normalization", "erd", "primary_foreign_key"], "keywords": ["schema", "normalization", "erd", "primary key", "foreign key"]},
    ]
    for pat in sql_patterns:
        t[pat["pattern_id"]] = _pat(pat["pattern_id"], pat["display_name"], pat["domain"], concepts=pat.get("concepts", []), keywords=pat.get("keywords", []),
            role_relevance={"software_developer": 0.5, "software_engineer": 0.5, "qa_test_engineer": 0.4, "data_analyst": 0.9, "data_scientist": 0.8},
            company_relevance={"tcs": 0.5, "infosys": 0.5, "wipro": 0.5, "accenture": 0.6, "cognizant": 0.5, "capgemini": 0.6, "hcltech": 0.5, "tech_mahindra": 0.5, "ltimindtree": 0.5, "mphasis": 0.5, "coforge": 0.6, "persistent": 0.6},
            assessment_relevance={"sql": 0.9, "cs_fundamentals": 0.6, "coding": 0.3},
        )

    # ── CS fundamentals patterns ─────────────────────────────────────────
    cs_patterns = [
        {"pattern_id": "cs.os.processes", "display_name": "Processes & Threads", "domain": "cs", "concepts": ["process", "thread", "scheduling", "context_switch"], "keywords": ["process", "thread", "scheduling", "context switch"]},
        {"pattern_id": "cs.os.memory", "display_name": "Memory Management", "domain": "cs", "concepts": ["virtual_memory", "paging", "segmentation", "page_replacement"], "keywords": ["memory management", "virtual memory", "paging", "segmentation"]},
        {"pattern_id": "cs.os.deadlocks", "display_name": "Deadlocks", "domain": "cs", "concepts": ["conditions", "prevention", "avoidance", "banker"], "keywords": ["deadlock", "banker algorithm", "deadlock prevention"]},
        {"pattern_id": "cs.networks.tcp_ip", "display_name": "TCP/IP", "domain": "cs", "concepts": ["tcp", "udp", "three_way_handshake", "flow_control"], "keywords": ["tcp", "udp", "three way handshake", "flow control"]},
        {"pattern_id": "cs.networks.http", "display_name": "HTTP & DNS", "domain": "cs", "concepts": ["http_methods", "status_codes", "dns", "ssl_tls"], "keywords": ["http", "https", "dns", "ssl", "tls", "status code"]},
        {"pattern_id": "cs.dbms.acid", "display_name": "ACID & Transactions", "domain": "cs", "concepts": ["atomicity", "consistency", "isolation", "durability"], "keywords": ["acid", "transaction", "commit", "rollback"]},
        {"pattern_id": "cs.dbms.normalization", "display_name": "Normalization", "domain": "cs", "concepts": ["1nf", "2nf", "3nf", "bcnf", "denormalization"], "keywords": ["normalization", "1nf", "2nf", "3nf", "bcnf", "denormalization"]},
        {"pattern_id": "cs.dbms.indexing", "display_name": "Indexing", "domain": "cs", "concepts": ["b_tree", "hash_index", "clustered_unclustered"], "keywords": ["index", "b tree", "clustered", "unclustered"]},
        {"pattern_id": "cs.oops.classes", "display_name": "Classes & Objects", "domain": "cs", "concepts": ["class", "object", "constructor", "destructor"], "keywords": ["class", "object", "constructor", "destructor"]},
        {"pattern_id": "cs.oops.pillars", "display_name": "OOP Pillars", "domain": "cs", "concepts": ["inheritance", "polymorphism", "encapsulation", "abstraction"], "keywords": ["inheritance", "polymorphism", "encapsulation", "abstraction"]},
        {"pattern_id": "cs.complexity.analysis", "display_name": "Complexity Analysis", "domain": "cs", "concepts": ["big_o", "time_space", "best_avg_worst"], "keywords": ["big o", "time complexity", "space complexity", "best case", "worst case"]},
    ]
    for pat in cs_patterns:
        t[pat["pattern_id"]] = _pat(pat["pattern_id"], pat["display_name"], pat["domain"], concepts=pat.get("concepts", []), keywords=pat.get("keywords", []),
            role_relevance={"software_developer": 0.7, "software_engineer": 0.7, "qa_test_engineer": 0.6, "data_analyst": 0.6, "data_scientist": 0.6},
            company_relevance={"tcs": 0.6, "infosys": 0.6, "wipro": 0.6, "accenture": 0.7, "cognizant": 0.6, "capgemini": 0.7, "hcltech": 0.6, "tech_mahindra": 0.6, "ltimindtree": 0.6, "mphasis": 0.6, "coforge": 0.7, "persistent": 0.7},
            assessment_relevance={"cs_fundamentals": 0.9, "coding": 0.3, "interview": 0.3},
        )

    return t


def _ensure_taxonomy() -> Dict[str, PatternDefinition]:
    global _TAXONOMY
    if not _TAXONOMY:
        _TAXONOMY = _build_taxonomy()
    return _TAXONOMY


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_pattern(pattern_id: str) -> Optional[PatternDefinition]:
    """Return a pattern definition by canonical pattern_id, or None."""
    return _ensure_taxonomy().get(pattern_id)


def get_all_patterns() -> Dict[str, PatternDefinition]:
    """Return the entire pattern taxonomy (read-only copy)."""
    return dict(_ensure_taxonomy())


def get_patterns_by_domain(domain: str) -> List[PatternDefinition]:
    """Return all patterns for a given domain."""
    return [p for p in _ensure_taxonomy().values() if p.domain == domain]


def get_patterns_for_company(company_id: str) -> Dict[str, PatternDefinition]:
    """Return patterns weighted by company relevance (threshold > 0)."""
    co_patterns = {}
    for pid, pat in _ensure_taxonomy().items():
        rel = pat.company_relevance.get(company_id.lower().strip(), 0.0)
        if rel > 0:
            co_patterns[pid] = pat
    return co_patterns


def get_children(pattern_id: str) -> List[PatternDefinition]:
    """Return direct child patterns."""
    return [p for p in _ensure_taxonomy().values() if p.parent_pattern == pattern_id]


def search_patterns(query: str, domain: Optional[str] = None) -> List[PatternDefinition]:
    """Search patterns by keyword in display_name, concepts, or keywords list."""
    q = query.lower().strip()
    if not q:
        return []
    results = []
    for pat in _ensure_taxonomy().values():
        if domain and pat.domain != domain:
            continue
        haystack = f"{pat.display_name} {' '.join(pat.concepts)} {' '.join(pat.keywords)}".lower()
        if q in haystack:
            results.append(pat)
    return results


def pattern_to_question_filters(pattern_id: str) -> Dict[str, Any]:
    """Convert a pattern_id to question_store filter kwargs where possible."""
    pat = get_pattern(pattern_id)
    if not pat:
        return {}
    # Map pattern domain to question_store fields
    domain_to_type = {
        "coding": "coding",
        "quant": "aptitude",
        "reasoning": "logical",
        "verbal": "verbal",
        "sql": "sql",
        "cs": "cs_fundamentals",
    }
    qtype = domain_to_type.get(pat.domain)
    filters: Dict[str, Any] = {}
    if qtype:
        filters["type"] = qtype
    # Try to map sub-pattern to topic if it matches known topic names
    if pat.domain == "coding":
        # Map coding pattern_id suffix to question_store topic
        sub = pattern_id.split(".")[-1] if "." in pattern_id else pattern_id
        topic_map = {
            "arrays_hashing": "Arrays",
            "two_pointers": "Two Pointers",
            "sliding_window": "Sliding Window",
            "binary_search": "Binary Search",
            "strings": "Strings",
            "linked_list": "Linked Lists",
            "stack_queue": "Stacks & Queues",
            "trees": "Trees",
            "heaps": "Heaps",
            "graphs": "Graphs",
            "dp_1d": "Dynamic Programming",
            "dp_2d": "Dynamic Programming",
            "greedy": "Greedy",
            "intervals": "Intervals",
            "bit_manipulation": "Bit Manipulation",
            "recursion_backtracking": "Recursion & Backtracking",
            "sorting": "Sorting",
            "tries": "Tries",
            "union_find": "Union Find",
            "shortest_path": "Shortest Path",
        }
        topic = topic_map.get(sub)
        if topic:
            filters["topic"] = topic
    return filters


# ---------------------------------------------------------------------------
# Migration helper: unify Striver patterns from question_store
# ---------------------------------------------------------------------------

def get_striver_pattern_mapping() -> Dict[str, str]:
    """Return a mapping from legacy Striver pattern names to canonical pattern_ids.

    This helps migrate questions already tagged with Striver pattern names.
    """
    mapping = {
        "Arrays": "coding.arrays_hashing",
        "Two Pointers": "coding.two_pointers",
        "Sliding Window": "coding.sliding_window",
        "Binary Search": "coding.binary_search",
        "Strings": "coding.strings",
        "Linked Lists": "coding.linked_list",
        "Stacks & Queues": "coding.stack_queue",
        "Trees": "coding.trees",
        "Heaps": "coding.heaps",
        "Graphs": "coding.graphs",
        "BFS & DFS": "coding.graphs",
        "Union Find": "coding.union_find",
        "Shortest Path": "coding.shortest_path",
        "Tries": "coding.tries",
        "Dynamic Programming 1D": "coding.dp_1d",
        "Dynamic Programming 2D": "coding.dp_2d",
        "Dynamic Programming on Strings": "coding.dp_strings",
        "DP on Subsequences": "coding.dp_subsequences",
        "DP on Trees": "coding.dp_trees",
        "Greedy": "coding.greedy",
        "Intervals": "coding.intervals",
        "Bit Manipulation": "coding.bit_manipulation",
        "Math & Number Theory": "coding.math_number_theory",
        "Recursion & Backtracking": "coding.recursion_backtracking",
        "Sorting": "coding.sorting",
        "Searching": "coding.searching",
        "String Matching": "coding.string_matching",
        "Design / OOP": "coding.design_oop",
    }
    return mapping


def map_striver_pattern_to_canonical(striver_name: str) -> Optional[str]:
    """Map a legacy Striver pattern display name to canonical pattern_id."""
    return get_striver_pattern_mapping().get(striver_name)
