import sys, json
sys.path.insert(0, r"D:\Project-Fremen\backend")
from scripts.content_factory import ContentGate

gate = ContentGate()

# Two Sum - candidate solution
def two_sum_solution(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        comp = target - num
        if comp in seen:
            return [seen[comp], i]
        seen[num] = i
    return []

# Independent oracle (brute force, different implementation)
def two_sum_oracle(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []

tests = [
    {"input": ([2, 7, 11, 15], 9), "expected": [0, 1]},
    {"input": ([3, 2, 4], 6), "expected": [1, 2]},
    {"input": ([3, 3], 6), "expected": [0, 1]},
]
edge = [
    {"input": ([-1, -2, -3, -4, -5], -8), "expected": [2, 4]},
    {"input": ([0, 4, 3, 0], 0), "expected": [0, 3]},
]

report = gate.verify(
    question_id="tcstest-001",
    title="Two Sum: find indices of two numbers adding to target",
    difficulty="easy",
    topic="arrays",
    skill="hashing",
    solution_fn=two_sum_solution,
    oracle_fn=two_sum_oracle,
    tests=tests,
    edge_cases=edge,
)
print(json.dumps(report, indent=2) if report else "no report")
import json
print("PUBLISHED:", report.get("published"), "candidate_pass:", report.get("candidate_pass"), "total:", report.get("tests_total"))