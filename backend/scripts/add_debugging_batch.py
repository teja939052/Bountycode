#!/usr/bin/env python3
"""Add high-value debugging problems to debugging_bank.json."""

import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "app" / "data" / "debugging_bank.json"

NEW_PROBLEMS = [
  {
    "id": "debug-006",
    "type": "debugging",
    "title": "Fix the Logic Error in find_max_subarray",
    "question": "This function should find the maximum sum of any contiguous subarray, but it returns wrong results for some inputs. Find and fix it.",
    "topic": "debugging",
    "sub_topic": "dynamic_programming",
    "pattern": "debugging",
    "difficulty": "medium",
    "companies": ["google", "amazon", "microsoft"],
    "provenance": "human_verified",
    "trust_status": "verified",
    "source_bank": "debugging_bank",
    "buggy_code": "def find_max_subarray(nums):\n    max_sum = 0\n    current_sum = 0\n    for num in nums:\n        current_sum += num\n        if current_sum > max_sum:\n            max_sum = current_sum\n    return max_sum",
    "correct_code": "def find_max_subarray(nums):\n    max_sum = float('-inf')\n    current_sum = 0\n    for num in nums:\n        current_sum = max(num, current_sum + num)\n        max_sum = max(max_sum, current_sum)\n    return max_sum",
    "test_cases": [
      {"input": [-2, 1, -3, 4, -1, 2, 1, -5, 4], "expected": 6},
      {"input": [1, 2, 3, 4, 5], "expected": 15},
      {"input": [-1, -2, -3, -4], "expected": -1}
    ],
    "explanation": "Kadane's algorithm requires tracking the maximum subarray ending at each position. The buggy code initializes max_sum to 0, which fails when all numbers are negative. It also doesn't reset current_sum when it becomes negative. The fix uses max(num, current_sum + num) to decide whether to start a new subarray or extend the current one.",
    "hints": [
      "Test with all negative numbers: [-5, -3, -2, -4]",
      "What should the answer be? Is it 0 or -2?",
      "The current code returns 0 for all-negative arrays",
      "Kadane's: current_sum = max(num, current_sum + num)"
    ],
    "common_trap": "Initializing max_sum to 0 instead of negative infinity. With all-negative arrays, the answer is the largest negative number, not 0.",
    "reasoning_steps": [
      "1. Understand: find contiguous subarray with maximum sum",
      "2. Test with [-5, -3, -2, -4]: expected -2, got 0",
      "3. Bug: max_sum initialized to 0, never updated for all-negative",
      "4. Bug: current_sum never resets when negative",
      "5. Fix: max_sum = -inf, current_sum = max(num, current_sum + num)"
    ]
  },
  {
    "id": "debug-007",
    "type": "debugging",
    "title": "Fix the Authentication Bypass",
    "question": "This authentication middleware should reject requests without a valid token, but it has a security flaw. Find and fix it.",
    "topic": "debugging",
    "sub_topic": "security",
    "pattern": "debugging",
    "difficulty": "hard",
    "companies": ["google", "amazon", "meta", "microsoft"],
    "provenance": "human_verified",
    "trust_status": "verified",
    "source_bank": "debugging_bank",
    "buggy_code": "def authenticate(request):\n    token = request.headers.get('Authorization')\n    if token is None:\n        return False\n    return validate_token(token)",
    "correct_code": "def authenticate(request):\n    token = request.headers.get('Authorization')\n    if token is None or token == '':\n        return False\n    if token.startswith('Bearer '):\n        token = token[7:]\n    if not token or token.isspace():\n        return False\n    return validate_token(token)",
    "test_cases": [
      {"input": "request with no Authorization header", "expected": False},
      {"input": "request with Authorization: ''", "expected": False},
      {"input": "request with Authorization: 'Bearer valid_token'", "expected": True},
      {"input": "request with Authorization: 'Bearer '", "expected": False}
    ],
    "explanation": "The buggy code only checks if token is None, but doesn't handle empty strings, whitespace-only tokens, or malformed Bearer tokens. An attacker could send an empty token or 'Bearer ' with a space, which might pass validation. The fix adds comprehensive checks for empty/whitespace tokens and properly extracts the Bearer token.",
    "hints": [
      "Check what happens with Authorization: ''",
      "Check what happens with Authorization: 'Bearer '",
      "Empty string is falsy but not None",
      "Strip whitespace from token before validation"
    ],
    "common_trap": "Only checking for None and not handling empty strings or whitespace. Authentication bugs often involve edge cases in input validation.",
    "reasoning_steps": [
      "1. Understand: reject requests without valid token",
      "2. Test with empty string: token = '' is not None, passes check",
      "3. Test with 'Bearer ': token = 'Bearer ' is not None, passes check",
      "4. validate_token might accept these malformed tokens",
      "5. Fix: check for empty/whitespace, extract Bearer token properly"
    ]
  },
  {
    "id": "debug-008",
    "type": "debugging",
    "title": "Fix the Memory Leak in Cache",
    "question": "This caching system should limit memory usage, but it grows unbounded. Find and fix it.",
    "topic": "debugging",
    "sub_topic": "data_structures",
    "pattern": "debugging",
    "difficulty": "hard",
    "companies": ["google", "amazon", "meta"],
    "provenance": "human_verified",
    "trust_status": "verified",
    "source_bank": "debugging_bank",
    "buggy_code": "class Cache:\n    def __init__(self, max_size):\n        self.max_size = max_size\n        self.cache = {}\n    \n    def get(self, key):\n        return self.cache.get(key)\n    \n    def put(self, key, value):\n        self.cache[key] = value\n        if len(self.cache) > self.max_size:\n            # Remove oldest item\n            oldest = min(self.cache.items(), key=lambda x: x[1][1])\n            del self.cache[oldest[0]]",
    "correct_code": "from collections import OrderedDict\n\nclass Cache:\n    def __init__(self, max_size):\n        self.max_size = max_size\n        self.cache = OrderedDict()\n    \n    def get(self, key):\n        if key in self.cache:\n            self.cache.move_to_end(key)\n            return self.cache[key]\n        return None\n    \n    def put(self, key, value):\n        if key in self.cache:\n            self.cache.move_to_end(key)\n        self.cache[key] = value\n        if len(self.cache) > self.max_size:\n            self.cache.popitem(last=False)",
    "test_cases": [
      {"input": "cache size=3, add 4 items", "expected": "only 3 items remain, oldest removed"},
      {"input": "get existing key", "expected": "value returned"},
      {"input": "get non-existing key", "expected": "None"}
    ],
    "explanation": "The buggy cache uses a regular dict with no eviction policy tracking. The 'oldest' logic tries to find the minimum by timestamp, but the code structure is broken: it stores (value, timestamp) tuples but the min() logic is fragile. The correct implementation uses OrderedDict which maintains insertion order and provides O(1) move_to_end and popitem operations. This is the standard LRU cache pattern.",
    "hints": [
      "Regular dicts don't maintain insertion order (in older Python)",
      "The min() logic assumes (value, timestamp) tuples",
      "What data structure maintains insertion order?",
      "OrderedDict has move_to_end() and popitem() methods"
    ],
    "common_trap": "Trying to implement LRU with a regular dict and manual timestamp tracking. Use OrderedDict for O(1) operations.",
    "reasoning_steps": [
      "1. Understand: cache with max_size should evict oldest when full",
      "2. Bug: regular dict doesn't guarantee order",
      "3. Bug: min() logic is fragile and O(n)",
      "4. Fix: use OrderedDict which maintains insertion order",
      "5. get() should move accessed item to end (most recent)",
      "6. put() should add to end, evict from front when full"
    ]
  },
  {
    "id": "debug-009",
    "type": "debugging",
    "title": "Fix the API Pagination Bug",
    "question": "This API endpoint should paginate results, but it returns duplicate items across pages. Find and fix it.",
    "topic": "debugging",
    "sub_topic": "api_design",
    "pattern": "debugging",
    "difficulty": "medium",
    "companies": ["amazon", "google", "microsoft"],
    "provenance": "human_verified",
    "trust_status": "verified",
    "source_bank": "debugging_bank",
    "buggy_code": "def get_paginated_results(items, page, page_size):\n    start = page * page_size\n    end = start + page_size\n    return items[start:end]",
    "correct_code": "def get_paginated_results(items, page, page_size):\n    if page < 1 or page_size < 1:\n        raise ValueError('Page and page_size must be positive')\n    start = (page - 1) * page_size\n    end = start + page_size\n    if start >= len(items):\n        return []\n    return items[start:end]",
    "test_cases": [
      {"input": "items=[1..10], page=1, page_size=3", "expected": [1, 2, 3]},
      {"input": "items=[1..10], page=2, page_size=3", "expected": [4, 5, 6]},
      {"input": "items=[1..10], page=0, page_size=3", "expected": "error or [1, 2, 3]"},
      {"input": "items=[1..10], page=5, page_size=3", "expected": "[]"}
    ],
    "explanation": "The buggy pagination uses 1-based page numbers but calculates start as page * page_size, which skips the first page_size items. Page 1 should start at index 0, not page_size. The fix uses (page - 1) * page_size. Additionally, the fix adds input validation and handles out-of-range pages gracefully.",
    "hints": [
      "Page 1 should return items[0:page_size]",
      "With buggy code, page 1 returns items[page_size:2*page_size]",
      "This skips the first page_size items",
      "Formula: start = (page - 1) * page_size"
    ],
    "common_trap": "Using 0-based indexing formula with 1-based page numbers. Always subtract 1 from page number when calculating start index.",
    "reasoning_steps": [
      "1. Understand: page 1 → items[0:3], page 2 → items[3:6]",
      "2. Bug: start = page * page_size",
      "3. Page 1: start = 1*3 = 3, returns items[3:6] — WRONG!",
      "4. Should be: start = (page - 1) * page_size",
      "5. Page 1: start = 0, returns items[0:3] — CORRECT",
      "6. Add validation for edge cases"
    ]
  },
  {
    "id": "debug-010",
    "type": "debugging",
    "title": "Fix the Race Condition in Counter",
    "question": "This concurrent counter should accurately count increments from multiple threads, but it produces wrong results. Find and fix it.",
    "topic": "debugging",
    "sub_topic": "concurrency",
    "pattern": "debugging",
    "difficulty": "hard",
    "companies": ["google", "amazon", "meta"],
    "provenance": "human_verified",
    "trust_status": "verified",
    "source_bank": "debugging_bank",
    "buggy_code": "class Counter:\n    def __init__(self):\n        self.value = 0\n    \n    def increment(self):\n        current = self.value\n        self.value = current + 1\n    \n    def get_value(self):\n        return self.value",
    "correct_code": "import threading\n\nclass Counter:\n    def __init__(self):\n        self.value = 0\n        self.lock = threading.Lock()\n    \n    def increment(self):\n        with self.lock:\n            self.value += 1\n    \n    def get_value(self):\n        with self.lock:\n            return self.value",
    "test_cases": [
      {"input": "10 threads, each increment 1000 times", "expected": 10000},
      {"input": "2 threads, each increment 500 times", "expected": 1000}
    ],
    "explanation": "The buggy counter has a race condition: read-modify-write is not atomic. Two threads can read the same value, increment it, and write back the same result, losing one increment. The fix uses a lock to make the increment operation atomic. This is a classic lost-update problem in concurrent programming.",
    "hints": [
      "Thread A reads value=5",
      "Thread B reads value=5",
      "Thread A writes value=6",
      "Thread B writes value=6 — one increment lost!"
    ],
    "common_trap": "Thinking read-modify-write is atomic. It's not. Always use locks or atomic operations for shared mutable state.",
    "reasoning_steps": [
      "1. Understand: multiple threads incrementing shared counter",
      "2. Operation: read value, add 1, write back",
      "3. Race: Thread A reads 5, Thread B reads 5",
      "4. Thread A writes 6, Thread B writes 6",
      "5. Result: 6 instead of 7 — lost update!",
      "6. Fix: use lock to make read-modify-write atomic"
    ]
  },
  {
    "id": "debug-011",
    "type": "debugging",
    "title": "Fix the JSON Serialization Error",
    "question": "This API should return JSON, but it crashes when serializing certain objects. Find and fix it.",
    "topic": "debugging",
    "sub_topic": "api_design",
    "pattern": "debugging",
    "difficulty": "medium",
    "companies": ["amazon", "google", "microsoft"],
    "provenance": "human_verified",
    "trust_status": "verified",
    "source_bank": "debugging_bank",
    "buggy_code": "def get_user_response(user):\n    return {\n        'id': user.id,\n        'name': user.name,\n        'email': user.email,\n        'created_at': user.created_at,\n        'is_active': user.is_active\n    }",
    "correct_code": "from datetime import datetime\n\ndef get_user_response(user):\n    return {\n        'id': str(user.id),\n        'name': user.name,\n        'email': user.email,\n        'created_at': user.created_at.isoformat() if isinstance(user.created_at, datetime) else str(user.created_at),\n        'is_active': bool(user.is_active)\n    }",
    "test_cases": [
      {"input": "user with datetime created_at", "expected": "ISO format string"},
      {"input": "user with string created_at", "expected": "string"},
      {"input": "user with ObjectId id", "expected": "string representation"}
    ],
    "explanation": "The buggy code assumes all fields are JSON-serializable. But datetime objects and ObjectIds are not natively serializable by json.dumps(). The fix explicitly converts non-serializable types: datetime to ISO format string, ObjectId to string, booleans to bool. In production, use a proper serializer like Pydantic or Marshmallow.",
    "hints": [
      "datetime objects are not JSON-serializable",
      "MongoDB ObjectIds need explicit conversion",
      "json.dumps() will raise TypeError for datetime",
      "Use .isoformat() for datetime, str() for ObjectId"
    ],
    "common_trap": "Assuming all Python objects are JSON-serializable. Always check datetime, date, Decimal, ObjectId, bytes.",
    "reasoning_steps": [
      "1. Understand: API returns JSON-serializable dict",
      "2. Crash: json.dumps() raises TypeError on datetime",
      "3. Bug: created_at is datetime, not serializable",
      "4. Bug: id might be ObjectId, not serializable",
      "5. Fix: convert datetime to ISO format, ObjectId to str"
    ]
  }
]

def main():
    data = json.loads(BASE.read_text())
    data.extend(NEW_PROBLEMS)
    BASE.write_text(json.dumps(data, indent=2))
    print(f"Added {len(NEW_PROBLEMS)} debugging problems. Total: {len(data)}")

if __name__ == "__main__":
    main()
