from typing import Dict, List, Any, Optional, Tuple
import json
import re


# ──────────────────────────────────────────────────────────────────
# Behavioral Judge — Precomputed Test Comparison
# ──────────────────────────────────────────────────────────────────

class BehavioralJudge:
    """
    Compares student output against PRECOMPUTED expected outputs.
    No execution — just behavior verification.
    Uses reference solution's test cases stored with the problem.
    """

    def __init__(self):
        self.normalizers = {
            "string": self._normalize_string,
            "number": self._normalize_number,
            "list": self._normalize_list,
            "dict": self._normalize_dict,
            "bool": self._normalize_bool,
        }

    def judge(self, problem_id: str, student_output: str, expected_output: str,
              output_type: str = "auto") -> Tuple[bool, str, Dict[str, Any]]:
        """
        Compare student output to expected output.
        Returns: (passed, feedback_message, details)
        """
        # Determine output type if auto
        if output_type == "auto":
            output_type = self._detect_output_type(expected_output)

        normalizer = self.normalizers.get(output_type, self._normalize_string)
        student_norm = normalizer(student_output)
        expected_norm = normalizer(expected_output)

        passed = student_norm == expected_norm

        if passed:
            return (True, "✓ Output matches expected", {
                "student_normalized": student_norm,
                "expected_normalized": expected_norm,
                "output_type": output_type,
            })
        else:
            diff = self._generate_diff(student_norm, expected_norm, output_type)
            return (False, f"✗ Output mismatch: {diff}", {
                "student_normalized": student_norm,
                "expected_normalized": expected_norm,
                "output_type": output_type,
                "diff": diff,
            })

    def judge_multiple(self, student_outputs: List[str],
                       expected_outputs: List[str],
                       output_types: List[str] = None) -> Dict[str, Any]:
        """Judge multiple test cases at once."""
        if output_types is None:
            output_types = ["auto"] * len(expected_outputs)

        results = []
        passed = 0

        for i, (stu_out, exp_out, out_type) in enumerate(zip(student_outputs, expected_outputs, output_types)):
            p, msg, details = self.judge("", stu_out, exp_out, out_type)
            results.append({
                "test_case": i + 1,
                "passed": p,
                "message": msg,
                "details": details,
            })
            if p:
                passed += 1

        return {
            "all_passed": passed == len(expected_outputs),
            "passed_count": passed,
            "total_count": len(expected_outputs),
            "score": round(passed / len(expected_outputs) * 100, 1) if expected_outputs else 0,
            "results": results,
        }

    def _detect_output_type(self, expected: str) -> str:
        """Detect output type from expected value."""
        expected = expected.strip()
        if expected.lower() in ("true", "false"):
            return "bool"
        if expected.startswith("[") and expected.endswith("]"):
            return "list"
        if expected.startswith("{") and expected.endswith("}"):
            return "dict"
        if re.match(r"^-?\d+(\.\d+)?$", expected):
            return "number"
        return "string"

    def _normalize_string(self, value: str) -> str:
        """Normalize string output — trim whitespace, handle newlines."""
        if value is None:
            return ""
        return "\n".join(line.rstrip() for line in str(value).strip().splitlines())

    def _normalize_number(self, value: str) -> str:
        """Normalize numeric output."""
        value = value.strip()
        try:
            # Handle both int and float
            if "." in value:
                return str(float(value))
            return str(int(value))
        except ValueError:
            return value.strip()

    def _normalize_list(self, value: str) -> str:
        """Normalize list output — parse and re-serialize."""
        value = value.strip()
        try:
            # Try to parse as JSON
            parsed = json.loads(value)
            if isinstance(parsed, list):
                return json.dumps(parsed, separators=(",", ":"))
        except json.JSONDecodeError:
            pass
        return self._normalize_string(value)

    def _normalize_dict(self, value: str) -> str:
        """Normalize dict output."""
        value = value.strip()
        try:
            parsed = json.loads(value)
            if isinstance(parsed, dict):
                return json.dumps(parsed, sort_keys=True, separators=(",", ":"))
        except json.JSONDecodeError:
            pass
        return self._normalize_string(value)

    def _normalize_bool(self, value: str) -> str:
        """Normalize boolean output."""
        value = value.strip().lower()
        if value in ("true", "1", "yes", "t"):
            return "true"
        if value in ("false", "0", "no", "f"):
            return "false"
        return value

    def _generate_diff(self, student: str, expected: str, output_type: str) -> str:
        """Generate human-readable diff."""
        if output_type == "list":
            try:
                stu_list = json.loads(student)
                exp_list = json.loads(expected)
                if len(stu_list) != len(exp_list):
                    return f"Length mismatch: got {len(stu_list)}, expected {len(exp_list)}"
                for i, (s, e) in enumerate(zip(stu_list, exp_list)):
                    if s != e:
                        return f"Index {i}: got {s}, expected {e}"
            except:
                pass

        if len(student) > 100 or len(expected) > 100:
            return "Output too long to show diff. First 50 chars differ."

        return f"Got: '{student[:50]}' | Expected: '{expected[:50]}'"

    def check_expected_outputs(self, problem: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract and normalize expected outputs from problem definition."""
        test_cases = problem.get("test_cases", [])
        normalized = []

        for tc in test_cases:
            expected = tc.get("expected", tc.get("expected_output", ""))
            normalized.append({
                "input": tc.get("input", ""),
                "expected": expected,
                "is_hidden": tc.get("is_hidden", False),
            })

        return normalized


# ──────────────────────────────────────────────────────────────────
# Precomputed Test Store (loaded from problem definitions)
# ──────────────────────────────────────────────────────────────────

class PrecomputedTestStore:
    """Stores and retrieves precomputed test cases for problems."""

    def __init__(self):
        self._tests: Dict[str, List[Dict[str, Any]]] = {}

    def load_from_problem(self, problem: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract test cases from problem definition."""
        test_cases = problem.get("test_cases", [])
        self._tests[problem["id"]] = test_cases
        return test_cases

    def get_tests(self, problem_id: str) -> List[Dict[str, Any]]:
        return self._tests.get(problem_id, [])

    def get_visible_tests(self, problem_id: str) -> List[Dict[str, Any]]:
        return [tc for tc in self.get_tests(problem_id) if not tc.get("is_hidden", False)]

    def get_hidden_tests(self, problem_id: str) -> List[Dict[str, Any]]:
        return [tc for tc in self.get_tests(problem_id) if tc.get("is_hidden", False)]