"""
Code Trace Instrumentation — AST-level code instrumentation for real-time step capture.
Parses user code, injects tracing hooks, executes, and returns step-by-step variable snapshots.
Supports Python natively (AST). Other languages fall back to AI-generated traces.
"""
import ast
import json
import sys
import io
import textwrap
from typing import Dict, List, Any, Optional


class CodeTracer(ast.NodeTransformer):
    """AST transformer that injects tracing calls into Python code."""

    def __init__(self):
        self.step_counter = 0
        self.traced_vars: set = set()
        self.source_map: Dict[int, str] = {}

    def _make_trace_call(self, line: int, var_names: list) -> ast.Expr:
        """Create: __trace__.append({'step': N, 'line': L, 'vars': {k: repr(v) ...}})"""
        # Build the dict comprehension for captured variables
        keys = [ast.Constant(value=name) for name in var_names]
        values = [ast.Name(id=name, ctx=ast.Load()) for name in var_names]
        dict_node = ast.Dict(keys=keys, values=values)

        # Build: repr(v) for each value to safely serialize
        repr_keys = [ast.Constant(value=name) for name in var_names]
        repr_values = [
            ast.Call(
                func=ast.Name(id='repr', ctx=ast.Load()),
                args=[ast.Name(id=name, ctx=ast.Load())],
                keywords=[],
            )
            for name in var_names
        ]
        repr_dict = ast.Dict(keys=repr_keys, values=repr_values)

        # __trace__.append({...})
        return ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id='__trace__', ctx=ast.Load()),
                    attr='append',
                    ctx=ast.Load(),
                ),
                args=[
                    ast.Dict(
                        keys=[
                            ast.Constant(value='step'),
                            ast.Constant(value='line'),
                            ast.Constant(value='vars'),
                        ],
                        values=[
                            ast.Constant(value=self.step_counter),
                            ast.Constant(value=line),
                            repr_dict,
                        ],
                    )
                ],
                keywords=[],
            )
        )

    def _collect_local_vars(self, node) -> list:
        """Extract variable names referenced on the right side of this assignment."""
        var_names = []
        for target in ast.walk(node):
            if isinstance(target, ast.Name):
                if target.id not in ('__trace__', 'print', 'len', 'range', 'repr', 'int', 'float', 'str', 'list', 'dict', 'set', 'True', 'False', 'None', 'self'):
                    var_names.append(target.id)
        return var_names[:10]  # Cap at 10 to avoid perf issues

    def visit_Assign(self, node: ast.Assign) -> Any:
        self.generic_visit(node)
        line = getattr(node, 'lineno', 0)
        var_names = self._collect_local_vars(node)
        if var_names:
            for v in var_names:
                self.traced_vars.add(v)
            self.step_counter += 1
            # Trace call AFTER assignment so variable is defined
            return [node, self._make_trace_call(line, var_names)]
        return node

    def visit_AugAssign(self, node: ast.AugAssign) -> Any:
        self.generic_visit(node)
        line = getattr(node, 'lineno', 0)
        if isinstance(node.target, ast.Name):
            name = node.target.id
            self.traced_vars.add(name)
            self.step_counter += 1
            return [
                node,
                self._make_trace_call(line, [name]),
            ]
        return node

    def visit_AnnAssign(self, node: ast.AnnAssign) -> Any:
        self.generic_visit(node)
        if node.target and isinstance(node.target, ast.Name):
            line = getattr(node, 'lineno', 0)
            name = node.target.id
            self.traced_vars.add(name)
            self.step_counter += 1
            return [
                node,
                self._make_trace_call(line, [name]),
            ]
        return node

    def visit_For(self, node: ast.For) -> Any:
        self.generic_visit(node)
        line = getattr(node, 'lineno', 0)
        # Capture loop variable(s)
        loop_vars = []
        if isinstance(node.target, ast.Name):
            loop_vars.append(node.target.id)
            self.traced_vars.add(node.target.id)
        elif isinstance(node.target, ast.Tuple):
            for elt in node.target.elts:
                if isinstance(elt, ast.Name):
                    loop_vars.append(elt.id)
                    self.traced_vars.add(elt.id)
        if loop_vars:
            self.step_counter += 1
            # Insert trace call as first statement inside the loop body
            trace_stmt = self._make_trace_call(line, loop_vars)
            node.body.insert(0, trace_stmt)
        return node

    def visit_While(self, node: ast.While) -> Any:
        self.generic_visit(node)
        return node

    def visit_If(self, node: ast.If) -> Any:
        self.generic_visit(node)
        return node

    def visit_Return(self, node: ast.Return) -> Any:
        self.generic_visit(node)
        self.step_counter += 1
        line = getattr(node, 'lineno', 0)
        if self.traced_vars:
            return [
                self._make_trace_call(line, list(self.traced_vars)[:8]),
                node,
            ]
        return node

    def visit_Expr(self, node: ast.Expr) -> Any:
        self.generic_visit(node)
        # Trace print() calls
        if isinstance(node.value, ast.Call):
            func = node.value.func
            if isinstance(func, ast.Name) and func.id == 'print':
                self.step_counter += 1
                line = getattr(node, 'lineno', 0)
                if self.traced_vars:
                    return [
                        self._make_trace_call(line, list(self.traced_vars)[:8]),
                        node,
                    ]
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        # Don't transform inner function defs
        self.generic_visit(node)
        return node

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        self.generic_visit(node)
        return node


def instrument_python_code(code: str) -> str:
    """Parse Python code and inject tracing calls. Returns instrumented code."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return code  # Return original if unparseable

    tracer = CodeTracer()
    new_tree = tracer.visit(tree)
    ast.fix_missing_locations(new_tree)

    # Prepend __trace__ = [] and append return __trace__
    pre = "__trace__ = []\n"
    post = "\n__trace__"

    instrumented = ast.unparse(new_tree)
    return pre + instrumented + post


def execute_with_trace(code: str, stdin: str = "", timeout: int = 5) -> Dict[str, Any]:
    """
    Execute instrumented Python code and return trace data.
    Returns: { steps: [...], output: str, error: str|None }
    """
    instrumented = instrument_python_code(code)

    # Capture stdout
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()

    result = {
        "steps": [],
        "output": "",
        "error": None,
        "instrumented_code": instrumented,
    }

    try:
        sys.stdout = stdout_capture
        sys.stderr = stderr_capture

        # Provide stdin if needed
        if stdin:
            import builtins
            original_input = builtins.input
            stdin_lines = stdin.strip().split('\n')
            stdin_iter = iter(stdin_lines)
            builtins.input = lambda *a: next(stdin_iter)

        namespace = {"__builtins__": __builtins__, "__name__": "__main__"}
        exec(compile(instrumented, "<trace>", "exec"), namespace)

        trace_result = namespace.get("__trace__", [])
        result["steps"] = trace_result
        result["output"] = stdout_capture.getvalue()

    except Exception as e:
        result["error"] = f"{type(e).__name__}: {str(e)}"
        result["output"] = stdout_capture.getvalue()
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        if stdin:
            builtins.input = original_input

    return result


def detect_algorithm_type(code: str, steps: list) -> str:
    """Detect what algorithm pattern the code implements."""
    code_lower = code.lower()

    # Check keywords in code
    if "sort" in code_lower or "sorted" in code_lower:
        if "merge" in code_lower:
            return "merge_sort"
        elif "quick" in code_lower or "partition" in code_lower:
            return "quick_sort"
        elif "bubble" in code_lower:
            return "bubble_sort"
        return "sorting"

    if "binary" in code_lower and ("search" in code_lower or "low" in code_lower or "high" in code_lower):
        return "binary_search"

    # Detect binary search from variable patterns (low/high/mid without "binary" keyword)
    has_low = "low" in code_lower
    has_high = "high" in code_lower
    has_mid = "mid" in code_lower
    if has_low and has_high and has_mid:
        return "binary_search"

    if "bfs" in code_lower or "queue" in code_lower or "deque" in code_lower:
        return "bfs"

    if "dfs" in code_lower or "stack" in code_lower or "recursion" in code_lower or "recursive" in code_lower:
        return "dfs"

    if "linkedlist" in code_lower or "linked_list" in code_lower or ("node" in code_lower and "next" in code_lower):
        if "reverse" in code_lower:
            return "linked_list_reverse"
        return "linked_list"

    if "tree" in code_lower or ("node" in code_lower and ("left" in code_lower or "right" in code_lower)):
        return "binary_tree"

    if "dp" in code_lower or "memo" in code_lower or "memoize" in code_lower:
        return "dynamic_programming"

    if "window" in code_lower or "sliding" in code_lower:
        return "sliding_window"

    if "hash" in code_lower or "dict" in code_lower or "map" in code_lower:
        return "two_sum"

    if "backtrack" in code_lower or "permut" in code_lower or "combin" in code_lower:
        return "backtracking"

    if "graph" in code_lower or "adjacent" in code_lower or "vertex" in code_lower or "vertices" in code_lower:
        return "graph_traversal"

    # Detect from step variable patterns
    if steps:
        var_keys = set()
        for step in steps:
            if isinstance(step, dict) and "vars" in step:
                var_keys.update(step.get("vars", {}).keys())

        if "low" in var_keys and "high" in var_keys and "mid" in var_keys:
            return "binary_search"
        if "queue" in var_keys or "visited" in var_keys:
            return "bfs"
        if "stack" in var_keys:
            return "dfs"
        if "prev" in var_keys and "curr" in var_keys:
            return "linked_list"
        if "dp" in var_keys or "memo" in var_keys:
            return "dynamic_programming"

    return "unknown"
