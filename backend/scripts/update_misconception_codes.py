#!/usr/bin/env python3
"""Update all mission pack misconception codes to service-placement focused codes."""

import json
import os
from pathlib import Path

# Mapping of old generic codes to new service-placement codes
CODE_MAPPING = {
    # APTITUDE
    "percentage_vs_percentage_points": "apt_percentage_point_confusion",
    "additive_percentage": "apt_percent_base_confusion",
    "ratio_as_fraction": "apt_ratio_interpretation_error",
    "proportion_cross_misuse": "apt_ratio_interpretation_error",
    "average_ignores_count": "apt_average_denominator_error",
    "additive_time": "apt_rate_work_relationship",
    "average_speed_arithmetic_mean": "apt_rate_work_relationship",
    "relative_speed_wrong_sign": "apt_rate_work_relationship",
    "wrong_base_for_percent": "apt_percent_base_confusion",
    "discount_then_tax_same_base": "apt_percent_base_confusion",
    "probability_greater_than_one": "apt_rate_work_relationship",
    "ignore_exclusive_events": "apt_rate_work_relationship",
    "permutation_as_combination": "apt_ratio_interpretation_error",
    "double_count": "apt_ratio_interpretation_error",
    "log_as_root": "apt_rate_work_relationship",
    "base_confusion": "apt_percent_base_confusion",
    "compound_as_simple": "apt_rate_work_relationship",
    "wrong_time_base": "apt_rate_work_relationship",
    "wrong_reference_value": "apt_percent_base_confusion",
    "ignore_unit": "apt_unit_conversion_error",
    "gender_confusion": "apt_ratio_interpretation_error",
    
    # REASONING
    "assume_fact": "reasoning_assumption_error",
    "reverse_direction": "reasoning_ordering_error",
    "single_pattern_assumption": "reasoning_assumption_error",
    "skip_obvious_operation": "reasoning_sequence_inference",
    "fix_first_person": "reasoning_ordering_error",
    "ignore_relative_clues": "reasoning_constraint_omission",
    "assume_minimum": "reasoning_assumption_error",
    "ignore_constraint": "reasoning_constraint_omission",
    "left_right_mirror": "reasoning_ordering_error",
    "north_south_confusion": "reasoning_ordering_error",
    "solve_instead_of_check": "reasoning_sequence_inference",
    "ignore_redundancy": "reasoning_constraint_omission",
    "fixed_alphabet_shift": "reasoning_sequence_inference",
    "reverse_word_misread": "reasoning_ordering_error",
    
    # VERBAL
    "context_ignored": "verbal_vocabulary_context",
    "spelling_sound_alike": "verbal_vocabulary_context",
    "subject_verb_agreement": "verbal_grammar_agreement",
    "tense_sequence": "verbal_tense_misuse",
    "speed_over_accuracy": "verbal_inference_error",
    "outside_knowledge": "verbal_inference_error",
    "first_sentence_trap": "verbal_inference_error",
    "ignore_link_words": "verbal_vocabulary_context",
    "literal_interpretation": "verbal_vocabulary_context",
    "context_mismatch": "verbal_vocabulary_context",
    "tense_mixing": "verbal_tense_misuse",
    "voice_confusion": "verbal_grammar_agreement",
    "word_fit_without_context": "verbal_vocabulary_context",
    "ignore_tense_flow": "verbal_tense_misuse",
    
    # CODING
    "assignment_as_equality": "coding_state_trace_error",
    "print_changes_variable": "coding_state_trace_error",
    "print_returns_value": "coding_state_trace_error",
    "source_is_result": "coding_state_trace_error",
    "string_mutation": "coding_state_trace_error",
    "off_by_one_substring": "coding_array_index_error",
    "no_base_case": "coding_loop_boundary_error",
    "recursion_always_better": "coding_complexity_misconception",
    "pointer_is_value": "coding_state_trace_error",
    "reference_is_pointer": "coding_state_trace_error",
    "off_by_one": "coding_loop_boundary_error",
    "loop_else_confusion": "coding_condition_boundary_error",
    "print_instead_of_return": "coding_state_trace_error",
    "parameter_mutation": "coding_state_trace_error",
    "order_doesnt_matter": "coding_condition_boundary_error",
    "index_from_one": "coding_array_index_error",
    "slice_inclusive": "coding_array_index_error",
    
    # CS_CORE / SQL
    "join_returns_union": "sql_join_key_confusion",
    "testing_only_manual": "cs_core_normalization_misconception",
    "waterfall_only": "cs_core_process_thread_confusion",
    "kernel_is_os": "cs_core_process_thread_confusion",
    "threads_always_faster": "cs_core_process_thread_confusion",
    "class_is_object": "cs_core_oop_relationship_misconception",
    "inheritance_is_copy": "cs_core_oop_relationship_misconception",
    "osi_tcpip_confusion": "cs_core_network_layer_confusion",
    "udp_reliable": "cs_core_network_layer_confusion",
    "primary_key_duplicate": "cs_core_normalization_misconception",
    "normalization_optional": "cs_core_normalization_misconception",
}

def update_misconception_codes(pack_dir: Path):
    updated = []
    for json_file in pack_dir.glob("*.json"):
        if json_file.name.startswith("company."):
            continue
            
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        misconceptions = data.get("misconceptions", [])
        changed = False
        for m in misconceptions:
            old_code = m.get("code", "")
            if old_code in CODE_MAPPING:
                new_code = CODE_MAPPING[old_code]
                m["code"] = new_code
                changed = True
                print(f"  {json_file.name}: {old_code} -> {new_code}")
        
        if changed:
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            updated.append(json_file.name)
    
    return updated

def update_company_variants(pack_dir: Path):
    updated = []
    for json_file in pack_dir.glob("company.*.json"):
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        company_variants = data.get("company_variants", [])
        if not company_variants:
            company = data.get("id", "").replace("company.", "")
            data["company_variants"] = [
                {
                    "company": company,
                    "role": "sde",
                    "difficulty": "medium",
                    "proof_questions": []
                }
            ]
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            updated.append(json_file.name)
            print(f"  {json_file.name}: added empty company_variants")
    
    return updated

if __name__ == "__main__":
    pack_dir = Path("D:/Project-Fremen/backend/app/content/mission_packs")
    
    print("Updating misconception codes...")
    updated = update_misconception_codes(pack_dir)
    print(f"Updated {len(updated)} files")
    
    print("\nUpdating company variants...")
    updated_companies = update_company_variants(pack_dir)
    print(f"Updated {len(updated_companies)} company files")
    
    print("\nDone!")
