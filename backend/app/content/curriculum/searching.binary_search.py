"""Lesson module — Binary Search"""
from typing import Dict, Any

LESSON: Dict[str, Any] = {
            'lesson_id': 'searching.binary_search',
            'module_id': 'searching.binary.binary_search',
            'title': 'Binary Search',
            'description': 'Halve the search space each step on sorted data.',
            'difficulty': 'medium',
            'est_minutes': 20,
            'xp_reward': 100,
            'skills_taught': ['Binary Search'],
            'srs_concept_tag': 'searching.binary.binary_search',
            'domain': 'searching',
            'captain_byte': {
            'intro': 'Welcome to Binary Search. This is a core searching concept for placement prep. Follow the steps carefully.',
            'correct': ['Exactly right!', 'Perfect!', 'You have got it!'],
            'wrong': ['Not quite. Review the step and try again.', 'Close! Think about what the concept really means.'],
            'after_break': 'Now you see the broken assumption. Repair it and move on.',
            'after_mastery': 'You have mastered Binary Search. This will appear in your next test.',
            'retry_prompt': 'Give it another shot. You are close.'
        },
            'story_context': {
            'title': 'Binary Search',
            'narration': 'Halve the search space each step on sorted data.',
            'setting': 'binary_search',
            'character': 'Captain Byte',
            'intro_text': 'Halve the search space each step on sorted data.'
        },
            'steps': {
            'discover': {
            'prompt': 'A sorted list of 1 000 000 names is given. Find a name with at most 20 checks.',
            'question': 'Which algorithm makes this possible?',
            'options': ['Binary search', 'Linear search', 'Interpolation search', 'Hash lookup'],
            'interaction_kind': 'mcq_read'
        },
            'manipulate': {
            'prompt': 'Given lo=0, hi=7, what is mid? After discarding the left half, what is the new hi?',
            'answer': 'mid=3, hi=3',
            'hint': 'mid = (lo + hi) // 2. If target is bigger, lo = mid + 1.',
            'interaction_kind': 'numeric_input'
        },
            'predict': {
            'prompt': 'For a sorted list of length 16, what is the maximum number of comparisons in binary search?',
            'answer': '4',
            'options': ['2', '4', '8', '16'],
            'interaction_kind': 'mcq_bottleneck'
        },
            'build': {
            'prompt': 'Write binary search returning the index or -1.',
            'answer': 'def search(nums, target):\n    lo, hi = 0, len(nums)-1\n    while lo <= hi:\n        mid = (lo+hi)//2\n        if nums[mid] == target:\n            return mid\n        elif nums[mid] < target:\n            lo = mid + 1\n        else:\n            hi = mid - 1\n    return -1',
            'explanation': 'Use <= so a one-element range is reachable.',
            'interaction_kind': 'code_build'
        },
            'break_step': {
            'prompt': 'Why does `while lo < hi` fail for nums=[5], target=5?',
            'broken_code': 'lo, hi = 0, 0\nwhile lo < hi:\n    mid = (lo+hi)//2\n    print(nums[mid])',
            'expected_failure': 'Loop never executes for a single-element list.',
            'interaction_kind': 'mcq_diagnose'
        },
            'debug': {
            'prompt': 'Fix the off-by-one that can miss the first element.',
            'correct_code': 'lo, hi = 0, len(nums)-1\nwhile lo <= hi:\n    mid = (lo+hi)//2\n    if nums[mid] == target:\n        return mid\n    elif nums[mid] < target:\n        lo = mid + 1\n    else:\n        hi = mid - 1\nreturn -1',
            'interaction_kind': 'code_fix'
        },
            'retrieval': {
            'prompt': 'Why must the input be sorted for binary search?',
            'answer': 'Because ordering guarantees which half to discard.',
            'alternative': ['Sorted order lets you eliminate half the items each step.'],
            'interaction_kind': 'recall_formula'
        },
            'transfer': {
            'prompt': 'Find the first occurrence of target in a list with duplicates.',
            'answer': 'ans = -1\nwhile lo <= hi:\n    mid = (lo+hi)//2\n    if nums[mid] == target:\n        ans = mid\n        hi = mid - 1\n    elif nums[mid] < target:\n        lo = mid + 1\n    else:\n        hi = mid - 1\nprint(ans)',
            'explanation': 'After a match, continue searching left.',
            'interaction_kind': 'code_build'
        }
        },
            'practice': [{
            'kind': 'mcq',
            'prompt': 'What is the worst-case complexity of binary search?',
            'answer': 'O(log n)',
            'options': ['O(n)', 'O(log n)', 'O(1)', 'O(n log n)'],
            'explanation': 'Halving each step gives logarithmic time.',
            'difficulty': 'medium',
            'company_tags': ['tcs', 'infosys']
        }, {
            'kind': 'code',
            'prompt': 'Return first occurrence of target in sorted list.',
            'starter': 'nums = [1,2,3,3,3,4,5]\ntarget = 3',
            'answer': 'See transfer answer.',
            'language': ['tcs'],
            'difficulty': 'medium',
            'company_tags': ['tcs', 'infosys', 'wipro']
        }],
            'proof': [{
            'id': 'p1-maximum_comparisons_for_n=1024?',
            'prompt': 'Maximum comparisons for n=1024?',
            'answer_format': 'numeric',
            'correct': '10',
            'explanation': 'log2(1024)=10.',
            'time_limit_seconds': 60,
            'company_tags': ['tcs']
        }],
            'company_variants': [],
            'misconceptions': [{
            'code': 'coding_state_trace_error',
            'signature': 'Student loses track of index boundaries during search.',
            'reteach_route': 'visual_state',
            'reteach_action': 'trace_state_step_by_step'
        }],
            'srs_key_points': ['Binary search halves the search space each step.', 'Requires sorted input and inclusive loop bounds.', 'Worst case is O(log n).'],
            'srs_review_intervals': [1, 3, 7, 14, 30],
            'world_progression': {
            'world_id': 'searching',
            'competency_id': 'binary_search',
            'unlocks_next': [],
            'tower_badge': 'searching_binary_search'
        }
        }

SLUG = 'searching.binary_search'
