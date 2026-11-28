# 06 ARRAYS AND SORTING JOURNEY

**BountyCode — Phase 2 Design Freeze**
**Status: Design-only document**
**No application code written**

---

## 1. Purpose

Design a complete interactive learning journey for Arrays and Sorting using the
seven-beat instructional framework (Feel → Discover → Predict → Build → Break →
Debug → Retrieve → Transfer). This is a reference example demonstrating how the
architecture works for one skill domain.

This is a design document. No implementation is authorized.

---

## 2. Skill and Prerequisites

| Field | Value |
|-------|-------|
| Canonical skill ID | `dsa.arrays` |
| Skill name | Arrays |
| Domain | `dsa` |
| Prerequisites | `coding.loops`, `coding.variables` |
| Prerequisite status required | Competent (level 3+) |
| Estimated total time | 90–120 minutes |
| Interaction templates used | `select`, `manipulate`, `predict`, `trace`, `arrange`, `fill`, `debug` |

### 2.1 Misconception Mappings

| Misconception ID | Description | Evidence Trigger |
|-----------------|-------------|-----------------|
| `ZERO_BASED_INDEX_CONFUSION` | Student thinks arrays start at index 1 | Accesses `arr[1]` as first element |
| `LOOP_BOUNDARY_OFF_BY_ONE` | Loop goes one step too far or not far enough | `i <= len(arr)` instead of `i < len(arr)` |
| `POINTER_MOVEMENT_REVERSED` | Moves wrong pointer in two-pointer technique | Moves right when should move left |

---

## 3. Seven-Beat Journey Map

| Beat | Stage | Interaction Type | Student Action | Validation | Captain Byte Role |
|------|-------|-----------------|----------------|------------|-------------------|
| Feel | Challenge prompt | `select` | Attempt to find a pair in [3, 7, 2, 9, 1] summing to 10 without explanation | Server checks if pair found | "Try it first — no hints yet." |
| Discover | Array traversal | `manipulate` | Move a pointer through an array, printing each element | Each element visited exactly once | "Watch how the pointer visits every element." |
| Predict | Two-pointer setup | `predict` | Predict which pointer moves when sum < target | Compare with committed answer | "Make your guess before we run it." |
| Build | Two-pointer implementation | `fill` | Complete missing code in two-sum function | Hidden test cases pass | "You're doing the build — I'm just watching." |
| Break | Boundary test | `debug` | Find the input that breaks a buggy two-pointer implementation | Identifies unsorted input or empty array | "Can you break this? Find where it fails." |
| Debug | Fix buggy code | `debug` | Fix the boundary condition in broken code | All test cases pass | "You found the bug. Now fix it." |
| Transfer | Changed context | `transfer` | Apply two-pointer to container-with-most-water problem | Independent solution | "Same idea, different problem. Show me." |
| Retrieve | SRS review | `select` / `predict` | Review two-pointer rule after 1 day and 1 week | Correct without hints | "Remember this from earlier?" |
| Sort | Bubble sort | `manipulate` | Move adjacent elements to sort ascending | Each pass bubbles largest to end | "Watch how the largest bubbles to the right." |

---

## 4. Detailed Interaction Specifications

### 4.1 Beat 1 — Feel: Find a Pair

**Setup:**
```
Array: [3, 7, 2, 9, 1]
Target: 10
```

**Student action:** Select two numbers from the array that sum to 10.

**Validation:** Server checks if selected indices `i != j` and `arr[i] + arr[j] == target`.

**Expected outcomes:**
- Student finds (3, 7) at indices (0, 1) → correct
- Student finds (1, 9) at indices (4, 3) → correct
- Student selects same element twice → invalid
- Student selects pair that doesn't sum to 10 → incorrect

**Captain Byte:** "Try it first. Pick any two numbers that add to 10. No hints — just see what happens."

**Evidence emitted:**
```json
{
  "interaction_type": "select",
  "task_novelty": "guided",
  "correct": true/false,
  "first_committed_answer": "[3, 7]",
  "hints_used": 0,
  "scaffolding_level": "none"
}
```

### 4.2 Beat 2 — Discover: Pointer Traversal

**Setup:** Array `[10, 20, 30, 40, 50]`, pointer at index 0.

**Student action:** Move the pointer right one step at a time, observing each element.

**Validation:** Each element visited exactly once; pointer stops at last element.

**Expected outcomes:**
- Student visits all 5 elements in order → correct
- Student skips an element → incorrect
- Student moves pointer left (backward) → allowed but flagged

**Captain Byte:** "Watch the pointer. Each step visits one element. No element is visited twice."

**Evidence emitted:**
```json
{
  "interaction_type": "manipulate",
  "operation_sequence": ["move_right", "move_right", "move_right", "move_right"],
  "elements_visited": [10, 20, 30, 40, 50],
  "correct": true,
  "hints_used": 0
}
```

### 4.3 Beat 3 — Predict: Pointer Movement Rule

**Setup:** Sorted array `[1, 4, 6, 8]`, target `10`, left at index 0 (value 1), right at index 3 (value 8). Sum = 9 < 10.

**Student action:** Predict which pointer moves: left or right?

**Validation:** Compare committed answer with `left` (because sum < target, move left right).

**Expected outcomes:**
- Student predicts "left" → correct
- Student predicts "right" → incorrect (would make sum smaller)
- Student predicts "both" → incorrect

**Captain Byte:** "The sum is 9, which is less than 10. We need a bigger sum. Which pointer should move?"

**Misconception:** `POINTER_MOVEMENT_REVERSED` — student thinks moving right pointer left makes sum bigger.

**Evidence emitted:**
```json
{
  "interaction_type": "predict",
  "first_committed_answer": "left",
  "correct": true,
  "hints_used": 0,
  "scaffolding_level": "none"
}
```

### 4.4 Beat 4 — Build: Two-Sum Implementation

**Setup:** Sorted array, target value. Starter code:

```python
def two_sum(nums, target):
    left = 0
    right = len(nums) - 1
    # TODO: complete the loop
    return None
```

**Student action:** Fill in the while loop and pointer movement logic.

**Validation:** Hidden test cases:
- `[1, 2, 4, 6, 8]`, target `10` → `[1, 3]` (indices of 2 and 8)
- `[1, 2, 4, 8]`, target `20` → `None`
- `[]`, target `5` → `None`
- `[5]`, target `10` → `None`

**Expected outcomes:**
- All test cases pass → correct, mastery evidence
- Some test cases fail → incorrect, specific feedback on which case failed
- Infinite loop (pointer never moves) → detected by test timeout, incorrect

**Captain Byte:** "You're writing the code now. I'll check it against hidden tests when you submit."

**Evidence emitted:**
```json
{
  "interaction_type": "fill",
  "test_cases_passed": 3,
  "test_cases_total": 4,
  "correct": true,
  "hints_used": 1,
  "scaffolding_level": "partial"
}
```

### 4.5 Beat 5 — Break: Find the Breaking Input

**Setup:** Buggy two-pointer implementation that assumes sorted input:

```python
def two_sum_buggy(nums, target):
    left = 0
    right = len(nums) - 1
    while left < right:
        s = nums[left] + nums[right]
        if s == target:
            return [left, right]
        elif s < target:
            left += 1
        else:
            right -= 1
    return None
```

**Student action:** Find an input array where this code gives the wrong answer.

**Validation:** Student submits `[4, 1, 8, 2]`, target `6`. Code returns wrong pair or misses it because array is unsorted.

**Expected outcomes:**
- Student provides unsorted array → correct (breaks precondition)
- Student provides sorted array that works → incorrect (didn't break it)
- Student provides empty array → incorrect (edge case, not the core bug)

**Captain Byte:** "This code has a hidden assumption. Can you find an input where it breaks?"

**Evidence emitted:**
```json
{
  "interaction_type": "debug",
  "breaking_input": [4, 1, 8, 2],
  "target": 6,
  "correct": true,
  "explanation": "Array must be sorted for two-pointer to work"
}
```

### 4.6 Beat 6 — Debug: Fix the Code

**Setup:** Same buggy code, but now with boundary issue:

```python
def two_sum(nums, target):
    left = 0
    right = len(nums)  # BUG: should be len(nums) - 1
    while left < right:
        ...
```

**Student action:** Fix the boundary condition.

**Validation:** All test cases pass including single-element and two-element arrays.

**Expected outcomes:**
- Student changes `right = len(nums)` to `right = len(nums) - 1` → correct
- Student changes loop condition incorrectly → incorrect

**Captain Byte:** "You found where it breaks. Now fix it."

**Evidence emitted:**
```json
{
  "interaction_type": "debug",
  "fix_applied": "right = len(nums) - 1",
  "test_cases_passed": 4,
  "test_cases_total": 4,
  "correct": true
}
```

### 4.7 Beat 7 — Transfer: Container With Most Water

**Setup:** Array of heights `[1, 8, 6, 2, 5, 4, 8, 3, 7]`. Find two lines that together with x-axis form a container holding most water.

**Student action:** Apply two-pointer technique to maximize `min(height[i], height[j]) * (j - i)`.

**Validation:** Independent solution — no starter code, no hints unless requested.

**Expected outcomes:**
- Student computes correct maximum area (49) → correct, transfer_capable
- Student uses O(n²) approach → correct answer but not transfer of technique (note: technique not applied)
- Student can't solve → incorrect, needs more practice

**Captain Byte:** "Same idea, new problem. Two pointers on sorted data helped before. Here the data isn't sorted, but the idea of converging pointers still works. Show me."

**Evidence emitted:**
```json
{
  "interaction_type": "transfer",
  "task_novelty": "independent",
  "correct": true,
  "hints_used": 0,
  "scaffolding_level": "none"
}
```

### 4.8 Beat 8 — Retrieve: SRS Review

**Setup:** One day later, student logs in. SRS identifies `dsa.two_pointers` as due for review.

**Student action:** Answer a predictive question: "When sum < target in a sorted array, which pointer moves?"

**Validation:** Correct without hints.

**Expected outcomes:**
- Correct without hints → retention confirmed, next review scheduled further out
- Correct with hints → partial retention, review sooner
- Incorrect → needs_review, repair scheduled

**Captain Byte:** "Remember this from earlier? When the sum is too small, which pointer moves?"

**Captain Byte:** "Remember this from earlier? When the sum is too small, which pointer moves?"

**Evidence emitted:**
```json
{
  "interaction_type": "select",
  "task_novelty": "guided",
  "correct": true,
  "hints_used": 0,
  "scaffolding_level": "none",
  "srs_retrieval": true
}
```

### 4.9 Additional Domain — Bubble Sort (Separate Skill Domain)

**Setup:** Array `[5, 3, 8, 4, 2]`, unsorted.

**Student action:** Move adjacent elements that are out of order, bubbling the largest element to the rightmost position in each pass.

**Validation:** Each pass correctly bubbles the largest unsorted element to its final position. After pass 1: `[3, 4, 2, 5, 8]`. After pass 2: `[3, 2, 4, 5, 8]`. After pass 3: `[2, 3, 4, 5, 8]`.

**Expected outcomes:**
- Student correctly identifies adjacent out-of-order pairs → correct
- Student swaps non-adjacent elements → incorrect
- Student stops before array is fully sorted → incomplete

**Captain Byte:** "Compare adjacent elements. If they're out of order, swap them. The largest element will bubble to the end on each pass."

**Evidence emitted:**
```json
{
  "interaction_type": "manipulate",
  "passes": [
    {"pass": 1, "array": [3, 4, 2, 5, 8]},
    {"pass": 2, "array": [3, 2, 4, 5, 8]},
    {"pass": 3, "array": [2, 3, 4, 5, 8]}
  ],
  "correct": true,
  "hints_used": 0
}
```

**Note:** Bubble sort is a separate skill domain (`dsa.sorting`), not part of the seven-beat teaching framework. It follows the same interaction patterns (manipulate) but is assessed independently of the two-pointer journey.

| Case | Input | Target | Expected | Reason |
|------|-------|--------|----------|--------|
| Normal pair | `[1, 2, 4, 6, 8]` | 10 | `[2, 3]` (values 4, 6) | 4+6=10 |
| Negative values | `[-8, -3, 1, 5, 9]` | 6 | `[1, 4]` (values -3, 9) or `[2, 3]` (values 1, 5) | Negatives handled |
| Duplicates | `[1, 3, 3, 7]` | 6 | `[1, 2]` (distinct indices) | Same value, different indices |
| No possible pair | `[1, 2, 4, 8]` | 20 | `None` | Sum never reaches target |
| Empty input | `[]` | 5 | `None` | Safe handling |
| Single element | `[5]` | 10 | `None` | Can't form pair |
| Two-element success | `[2, 8]` | 10 | `[0, 1]` | Both elements used |
| Pair at boundaries | `[1, 4, 6, 9]` | 10 | `[0, 3]` | First and last |
| Unsorted input | `[4, 1, 8, 2]` | 3 | Algorithm returns `None` but `[1, 2]` sums to 3 | Precondition violated: algorithm fails on unsorted input |
| Negative target | `[-9, -4, -1]` | -5 | `[1, 2]` (values -4, -1) | Negative target works |
| Target below all sums | `[10, 20, 30]` | 5 | `None` | All sums > target |
| Target above all sums | `[1, 2, 3]` | 100 | `None` | All sums < target |
| Multiple valid pairs | `[1, 2, 3, 4, 5]` | 5 | `[0, 3]` or `[1, 2]` | Either acceptable |
| Pointer crossing | `[1, 2]` | 3 | `[0, 1]` | Pointers meet at answer |

### 5.1 Test Oracle

The reference implementation:

```python
def two_sum(nums, target):
    # Precondition check: array must be sorted in non-decreasing order
    # O(n) check - one pass through the array
    for i in range(len(nums) - 1):
        if nums[i] > nums[i + 1]:
            raise ValueError("Array must be sorted in non-decreasing order")
    
    left = 0
    right = len(nums) - 1
    while left < right:
        s = nums[left] + nums[right]
        if s == target:
            return [left, right]
        elif s < target:
            left += 1
        else:
            right -= 1
    return None
```

**Precondition check:** If `nums` is not sorted in non-decreasing order, raise `ValueError("Array must be sorted")`. The check itself is O(n) — a single pass through the array.

### 5.2 Complexity

- Time: O(n) — each element visited at most once by the two pointers
- Space: O(1) — two pointers only
- Precondition validation (sort check): O(n) — one pass to verify sorted order
- Total with validation: O(n) — not O(n log n); no sorting is performed, only a linear scan to verify the precondition

---

## 6. Student Experience Summary

| Phase | What Student Does | What System Validates | Captain Byte Says |
|-------|-------------------|----------------------|-------------------|
| Feel | Find any pair summing to 10 | Pair sums correctly | "Try it first." |
| Discover | Move pointer through array | Each element visited once | "Watch the pointer." |
| Predict | Predict pointer movement | Answer matches rule | "Make your guess." |
| Build | Implement two-sum | Hidden tests pass | "You're writing the code." |
| Break | Find unsorted input that breaks code | Input violates precondition | "Can you break this?" |
| Debug | Fix boundary condition | All tests pass | "Fix the bug." |
| Transfer | Solve container problem independently | Correct maximum area | "Same idea, new problem." |
| Retrieve | Answer prediction question next day | Correct without hints | "Remember this?" |

---

## 7. Design Review Checklist

| # | Question | Status |
|---|----------|--------|
| 1 | Seven beats all present? | Yes |
| 2 | Every beat has meaningful student action? | Yes |
| 3 | Answer not revealed before commit? | Yes (predict beat) |
| 4 | Hints are progressive? | Yes (3-level ladder) |
| 5 | Transfer task is meaningfully changed? | Yes (container problem) |
| 6 | Algorithm correctness verified? | Yes (test matrix) |
| 7 | Precondition (sorted input) explicit? | Yes |
| 8 | Misconceptions mapped? | Yes (3 misconceptions) |
| 7 | Evidence emitted at every step? | Yes |
| 10 | Accessibility considered? | Yes |

---

**End of 06 Arrays and Sorting Journey**
