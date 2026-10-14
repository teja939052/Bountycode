#!/usr/bin/env python3
"""Verify evidence-based misconception diagnosis and reteach gating."""

import asyncio
from app.services.misconception_diagnosis import diagnose_misconception

def test_single_wrong_no_reteach():
    """Single wrong answer should NOT trigger reteach (low confidence)."""
    trace = [{"type": "predict_wrong", "data": {"answer": "50%"}}]
    result = diagnose_misconception(trace, "aptitude.percentages", ["apt_percent_base_confusion"])
    print(f"Single wrong: confidence={result['confidence']}, evidence={result['evidence_count']}")
    assert result["confidence"] < 0.7, "Single wrong should not trigger reteach"
    assert result["evidence_count"] == 1
    print("PASS: Single wrong does not trigger reteach")

def test_double_wrong_triggers_reteach():
    """Two wrong answers SHOULD trigger reteach (confidence >= 0.7)."""
    trace = [
        {"type": "predict_wrong", "data": {"answer": "50%"}},
        {"type": "predict_wrong", "data": {"answer": "100%"}},
    ]
    result = diagnose_misconception(trace, "aptitude.percentages", ["apt_percent_base_confusion"])
    print(f"Double wrong: confidence={result['confidence']}, evidence={result['evidence_count']}")
    assert result["confidence"] >= 0.7, "Double wrong should trigger reteach"
    assert result["evidence_count"] == 2
    print("PASS: Double wrong triggers reteach")

def test_triple_wrong_high_confidence():
    """Three wrong answers should have high confidence."""
    trace = [
        {"type": "predict_wrong", "data": {"answer": "50%"}},
        {"type": "predict_wrong", "data": {"answer": "100%"}},
        {"type": "predict_wrong", "data": {"answer": "200%"}},
    ]
    result = diagnose_misconception(trace, "aptitude.percentages", ["apt_percent_base_confusion"])
    print(f"Triple wrong: confidence={result['confidence']}, evidence={result['evidence_count']}")
    assert result["confidence"] >= 0.7
    assert result["evidence_count"] == 3
    print("PASS: Triple wrong has high confidence")

def test_correct_no_diagnosis():
    """Correct answer should not trigger diagnosis."""
    trace = [{"type": "predict_correct", "data": {"answer": "50"}}]
    result = diagnose_misconception(trace, "aptitude.percentages", ["apt_percent_base_confusion"])
    print(f"Correct: confidence={result['confidence']}, evidence={result['evidence_count']}")
    assert result["confidence"] == 0.0
    assert result["evidence_count"] == 0
    print("PASS: Correct answer does not trigger diagnosis")

def test_different_misconception_codes():
    """Test that different domains use correct codes."""
    # APTITUDE
    trace = [{"type": "predict_wrong", "data": {"answer": "ratio"}}]
    result = diagnose_misconception(trace, "aptitude.ratios", ["apt_ratio_interpretation_error"])
    assert result["misconception_code"] == "apt_ratio_interpretation_error"
    print("PASS: APTITUDE code works")
    
    # REASONING
    trace = [{"type": "predict_wrong", "data": {"answer": "assume"}}]
    result = diagnose_misconception(trace, "reasoning.relationships", ["reasoning_assumption_error"])
    assert result["misconception_code"] == "reasoning_assumption_error"
    print("PASS: REASONING code works")
    
    # VERBAL
    trace = [{"type": "predict_wrong", "data": {"answer": "grammar"}}]
    result = diagnose_misconception(trace, "verbal.grammar", ["verbal_grammar_agreement"])
    assert result["misconception_code"] == "verbal_grammar_agreement"
    print("PASS: VERBAL code works")
    
    # CODING
    trace = [{"type": "code_blocks_wrong", "data": {"answer": "loop"}}]
    result = diagnose_misconception(trace, "coding.loops", ["coding_loop_boundary_error"])
    assert result["misconception_code"] == "coding_loop_boundary_error"
    print("PASS: CODING code works")
    
    # SQL
    trace = [{"type": "predict_wrong", "data": {"answer": "join"}}]
    result = diagnose_misconception(trace, "sql.joins", ["sql_join_key_confusion"])
    assert result["misconception_code"] == "sql_join_key_confusion"
    print("PASS: SQL code works")
    
    # CS_CORE
    trace = [{"type": "predict_wrong", "data": {"answer": "process"}}]
    result = diagnose_misconception(trace, "cs_core.os", ["cs_core_process_thread_confusion"])
    assert result["misconception_code"] == "cs_core_process_thread_confusion"
    print("PASS: CS_CORE code works")

def test_mixed_correct_wrong():
    """Mixed correct/wrong should only count wrong ones."""
    trace = [
        {"type": "predict_correct", "data": {"answer": "50"}},
        {"type": "predict_wrong", "data": {"answer": "100%"}},
    ]
    result = diagnose_misconception(trace, "aptitude.percentages", ["apt_percent_base_confusion"])
    print(f"Mixed: confidence={result['confidence']}, evidence={result['evidence_count']}")
    assert result["evidence_count"] == 1
    assert result["confidence"] == 0.35
    print("PASS: Mixed correct/wrong counts only wrong")

if __name__ == "__main__":
    print("=" * 60)
    print("Testing evidence-based misconception diagnosis")
    print("=" * 60)
    
    test_single_wrong_no_reteach()
    print()
    test_double_wrong_triggers_reteach()
    print()
    test_triple_wrong_high_confidence()
    print()
    test_correct_no_diagnosis()
    print()
    test_different_misconception_codes()
    print()
    test_mixed_correct_wrong()
    print()
    
    print("=" * 60)
    print("All tests passed!")
    print("=" * 60)
