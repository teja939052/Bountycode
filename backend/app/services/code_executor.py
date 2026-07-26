import httpx
import asyncio
from typing import Dict, Any, List, Optional


class CodeExecutionEngine:
    """
    Production code execution engine using Piston API.
    Executes code in isolated sandbox environment.
    """

    PISTON_URL = "https://emkc.org/api/v2/piston/execute"

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
        lang = language.lower()
        if lang not in self.SUPPORTED_LANGUAGES:
            return {
                "success": False,
                "error": f"Language '{language}' not supported",
                "supported_languages": list(self.SUPPORTED_LANGUAGES.keys()),
            }

        lang_config = self.SUPPORTED_LANGUAGES[lang]
        filename = f"main.{lang_config['extension']}"

        payload = {
            "language": lang_config["language"],
            "version": lang_config["version"],
            "files": [{"name": filename, "content": code}],
            "stdin": stdin,
        }

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(self.PISTON_URL, json=payload)

                if response.status_code != 200:
                    return {
                        "success": False,
                        "error": f"Piston API error: {response.status_code}",
                    }

                result = response.json()

            # Parse output
            run_output = result.get("run", {})
            compile_output = result.get("compile", {})

            stdout = run_output.get("output", "")
            stderr = run_output.get("stderr", "")
            exit_code = run_output.get("code", 1)

            return {
                "success": exit_code == 0,
                "exit_code": exit_code,
                "stdout": stdout.strip(),
                "stderr": stderr.strip(),
                "compile_error": compile_output.get("stderr", "") if compile_output.get("code", 0) != 0 else None,
                "language": language,
                "execution_time": run_output.get("time", 0),
                "memory_usage": run_output.get("memory", 0),
            }

        except httpx.TimeoutException:
            return {
                "success": False,
                "error": "Code execution timed out (possible infinite loop)",
                "hint": "Check for infinite loops or very long-running operations",
            }
        except httpx.RequestError as e:
            return {
                "success": False,
                "error": f"Network error: {str(e)}",
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Execution failed: {str(e)}",
            }

    async def execute_against_test_cases(
        self,
        source_code: str,
        language: str,
        test_cases: List[Dict[str, str]],
    ) -> Dict[str, Any]:
        """
        Execute code against multiple test cases.
        Returns pass/fail for each test case.
        """
        lang = language.lower()
        if lang not in self.SUPPORTED_LANGUAGES:
            return {
                "success": False,
                "error": f"Language '{language}' is not supported",
                "supported_languages": list(self.SUPPORTED_LANGUAGES.keys()),
            }

        results = []
        all_passed = True
        passed_count = 0

        for idx, case in enumerate(test_cases):
            stdin = case.get("input", "")
            expected = case.get("expected", case.get("expected_output", ""))
            is_hidden = case.get("is_hidden", False)

            execution = await self.execute_code(source_code, language, stdin)

            if execution["success"]:
                actual = execution["stdout"].strip()
                passed = actual == expected.strip()
                if passed:
                    passed_count += 1
                else:
                    all_passed = False
            else:
                actual = execution.get("error", "Execution failed")
                passed = False
                all_passed = False

            results.append({
                "test_case_index": idx + 1,
                "passed": passed,
                "is_hidden": is_hidden,
                "input": stdin if not is_hidden else "[HIDDEN]",
                "expected": expected if not is_hidden else "[HIDDEN]",
                "actual": actual if not is_hidden else "[HIDDEN]",
                "error": execution.get("error") if not execution["success"] else None,
                "execution_time": execution.get("execution_time", 0),
            })

        return {
            "success": True,
            "all_passed": all_passed,
            "passed_count": passed_count,
            "total_count": len(test_cases),
            "score": round(passed_count / len(test_cases) * 100, 1) if test_cases else 0,
            "summary": f"{passed_count}/{len(test_cases)} Test Cases Passed",
            "results": results,
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
