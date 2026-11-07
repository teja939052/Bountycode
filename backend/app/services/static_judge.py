import ast
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass


# ──────────────────────────────────────────────────────────────────
# Static Judge — AST + Pattern Analysis
# ──────────────────────────────────────────────────────────────────

class StaticJudge:
    """
    Analyzes student code WITHOUT execution.
    Detects: structure, patterns, suspicious constructs, complexity hints.
    """

    def __init__(self):
        self.patterns = {
            "has_while_loop": r"while\s+",
            "has_for_loop": r"for\s+",
            "has_if": r"if\s+",
            "has_function": r"def\s+\w+\s*\(",
            "has_class": r"class\s+\w+",
            "has_recursion": r"\w+\s*\(\s*\w+\s*\)",  # simplified
            "uses_slicing": r"\[::\]",
            "uses_builtin_sort": r"\.sort\(\)|\bsorted\(",
            "uses_reverse": r"\[::-1\]",
        }

    def analyze(self, code: str, language: str) -> Dict[str, Any]:
        """Return static analysis results."""
        result = {
            "language": language,
            "ast_valid": False,
            "ast_nodes": [],
            "patterns": {},
            "variables": [],
            "functions": [],
            "loops": [],
            "conditionals": [],
            "complexity_hint": None,
            "errors": [],
        }

        if language == "python":
            result.update(self._analyze_python(code))
        elif language == "javascript":
            result.update(self._analyze_javascript(code))
        elif language in ("cpp", "c", "java"):
            result.update(self._analyze_c_family(code, language))
        else:
            result["errors"].append(f"Unsupported language for static analysis: {language}")

        return result

    def _analyze_python(self, code: str) -> Dict[str, Any]:
        out = {"patterns": {}, "variables": [], "functions": [], "loops": [], "conditionals": []}

        try:
            tree = ast.parse(code)
            out["ast_valid"] = True

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    out["functions"].append({
                        "name": node.name,
                        "args": [a.arg for a in node.args.args],
                        "returns": getattr(node, "returns", None),
                    })
                elif isinstance(node, ast.While):
                    out["loops"].append({"type": "while", "lineno": node.lineno})
                elif isinstance(node, ast.For):
                    out["loops"].append({"type": "for", "lineno": node.lineno})
                elif isinstance(node, ast.If):
                    out["conditionals"].append({"lineno": node.lineno})
                elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                    out["variables"].append(node.id)

            # Pattern detection
            for name, pattern in self.patterns.items():
                out["patterns"][name] = bool(re.search(pattern, code))

            # Complexity heuristic
            loop_count = len(out["loops"])
            if loop_count >= 2:
                out["complexity_hint"] = "O(n²) or worse (nested loops detected)"
            elif loop_count == 1:
                out["complexity_hint"] = "O(n) (single loop)"
            else:
                out["complexity_hint"] = "O(1) or O(log n) (no loops)"

        except SyntaxError as e:
            out["ast_valid"] = False
            out["errors"].append(f"Syntax error: {e.msg} at line {e.lineno}")

        return out

    def _analyze_javascript(self, code: str) -> Dict[str, Any]:
        """Lightweight JS analysis using regex (no full parser)."""
        out = {"patterns": {}, "variables": [], "functions": [], "loops": [], "conditionals": []}

        # Simple patterns
        patterns = {
            "has_while_loop": r"while\s*\(",
            "has_for_loop": r"for\s*\(",
            "has_for_of": r"for\s+\(.*\bof\b",
            "has_if": r"if\s*\(",
            "has_function": r"function\s+\w+\s*\(",
            "has_arrow_function": r"=>\s*\{",
            "has_class": r"class\s+\w+",
            "uses_reverse": r"\.reverse\(\)",
            "uses_sort": r"\.sort\(",
        }

        for name, pattern in patterns.items():
            out["patterns"][name] = bool(re.search(pattern, code))

        # Extract function names
        func_matches = re.findall(r"function\s+(\w+)\s*\(", code)
        out["functions"] = func_matches

        # Variables (simplified)
        var_matches = re.findall(r"(?:let|const|var)\s+(\w+)", code)
        out["variables"] = var_matches

        out["ast_valid"] = True  # We don't fully parse JS
        return out

    def _analyze_c_family(self, code: str, language: str) -> Dict[str, Any]:
        """Lightweight C/C++/Java analysis using regex."""
        out = {"patterns": {}, "variables": [], "functions": [], "loops": [], "conditionals": []}

        patterns = {
            "has_while_loop": r"while\s*\(",
            "has_for_loop": r"for\s*\(",
            "has_if": r"if\s*\(",
            "has_switch": r"switch\s*\(",
            "has_function": r"\w+\s+\w+\s*\(",
            "uses_std_vector": r"std::vector",
            "uses_std_sort": r"std::sort",
            "uses_reverse_iterator": r"rbegin\(\)",
        }

        for name, pattern in patterns.items():
            out["patterns"][name] = bool(re.search(pattern, code))

        # Extract variables (very simplified)
        var_matches = re.findall(r"(?:int|long|float|double|string|String|vector)\s+(\w+)", code)
        out["variables"] = var_matches

        out["ast_valid"] = True
        return out

    def check_lock(self, code: str, lock_def: Dict[str, Any], language: str) -> Tuple[bool, str]:
        """
        Check if student code satisfies a specific lock.
        Returns (passed, feedback_message).
        """
        lock_type = lock_def.get("type")
        accepted = lock_def.get("accepted", [])
        rejected = lock_def.get("rejected", [])

        if lock_type == "code_expression":
            return self._check_code_expression(code, accepted, rejected, language)
        elif lock_type == "multiple_choice":
            return self._check_multiple_choice(code, accepted, rejected)
        elif lock_type == "concept_check":
            return self._check_concept_check(code, accepted, rejected, language)
        elif lock_type == "fill_the_lock":
            return self._check_fill_the_lock(code, accepted, rejected, language)
        elif lock_type == "fix_the_bug":
            return self._check_fix_the_bug(code, accepted, rejected, language)
        elif lock_type == "arrange":
            return self._check_arrange(code, accepted, rejected)
        elif lock_type == "prediction":
            return self._check_prediction(code, accepted, rejected)
        return (False, "Unknown lock type")

    def _check_code_expression(self, code: str, accepted: List[str], rejected: List[str], language: str) -> Tuple[bool, str]:
        """Check if code contains one of the accepted expressions."""
        # Normalize whitespace
        normalized = re.sub(r"\s+", " ", code.strip())

        for pattern in accepted:
            # Convert pattern to regex-friendly
            regex = re.escape(pattern).replace(r"\_\_\_", r".+?")  # Allow any expression in blanks
            if re.search(regex, normalized):
                return (True, f"✓ Expression matches: {pattern}")

        for bad in rejected:
            if re.search(re.escape(bad), normalized):
                return (False, f"✗ Detected incorrect pattern: {bad}")

        return (False, "Expected expression not found. Check the hint.")

    def _check_multiple_choice(self, code: str, accepted: List[str], rejected: List[str]) -> Tuple[bool, str]:
        """For multiple choice, code is the selected option letter."""
        if code.strip().upper() in [a.upper() for a in accepted]:
            return (True, "✓ Correct choice")
        return (False, "Incorrect choice. Think about the sorted property.")

    def _check_concept_check(self, code: str, accepted: List[str], rejected: List[str], language: str) -> Tuple[bool, str]:
        """Concept check - student explains in text."""
        normalized = code.strip().lower()
        for pattern in accepted:
            if pattern.lower() in normalized:
                return (True, "✓ Concept understood")
        return (False, "Keep thinking. The hint will guide you.")

    def _check_fill_the_lock(self, code: str, accepted: List[str], rejected: List[str], language: str) -> Tuple[bool, str]:
        """Fill-in-the-blank style."""
        return self._check_code_expression(code, accepted, rejected, language)

    def _check_fix_the_bug(self, code: str, accepted: List[str], rejected: List[str], language: str) -> Tuple[bool, str]:
        """Bug fix - detect if student identified the bug."""
        normalized = code.strip().lower()
        for bug in rejected:
            if bug.lower() in normalized:
                return (False, f"✗ You identified the bug but the fix is wrong. {bug}")
        for fix in accepted:
            if fix.lower() in normalized:
                return (True, "✓ Bug correctly identified and fixed!")
        return (False, "What's wrong with this code? Look at the boundary movement.")

    def _check_arrange(self, code: str, accepted: List[str], rejected: List[str]) -> Tuple[bool, str]:
        """Code arrangement - check if order matches."""
        # Student submits ordered list of statement IDs
        normalized = code.strip()
        for correct_order in accepted:
            if normalized == correct_order:
                return (True, "✓ Statements in correct order")
        return (False, "Order matters. Think about the algorithm flow.")

    def _check_prediction(self, code: str, accepted: List[str], rejected: List[str]) -> Tuple[bool, str]:
        """Prediction - student predicts output/state."""
        if code.strip() in accepted:
            return (True, "✓ Correct prediction!")
        return (False, "Your prediction doesn't match the expected behavior.")