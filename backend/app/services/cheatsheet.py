from typing import Dict, Any, List
from app.services.ai import chat_completion, parse_json


class CheatSheetGenerator:
    """Generate interview survival cheat sheets for last-minute review."""

    # Company-specific biases (algorithmic, no LLM cost)
    COMPANY_BIASES = {
        "google": {
            "focus": "Time complexity optimization. They run hidden test cases with large inputs.",
            "must_know": ["Graph algorithms", "Dynamic programming", "System design trade-offs"],
            "boilerplate": "import sys\nsys.setrecursionlimit(10000)",
            "pitfalls": ["Integer overflow on large arrays", "Off-by-one errors in binary search"],
        },
        "amazon": {
            "focus": "Leadership Principles integration. Every answer must tie to LPs.",
            "must_know": ["STAR method", "Customer Obsession", "Ownership principle"],
            "boilerplate": "# Always start with the customer impact",
            "pitfalls": ["Not quantifying results", "Using 'we' instead of 'I'"],
        },
        "meta": {
            "focus": "Product sense + coding. Think about user impact.",
            "must_know": ["Graph traversal", "System design scale", "Product metrics"],
            "boilerplate": "# Consider: How would this scale to 1B users?",
            "pitfalls": ["Ignoring edge cases", "Not discussing trade-offs"],
        },
        "tcs": {
            "focus": "Basic programming + aptitude. Clear fundamentals.",
            "must_know": ["Basic syntax", "Pattern printing", "Simple logic"],
            "boilerplate": "# Keep it simple and readable",
            "pitfalls": ["Overcomplicating solutions", "Syntax errors"],
        },
    }

    # Topic-specific quick implementations
    TOPIC_IMPLEMENTATIONS = {
        "sliding_window": {
            "pattern": "Use two pointers to maintain a window",
            "template": """def sliding_window(nums, k):
    window_start = 0
    window_sum = 0
    max_sum = 0
    
    for window_end in range(len(nums)):
        window_sum += nums[window_end]
        
        if window_end >= k - 1:
            max_sum = max(max_sum, window_sum)
            window_sum -= nums[window_start]
            window_start += 1
    
    return max_sum""",
            "time": "O(n)",
            "space": "O(1)",
        },
        "fast_slow_pointer": {
            "pattern": "Two pointers moving at different speeds",
            "template": """def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False""",
            "time": "O(n)",
            "space": "O(1)",
        },
        "binary_search": {
            "pattern": "Eliminate half the search space each step",
            "template": """def binary_search(nums, target):
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1""",
            "time": "O(log n)",
            "space": "O(1)",
        },
        "bfs": {
            "pattern": "Level-by-level traversal using queue",
            "template": """from collections import deque

def bfs(root):
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        node = queue.popleft()
        result.append(node.val)
        
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    
    return result""",
            "time": "O(n)",
            "space": "O(n)",
        },
        "dfs": {
            "pattern": "Deep traversal using recursion or stack",
            "template": """def dfs(node, result=None):
    if result is None:
        result = []
    if not node:
        return result
    
    result.append(node.val)
    dfs(node.left, result)
    dfs(node.right, result)
    return result""",
            "time": "O(n)",
            "space": "O(h)",
        },
    }

    async def generate_cheatsheet(self, company: str, topic: str) -> Dict[str, Any]:
        """Generate a single-page interview survival cheat sheet."""
        company_bias = self.COMPANY_BIASES.get(company.lower(), self.COMPANY_BIASES.get("google", {}))
        topic_impl = self.TOPIC_IMPLEMENTATIONS.get(topic.lower(), {})

        # Build the cheat sheet with algorithmic content + LLM enhancement
        system_prompt = (
            "You are creating a last-minute interview cheat sheet. "
            "Make it extremely scannable - bullet points, code snippets, no paragraphs. "
            "Students will read this 15 minutes before their interview. "
            "Return valid JSON with structured sections."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"""Create a cheat sheet for {company} interview, focusing on {topic}.

Company bias: {company_bias.get('focus', 'General best practices')}
Must-know concepts: {', '.join(company_bias.get('must_know', []))}
Common pitfalls: {', '.join(company_bias.get('pitfalls', []))}

Include:
1. Quick pattern recognition (when to use what)
2. Template code (copy-paste ready)
3. Time/space complexity
4. Edge cases to mention
5. Company-specific tips"""},
        ]

        response = await chat_completion(messages)
        llm_result = parse_json(response)

        # Merge algorithmic + LLM content
        return {
            "company": company,
            "topic": topic,
            "company_bias": company_bias.get("focus", ""),
            "boilerplate": company_bias.get("boilerplate", ""),
            "must_know": company_bias.get("must_know", []),
            "common_pitfalls": company_bias.get("pitfalls", []),
            "implementations": {
                topic: topic_impl.get("template", "No template available")
            } if topic_impl else {},
            "quick_tips": llm_result.get("quick_tips", llm_result.get("tips", [])),
            "edge_cases": llm_result.get("edge_cases", []),
            "what_to_say": llm_result.get("what_to_say", "Explain your approach before coding"),
        }

    def get_quick_implementations(self, topics: List[str]) -> Dict[str, str]:
        """Get copy-paste code templates for multiple topics."""
        return {
            topic: self.TOPIC_IMPLEMENTATIONS.get(topic, {}).get("template", "")
            for topic in topics
        }
