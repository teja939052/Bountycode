"""Regression tests for the verification harness and ground-truth gate.

Proves, deterministically:
  1. _values_equal compares string outputs against list expectations
     (stdin-wrapper class, e.g. pp-* stdout strings).
  2. invoke_conventions rescues arity-1 raw-input wrappers without
     loosening the gate (stubs still fail downstream exact-match).
  3. ground_truth_status confirms against the real platform oracle,
     mismatches on contradiction, and stays neutral without a source.
  4. intake_lint rejects literal-return stubs and formatter-as-solution
     filler while accepting genuine solutions and list-style MCQs.
  5. The tranche ground_truth gate passes neutral items and fails only
     on genuine oracle disagreement.
"""
import copy


def test_values_equal_string_vs_list():
    from app.services.auto_verify import _values_equal
    assert _values_equal("[[], [1]]", "[[],[1]]") is True
    assert _values_equal("[[], [2]]", "[[],[1]]") is False
    assert _values_equal("hello", "world") is False


def test_invoke_conventions_raw_wrapper():
    from app.services.auto_verify import invoke_conventions, _fn_arity
    src = ("def solve(raw):\n"
           "    import ast\n"
           "    nums, target = raw.strip().split(chr(10))\n"
           "    nums = ast.literal_eval(nums)\n"
           "    target = int(target)\n"
           "    seen = {}\n"
           "    for i, n in enumerate(nums):\n"
           "        if target - n in seen:\n"
           "            return [seen[target - n], i]\n"
           "        seen[n] = i\n"
           "    return []\n")
    ns: dict = {}
    exec(src, ns)
    f = ns["solve"]
    assert _fn_arity(f) == 1
    ok, actual, _err = invoke_conventions(f, [[[2, 7, 11, 15], 9]],
                                          "[2,7,11,15]\n9", 1)
    assert ok and list(actual) == [0, 1]


def test_invoke_conventions_stub_still_fails_downstream():
    from app.services.auto_verify import (
        invoke_conventions, _fn_arity, _values_equal,
    )
    ns: dict = {}
    exec("def largest(nums):\n    return 0\n", ns)
    f = ns["largest"]
    ok, actual, _err = invoke_conventions(f, [[1, 2, 3]], "[1,2,3]", 1)
    assert ok is True  # invocation works; the GATE must still reject it
    assert _values_equal(actual, "[1]") is False


def test_ground_truth_oracle_confirmed_and_mismatch():
    from app.services.ground_truth import ground_truth_status
    good = {
        "id": "t-reverse-string", "type": "coding",
        "question": "Reverse String",
        "solution": {"code": "def reverse_string(s):\n    return s[::-1]\n"},
    }
    res = ground_truth_status(good)
    assert res["state"] == "confirmed", res
    bad = copy.deepcopy(good)
    bad["solution"] = {"code": "def reverse_string(s):\n    return s\n"}
    res = ground_truth_status(bad)
    assert res["state"] == "mismatch", res


def test_ground_truth_neutral_without_source():
    from app.services.ground_truth import ground_truth_status
    item = {
        "id": "t-no-source", "type": "coding",
        "question": "Definitely Not A Real Bank Title Zzz",
        "solution": {"code": "def f(x):\n    return x\n"},
        "test_cases": [{"input": "1", "output": "1"}],
    }
    res = ground_truth_status(item)
    assert res["state"] == "no_independent_source", res


def test_dual_solution_agreement_and_disagreement():
    from app.services.ground_truth import dual_solution_check
    code_a = "def add(a, b):\n    return a + b\n"
    code_b = "def add(a, b):\n    return b + a\n"
    code_c = "def add(a, b):\n    return a - b\n"
    tcs = [{"input": "2\n3", "output": "5"}]
    base = {"solution": {"code": code_a}, "test_cases": tcs}
    assert dual_solution_check({**base, "verification_solution": {"code": code_b}})["state"] == "confirmed"
    assert dual_solution_check({**base, "verification_solution": {"code": code_c}})["state"] == "mismatch"
    assert dual_solution_check(base)["state"] == "no_independent_source"


def test_intake_lint_rejects_stubs_accepts_real():
    from app.services.intake_lint import lint_question
    stub = {"type": "coding", "question": "Largest",
            "solution": {"code": "def largest(nums):\n    return 0\n"},
            "test_cases": [{"input": "[1]", "output": "0"}]}
    assert lint_question(stub)["verdict"] == "rejected"
    fmt = {"type": "coding", "question": "Two Sum",
           "solution": {"code": "def fmt(x):\n    return str(x)\n"},
           "test_cases": [{"input": "1", "output": "1"}]}
    assert lint_question(fmt)["verdict"] == "rejected"
    real = {"type": "coding", "question": "Two Sum",
            "solution": {"code": "def two_sum(nums, target):\n    seen = {}\n    for i, n in enumerate(nums):\n        if target - n in seen:\n            return [seen[target - n], i]\n        seen[n] = i\n    return []\n"},
            "test_cases": [{"input": "[2,7]\n9", "output": "[0, 1]"}]}
    assert lint_question(real)["verdict"] in ("pass", "needs_work")
    mcq = {"type": "cs_fundamentals", "question": "LIFO?",
           "options": ["Stack", "Queue", "Array", "Map"],
           "correct_answer": "Stack", "correct_index": 0}
    assert lint_question(mcq)["verdict"] in ("pass", "needs_work")


def test_tranche_ground_truth_gate_neutral_pass_mismatch_fail():
    import sys
    sys.path.insert(0, "scripts")
    from auto_promote import gate_ground_truth
    neutral = {"id": "x", "type": "coding", "question": "No Oracle Here Zzz",
               "solution": {"code": "def f(x):\n    return x\n"}}
    ok, _why = gate_ground_truth(neutral)
    assert ok is True
    bad = {"id": "y", "type": "coding", "question": "Reverse String",
           "solution": {"code": "def reverse_string(s):\n    return s\n"}}
    ok, _why = gate_ground_truth(bad)
    assert ok is False
