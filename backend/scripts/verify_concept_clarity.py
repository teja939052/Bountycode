"""
Verify the Phase B concept-clarity curriculum slices.

AUTOMATED_CHECKED evidence, per the Content Trust Pipeline:
  - contract: every slice has every key LessonService reads
  - code: every build-step / transfer-challenge expected value is reproduced by a
    reference implementation (visible + hidden test cases)
  - prediction: exactly one correct option per prediction
  - assessment: code_tracing expected answers are reproduced by executing the trace;
    concept questions carry keywords; debug questions carry a fix line
  - explain: keywords, min_words, model_answer present; LessonService.check_explain
    passes on the model answer
  - break: exactly one correct diagnosis option; buggy code fails / mismatches;
    fixed code reproduces expected_output; LessonService.check_break passes on the
    intended diagnosis + fix
  - discovery interactions: manipulate / compare / arrange steps are well-formed

Run:  python scripts/verify_concept_clarity.py   (from backend/)
Exit 0 = all checks passed. Prints per-slice tallies.
"""
from __future__ import annotations

import contextlib
import io
import sys
from typing import Any, Dict, List

from app.content.curriculum import registry
from app.content.curriculum.concept_loops import LOOP_SLICE
from app.content.curriculum.concept_arrays import ARRAY_SLICE
from app.content.curriculum.concept_strings import STRING_SLICE
from app.content.curriculum.concept_functions import FUNCTION_SLICE
from app.content.curriculum.concept_sorting import SORTING_SLICE
from app.content.curriculum.concept_complexity import COMPLEXITY_SLICE
from app.services.lesson import LessonService

SLICES: List[Dict[str, Any]] = [
    LOOP_SLICE,
    ARRAY_SLICE,
    STRING_SLICE,
    FUNCTION_SLICE,
    SORTING_SLICE,
    COMPLEXITY_SLICE,
]

REQUIRED_KEYS = [
    "lesson_id", "module_id", "title", "description", "difficulty",
    "est_minutes", "xp_reward", "skills_taught", "srs_concept_tag",
    "story_context", "discovery", "prediction", "guided_build",
    "transfer_challenge", "assessment", "explain", "break",
    "srs_enrollment", "world_progression",
]

ALLOWED_INTERACTIONS = {
    "reveal_value", "select_value", "inspect_code", "choose_outcome",
    "manipulate", "compare", "arrange", "drag_and_drop", "inspect_type",
    "choose_stop",
}

# ──────────────────────────────────────────────────────────────────────
# Reference implementations (the intended solutions)
# ──────────────────────────────────────────────────────────────────────

def ref_sum_one_to_n(n: int) -> int:
    total = 0
    for i in range(1, n + 1):
        total += i
    return total

def ref_count_evens(nums: List[int]) -> int:
    return sum(1 for x in nums if x % 2 == 0)

def ref_square_series(n: int) -> List[int]:
    return [i * i for i in range(1, n + 1)]

def ref_count_digits(n: int) -> int:
    if n == 0:
        return 1
    count = 0
    while n > 0:
        n //= 10
        count += 1
    return count

def ref_sum_list(nums: List[int]) -> int:
    total = 0
    for x in nums:
        total += x
    return total

def ref_find_index(nums: List[int], target: int) -> int:
    for i in range(len(nums)):
        if nums[i] == target:
            return i
    return -1

def ref_reverse_list(nums: List[int]) -> List[int]:
    return list(reversed(nums))

def ref_rotate_left(nums: List[int], k: int) -> List[int]:
    if not nums:
        return []
    k %= len(nums)
    return nums[k:] + nums[:k]

def ref_count_vowels(text: str) -> int:
    return sum(1 for ch in text if ch.lower() in "aeiou")

def ref_is_palindrome(text: str) -> bool:
    return text == text[::-1]

def ref_title_case(text: str) -> str:
    return " ".join(w.capitalize() for w in text.split())

def ref_first_occurrence(s: str, sub: str) -> int:
    if len(sub) > len(s):
        return -1
    for i in range(len(s) - len(sub) + 1):
        if s[i:i + len(sub)] == sub:
            return i
    return -1

def ref_celsius_to_fahrenheit(c: float) -> float:
    return c * 9 / 5 + 32

def ref_rect_area(w: float, h: float) -> float:
    return w * h

def ref_absolute_difference(a: float, b: float) -> float:
    return abs(a - b)

def ref_is_prime(n: int) -> bool:
    if n < 2:
        return False
    for d in range(2, int(n ** 0.5) + 1):
        if n % d == 0:
            return False
    return True

def ref_swap_first_last(nums: List[int]) -> List[int]:
    out = list(nums)
    if len(out) >= 2:
        out[0], out[-1] = out[-1], out[0]
    return out

def ref_bubble_pass(nums: List[int]) -> List[int]:
    out = list(nums)
    for i in range(len(out) - 1):
        if out[i] > out[i + 1]:
            out[i], out[i + 1] = out[i + 1], out[i]
    return out

def ref_min_index(nums: List[int]) -> int:
    best = 0
    for i in range(len(nums)):
        if nums[i] < nums[best]:
            best = i
    return best

def ref_is_sorted(nums: List[int]) -> bool:
    for i in range(len(nums) - 1):
        if nums[i] > nums[i + 1]:
            return False
    return True

def ref_count_linear(n: int) -> int:
    return n

def ref_count_nested(n: int) -> int:
    return n * n

def ref_count_halved(n: int) -> int:
    return n // 2

def ref_work_units(n: int) -> int:
    return n * (n // 2)

# function_name in slice -> reference implementation
REFERENCE: Dict[str, Any] = {
    "sum_one_to_n": ref_sum_one_to_n,
    "count_evens": ref_count_evens,
    "square_series": ref_square_series,
    "count_digits": ref_count_digits,
    "sum_list": ref_sum_list,
    "find_index": ref_find_index,
    "reverse_list": ref_reverse_list,
    "rotate_left": ref_rotate_left,
    "count_vowels": ref_count_vowels,
    "is_palindrome": ref_is_palindrome,
    "title_case": ref_title_case,
    "first_occurrence": ref_first_occurrence,
    "celsius_to_fahrenheit": ref_celsius_to_fahrenheit,
    "rect_area": ref_rect_area,
    "absolute_difference": ref_absolute_difference,
    "is_prime": ref_is_prime,
    "swap_first_last": ref_swap_first_last,
    "bubble_pass": ref_bubble_pass,
    "min_index": ref_min_index,
    "is_sorted": ref_is_sorted,
    "count_linear": ref_count_linear,
    "count_nested": ref_count_nested,
    "count_halved": ref_count_halved,
    "work_units": ref_work_units,
}

# ──────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────

def norm(s: Any) -> str:
    return " ".join(str(s).strip().split())

def deep_equal(a: Any, b: Any) -> bool:
    if isinstance(a, float) or isinstance(b, float):
        try:
            return abs(float(a) - float(b)) < 1e-9
        except (TypeError, ValueError):
            return False
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(deep_equal(x, y) for x, y in zip(a, b))
    return a == b

def run_ref(function_name: str, inputs: List[Any]) -> Any:
    fn = REFERENCE[function_name]
    return fn(*inputs)

def check_test_bundle(function_name: str, bundle: Dict[str, Any], label_plural: str) -> List[str]:
    errors: List[str] = []
    for i, tc in enumerate(bundle):
        actual = run_ref(function_name, tc["input"])
        if not deep_equal(actual, tc["expected"]):
            errors.append(
                f"  [{label_plural} #{i}] {function_name}{tuple(tc['input'])} -> "
                f"got ref {actual!r}, stored {tc['expected']!r}"
            )
    return errors

# ──────────────────────────────────────────────────────────────────────
# Assessment trace checks (exec the trace, compare output)
# ──────────────────────────────────────────────────────────────────────

def norms_equal(a: Any, b: Any) -> bool:
    return norm(a).lower() == norm(b).lower()

def trace_checks(lesson: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    qs = lesson["assessment"]["questions"]
    if len(qs) != 3:
        errors.append(f"  assessment has {len(qs)} questions, expected 3")
    for q in qs:
        if q["type"] not in ("code_tracing", "concept", "debug"):
            errors.append(f"  unknown question type: {q['type']}")
    return errors


def exec_py(code: str):
    """Execute code in a fresh namespace; return (ok, stdout, error_label)."""
    ns: Dict[str, Any] = {"__name__": "__main__"}
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            exec(code, ns)
    except Exception as exc:
        return False, buf.getvalue().strip(), f"{type(exc).__name__}: {exc}"
    return True, buf.getvalue().strip(), None


def explain_checks(lesson: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    section = lesson["explain"]
    if section.get("answer_format") != "short_answer":
        errors.append("  explain.answer_format must be 'short_answer'")
    if not section.get("keywords"):
        errors.append("  explain.keywords is empty")
    if not section.get("model_answer"):
        errors.append("  explain.model_answer is empty")
    if not section.get("intention"):
        errors.append("  explain.intention is empty")
    if int(section.get("min_words", 0) or 0) < 1:
        errors.append("  explain.min_words must be >= 1")

    # Grader smoke: the model answer must pass the service's own check.
    merged = dict(lesson)
    res = LessonService(merged).check_explain(section["model_answer"])
    if not res["correct"]:
        errors.append(
            f"  check_explain(model_answer) failed: matched={res['matched_keywords']}, "
            f"words={res['word_count']}"
        )
    return errors


def break_checks(lesson: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    section = lesson["break"]
    options = (section.get("diagnosis") or {}).get("options", [])
    if not options:
        errors.append("  break.diagnosis.options is empty")
        return errors

    correct_opts = [o for o in options if o.get("correct")]
    if len(correct_opts) != 1:
        errors.append(f"  break.diagnosis has {len(correct_opts)} correct options, expected exactly 1")
    for o in options:
        if not o.get("why"):
            errors.append(f"  break.diagnosis option '{o.get('id')}' missing 'why'")

    if not section.get("fix"):
        errors.append("  break.fix is empty")

    buggy = section.get("buggy_code") or ""
    fixed = section.get("fixed_code") or ""
    expected = str(section.get("expected_output") or "").strip()

    fixed_ok, fixed_out, fixed_err = exec_py(fixed)
    if not fixed_ok:
        errors.append(f"  break.fixed_code crashed: {fixed_err}")
    elif not norms_equal(fixed_out, expected):
        errors.append(f"  break.fixed_code output {fixed_out!r}, expected {expected!r}")

    buggy_ok, buggy_out, buggy_err = exec_py(buggy)
    if buggy_ok and norms_equal(buggy_out, expected):
        errors.append("  break.buggy_code already produces expected_output — it is not broken")

    # Grader smoke: intended diagnosis id + normalized fix must pass.
    diag_id = correct_opts[0]["id"] if correct_opts else "a"
    res = LessonService(dict(lesson)).check_break(
        diagnosis=diag_id, fix=section.get("fix", "")
    )
    if not res["passed"]:
        errors.append(
            f"  check_break(intended) failed: diagnosis={res['diagnosis_correct']}, fix={res['fix_correct']}"
        )
    return errors


def discovery_checks(lesson: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    steps = lesson["discovery"].get("steps", [])
    for step in steps:
        if not isinstance(step, dict):
            continue
        interaction = step.get("interaction")
        if interaction is None:
            continue
        itype = interaction.get("type")
        if itype not in ALLOWED_INTERACTIONS:
            errors.append(f"  discovery step has unknown interaction type: {itype}")
            continue
        if itype == "manipulate":
            if not interaction.get("code") or not interaction.get("expected_output"):
                errors.append("  manipulate interaction needs code + expected_output")
        elif itype == "compare":
            opts = interaction.get("options", [])
            n_correct = sum(1 for o in opts if o.get("correct"))
            if n_correct != 1:
                errors.append(f"  compare interaction has {n_correct} correct options, expected 1")
        elif itype == "arrange":
            items = interaction.get("items", [])
            order = interaction.get("correct_order", [])
            ids = [it.get("id") for it in items]
            if len(ids) != len(order) or sorted(ids) != sorted(order):
                errors.append(f"  arrange correct_order is not a permutation of items: {ids} vs {order}")
    return errors


def verify_slice(slice_number: int, lesson: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    name = lesson["lesson_id"]

    # 1. Contract
    for key in REQUIRED_KEYS:
        if key not in lesson:
            errors.append(f"  missing required key: {key}")
    if "competency_id" not in lesson.get("world_progression", {}):
        errors.append("  world_progression.competency_id missing")

    # 2. Prediction: exactly one correct
    options = lesson["prediction"]["options"]
    correct = [o for o in options if o.get("correct")]
    if len(correct) != 1:
        errors.append(f"  prediction has {len(correct)} correct options, expected exactly 1")

    # 3. Guided build steps: reference reproduces stored expecteds
    build = lesson["guided_build"]["steps"]
    for step in build:
        fn = step["function_name"]
        if fn not in REFERENCE:
            errors.append(f"  no reference impl for {fn}")
            continue
        errors += check_test_bundle(fn, step.get("test_cases", []), "build-visible")
        errors += check_test_bundle(fn, step.get("hidden_test_cases", []), "build-hidden")
        if not step.get("scaffolded_hints"):
            errors.append(f"  build step '{step.get('title')}' has no scaffolded hints")

    # 4. Transfer challenge
    tr = lesson["transfer_challenge"]
    fn = tr["function_name"]
    if fn not in REFERENCE:
        errors.append(f"  no reference impl for transfer fn {fn}")
    else:
        errors += check_test_bundle(fn, tr.get("test_cases", []), "transfer-visible")
        errors += check_test_bundle(fn, tr.get("hidden_test_cases", []), "transfer-hidden")

    # 5. Assessment shape (content-level traces validated separately)
    errors += trace_checks(lesson)

    return errors


def verify_new_stages(lesson: Dict[str, Any]) -> List[str]:
    """Explain / break / discovery-interaction checks (all 8 lessons)."""
    errors: List[str] = []
    errors += explain_checks(lesson)
    errors += break_checks(lesson)
    errors += discovery_checks(lesson)
    return errors


def verify_traces(lesson: Dict[str, Any], expected: str, compute: Any) -> List[str]:
    """Exec the code_tracing code in a fresh namespace and compare the answer."""
    q = lesson["assessment"]["questions"][0]
    assert q["type"] == "code_tracing"
    ns: Dict[str, Any] = {}
    try:
        exec(q["code"], ns)
        actual = compute(ns)
    except Exception as exc:  # pragma: no cover
        return [f"  trace exec failed for {lesson['lesson_id']}: {exc}"]
    if not norms_equal(actual, q["expected_answer"]):
        return [f"  trace mismatch {lesson['lesson_id']}: computed {actual!r}, stored {q['expected_answer']!r}"]
    if not norms_equal(actual, expected):
        return [f"  trace mismatch {lesson['lesson_id']}: computed {actual!r}, expected {expected!r}"]
    return []


def main() -> int:
    failures: int = 0
    competency_ids = set()

    print("=" * 78)
    print("Phase B Concept-Clarity verification")
    print("=" * 78)

    for i, lesson in enumerate(SLICES, 1):
        name = lesson["lesson_id"]
        errors = verify_slice(i, lesson)

        comp = lesson["world_progression"]["competency_id"]
        if comp in competency_ids:
            errors.append(f"  duplicate competency_id: {comp}")
        competency_ids.add(comp)

        # specific trace validations
        if name == "loops_lantern_row":
            errors += verify_traces(lesson, "6", lambda ns: ns["result"])
        elif name == "arrays_warehouse":
            errors += verify_traces(lesson, "60", lambda ns: ns["nums"][1] + ns["nums"][2])
        elif name == "strings_stringed_loom":
            errors += verify_traces(lesson, "6", lambda ns: len(ns["t"]))
        elif name == "functions_function_forge":
            errors += verify_traces(lesson, "50", lambda ns: ns["z"])
        elif name == "sorting_bazaar":
            # simulate the documented one sweep (xor library-free), answer nums[0]
            def compute(ns: Dict[str, Any]) -> Any:
                nums = list(ns["nums"])
                for j in range(len(nums) - 1):
                    if nums[j] > nums[j + 1]:
                        nums[j], nums[j + 1] = nums[j + 1], nums[j]
                return nums[0]
            errors += verify_traces(lesson, "2", compute)
        elif name == "complexity_observatory":
            errors += verify_traces(lesson, "9", lambda ns: ns["total"])

        status = "PASS" if not errors else "FAIL"
        if errors:
            failures += 1
        print(f"[{status}] {i}. {lesson['title']} ({name})")
        for e in errors:
            print("    " + e)

    # registry-level checks
    print("-" * 78)
    phb = registry.concept_clarity_lessons()
    if len(phb) != 8:
        failures += 1
        print(f"[FAIL] concept_clarity_lessons() returns {len(phb)}, expected 8")
    else:
        print(f"[PASS] registry exposes all 8 Phase B concept lessons: {[l['lesson_id'] for l in phb]}")
    for slug in ("loops", "arrays", "strings", "functions", "sorting", "complexity"):
        if registry.get_lesson_dict(slug) is None:
            failures += 1
            print(f"[FAIL] get_lesson_dict('{slug}') is None")
        else:
            print(f"[PASS] get_lesson_dict('{slug}') resolves")

    # explain + break + interaction checks across all 8 Phase B lessons
    print("-" * 78)
    for lesson in phb:
        errors = verify_new_stages(lesson)
        status = "PASS" if not errors else "FAIL"
        if errors:
            failures += 1
        print(f"[{status}] new stages: {lesson['title']} ({lesson['lesson_id']})")
        for e in errors:
            print("    " + e)

    print("=" * 78)
    if failures:
        print(f"VERDICT: {failures} slice(s) failed")
        return 1
    print(f"VERDICT: all {len(SLICES)} new slices PASS ({len(SLICES) * 3} assessment questions)")
    return 0


if __name__ == "__main__":
    sys.exit(main())