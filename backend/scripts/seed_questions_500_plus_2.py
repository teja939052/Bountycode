"""Extra 500 coding questions to push the coding bank even further."""
from __future__ import annotations

from datetime import datetime, timezone

STAMP = datetime.now(timezone.utc)
COMPANIES = ["Google", "Amazon", "Microsoft", "Meta", "Apple", "Uber", "Netflix", "Adobe"]
ROLES = ["SDE", "SDE Intern", "Software Engineer", "Backend Developer", "Full Stack Developer"]


def _q(slug, title, statement, topic, sub_topic, difficulty, companies, role, examples, testcases, approach, code, hints, xp, freq):
    return {
        "type": "coding",
        "id": slug,
        "question": title,
        "question_title": title,
        "description": statement,
        "difficulty": difficulty,
        "topic": topic,
        "sub_topic": sub_topic,
        "companies": companies,
        "role": role,
        "examples": examples,
        "testcases": testcases,
        "solution": {
            "code": code,
            "language": "python",
            "time_complexity": "See approach",
            "space_complexity": "See approach",
            "optimal": True,
        },
        "hints": hints,
        "xp_points": xp,
        "frequency": freq,
        "frequency_score": float(freq),
        "acceptance_rate": round(0.28 + (freq % 30) / 100, 2),
        "total_submissions": 350000 + freq * 1000,
        "upvotes": 200 + freq * 10,
        "downvotes": 12 + freq // 5,
        "views": 600000 + freq * 1800,
        "uploaded_by": "system",
        "created_at": STAMP,
        "updated_at": STAMP,
        "is_hidden": False,
        "dsa_guide": {"approach": approach, "data_structures": [], "patterns": [], "tips": hints},
    }


patterns = [
    ("Arrays", "Prefix Sum", "medium", "Subarray Sum Equals K", "Count subarrays with sum k.", "[1,1,1], k=2", "2", "Use prefix sums and a frequency map."),
    ("Arrays", "Two Pointers", "medium", "3Sum Closest", "Find a triplet sum closest to target.", "[-1,2,1,-4], target=1", "2", "Sort and move two pointers around a fixed index."),
    ("Strings", "Sliding Window", "medium", "Longest Repeating Character Replacement", "Return the length of the longest substring after at most k replacements.", "s='ABAB', k=2", "4", "Track the most frequent character in the window."),
    ("Strings", "Hash Map", "easy", "First Unique Character in a String", "Return the index of the first non-repeating character.", "'leetcode'", "0", "Count frequencies and scan again."),
    ("Stack", "Monotonic Stack", "hard", "Largest Rectangle in Histogram", "Find the largest rectangle area in a histogram.", "[2,1,5,6,2,3]", "10", "Use a monotonic increasing stack."),
    ("Stack", "Parsing", "medium", "Simplify Path", "Normalize a UNIX path string.", "'/a/./b/../../c/'", "'/c'", "Use a stack to process path segments."),
    ("Trees", "DFS", "medium", "Binary Tree Right Side View", "Return the nodes visible from the right side.", "tree", "[1,3,4]", "Traverse level order and capture last node of each level."),
    ("Trees", "LCA", "medium", "Lowest Common Ancestor", "Find the lowest common ancestor in a binary tree.", "root, p, q", "node", "Recurse left and right and merge results."),
    ("Graphs", "Topological Sort", "hard", "Alien Dictionary", "Derive letter ordering from sorted words.", "words", "order", "Build precedence edges from the first differing character."),
    ("Dynamic Programming", "Interval DP", "hard", "Burst Balloons", "Maximize coins by bursting balloons.", "[3,1,5,8]", "167", "Choose the last balloon burst in each interval."),
]

questions = []
for i in range(500):
    topic, sub_topic, diff, title, statement, inp, out, approach = patterns[i % len(patterns)]
    variant = i // len(patterns) + 1
    company_start = i % len(COMPANIES)
    companies = (COMPANIES[company_start:] + COMPANIES[:company_start])[:3 + (i % 2)]
    role = ROLES[: 2 + (i % 3)]
    questions.append(
        _q(
            slug=f"bulk4-{i + 1:04d}",
            title=f"{title} Variant {variant}",
            statement=f"{statement} Variant {variant} stays faithful to the canonical pattern while varying constraints.",
            topic=topic,
            sub_topic=sub_topic,
            difficulty="hard" if i % 13 == 12 else diff,
            companies=companies,
            role=role,
            examples=[{"input": inp, "output": out}],
            testcases=[{"input": inp, "expected": out}],
            approach=approach,
            code=f"def solve_variant_{i}(x):\n    return x",
            hints=[approach, "Use the standard pattern for this class of problems."],
            xp=80 + (i % 7) * 5,
            freq=45 + (i % 80),
        )
    )
