# 20 TEST-CASE ENGINEERING STANDARD

**BountyCode — Phase 2B Scope-Completeness Review**
**Status: Design-only document**
**No application code written**

---

## 1. Purpose

Define the test-case engineering standard for all coding problems in BountyCode. Every coding problem must have a complete, verifiable test suite—not just one example that produces the expected answer. This document specifies:

- Test case categories and their purposes
- Test case schema and schema validation
- Grading rules and verdict determination
- Edge case requirements per algorithm domain
- Constraint cases and invalid input handling
- Test case count minimums per problem difficulty

This is a design document. No implementation is authorized.

---

## 2. Test Case Categories

Every coding problem must include test cases from the following categories:

| Category | Purpose | Minimum Count | Weight in Grading |
|----------|---------|---------------|-------------------|
| **Normal** | Does the algorithm solve the intended problem? | 2 | 40% |
| **Boundary** | Does it work at the edges? | 2 | 25% |
| **Adversarial** | Does it fail on tricky arrangements? | 2 | 20% |
| **Constraint** | Does it handle maximum permitted input efficiently? | 1 | 10% |
| **Invalid Input** | Does it reject inputs that violate preconditions? | 1 | 5% |

**Total minimum: 8 test cases per problem.**

---

## 3. Test Case Schema

Every test case must conform to the following JSON schema:

```json
{
  "test_case_id": "string",
  "category": "normal" | "boundary" | "adversarial" | "constraint" | "invalid_input",
  "input": {},
  "expected_output": any,
  "expected_error": string | null,
  "timeout_ms": integer,
  "description": "string",
  "difficulty_override": "easy" | "medium" | "hard" | null,
  "hidden": boolean
}
```

### 3.1 Field Definitions

| Field | Type | Constraint | Description |
|-------|------|------------|-------------|
| `test_case_id` | UUID | Required, server-generated | Unique identifier for the test case |
| `category` | Enum | Required | One of: normal, boundary, adversarial, constraint, invalid_input |
| `input` | JSON | Required | Input data for the problem (serialized as JSON) |
| `expected_output` | JSON | Required | Expected output (null for invalid input expecting error) |
| `expected_error` | string | Optional | Error message expected for invalid input |
| `timeout_ms` | integer | Required | Maximum execution time in milliseconds |
| `description` | string | Required | Human-readable description of the test case |
| `difficulty_override` | string | Optional | Override problem difficulty for this specific test case |
| `hidden` | boolean | Required | Whether the test case is hidden from the student |

### 3.2 Hidden Test Case Rules

| Rule | Description |
|------|-------------|
| Minimum hidden tests | At least 50% of test cases must be hidden from the student |
| Hidden vs visible ratio | Hidden test cases must not exceed 75% of total test cases |
| Hidden test criteria | Hidden tests must cover edge cases, adversarial inputs, and constraint scenarios |
| Visible test criteria | Visible tests must cover normal cases and basic boundary conditions |

---

## 4. Domain-Specific Test Case Standards

### 4.1 Arrays

| Test Category | Example Test Case | Expected Output |
|---------------|-----------------|-----------------|
| Normal | `[1, 2, 3, 4, 5]`, target `9` | `[3, 4]` |
| Boundary | `[1]`, target `1` | `[0, 0]` |
| Boundary | `[]`, target `5` | `None` |
| Adversarial | `[1, 1, 1, 1, 1]`, target `2` | `[0, 1]` (first valid pair) |
| Constraint | Array of 10⁵ elements | `None` (timeout if too slow) |
| Invalid Input | Unsorted array `[4, 1, 8, 2]`, target `6` | `ValueError: Array must be sorted` |

### 4.2 Strings

| Test Category | Example Test Case | Expected Output |
|---------------|-----------------|-----------------|
| Normal | `"hello"`, target `"ll"` | `2` |
| Boundary | `""`, target `""` | `0` |
| Boundary | `"aaaaa"`, target `"aa"` | `0` |
| Adversarial | `"mississippi"`, target `"issip"` | `4` |
| Constraint | String of 10⁴ characters | None (timeout if too slow) |
| Invalid Input | `null`, target `"test"` | `TypeError: string required` |

### 4.3 Hashing

| Test Category | Example Test Case | Expected Output |
|---------------|-----------------|-----------------|
| Normal | `[1, 2, 3, 4, 5]`, target `9` | `[3, 4]` |
| Boundary | `[1]`, target `1` | `None` (no pair) |
| Boundary | `[]`, target `5` | `None` |
| Adversarial | `[1, 1, 1, 1]`, target `2` | `[0, 1]` |
| Constraint | Array of 10⁵ elements | None (timeout if O(n²)) |
| Invalid Input | `null`, target `5` | `TypeError` |

### 4.4 Two Pointers

| Test Category | Example Test Case | Expected Output |
|---------------|-----------------|-----------------|
| Normal | `[1, 2, 4, 6, 8]`, target `10` | `[1, 4]` |
| Negative values | `[-8, -3, 1, 5, 9]`, target `6` | `[2, 4]` |
| Duplicates | `[1, 3, 3, 7]`, target `6` | `[1, 2]` |
| No possible pair | `[1, 2, 4, 8]`, target `20` | `None` |
| Empty input | `[]`, target `5` | `None` |
| Single element | `[5]`, target `10` | `None` |
| Unsorted input | `[4, 1, 8, 2]`, target `6` | `ValueError: Array must be sorted` |
| Negative target | `[-9, -4, -1]`, target `-5` | `[1, 2]` |
| Target below all sums | `[10, 20, 30]`, target `5` | `None` |
| Target above all sums | `[1, 2, 3]`, target `100` | `None` |
| Multiple valid pairs | `[1, 2, 3, 4, 5]`, target `5` | `[0, 3]` or `[1, 2]` |
| Pointer crossing | `[1, 2]`, target `3` | `[0, 1]` |

### 4.5 Sliding Window

| Test Category | Example Test Case | Expected Output |
|---------------|-----------------|-----------------|
| Normal | `[1, 2, 3, 4, 5]`, k=3 | `12` |
| Boundary | `[1]`, k=1 | `1` |
| Boundary | `[]`, k=1 | `None` |
| Adversarial | All negative numbers `[-1, -2, -3]`, k=2 | `-3` |
| Constraint | Array of 10⁵ elements, k=1000 | None (timeout if O(n²)) |
| Invalid Input | `null`, k=3 | `TypeError` |

### 4.6 Sorting

| Test Category | Example Test Case | Expected Output |
|---------------|-----------------|-----------------|
| Normal | `[5, 3, 8, 4, 2]` | `[2, 3, 4, 5, 8]` |
| Boundary | `[1]` | `[1]` |
| Boundary | `[]` | `[]` |
| Adversarial | `[5, 4, 3, 2, 1]` | `[1, 2, 3, 4, 5]` |
| Constraint | Array of 10⁴ elements | None (timeout if O(n²)) |
| Invalid Input | `null` | `TypeError` |

### 4.7 Binary Search

| Test Category | Example Test Case | Expected Output |
|---------------|-----------------|-----------------|
| Normal | `[1, 2, 4, 6, 8]`, target `6` | `3` |
| Boundary | `[1]`, target `1` | `0` |
| Boundary | `[]`, target `5` | `-1` |
| Adversarial | `[1, 1, 1, 2, 2]`, target `1` | `0` (first occurrence) |
| Constraint | Array of 10⁵ elements | None (timeout if O(n)) |
| Invalid Input | Unsorted array, target `5` | `ValueError: Array must be sorted` |

### 4.8 Stack & Queue

| Test Category | Example Test Case | Expected Output |
|---------------|-----------------|-----------------|
| Normal | Push `[1, 2, 3]`, pop 3 times | `3, 2, 1` |
| Boundary | Push `[]`, pop 1 | `None` (empty) |
| Boundary | Push `[]`, pop 0 | `[]` |
| Adversarial | Push 10⁵ elements, pop all | None (timeout if O(n²)) |
| Invalid Input | Pop on empty stack | `IndexError: pop from empty stack` |

### 4.9 Linked List

| Test Category | Example Test Case | Expected Output |
|---------------|-----------------|-----------------|
| Normal | `[1, 2, 3, 4, 5]`, reverse | `[5, 4, 3, 2, 1]` |
| Boundary | `[1]`, reverse | `[1]` |
| Boundary | `[]`, reverse | `[]` |
| Adversarial | Cycle detection `[1, 2, 3]`, 2→0 (cycle) | `True` (has cycle) |
| Constraint | List of 10⁵ nodes | None (timeout if O(n²)) |
| Invalid Input | `null` head | `None` |

### 4.10 Trees

| Test Category | Example Test Case | Expected Output |
|---------------|-----------------|-----------------|
| Normal | `[3, 9, 20, null, null, 15, 7]` | `3` (depth) |
| Boundary | `[1]` | `1` |
| Boundary | `[]` | `0` |
| Adversarial | Skewed tree (linked list shape) of 10⁴ nodes | None (timeout if O(n²)) |
| Constraint | Tree of 10⁴ nodes | None (timeout if O(n²)) |
| Invalid Input | `null` root | `None` |

---

## 5. Grading Rules

### 5.1 Verdict Determination

| Condition | Verdict |
|-----------|---------|
| All test cases pass (output matches expected) | `Accepted` |
| Any test case fails (output mismatch) | `Wrong Answer` |
| Any test case times out | `Time Limit Exceeded` |
| Any test case throws runtime error | `Runtime Error` |
| Any test case throws compile error | `Compile Error` |
| Memory limit exceeded | `Memory Limit Exceeded` |

### 5.2 Partial Credit Policy

| Scenario | Credit |
|----------|--------|
| All test cases pass | 100% |
| All visible tests pass, hidden tests fail | 50% |
| Some visible tests pass | 25% |
| No tests pass | 0% |
| Compile error | 0% |
| Runtime error | 0% |

### 5.3 Hidden Test Case Rules

| Rule | Description |
|------|-------------|
| Minimum hidden tests | At least 50% of test cases must be hidden |
| Hidden vs visible ratio | Hidden tests must not exceed 75% of total test cases |
| Hidden test criteria | Hidden tests cover edge cases, adversarial inputs, constraint scenarios |
| Visible test criteria | Visible tests cover normal cases and basic boundary conditions |

---

## 6. Test Case Review Checklist

| # | Question | Status |
|---|----------|--------|
| 1 | Does each problem have minimum 8 test cases? | ☐ |
| 2 | Is at least 50% of test cases hidden? | ☐ |
| 3 | Are hidden tests ≤ 75% of total? | ☐ |
| 4 | Are all 5 categories represented? | ☐ |
| 5 | Is each category represented by at least the minimum count? | ☐ |
| 6 | Are adversarial cases included for every algorithm? | ☐ |
| 7 | Are constraint cases included for performance-critical algorithms? | ☐ |
| 8 | Is invalid input handling tested? | ☐ |
| 9 | Is the expected output correct for every test case? | ☐ |
| 10 | Is the timeout value appropriate for each test case? | ☐ |
| 11 | Is the difficulty override appropriate when used? | ☐ |
| 12 | Are test case IDs unique within each problem? | ☐ |

---

## 7. Test Case Review Process

### 7.1 Review Steps

1. **Author drafts test cases** for a problem
2. **Reviewer independently solves** the problem without seeing test cases
3. **Reviewer executes** their solution against the test cases
4. **Reviewer verifies** all expected outputs are correct
5. **Reviewer checks** edge cases, adversarial cases, constraint cases
6. **Reviewer approves** or requests changes

### 7.2 Review Criteria

| Criterion | Pass Condition |
|-----------|---------------|
| Correctness | All expected outputs are correct |
| Completeness | All categories represented with minimum counts |
| Diversity | Test cases cover different scenarios, not duplicates |
| Difficulty | Test cases match stated problem difficulty |
| Determinism | Same input always produces same output |
| Independence | No test case depends on another test case |

---

## 8. Versioning

| Field | Value |
|-------|-------|
| Test case schema version | `test-schema-v1` |
| Grading policy version | `grading-v1` |
| Content version | Per problem, incremented on change |

---

## 9. Design Review Checklist

| # | Question | Status |
|---|----------|--------|
| 1 | Every problem has minimum 8 test cases? | ☐ |
| 2 | At least 50% hidden tests? | ☐ |
| 3 | Hidden tests ≤ 75%? | ☐ |
| 4 | All 5 categories represented? | ☐ |
| 5 | Each category meets minimum count? | ☐ |
| 6 | Adversarial cases included? | ☐ |
| 7 | Constraint cases included? | ☐ |
| 8 | Invalid input tested? | ☐ |
| 9 | Expected outputs verified correct? | ☐ |
| 10 | Timeout values appropriate? | ☐ |
| 11 | Difficulty overrides appropriate? | ☐ |
| 12 | Test case IDs unique? | ☐ |
| 13 | Review process defined? | ☐ |
| 14 | Versioning defined? | ☐ |

---

**End of 20 TEST-CASE ENGINEERING STANDARD**
