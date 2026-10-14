"""Domain-specific misconception libraries.

Each domain exposes:
  MISCONCEPTION_CODES: dict[str, dict]  — signature + reteach route
  CODES_BY_CONCEPT:   dict[str, list[str]] — which codes apply to each concept

These are consumed by:
  - lesson_orchestrator.py  (diagnose after each wrong/confused action)
  - action_trace_logger.py  (passes domain-appropriate codes)
"""

from __future__ import annotations

from typing import Any, Dict, List

# ═══════════════════════════════════════════════════════════════
# BEHAVIORAL
# ═══════════════════════════════════════════════════════════════

BEHAVIORAL_MISCONCEPTIONS: Dict[str, Dict[str, Any]] = {
    "missing_situation": {
        "keywords": [
            "project", "team", "company", "worked", "time", "when",
            "during", "at my", "in my", "while",
        ],
        "interaction_patterns": [
            "freeze_predict_wrong", "skip_manipulation",
        ],
        "reteach_route": "worked_example",
        "reteach_action": "show_situation_first",
    },
    "missing_task": {
        "keywords": [
            "role", "responsible", "tasked", "objective", "goal",
            "needed to", "had to", "my task",
        ],
        "interaction_patterns": [
            "freeze_predict_wrong", "skip_explain",
        ],
        "reteach_route": "worked_example",
        "reteach_action": "show_task_ownership",
    },
    "missing_action": {
        "keywords": [
            "built", "created", "implemented", "designed", "led",
            "managed", "developed", "analyzed", "optimized",
            "we did", "team did", "they did",
        ],
        "interaction_patterns": [
            "freeze_predict_wrong", "hint_requested_early",
        ],
        "reteach_route": "visual_state",
        "reteach_action": "highlight_i_statements",
    },
    "missing_result": {
        "keywords": [
            "result", "outcome", "improved", "increased", "reduced",
            "saved", "achieved", "delivered", "metric", "%",
        ],
        "interaction_patterns": [
            "freeze_predict_wrong", "state_manipulation_confused",
        ],
        "reteach_route": "worked_example",
        "reteach_action": "show_quantified_impact",
    },
    "vague_story": {
        "keywords": [
            "stuff", "things", "helped", "worked on", "involved",
            "various", "some", "many",
        ],
        "interaction_patterns": [
            "code_blocks_wrong", "predict_wrong",
        ],
        "reteach_route": "worked_example",
        "reteach_action": "decompose_into_star",
    },
    "team_not_self": {
        "keywords": [
            "we built", "we created", "team built", "we implemented",
            "our team", "we decided",
        ],
        "interaction_patterns": [
            "freeze_predict_wrong", "skip_manipulation",
        ],
        "reteach_route": "compare_worlds",
        "reteach_action": "highlight_i_vs_we",
    },
    "no_metrics": {
        "keywords": [
            "better", "faster", "improved", "successful", "good",
            "great", "effective",
        ],
        "interaction_patterns": [
            "time_travel_confused", "predict_wrong",
        ],
        "reteach_route": "worked_example",
        "reteach_action": "add_numbers_to_result",
    },
}

BEHAVIORAL_CODES_BY_CONCEPT: Dict[str, List[str]] = {
    "behavioral_fundamentals": [
        "missing_situation", "missing_task", "missing_action", "missing_result",
        "vague_story", "team_not_self", "no_metrics",
    ],
    "star_method": [
        "missing_situation", "missing_task", "missing_action", "missing_result",
    ],
    "behavioral_senior": [
        "vague_story", "team_not_self", "no_metrics",
    ],
}

# ═══════════════════════════════════════════════════════════════
# SYSTEM DESIGN
# ═══════════════════════════════════════════════════════════════

SYSTEM_DESIGN_MISCONCEPTIONS: Dict[str, Dict[str, Any]] = {
    "no_requirements": {
        "keywords": [
            "build", "create", "design", "system", "app",
            "without", "skip", "ignore", "assume",
        ],
        "interaction_patterns": [
            "freeze_predict_wrong", "skip_explain",
        ],
        "reteach_route": "worked_example",
        "reteach_action": "show_requirements_first",
    },
    "no_bottlenecks": {
        "keywords": [
            "fast", "simple", "direct", "straightforward",
            "no issue", "no problem", "works fine",
        ],
        "interaction_patterns": [
            "code_blocks_wrong", "predict_wrong",
        ],
        "reteach_route": "time_travel",
        "reteach_action": "show_load_accumulation",
    },
    "no_tradeoffs": {
        "keywords": [
            "perfect", "best", "always", "never",
            "no downside", "no compromise",
        ],
        "interaction_patterns": [
            "time_travel_confused", "first_wrong_moment_middle",
        ],
        "reteach_route": "compare_worlds",
        "reteach_action": "highlight_cap_theorem",
    },
    "single_point_failure": {
        "keywords": [
            "one server", "single", "standalone", "monolith",
            "no backup", "no replica",
        ],
        "interaction_patterns": [
            "freeze_predict_wrong", "state_manipulation_confused",
        ],
        "reteach_route": "bug_surgery",
        "reteach_action": "show_spof_failure",
    },
    "no_scalability": {
        "keywords": [
            "small", "simple", "few users", "not many",
            "no scale", "current only",
        ],
        "interaction_patterns": [
            "skip_explain", "predict_wrong",
        ],
        "reteach_route": "time_travel",
        "reteach_action": "show_growth_curve",
    },
    "database_monolith": {
        "keywords": [
            "one database", "single db", "all in one",
            "sql only", "nosql only",
        ],
        "interaction_patterns": [
            "code_blocks_wrong", "first_wrong_moment_middle",
        ],
        "reteach_route": "compare_worlds",
        "reteach_action": "show_data_partitioning",
    },
    "no_caching": {
        "keywords": [
            "direct", "always read", "always write",
            "no cache", "cache not needed",
        ],
        "interaction_patterns": [
            "freeze_predict_wrong", "hint_requested_early",
        ],
        "reteach_route": "bug_surgery",
        "reteach_action": "show_read_amplification",
    },
    "no_cdn": {
        "keywords": [
            "direct", "same server", "origin server",
            "no cdn", "cdn not needed",
        ],
        "interaction_patterns": [
            "skip_explain", "predict_wrong",
        ],
        "reteach_route": "worked_example",
        "reteach_action": "show_latency_map",
    },
}

SYSTEM_DESIGN_CODES_BY_CONCEPT: Dict[str, List[str]] = {
    "system_design_fundamentals": [
        "no_requirements", "no_bottlenecks", "no_tradeoffs",
        "single_point_failure", "no_scalability",
    ],
    "distributed_systems": [
        "single_point_failure", "no_scalability", "no_caching", "no_cdn",
    ],
    "data_systems": [
        "database_monolith", "no_caching", "no_scalability",
    ],
    "scalability": [
        "no_scalability", "no_bottlenecks", "no_caching",
    ],
}

# ═══════════════════════════════════════════════════════════════
# APTITUDE
# ═══════════════════════════════════════════════════════════════

APTITUDE_MISCONCEPTIONS: Dict[str, Dict[str, Any]] = {
    "apt_percent_base_confusion": {
        "keywords": ["percent", "%", "base", "of", "increase", "decrease"],
        "interaction_patterns": ["freeze_predict_wrong", "skip_explain"],
        "reteach_route": "worked_example",
        "reteach_action": "show_base_vs_change",
    },
    "apt_percentage_point_confusion": {
        "keywords": ["percentage point", "percent", "absolute", "relative"],
        "interaction_patterns": ["predict_wrong", "code_blocks_wrong"],
        "reteach_route": "compare_worlds",
        "reteach_action": "highlight_percent_vs_percentage_point",
    },
    "apt_ratio_interpretation_error": {
        "keywords": ["ratio", "proportion", "fraction", "part", "whole"],
        "interaction_patterns": ["freeze_predict_wrong", "state_manipulation_confused"],
        "reteach_route": "visual_state",
        "reteach_action": "show_ratio_as_division",
    },
    "apt_average_denominator_error": {
        "keywords": ["average", "mean", "total", "sum", "divided by"],
        "interaction_patterns": ["predict_wrong", "skip_explain"],
        "reteach_route": "worked_example",
        "reteach_action": "show_weighted_vs_simple_average",
    },
    "apt_rate_work_relationship": {
        "keywords": ["rate", "work", "time", "speed", "efficiency"],
        "interaction_patterns": ["time_travel_confused", "predict_wrong"],
        "reteach_route": "time_travel",
        "reteach_action": "show_rate_time_work_formula",
    },
    "apt_unit_conversion_error": {
        "keywords": ["unit", "convert", "km", "miles", "kg", "pounds"],
        "interaction_patterns": ["code_blocks_wrong", "predict_wrong"],
        "reteach_route": "worked_example",
        "reteach_action": "show_conversion_factors",
    },
}

APTITUDE_CODES_BY_CONCEPT: Dict[str, List[str]] = {
    "aptitude.percentages": [
        "apt_percent_base_confusion", "apt_percentage_point_confusion",
    ],
    "aptitude.ratios": [
        "apt_ratio_interpretation_error", "apt_average_denominator_error",
    ],
    "aptitude.rates": [
        "apt_rate_work_relationship", "apt_unit_conversion_error",
    ],
}

# ═══════════════════════════════════════════════════════════════
# REASONING
# ═══════════════════════════════════════════════════════════════

REASONING_MISCONCEPTIONS: Dict[str, Dict[str, Any]] = {
    "reasoning_relationship_chain_error": {
        "keywords": ["relationship", "chain", "family", "related", "connected"],
        "interaction_patterns": ["freeze_predict_wrong", "skip_explain"],
        "reteach_route": "worked_example",
        "reteach_action": "show_relationship_chain",
    },
    "reasoning_assumption_error": {
        "keywords": ["assume", "assumption", "always", "never", "must"],
        "interaction_patterns": ["predict_wrong", "code_blocks_wrong"],
        "reteach_route": "compare_worlds",
        "reteach_action": "highlight_assumption_vs_fact",
    },
    "reasoning_ordering_error": {
        "keywords": ["order", "sequence", "arrange", "before", "after"],
        "interaction_patterns": ["time_travel_confused", "predict_wrong"],
        "reteach_route": "time_travel",
        "reteach_action": "show_ordering_constraints",
    },
    "reasoning_constraint_omission": {
        "keywords": ["constraint", "condition", "only if", "unless", "except"],
        "interaction_patterns": ["skip_explain", "predict_wrong"],
        "reteach_route": "bug_surgery",
        "reteach_action": "show_missing_constraint",
    },
    "reasoning_sequence_inference": {
        "keywords": ["infer", "deduce", "conclude", "therefore", "implies"],
        "interaction_patterns": ["freeze_predict_wrong", "state_manipulation_confused"],
        "reteach_route": "visual_state",
        "reteach_action": "show_inference_chain",
    },
    "reasoning_case_elimination": {
        "keywords": ["eliminate", "exclude", "remove", "discard", "filter"],
        "interaction_patterns": ["code_blocks_wrong", "first_wrong_moment_middle"],
        "reteach_route": "compare_worlds",
        "reteach_action": "show_case_by_case_analysis",
    },
}

REASONING_CODES_BY_CONCEPT: Dict[str, List[str]] = {
    "reasoning.relationships": [
        "reasoning_relationship_chain_error", "reasoning_assumption_error",
    ],
    "reasoning.ordering": [
        "reasoning_ordering_error", "reasoning_constraint_omission",
    ],
    "reasoning.inference": [
        "reasoning_sequence_inference", "reasoning_case_elimination",
    ],
}

# ═══════════════════════════════════════════════════════════════
# VERBAL
# ═══════════════════════════════════════════════════════════════

VERBAL_MISCONCEPTIONS: Dict[str, Dict[str, Any]] = {
    "verbal_tone_mismatch": {
        "keywords": ["tone", "formal", "informal", "polite", "rude", "attitude"],
        "interaction_patterns": ["freeze_predict_wrong", "skip_explain"],
        "reteach_route": "worked_example",
        "reteach_action": "show_tone_markers",
    },
    "verbal_grammar_agreement": {
        "keywords": ["subject", "verb", "agreement", "singular", "plural"],
        "interaction_patterns": ["predict_wrong", "code_blocks_wrong"],
        "reteach_route": "compare_worlds",
        "reteach_action": "highlight_subject_verb_agreement",
    },
    "verbal_tense_misuse": {
        "keywords": ["tense", "past", "present", "future", "perfect"],
        "interaction_patterns": ["time_travel_confused", "predict_wrong"],
        "reteach_route": "time_travel",
        "reteach_action": "show_tense_timeline",
    },
    "verbal_inference_error": {
        "keywords": ["infer", "imply", "suggest", "conclude", "passage"],
        "interaction_patterns": ["freeze_predict_wrong", "state_manipulation_confused"],
        "reteach_route": "visual_state",
        "reteach_action": "show_text_evidence_vs_inference",
    },
    "verbal_vocabulary_context": {
        "keywords": ["meaning", "context", "synonym", "antonym", "word"],
        "interaction_patterns": ["code_blocks_wrong", "first_wrong_moment_middle"],
        "reteach_route": "compare_worlds",
        "reteach_action": "show_contextual_meaning",
    },
}

VERBAL_CODES_BY_CONCEPT: Dict[str, List[str]] = {
    "verbal.grammar": [
        "verbal_tone_mismatch", "verbal_grammar_agreement", "verbal_tense_misuse",
    ],
    "verbal.comprehension": [
        "verbal_inference_error", "verbal_vocabulary_context",
    ],
}

# ═══════════════════════════════════════════════════════════════
# SQL
# ═══════════════════════════════════════════════════════════════

SQL_MISCONCEPTIONS: Dict[str, Dict[str, Any]] = {
    "sql_join_key_confusion": {
        "keywords": ["join", "key", "foreign", "primary", "match"],
        "interaction_patterns": ["freeze_predict_wrong", "skip_explain"],
        "reteach_route": "worked_example",
        "reteach_action": "show_join_keys_visual",
    },
    "sql_filtering_stage_confusion": {
        "keywords": ["where", "having", "filter", "group", "before", "after"],
        "interaction_patterns": ["predict_wrong", "code_blocks_wrong"],
        "reteach_route": "time_travel",
        "reteach_action": "show_filtering_stage_order",
    },
    "sql_grouping_grain_error": {
        "keywords": ["group by", "aggregate", "row", "column", "granularity"],
        "interaction_patterns": ["state_manipulation_confused", "predict_wrong"],
        "reteach_route": "visual_state",
        "reteach_action": "show_grouping_granularity",
    },
    "sql_null_semantics_error": {
        "keywords": ["null", "none", "empty", "unknown", "missing"],
        "interaction_patterns": ["freeze_predict_wrong", "compare_worlds_confused"],
        "reteach_route": "compare_worlds",
        "reteach_action": "highlight_null_vs_empty",
    },
    "sql_aggregation_granule_error": {
        "keywords": ["sum", "count", "avg", "min", "max", "aggregate"],
        "interaction_patterns": ["predict_wrong", "skip_explain"],
        "reteach_route": "worked_example",
        "reteach_action": "show_aggregation_granule",
    },
}

SQL_CODES_BY_CONCEPT: Dict[str, List[str]] = {
    "sql.joins": [
        "sql_join_key_confusion", "sql_filtering_stage_confusion",
    ],
    "sql.grouping": [
        "sql_grouping_grain_error", "sql_aggregation_granule_error",
    ],
    "sql.nulls": [
        "sql_null_semantics_error",
    ],
}

# ═══════════════════════════════════════════════════════════════
# CS_CORE
# ═══════════════════════════════════════════════════════════════

CS_CORE_MISCONCEPTIONS: Dict[str, Dict[str, Any]] = {
    "cs_core_process_thread_confusion": {
        "keywords": ["process", "thread", "concurrent", "parallel", "multitask"],
        "interaction_patterns": ["freeze_predict_wrong", "skip_manipulation"],
        "reteach_route": "visual_state",
        "reteach_action": "show_process_vs_thread",
    },
    "cs_core_stack_heap_misconception": {
        "keywords": ["stack", "heap", "memory", "allocation", "pointer"],
        "interaction_patterns": ["freeze_predict_wrong", "hint_requested_early"],
        "reteach_route": "memory_board",
        "reteach_action": "show_stack_heap_visual",
    },
    "cs_core_normalization_misconception": {
        "keywords": ["normalize", "1nf", "2nf", "3nf", "redundant"],
        "interaction_patterns": ["code_blocks_wrong", "first_wrong_moment_middle"],
        "reteach_route": "bug_surgery",
        "reteach_action": "show_normalization_steps",
    },
    "cs_core_network_layer_confusion": {
        "keywords": ["layer", "osi", "tcp", "ip", "network", "protocol"],
        "interaction_patterns": ["time_travel_confused", "predict_wrong"],
        "reteach_route": "time_travel",
        "reteach_action": "show_layer_responsibilities",
    },
    "cs_core_oop_relationship_misconception": {
        "keywords": ["inheritance", "polymorphism", "encapsulation", "abstraction", "is-a", "has-a"],
        "interaction_patterns": ["freeze_predict_wrong", "state_manipulation_confused"],
        "reteach_route": "compare_worlds",
        "reteach_action": "show_oop_relationships",
    },
}

CS_CORE_CODES_BY_CONCEPT: Dict[str, List[str]] = {
    "cs_core.os": [
        "cs_core_process_thread_confusion", "cs_core_stack_heap_misconception",
    ],
    "cs_core.dbms": [
        "cs_core_normalization_misconception",
    ],
    "cs_core.networks": [
        "cs_core_network_layer_confusion",
    ],
    "cs_core.oops": [
        "cs_core_oop_relationship_misconception",
    ],
}

# ═══════════════════════════════════════════════════════════════
# SERVICE-PLACEMENT CODING  (replaces generic coding misconceptions)
# ═══════════════════════════════════════════════════════════════

CODING_MISCONCEPTIONS: Dict[str, Dict[str, Any]] = {
    "coding_state_trace_error": {
        "keywords": ["state", "variable", "value", "change", "after", "before"],
        "interaction_patterns": ["freeze_predict_wrong", "state_manipulation_confused"],
        "reteach_route": "visual_state",
        "reteach_action": "trace_state_step_by_step",
    },
    "coding_loop_boundary_error": {
        "keywords": ["loop", "boundary", "off by one", "index", "range"],
        "interaction_patterns": ["code_blocks_wrong", "first_wrong_moment_middle"],
        "reteach_route": "bug_surgery",
        "reteach_action": "show_loop_boundary",
    },
    "coding_condition_boundary_error": {
        "keywords": ["if", "else", "condition", "boundary", "edge case"],
        "interaction_patterns": ["predict_wrong", "freeze_predict_wrong"],
        "reteach_route": "compare_worlds",
        "reteach_action": "show_condition_boundary",
    },
    "coding_array_index_error": {
        "keywords": ["array", "index", "out of bounds", "negative", "access"],
        "interaction_patterns": ["code_blocks_wrong", "predict_wrong"],
        "reteach_route": "bug_surgery",
        "reteach_action": "show_array_index_visual",
    },
    "coding_complexity_misconception": {
        "keywords": ["complexity", "big o", "time", "space", "efficient"],
        "interaction_patterns": ["skip_explain", "predict_wrong"],
        "reteach_route": "worked_example",
        "reteach_action": "show_complexity_comparison",
    },
}

CODING_CODES_BY_CONCEPT: Dict[str, List[str]] = {
    "coding.state_trace": [
        "coding_state_trace_error",
    ],
    "coding.loops": [
        "coding_loop_boundary_error",
    ],
    "coding.conditions": [
        "coding_condition_boundary_error",
    ],
    "coding.arrays": [
        "coding_array_index_error",
    ],
    "coding.complexity": [
        "coding_complexity_misconception",
    ],
}

# ═══════════════════════════════════════════════════════════════
# ROUTE MAP
# ═══════════════════════════════════════════════════════════════

RETEACH_ROUTE_MAP: Dict[str, Dict[str, Any]] = {
    "visual_state": {
        "mode": "interactions",
        "interactions": ["state_manipulation", "memory_board", "freeze_predict"],
        "teacher_focus": "Make the invisible state visible and tangible",
    },
    "worked_example": {
        "mode": "explain",
        "interactions": ["explain", "show", "fill_missing"],
        "teacher_focus": "Show a complete worked example before independent practice",
    },
    "time_travel": {
        "mode": "interactions",
        "interactions": ["time_travel", "freeze_predict", "first_wrong_moment"],
        "teacher_focus": "Step through execution one line at a time",
    },
    "bug_surgery": {
        "mode": "interactions",
        "interactions": ["bug_surgery", "compare_worlds", "first_wrong_moment"],
        "teacher_focus": "Show the exact consequence of the misconception",
    },
    "compare_worlds": {
        "mode": "interactions",
        "interactions": ["compare_worlds", "counterexample_builder"],
        "teacher_focus": "Highlight the difference between correct and incorrect mental model",
    },
}


def get_domain_library(domain: str) -> Dict[str, Any]:
    """Return the misconception library for a domain."""
    if domain == "coding":
        return {
            "codes": CODING_MISCONCEPTIONS,
            "by_concept": CODING_CODES_BY_CONCEPT,
        }
    if domain == "behavioral":
        return {
            "codes": BEHAVIORAL_MISCONCEPTIONS,
            "by_concept": BEHAVIORAL_CODES_BY_CONCEPT,
        }
    if domain == "system_design":
        return {
            "codes": SYSTEM_DESIGN_MISCONCEPTIONS,
            "by_concept": SYSTEM_DESIGN_CODES_BY_CONCEPT,
        }
    if domain == "aptitude":
        return {
            "codes": APTITUDE_MISCONCEPTIONS,
            "by_concept": APTITUDE_CODES_BY_CONCEPT,
        }
    if domain == "reasoning":
        return {
            "codes": REASONING_MISCONCEPTIONS,
            "by_concept": REASONING_CODES_BY_CONCEPT,
        }
    if domain == "verbal":
        return {
            "codes": VERBAL_MISCONCEPTIONS,
            "by_concept": VERBAL_CODES_BY_CONCEPT,
        }
    if domain == "sql":
        return {
            "codes": SQL_MISCONCEPTIONS,
            "by_concept": SQL_CODES_BY_CONCEPT,
        }
    if domain == "cs_core":
        return {
            "codes": CS_CORE_MISCONCEPTIONS,
            "by_concept": CS_CORE_CODES_BY_CONCEPT,
        }
    return {"codes": {}, "by_concept": {}}


def get_reteach_plan(misconception_code: str) -> Dict[str, Any]:
    """Get the reteach plan for a diagnosed misconception code."""
    for library in [
        CODING_MISCONCEPTIONS,
        BEHAVIORAL_MISCONCEPTIONS,
        SYSTEM_DESIGN_MISCONCEPTIONS,
        APTITUDE_MISCONCEPTIONS,
        REASONING_MISCONCEPTIONS,
        VERBAL_MISCONCEPTIONS,
        SQL_MISCONCEPTIONS,
        CS_CORE_MISCONCEPTIONS,
    ]:
        sig = library.get(misconception_code)
        if sig:
            route = sig.get("reteach_route", "visual_state")
            return RETEACH_ROUTE_MAP.get(route, RETEACH_ROUTE_MAP["visual_state"])
    return RETEACH_ROUTE_MAP["visual_state"]
