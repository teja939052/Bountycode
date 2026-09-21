import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.services.auto_verify import _run_python_tests

# sw_001 solution
code_001 = """def max_avg_subarray(nums, k):
    window_sum = sum(nums[:k])
    max_sum = window_sum
    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i-k]
        max_sum = max(max_sum, window_sum)
    return max_sum / k"""

# sw_004 solution  
code_004 = """from collections import defaultdict
def longest_substring_k_distinct(s, k):
    char_count = defaultdict(int)
    left = 0
    max_len = 0
    for right in range(len(s)):
        char_count[s[right]] += 1
        while len(char_count) > k:
            char_count[s[left]] -= 1
            if char_count[s[left]] == 0:
                del char_count[s[left]]
            left += 1
        max_len = max(max_len, right - left + 1)
    return max_len"""

# Test cases for sw_001
tcs_001 = [
    {"input": "[1,12,-5,-6,50,3]\n4", "output": "12.75", "hidden": False},
    {"input": "[5]\n1", "output": "5.0", "hidden": False},
    {"input": "[-1,-2,-3,-4]\n2", "output": "-1.5", "hidden": False},
    {"input": "[0,4,0,3,2]\n1", "output": "4.0", "hidden": True},
    {"input": "[1,0,0,0,1]\n4", "output": "0.5", "hidden": True},
]

# Test cases for sw_004
tcs_004 = [
    {"input": '"eceba"\n2', "output": "3", "hidden": False},
    {"input": '"aaa"\n1', "output": "3", "hidden": False},
    {"input": '"abcbbbb"\n2', "output": "5", "hidden": True},
    {"input": '""\n1', "output": "0", "hidden": True},
]

q_001 = {"id": "sw_001", "solution": {"code": code_001}, "test_cases": tcs_001}
q_004 = {"id": "sw_004", "solution": {"code": code_004}, "test_cases": tcs_004}

print("=== sw_001 ===")
passed, reason, p, t = _run_python_tests(q_001)
print(f"Passed: {p}/{t}, Reason: {reason}")

print()
print("=== sw_004 ===")
passed, reason, p, t = _run_python_tests(q_004)
print(f"Passed: {p}/{t}, Reason: {reason}")
