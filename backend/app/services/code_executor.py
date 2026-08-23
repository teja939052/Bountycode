import httpx
import asyncio
import time
from typing import Dict, Any, List, Optional
from app.services.request_metrics import metrics as request_metrics
from app.services.circuit_breaker import compiler_breaker
from app.services.code_tracer import execute_with_trace, detect_algorithm_type


# Circuit breaker — now uses async-safe CircuitBreaker class
# compiler_breaker imported at top of file


from app.config import get_settings
from app.services.local_sandbox import execute_local, LOCAL_LANGUAGES
from app.services.remote_fallbacks import execute_remote_fallback


class CodeExecutionEngine:
    """
    Production code execution engine using Piston API.
    Executes code in isolated sandbox environment.
    """

    MAX_CODE_LENGTH = 120_000
    MAX_TIMEOUT = 30
    MAX_TEST_CASES = 50

    def __init__(self):
        self._client: Optional[httpx.AsyncClient] = None
        self._client_lock = None
        self._semaphore = None
        settings = get_settings()
        self._piston_url = settings.PISTON_API_URL
        self._piston_headers = (
            {"Authorization": settings.PISTON_API_KEY} if settings.PISTON_API_KEY else {}
        )

    SUPPORTED_LANGUAGES = {
        "python": {"language": "python", "version": "3.10.0", "extension": "py"},
        "javascript": {"language": "javascript", "version": "18.15.0", "extension": "js"},
        "typescript": {"language": "typescript", "version": "5.0.3", "extension": "ts"},
        "java": {"language": "java", "version": "15.0.2", "extension": "java"},
        "cpp": {"language": "c++", "version": "10.2.0", "extension": "cpp"},
        "c": {"language": "c", "version": "10.2.0", "extension": "c"},
        "go": {"language": "go", "version": "1.16.2", "extension": "go"},
        "rust": {"language": "rust", "version": "1.68.2", "extension": "rs"},
        "ruby": {"language": "ruby", "version": "3.0.1", "extension": "rb"},
        "php": {"language": "php", "version": "8.2.3", "extension": "php"},
        "swift": {"language": "swift", "version": "5.3.3", "extension": "swift"},
        "kotlin": {"language": "kotlin", "version": "1.8.20", "extension": "kt"},
    }

    BOILERPLATES = {
        "python": {
            "general": '''def solution():
    # Your code here
    pass

if __name__ == "__main__":
    print(solution())''',
            "class": '''class Solution:
    def solve(self, nums):
        # Your code here
        pass''',
            "input": '''import sys

def solution():
    # Read input from stdin
    # Process
    # Return output
    pass

print(solution())''',
            "linked_list": '''class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def solve(self, head):
        # Your code here
        pass''',
            "binary_tree": '''class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def solve(self, root):
        # Your code here
        pass''',
            "graph": '''from collections import deque, defaultdict

class Solution:
    def solve(self, graph):
        # Your code here
        pass''',
            "dp": '''def solution(n):
    # Your code here
    # Use dynamic programming
    pass

if __name__ == "__main__":
    print(solution(int(input())))''',
        },
        "javascript": {
            "general": '''function solution() {
    // Your code here
}

console.log(solution());''',
            "class": '''class Solution {
    solve(nums) {
        // Your code here
    }
}''',
            "linked_list": '''class ListNode {
    constructor(val, next = null) {
        this.val = val;
        this.next = next;
    }
}

class Solution {
    solve(head) {
        // Your code here
    }
}''',
            "binary_tree": '''class TreeNode {
    constructor(val, left = null, right = null) {
        this.val = val;
        this.left = left;
        this.right = right;
    }
}

class Solution {
    solve(root) {
        // Your code here
    }
}''',
        },
        "java": {
            "general": '''public class Main {
    public static void main(String[] args) {
        // Your code here
    }
}''',
            "class": '''class Solution {
    public int[] solve(int[] nums) {
        // Your code here
        return nums;
    }
}''',
            "linked_list": '''class ListNode {
    int val;
    ListNode next;
    ListNode(int val) { this.val = val; }
}

class Solution {
    public ListNode solve(ListNode head) {
        // Your code here
        return head;
    }
}''',
            "binary_tree": '''class TreeNode {
    int val;
    TreeNode left, right;
    TreeNode(int val) { this.val = val; }
}

class Solution {
    public int solve(TreeNode root) {
        // Your code here
        return 0;
    }
}''',
        },
        "cpp": {
            "general": '''#include <iostream>
#include <vector>
using namespace std;

int main() {
    // Your code here
    return 0;
}''',
            "class": '''class Solution {
public:
    vector<int> solve(vector<int>& nums) {
        // Your code here
        return nums;
    }
};''',
            "linked_list": '''struct ListNode {
    int val;
    ListNode* next;
    ListNode(int x) : val(x), next(nullptr) {}
};

class Solution {
public:
    ListNode* solve(ListNode* head) {
        // Your code here
        return head;
    }
};''',
            "binary_tree": '''struct TreeNode {
    int val;
    TreeNode *left, *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class Solution {
public:
    int solve(TreeNode* root) {
        // Your code here
        return 0;
    }
};''',
        },
        "go": {
            "general": '''package main

import "fmt"

func main() {
    // Your code here
}''',
        },
        "rust": {
            "general": '''fn main() {
    // Your code here
}''',
        },
    }

    async def execute_code(
        self,
        code: str,
        language: str,
        stdin: str = "",
        timeout: int = 5,
    ) -> Dict[str, Any]:
        """
        Execute code in isolated sandbox via Piston API.
        Returns compilation status, runtime output, and errors.
        """
        if len(code or "") > self.MAX_CODE_LENGTH:
            await request_metrics.record("compiler", "failure", error="Code too large")
            return {
                "success": False,
                "error": f"Code too large. Maximum allowed size is {self.MAX_CODE_LENGTH} characters.",
            }

        if not await self._check_circuit_breaker():
            await request_metrics.record("compiler", "failure", error="Circuit breaker open")
            return {
                "success": False,
                "error": "Compiler temporarily unavailable. Please retry in a moment.",
            }

        lang = language.lower()
        if lang not in self.SUPPORTED_LANGUAGES:
            await request_metrics.record("compiler", "failure", error=f"Unsupported language: {language}")
            return {
                "success": False,
                "error": f"Language '{language}' not supported",
                "supported_languages": list(self.SUPPORTED_LANGUAGES.keys()),
            }

        timeout = max(1, min(int(timeout or 5), self.MAX_TIMEOUT))
        lang_config = self.SUPPORTED_LANGUAGES[lang]
        filename = f"main.{lang_config['extension']}"

        payload = {
            "language": lang_config["language"],
            "version": lang_config["version"],
            "files": [{"name": filename, "content": code}],
            "stdin": stdin,
        }

        started = time.perf_counter()
        try:
            client = await self._get_client()
            semaphore = await self._get_semaphore()

            async with semaphore:
                response = await client.post(self._piston_url, json=payload, headers=self._piston_headers)

                if response.status_code != 200:
                    await self._record_failure()
                    await request_metrics.record(
                        "compiler",
                        "failure",
                        duration_ms=(time.perf_counter() - started) * 1000,
                        error=f"Piston API error: {response.status_code}",
                    )
                    error_message = f"Piston API error: {response.status_code}"
                    if response.status_code == 401 and not self._piston_headers:
                        error_message = (
                            "Piston API rejected the request (401). Set PISTON_API_KEY in backend/.env "
                            "(get a free key from the Piston Discord server) or self-host Piston via Docker."
                        )
                    fallback = await self._try_fallback(language, code, stdin, timeout)
                    if fallback:
                        return fallback
                    return {
                        "success": False,
                        "error": error_message,
                    }

                try:
                    result = response.json()
                except Exception:
                    await self._record_failure()
                    await request_metrics.record(
                        "compiler",
                        "failure",
                        duration_ms=(time.perf_counter() - started) * 1000,
                        error="Invalid JSON from Piston",
                    )
                    fallback = await self._try_fallback(language, code, stdin, timeout)
                    if fallback:
                        return fallback
                    return {
                        "success": False,
                        "error": "Piston API returned invalid JSON",
                    }

            # Parse output
            run_output = result.get("run", {})
            compile_output = result.get("compile", {})

            stdout = run_output.get("output", "")
            stderr = run_output.get("stderr", "")
            exit_code = run_output.get("code", 1)
            success = exit_code == 0

            if success:
                await self._record_success()
                await request_metrics.record(
                    "compiler",
                    "success",
                    duration_ms=(time.perf_counter() - started) * 1000,
                )
            else:
                await self._record_failure()
                await request_metrics.record(
                    "compiler",
                    "failure",
                    duration_ms=(time.perf_counter() - started) * 1000,
                    error=stderr or "Runtime error",
                )

            return {
                "success": success,
                "exit_code": exit_code,
                "stdout": stdout.strip(),
                "stderr": stderr.strip(),
                "compile_error": compile_output.get("stderr", "") if compile_output.get("code", 0) != 0 else None,
                "language": language,
                "execution_time": run_output.get("time", 0),
                "memory_usage": run_output.get("memory", 0),
            }

        except httpx.TimeoutException:
            await self._record_failure()
            await request_metrics.record("compiler", "failure", duration_ms=(time.perf_counter() - started) * 1000, error="Timeout")
            fallback = await self._try_fallback(language, code, stdin, timeout)
            if fallback:
                return fallback
            return {
                "success": False,
                "error": "Code execution timed out (possible infinite loop)",
                "hint": "Check for infinite loops or very long-running operations",
            }
        except httpx.RequestError as e:
            await self._record_failure()
            await request_metrics.record("compiler", "failure", duration_ms=(time.perf_counter() - started) * 1000, error=str(e))
            fallback = await self._try_fallback(language, code, stdin, timeout)
            if fallback:
                return fallback
            return {
                "success": False,
                "error": f"Network error: {str(e)}",
            }
        except Exception as e:
            await self._record_failure()
            await request_metrics.record("compiler", "failure", duration_ms=(time.perf_counter() - started) * 1000, error=str(e))
            return {
                "success": False,
                "error": f"Execution failed: {str(e)}",
            }

    async def execute_against_test_cases(
        self,
        source_code: str,
        language: str,
        test_cases: List[Dict[str, str]],
        function_name: str = "",
    ) -> Dict[str, Any]:
        """
        Execute code against multiple test cases in parallel using asyncio.gather.
        Returns pass/fail for each test case at lightning speed.
        """
        if len(test_cases) > self.MAX_TEST_CASES:
            return {
                "success": False,
                "error": f"Too many test cases. Maximum allowed is {self.MAX_TEST_CASES}.",
            }

        lang = language.lower()
        if lang not in self.SUPPORTED_LANGUAGES:
            return {
                "success": False,
                "error": f"Language '{language}' is not supported",
                "supported_languages": list(self.SUPPORTED_LANGUAGES.keys()),
            }

        # ── Oracle path: batch ALL test cases into ONE local sandbox run ──
        # Zero Piston API calls for Python submissions (the default language).
        if lang == "python":
            oracle = await self._grade_python_batched(
                source_code, test_cases, function_name=function_name or ""
            )
            if oracle is not None:
                return oracle
            # Oracle unavailable (no local interpreter etc.) → legacy per-case path.

        tc_semaphore = asyncio.Semaphore(6)

        async def run_single_test(idx: int, case: Dict[str, str]):
            async with tc_semaphore:
                stdin = case.get("input", "")
                expected = case.get("expected", case.get("expected_output", ""))
                is_hidden = case.get("is_hidden", False)

                execution = await self.execute_code(source_code, language, stdin)
                passed = False
                actual = ""

                if execution["success"]:
                    actual = self._normalize_text(execution["stdout"])
                    passed = actual == self._normalize_text(expected)
                else:
                    actual = execution.get("error", "Execution failed")

                return {
                    "test_case_index": idx + 1,
                    "passed": passed,
                    "is_hidden": is_hidden,
                    "input": stdin if not is_hidden else "[HIDDEN]",
                    "expected": expected if not is_hidden else "[HIDDEN]",
                    "actual": actual if not is_hidden else "[HIDDEN]",
                    "error": execution.get("error") if not execution["success"] else None,
                    "execution_time": execution.get("execution_time", 0),
                }

        tasks = [run_single_test(idx, case) for idx, case in enumerate(test_cases)]
        results = await asyncio.gather(*tasks)

        passed_count = sum(1 for r in results if r["passed"])
        all_passed = passed_count == len(test_cases)

        return {
            "success": True,
            "all_passed": all_passed,
            "passed_count": passed_count,
            "total_count": len(test_cases),
            "score": round(passed_count / len(test_cases) * 100, 1) if test_cases else 0,
            "summary": f"{passed_count}/{len(test_cases)} Test Cases Passed",
            "results": list(results),
        }

    async def generate_execution_trace(
        self,
        code: str,
        language: str,
        stdin: str = "",
    ) -> Dict[str, Any]:
        """
        Generate step-by-step execution trace for algorithm visualizer.
        Returns line-by-line execution steps, variable state, data structure visualization, and output.
        """
        from app.services.ai import chat_completion, parse_json

        lang = (language or "").lower()

        def _infer_visualization_type(algo: str, steps: List[Dict[str, Any]]) -> str:
            if not steps:
                return "none"
            if algo in {"binary_search", "sorting", "merge_sort", "quick_sort", "bubble_sort"}:
                return "bars" if algo != "binary_search" else "array"
            if algo in {"linked_list", "linked_list_reverse"}:
                return "linked_list"
            if algo in {"bfs", "dfs", "graph_traversal"}:
                return "queue" if algo == "bfs" else "stack"
            if algo == "binary_tree":
                return "tree"
            if algo == "dynamic_programming":
                return "matrix"
            return "array" if any(isinstance(step, dict) and step.get("array_data") for step in steps) else "none"

        def _shape_ast_trace(trace_result: Dict[str, Any]) -> Dict[str, Any]:
            raw_steps = trace_result.get("steps", []) or []
            shaped_steps = []
            if raw_steps:
                for idx, step in enumerate(raw_steps, start=1):
                    variables = step.get("vars", {}) if isinstance(step, dict) else {}
                    shaped_steps.append({
                        "step": step.get("step", idx) if isinstance(step, dict) else idx,
                        "line": step.get("line", idx) if isinstance(step, dict) else idx,
                        "code_snippet": step.get("code_snippet", "") if isinstance(step, dict) else "",
                        "action": f"Line {step.get('line', idx)}" if isinstance(step, dict) else f"Line {idx}",
                        "variables": variables,
                        "pointers": {},
                        "array_data": [],
                        "active_indices": [],
                        "data_structures": {
                            "type": "runtime_state",
                            "elements": [],
                            "pointers": {},
                        },
                        "explanation": (
                            f"Executed line {step.get('line', idx)} with state: "
                            f"{', '.join(f'{k}={v}' for k, v in list(variables.items())[:6])}"
                            if variables else f"Executed line {step.get('line', idx)}"
                        ),
                    })
            else:
                shaped_steps.append({
                    "step": 1,
                    "line": 1,
                    "code_snippet": "Program start",
                    "action": "Executed program",
                    "variables": {},
                    "pointers": {},
                    "array_data": [],
                    "active_indices": [],
                    "data_structures": {
                        "type": "runtime_state",
                        "elements": [],
                        "pointers": {},
                    },
                    "explanation": "No traceable state changes were captured, so this view shows the overall execution result.",
                })

            algo = detect_algorithm_type(code, raw_steps)
            viz_type = _infer_visualization_type(algo, shaped_steps)
            return {
                "success": True,
                "source": "ast_trace",
                "language": lang,
                "algorithm": algo,
                "visualization_type": viz_type,
                "stdout": trace_result.get("output", ""),
                "steps": shaped_steps,
                "time_complexity": "Detected from trace",
                "space_complexity": "Detected from trace",
                "key_insights": [
                    f"Traced {len(shaped_steps)} execution steps via Python AST instrumentation",
                    f"Detected algorithm pattern: {algo}",
                ],
            }

        if lang == "python":
            trace_result = execute_with_trace(code, stdin)
            shaped = _shape_ast_trace(trace_result)
            if trace_result.get("error"):
                shaped["error"] = trace_result["error"]
            return shaped

        prompt = f"""You are a master DSA execution visualizer and compiler judge.
Analyze the following {language} code and input, and trace its line-by-line execution.

Source Code ({language}):
```
{code}
```

Input (stdin):
{stdin or "None"}

Produce a detailed, highly accurate step-by-step execution trace JSON object matching this schema:
{{
  "language": "{language}",
  "stdout": "overall program output",
  "data_structure_type": "array|linked_list|tree|graph|stack|queue|hashmap|none",
  "steps": [
    {{
      "step": 1,
      "line": 4,
      "code_snippet": "i = 0",
      "action": "Initialize loop index i to 0",
      "variables": {{"i": 0, "nums": [2, 7, 11, 15], "target": 9}},
      "pointers": {{"left": 0, "right": 3, "mid": 1}},
      "array_data": [2, 7, 11, 15],
      "active_indices": [0, 3],
      "data_structures": {{
        "type": "array",
        "elements": [2, 7, 11, 15],
        "pointers": {{"left": 0, "right": 3}}
      }},
      "explanation": "Pointers initialized at the boundaries of the sorted array."
    }}
  ],
  "time_complexity": "O(n)",
  "space_complexity": "O(1)"
}}

Provide 4 to 12 meaningful, educational execution steps. Focus on loop iterations, variable changes, pointer updates, array access, and returned results."""

        try:
            result_str = await chat_completion(
                messages=[{"role": "user", "content": prompt}],
                use_cache=True,
                max_tokens=2500,
            )
            trace_data = parse_json(result_str)
            if isinstance(trace_data, dict) and "steps" in trace_data:
                trace_data.setdefault("language", lang)
                trace_data.setdefault("source", "ai_trace")
                trace_data.setdefault("visualization_type", trace_data.get("data_structure_type", "none"))
                trace_data.setdefault("algorithm", trace_data.get("algorithm", "unknown"))
                trace_data["success"] = True
                return trace_data
        except Exception as e:
            pass

        # Fallback trace if AI is offline or parsing fails
        lines = [l.strip() for l in code.strip().splitlines() if l.strip() and not l.strip().startswith("#")]
        steps = []
        for idx, line in enumerate(lines[:8]):
            steps.append({
                "step": idx + 1,
                "line": idx + 1,
                "code_snippet": line,
                "action": f"Executing: {line}",
                "variables": {"step": idx + 1},
                "pointers": {},
                "array_data": [],
                "active_indices": [],
                "explanation": f"Step {idx + 1}: Line execution"
            })

        return {
            "success": True,
            "language": lang,
            "source": "fallback_trace",
            "algorithm": detect_algorithm_type(code, steps),
            "visualization_type": "array",
            "stdout": "Executed successfully",
            "data_structure_type": "array",
            "steps": steps,
            "time_complexity": "O(N)",
            "space_complexity": "O(1)"
        }

    def get_boilerplate(self, language: str, problem_type: str = "general") -> str:
        """Get starter code boilerplate for a language."""
        lang_boilerplates = self.BOILERPLATES.get(language.lower(), {})
        return lang_boilerplates.get(problem_type, lang_boilerplates.get("general", "# Your code here"))

    def get_problem_boilerplate(self, language: str, problem_topics: List[str]) -> str:
        """Get boilerplate based on problem's topic categories."""
        lang = language.lower()
        topic_set = set(t.lower() for t in problem_topics)

        # Map problem topics to boilerplate types
        if any(t in topic_set for t in ["linked list", "linked_list", "linkedlist"]):
            return self.get_boilerplate(lang, "linked_list")
        elif any(t in topic_set for t in ["binary tree", "binary_tree", "tree", "bst"]):
            return self.get_boilerplate(lang, "binary_tree")
        elif any(t in topic_set for t in ["graph", "bfs", "dfs"]):
            return self.get_boilerplate(lang, "graph")
        elif any(t in topic_set for t in ["dynamic programming", "dp"]):
            return self.get_boilerplate(lang, "dp")
        else:
            return self.get_boilerplate(lang, "class")

    def get_supported_languages(self) -> List[Dict[str, str]]:
        """Get list of supported languages."""
        return [
            {"id": lang, "name": config["language"].title(), "version": config["version"]}
            for lang, config in self.SUPPORTED_LANGUAGES.items()
        ]

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is not None and not self._client.is_closed:
            return self._client

        if self._client_lock is None:
            self._client_lock = asyncio.Lock()

        async with self._client_lock:
            if self._client is None or self._client.is_closed:
                limits = httpx.Limits(
                    max_connections=20,
                    max_keepalive_connections=10,
                    keepalive_expiry=30.0,
                )
                timeout = httpx.Timeout(10.0, connect=5.0)
                try:
                    import h2  # noqa: F401

                    http2 = True
                except ImportError:
                    http2 = False
                self._client = httpx.AsyncClient(timeout=timeout, limits=limits, http2=http2)
        return self._client

    async def _get_semaphore(self) -> asyncio.Semaphore:
        if self._semaphore is None:
            self._semaphore = asyncio.Semaphore(12)
        return self._semaphore

    @staticmethod
    def _normalize_text(value: str) -> str:
        return "\n".join(line.rstrip() for line in (value or "").strip().splitlines())

    async def _grade_python_batched(
        self,
        source_code: str,
        test_cases: List[Dict[str, str]],
        function_name: str = "",
    ) -> Optional[Dict[str, Any]]:
        """Grade a Python submission against all test cases in ONE local
        sandbox process. Returns the standard result dict, or None if the
        local batch runner is unavailable (caller falls back to legacy path)."""
        from app.services.local_sandbox import execute_local_python_batch

        stdins = [tc.get("input", "") for tc in test_cases]
        expecteds = [
            tc.get("expected", tc.get("expected_output", "")) for tc in test_cases
        ]

        started = time.perf_counter()
        batch = await execute_local_python_batch(
            source_code, stdins, timeout=self.MAX_TIMEOUT, function_name=function_name
        )
        duration_ms = (time.perf_counter() - started) * 1000

        if not batch.get("success"):
            err = batch.get("error", "")
            if "timed out" in err.lower():
                # Real timeout → report as failed run, don't retry via Piston.
                return {
                    "success": False,
                    "error": err,
                }
            return None  # infrastructure issue → let legacy path handle it

        compile_error = batch.get("compile_error")
        if compile_error:
            return {
                "success": False,
                "error": compile_error,
            }

        per_case_ms = duration_ms / max(len(test_cases), 1)
        results = []
        for idx, ((ok, output), case) in enumerate(zip(batch["results"], test_cases)):
            is_hidden = case.get("is_hidden", False)
            expected = expecteds[idx]
            if ok:
                actual = self._normalize_text(output)
                passed = actual == self._normalize_text(expected)
            else:
                actual = output
                passed = False

            results.append({
                "test_case_index": idx + 1,
                "passed": passed,
                "is_hidden": is_hidden,
                "input": stdins[idx] if not is_hidden else "[HIDDEN]",
                "expected": expected if not is_hidden else "[HIDDEN]",
                "actual": actual if not is_hidden else "[HIDDEN]",
                "error": None if ok else actual,
                "execution_time": round(per_case_ms / 1000, 4),
            })

        await request_metrics.record(
            "compiler", "local_oracle", duration_ms=duration_ms
        )
        passed_count = sum(1 for r in results if r["passed"])
        return {
            "success": True,
            "all_passed": passed_count == len(results),
            "passed_count": passed_count,
            "total_count": len(results),
            "score": round(passed_count / len(results) * 100, 1) if results else 0,
            "summary": f"{passed_count}/{len(results)} Test Cases Passed",
            "results": results,
            "engine": "local_oracle_batch",
        }

    async def close(self):
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    async def _check_circuit_breaker(self) -> bool:
        return await compiler_breaker.allow_request()

    async def _record_success(self):
        await compiler_breaker.record_success()

    async def _record_failure(self):
        await compiler_breaker.record_failure()

    async def _try_fallback(self, language: str, code: str, stdin: str, timeout: int) -> Dict[str, Any]:
        """Run code through free remote providers (Wandbox, Glot.io) then the local
        sandbox when Piston is unavailable.

        Chain: Wandbox -> Glot.io -> local sandbox. Remote providers are gated by
        the USE_REMOTE_FALLBACKS flag; the local sandbox by USE_LOCAL_SANDBOX.
        Returns {} when every hop fails so the caller surfaces the original error.
        """
        if get_settings().USE_REMOTE_FALLBACKS:
            try:
                remote = await execute_remote_fallback(language, code, stdin, timeout)
                if remote:
                    return remote
            except Exception:
                pass
        if not get_settings().USE_LOCAL_SANDBOX:
            return {}
        if (language or "").lower() not in LOCAL_LANGUAGES:
            return {}
        try:
            result = await execute_local(code, language, stdin, timeout)
            if result.get("source") == "local_sandbox":
                return result
        except Exception:
            return {}
        return {}
