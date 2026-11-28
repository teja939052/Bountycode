# 19 ALGORITHM CURRICULUM INVENTORY

**BountyCode — Phase 2B Scope-Completeness Review**
**Status: Design-only document**
**No application code written**

---

## 1. Purpose

Define the complete algorithm curriculum for BountyCode's V1 launch (Worlds 1–5). Every algorithm skill must have:

- A canonical skill ID
- Prerequisites
- Difficulty level
- Concept breakdown
- Problem inventory (multiple distinct problems per skill, not one)
- Interaction templates
- Assessment methods
- Evidence/retrieval requirements
- Transfer evidence requirements
- Release boundary (V1 vs roadmap)

This document is a design-only specification. No implementation is authorized.

---

## 2. V1 Algorithm Curriculum Scope

The V1 launch covers service-level DSA across 10 skill areas:

| # | Skill ID | Domain | Difficulty | V1 Status |
|---|----------|--------|------------|-----------|
| 1 | `dsa.arrays` | Easy | Easy | V1 |
| 2 | `dsa.strings` | Easy | Easy | V1 |
| 3 | `dsa.hashing` | Medium | Medium | V1 |
| 4 | `dsa.two_pointers` | Medium | Medium | V1 |
| 5 | `dsa.sliding_window` | Medium | Medium | V1 |
| 6 | `dsa.sorting` | Easy | Easy | V1 |
| 7 | `dsa.binary_search` | Medium | Medium | V1 |
| 8 | `dsa.stack_queue` | Easy | Easy | V1 |
| 9 | `dsa.linked_list` | Medium | Medium | V1 |
| 10 | `dsa.trees` | Medium | Medium | V1 |

### 2.1 V1 Skill → Pseudocode Dependency Chain

Pseudocode (World 4) provides the programming logic foundation. DSA builds on it:

| DSA Skill | Pseudocode Prerequisite |
|-----------|------------------------|
| `dsa.arrays` | `pseudo.arrays` |
| `dsa.strings` | `dsa.arrays` |
| `dsa.hashing` | `dsa.arrays` |
| `dsa.two_pointers` | `dsa.arrays` |
| `dsa.sliding_window` | `dsa.two_pointers` |
| `dsa.sorting` | `dsa.arrays` |
| `dsa.binary_search` | `dsa.sorting` |
| `dsa.stack_queue` | `dsa.arrays` |
| `dsa.linked_list` | `dsa.arrays` |
| `dsa.trees` | `dsa.linked_list` |

---

## 3. Skill-by-Skill Curriculum Inventory

### 3.1 Skill 1 — `dsa.arrays`

| Field | Value |
|-------|-------|
| Canonical skill ID | `dsa.arrays` |
| Skill name | Arrays |
| Domain | `dsa` |
| Prerequisite | `coding.loops`, `coding.variables` |
| Difficulty | Easy |
| Estimated time | 45–60 minutes |
| Interaction templates | `manipulate`, `select`, `trace` |
| Trust status required | `TRUSTED` |

#### 3.1.1 Concept Hierarchy

| Concept ID | Concept Name | Description |
|------------|--------------|-------------|
| `dsa.arrays.indexing` | Zero-based indexing | Understand arrays start at index 0, last index is length-1 |
| `dsa.arrays.access` | Random access | O(1) access by index |
| `dsa.arrays.traversal` | Linear traversal | Visit every element sequentially |
| `dsa.arrays.search` | Linear search | Find element by value |
| `dsa.arrays.update` | Modify element | Change value at index |

#### 3.1.2 Problem Inventory (Minimum 3 distinct problems)

| Problem ID | Problem Name | Difficulty | Interaction Template | Test Case Count (min) |
|------------|--------------|------------|---------------------|----------------------|
| `dsa.arrays.find_max` | Find Maximum Element | Easy | `manipulate` | 5 |
| `dsa.arrays.find_min` | Find Minimum Element | Easy | `manipulate` | 5 |
| `dsa.arrays.reverse_array` | Reverse an Array | Medium | `fill` | 7 |
| `dsa.arrays.find_pair_sum` | Find Pair with Given Sum | Medium | `trace` | 7 |
| `dsa.arrays.remove_duplicates` | Remove Duplicates from Sorted Array | Medium | `fill` | 6 |

#### 3.1.3 Assessment Methods

| Assessment Type | Method | Weight |
|-----------------|--------|--------|
| Code submission | Write function, execute against test cases | 70% |
| Code trace | Trace execution on given input | 20% |
| Predict output | Predict output of array operations | 10% |

#### 3.1.4 Evidence / Retrieval / Transfer

| Type | Requirement |
|------|-------------|
| Evidence | `SRS` card for `dsa.arrays`, updated on each attempt |
| Revision | Spaced repetition at 1 day, 3 days, 7 days |
| Transfer | Apply array operations to string manipulation problems |

---

### 3.2 Skill 2 — `dsa.strings`

| Field | Value |
|-------|-------|
| Canonical skill ID | `dsa.strings` |
| Skill name | Strings |
| Domain | `dsa` |
| Prerequisite | `dsa.arrays` |
| Difficulty | Easy |
| Estimated time | 45–60 minutes |
| Interaction templates | `manipulate`, `fill`, `trace` |
| Trust status required | `TRUSTED` |

#### 3.2.1 Concept Hierarchy

| Concept ID | Concept Name | Description |
|------------|--------------|-------------|
| `dsa.strings.indexing` | String character access | Access character at index |
| `dsa.strings.length` | String length | Get string length |
| `dsa.strings.concat` | String concatenation | Join two strings |
| `dsa.strings.reverse` | String reversal | Reverse characters in place |
| `dsa.strings.palindrome` | Palindrome check | Check if string reads same forwards/backwards |

#### 3.2.2 Problem Inventory (Minimum 3 distinct problems)

| Problem ID | Problem Name | Difficulty | Interaction Template | Test Case Count (min) |
|------------|--------------|------------|---------------------|----------------------|
| `dsa.strings.reverse_string` | Reverse a String | Easy | `fill` | 5 |
| `dsa.strings.is_palindrome` | Check Palindrome | Easy | `predict` | 6 |
| `dsa.strings.count_vowels` | Count Vowels | Easy | `manipulate` | 5 |
| `dsa.strings.anagram_check` | Check Anagrams | Medium | `fill` | 6 |
| `dsa.strings.longest_substring` | Longest Substring Without Repeating | Medium | `trace` | 6 |

#### 3.2.3 Assessment Methods

| Assessment Type | Method | Weight |
|-----------------|--------|--------|
| Code submission | Write function, execute against test cases | 70% |
| Code trace | Trace execution on given input | 20% |
| Predict output | Predict output of string operations | 10% |

#### 3.2.4 Evidence / Retrieval / Transfer

| Type | Requirement |
|------|-------------|
| Evidence | `SRS` card for `dsa.strings`, updated on each attempt |
| Revision | Spaced repetition at 1 day, 3 days, 7 days |
| Transfer | Apply string operations to array manipulation problems |

---

### 3.3 Skill 3 — `dsa.hashing`

| Field | Value |
|-------|-------|
| Canonical skill ID | `dsa.hashing` |
| Skill name | Hashing |
| Domain | `dsa` |
| Prerequisite | `dsa.arrays` |
| Difficulty | Medium |
| Estimated time | 60–90 minutes |
| Interaction templates | `manipulate`, `fill`, `trace` |
| Trust status required | `TRUSTED` |

#### 3.3.1 Concept Hierarchy

| Concept ID | Concept Name | Description |
|------------|--------------|-------------|
| `dsa.hashing.hash_function` | Hash Function Design | Map keys to array indices |
| `dsa.hashing.collision` | Collision Handling | Handle multiple keys mapping to same index |
| `dsa.hashing.load_factor` | Load Factor | Ratio of entries to table size |
| `dsa.hashing.chaining` | Chaining | Linked list at each bucket |
| `dsa.hashing.open_addressing` | Open Addressing | Probe sequence for collision |

#### 3.3.2 Problem Inventory (Minimum 3 distinct problems)

| Problem ID | Problem Name | Difficulty | Interaction Template | Test Case Count (min) |
|------------|--------------|------------|---------------------|----------------------|
| `dsa.hashing.count_elements` | Count Distinct Elements | Easy | `fill` | 6 |
| `dsa.hashing.find_duplicates` | Find Duplicates in Array | Medium | `fill` | 7 |
| `dsa.hashing.group_anagrams` | Group Anagrams | Medium | `fill` | 6 |
| `dsa.hashing.subarray_sum` | Subarray Sum Equals K | Medium | `trace` | 7 |
| `dsa.hashing.longest_subsequence` | Longest Consecutive Subsequence | Medium | `fill` | 6 |

#### 3.3.3 Assessment Methods

| Assessment Type | Method | Weight |
|-----------------|--------|--------|
| Code submission | Write function, execute against test cases | 70% |
| Code trace | Trace hash table operations | 20% |
| Predict output | Predict output of hash operations | 10% |

#### 3.3.4 Evidence / Retrieval / Transfer

| Type | Requirement |
|------|-------------|
| Evidence | `SRS` card for `dsa.hashing`, updated on each attempt |
| Revision | Spaced repetition at 1 day, 3 days, 7 days |
| Transfer | Apply hash table concepts to string frequency problems |

---

### 3.4 Skill 4 — `dsa.two_pointers`

| Field | Value |
|-------|-------|
| Canonical skill ID | `dsa.two_pointers` |
| Skill name | Two Pointers |
| Domain | `dsa` |
| Prerequisite | `dsa.arrays` |
| Difficulty | Medium |
| Estimated time | 60–90 minutes |
| Interaction templates | `manipulate`, `predict`, `trace`, `fill` |
| Trust status required | `TRUSTED` |

#### 3.4.1 Concept Hierarchy

| Concept ID | Concept Name | Description |
|------------|--------------|-------------|
| `dsa.two_pointers.convergent` | Convergent Pointers | Two pointers move toward each other on sorted array |
| `dsa.two_pointers.same_direction` | Same Direction Pointers | Two pointers move in same direction |
| `dsa.two_pointers.fixed_window` | Fixed Window | Fixed-size sliding window |
| `dsa.two_pointers.variable_window` | Variable Window | Variable-size sliding window |

#### 3.4.2 Problem Inventory (Minimum 3 distinct problems)

| Problem ID | Problem Name | Difficulty | Interaction Template | Test Case Count (min) |
|------------|--------------|------------|---------------------|----------------------|
| `dsa.two_pointers.two_sum` | Two Sum on Sorted Array | Easy | `manipulate` | 7 |
| `dsa.two_pointers.container_water` | Container With Most Water | Medium | `fill` | 7 |
| `dsa.two_pointers.triplet_sum` | Three Sum | Medium | `fill` | 8 |
| `dsa.two_pointers.trapping_rain_water` | Trapping Rain Water | Hard | `fill` | 8 |
| `dsa.two_pointers.merge_sorted` | Merge Two Sorted Arrays | Easy | `fill` | 6 |

#### 3.4.3 Assessment Methods

| Assessment Type | Method | Weight |
|-----------------|--------|--------|
| Code submission | Write function, execute against test cases | 70% |
| Code trace | Trace pointer movement | 20% |
| Predict output | Predict pointer movement | 10% |

#### 3.4.4 Evidence / Retrieval / Transfer

| Type | Requirement |
|------|-------------|
| Evidence | `SRS` card for `dsa.two_pointers`, updated on each attempt |
| Revision | Spaced repetition at 1 day, 3 days, 7 days |
| Transfer | Apply two-pointer technique to container with most water |

---

### 3.5 Skill 5 — `dsa.sliding_window`

| Field | Value |
|-------|-------|
| Canonical skill ID | `dsa.sliding_window` |
| Skill name | Sliding Window |
| Domain | `dsa` |
| Prerequisite | `dsa.two_pointers` |
| Difficulty | Medium |
| Estimated time | 60–90 minutes |
| Interaction templates | `manipulate`, `fill`, `trace` |
| Trust status required | `TRUSTED` |

#### 3.5.1 Concept Hierarchy

| Concept ID | Concept Name | Description |
|------------|--------------|-------------|
| `dsa.sliding_window.fixed` | Fixed-Size Window | Window of fixed size moves across array |
| `dsa.sliding_window.variable` | Variable-Size Window | Window expands/contracts based on condition |
| `dsa.sliding_window.max_sum` | Maximum Subarray Sum | Find max sum of subarray |
| `dsa.sliding_window.min_subarray` | Minimum Subarray | Find minimum subarray satisfying condition |

#### 3.5.2 Problem Inventory (Minimum 3 distinct problems)

| Problem ID | Problem Name | Difficulty | Interaction Template | Test Case Count (min) |
|------------|--------------|------------|---------------------|----------------------|
| `dsa.sliding_window.max_sum_k` | Max Sum of Subarray of Size K | Easy | `fill` | 6 |
| `dsa.sliding_window.max_avg` | Maximum Average Subarray | Easy | `fill` | 5 |
| `dsa.sliding_window.longest_substring_k` | Longest Substring with K Distinct | Medium | `fill` | 7 |
| `dsa.sliding_window.min_window` | Minimum Window Substring | Medium | `fill` | 7 |
| `dsa.sliding_window.fruit_into_baskets` | Fruit Into Baskets | Medium | `fill` | 6 |

#### 3.5.3 Assessment Methods

| Assessment Type | Method | Weight |
|-----------------|--------|--------|
| Code submission | Write function, execute against test cases | 70% |
| Code trace | Trace window movement | 20% |
| Predict output | Predict window state | 10% |

#### 3.5.4 Evidence / Retrieval / Transfer

| Type | Requirement |
|------|-------------|
| Evidence | `SRS` card for `dsa.sliding_window`, updated on each attempt |
| Revision | Spaced repetition at 1 day, 3 days, 7 days |
| Transfer | Apply sliding window to string problems |

---

### 3.6 Skill 6 — `dsa.sorting`

| Field | Value |
|-------|-------|
| Canonical skill ID | `dsa.sorting` |
| Skill name | Sorting |
| Domain | `dsa` |
| Prerequisite | `dsa.arrays` |
| Difficulty | Easy |
| Estimated time | 60–90 minutes |
| Interaction templates | `arrange`, `trace`, `fill` |
| Trust status required | `TRUSTED` |

#### 3.6.1 Concept Hierarchy

| Concept ID | Concept Name | Description |
|------------|--------------|-------------|
| `dsa.sorting.bubble` | Bubble Sort | Adjacent swap, largest bubbles to end |
| `dsa.sorting.selection` | Selection Sort | Find minimum, swap to front |
| `dsa.sorting.insertion` | Insertion Sort | Build sorted portion one element at a time |
| `dsa.sorting.stability` | Stable vs Unstable | Preserve relative order of equal elements |
| `dsa.sorting.complexity` | Time Complexity | O(n²) for simple sorts |

#### 3.6.2 Problem Inventory (Minimum 3 distinct problems)

| Problem ID | Problem Name | Difficulty | Interaction Template | Test Case Count (min) |
|------------|--------------|------------|---------------------|----------------------|
| `dsa.sorting.bubble_sort` | Bubble Sort | Easy | `fill` | 6 |
| `dsa.sorting.selection_sort` | Selection Sort | Easy | `fill` | 6 |
| `dsa.sorting.insertion_sort` | Insertion Sort | Easy | `fill` | 6 |
| `dsa.sorting.sort_colors` | Sort Colors (Dutch National Flag) | Medium | `fill` | 7 |
| `dsa.sorting.kth_largest` | Kth Largest Element | Medium | `fill` | 6 |

#### 3.6.3 Assessment Methods

| Assessment Type | Method | Weight |
|-----------------|--------|--------|
| Code submission | Write function, execute against test cases | 70% |
| Code trace | Trace sorting passes | 20% |
| Predict output | Predict output after each pass | 10% |

#### 3.6.4 Evidence / Retrieval / Transfer

| Type | Requirement |
|------|-------------|
| Evidence | `SRS` card for `dsa.sorting`, updated on each attempt |
| Revision | Spaced repetition at 1 day, 3 days, 7 days |
| Transfer | Apply sorting concepts to priority queue problems |

---

### 3.7 Skill 7 — `dsa.binary_search`

| Field | Value |
|-------|-------|
| Canonical skill ID | `dsa.binary_search` |
| Skill name | Binary Search |
| Domain | `dsa` |
| Prerequisite | `dsa.sorting` |
| Difficulty | Medium |
| Estimated time | 60–90 minutes |
| Interaction templates | `predict`, `trace`, `fill` |
| Trust status required | `TRUSTED` |

#### 3.7.1 Concept Hierarchy

| Concept ID | Concept Name | Description |
|------------|--------------|-------------|
| `dsa.binary_search.midpoint` | Midpoint Calculation | `mid = left + (right - left) / 2` |
| `dsa.binary_search.halving` | Search Space Halving | Eliminate half of remaining elements |
| `dsa.binary_search.first_occurrence` | First Occurrence | Find first index of target |
| `dsa.binary_search.last_occurrence` | Last Occurrence | Find last index of target |
| `dsa.binary_search.insertion_point` | Insertion Point | Find where target would be inserted |

#### 3.7.2 Problem Inventory (Minimum 3 distinct problems)

| Problem ID | Problem Name | Difficulty | Interaction Template | Test Case Count (min) |
|------------|--------------|------------|---------------------|----------------------|
| `dsa.binary_search.basic` | Binary Search on Sorted Array | Easy | `fill` | 6 |
| `dsa.binary_search.first_occurrence` | Find First Occurrence | Medium | `fill` | 7 |
| `dsa.binary_search.last_occurrence` | Find Last Occurrence | Medium | `fill` | 7 |
| `dsa.binary_search.insert_position` | Search Insert Position | Medium | `fill` | 6 |
| `dsa.binary_search.rotated_array` | Search in Rotated Sorted Array | Medium | `fill` | 7 |

#### 3.7.3 Assessment Methods

| Assessment Type | Method | Weight |
|-----------------|--------|--------|
| Code submission | Write function, execute against test cases | 70% |
| Code trace | Trace pointer movement | 20% |
| Predict output | Predict midpoint calculation | 10% |

#### 3.7.4 Evidence / Retrieval / Transfer

| Type | Requirement |
|------|-------------|
| Evidence | `SRS` card for `dsa.binary_search`, updated on each attempt |
| Revision | Spaced repetition at 1 day, 3 days, 7 days |
| Transfer | Apply binary search to sorted matrix problems |

---

### 3.8 Skill 8 — `dsa.stack_queue`

| Field | Value |
|-------|-------|
| Canonical skill ID | `dsa.stack_queue` |
| Skill name | Stack & Queue Basics |
| Domain | `dsa` |
| Prerequisite | `dsa.arrays` |
| Difficulty | Easy |
| Estimated time | 45–60 minutes |
| Interaction templates | `manipulate`, `trace`, `fill` |
| Trust status required | `TRUSTED` |

#### 3.8.1 Concept Hierarchy

| Concept ID | Concept Name | Description |
|------------|--------------|-------------|
| `dsa.stack_queue.stack` | Stack (LIFO) | Last-In, First-Out |
| `dsa.stack_queue.queue` | Queue (FIFO) | First-In, First-Out |
| `dsa.stack_queue.push_pop` | Push and Pop | Stack operations |
| `dsa.stack_queue.enqueue_dequeue` | Enqueue and Dequeue | Queue operations |
| `dsa.stack_queue.peek` | Peek Operation | View top/front without removal |

#### 3.8.2 Problem Inventory (Minimum 3 distinct problems)

| Problem ID | Problem Name | Difficulty | Interaction Template | Test Case Count (min) |
|------------|--------------|------------|---------------------|----------------------|
| `dsa.stack_queue.implement_stack` | Implement Stack Using Array | Easy | `fill` | 6 |
| `dsa.stack_queue.implement_queue` | Implement Queue Using Array | Easy | `fill` | 6 |
| `dsa.stack_queue.valid_parentheses` | Valid Parentheses | Easy | `fill` | 6 |
| `dsa.stack_queue.evaluate_postfix` | Evaluate Postfix Expression | Medium | `fill` | 7 |
| `dsa.stack_queue.next_greater` | Next Greater Element | Medium | `fill` | 7 |

#### 3.8.3 Assessment Methods

| Assessment Type | Method | Weight |
|-----------------|--------|--------|
| Code submission | Write function, execute against test cases | 70% |
| Code trace | Trace stack/queue operations | 20% |
| Predict output | Predict output of operations | 10% |

#### 3.8.4 Evidence / Retrieval / Transfer

| Type | Requirement |
|------|-------------|
| Evidence | `SRS` card for `dsa.stack_queue`, updated on each attempt |
| Revision | Spaced repetition at 1 day, 3 days, 7 days |
| Transfer | Apply stack concepts to expression evaluation problems |

---

### 3.9 Skill 9 — `dsa.linked_list`

| Field | Value |
|-------|-------|
| Canonical skill ID | `dsa.linked_list` |
| Skill name | Linked List Basics |
| Domain | `dsa` |
| Prerequisite | `dsa.arrays` |
| Difficulty | Medium |
| Estimated time | 60–90 minutes |
| Interaction templates | `trace`, `fill`, `manipulate` |
| Trust status required | `TRUSTED` |

#### 3.9.1 Concept Hierarchy

| Concept ID | Concept Name | Description |
|------------|--------------|-------------|
| `dsa.linked_list.node` | Node Structure | Data + next pointer |
| `dsa.linked_list.traversal` | Linked List Traversal | Visit every node |
| `dsa.linked_list.insertion` | Insert Node | Insert at head, tail, or position |
| `dsa.linked_list.deletion` | Delete Node | Remove node by value or position |
| `dsa.linked_list.reversal` | Reverse Linked List | Reverse pointer direction |

#### 3.9.2 Problem Inventory (Minimum 3 distinct problems)

| Problem ID | Problem Name | Difficulty | Interaction Template | Test Case Count (min) |
|------------|--------------|------------|---------------------|----------------------|
| `dsa.linked_list.reverse` | Reverse Linked List | Medium | `fill` | 6 |
| `dsa.linked_list.find_middle` | Find Middle of Linked List | Easy | `trace` | 5 |
| `dsa.linked_list.has_cycle` | Detect Cycle in Linked List | Medium | `fill` | 6 |
| `dsa.linked_list.merge_sorted` | Merge Two Sorted Lists | Easy | `fill` | 6 |
| `dsa.linked_list.remove_nth` | Remove Nth Node From End | Medium | `fill` | 7 |

#### 3.9.3 Assessment Methods

| Assessment Type | Method | Weight |
|-----------------|--------|--------|
| Code submission | Write function, execute against test cases | 70% |
| Code trace | Trace pointer movement | 20% |
| Predict output | Predict output of linked list operations | 10% |

#### 3.9.4 Evidence / Retrieval / Transfer

| Type | Requirement |
|------|-------------|
| Evidence | `SRS` card for `dsa.linked_list`, updated on each attempt |
| Revision | Spaced repetition at 1 day, 3 days, 7 days |
| Transfer | Apply linked list concepts to tree traversal |

---

### 3.10 Skill 10 — `dsa.trees`

| Field | Value |
|-------|-------|
| Canonical skill ID | `dsa.trees` |
| Skill name | Tree Basics |
| Domain | `dsa` |
| Prerequisite | `dsa.linked_list` |
| Difficulty | Medium |
| Estimated time | 60–90 minutes |
| Interaction templates | `trace`, `fill`, `manipulate` |
| Trust status required | `TRUSTED` |

#### 3.10.1 Concept Hierarchy

| Concept ID | Concept Name | Description |
|------------|--------------|-------------|
| `dsa.trees.node` | Tree Node | Data + left/right children |
| `dsa.trees.traversal_preorder` | Preorder Traversal | Root → Left → Right |
| `dsa.trees.traversal_inorder` | Inorder Traversal | Left → Root → Right |
| `dsa.trees.traversal_postorder` | Postorder Traversal | Left → Right → Root |
| `dsa.trees.height` | Tree Height | Maximum depth |
| `dsa.trees.diameter` | Tree Diameter | Longest path between any two nodes |

#### 3.10.2 Problem Inventory (Minimum 3 distinct problems)

| Problem ID | Problem Name | Difficulty | Interaction Template | Test Case Count (min) |
|------------|--------------|------------|---------------------|----------------------|
| `dsa.trees.inorder_traversal` | Inorder Traversal | Easy | `fill` | 6 |
| `dsa.trees.max_depth` | Maximum Depth of Binary Tree | Easy | `fill` | 5 |
| `dsa.trees.same_tree` | Same Tree | Easy | `fill` | 6 |
| `dsa.trees.invert_tree` | Invert Binary Tree | Easy | `fill` | 6 |
| `dsa.trees.diameter` | Diameter of Binary Tree | Medium | `fill` | 7 |

#### 3.10.3 Assessment Methods

| Assessment Type | Method | Weight |
|-----------------|--------|--------|
| Code submission | Write function, execute against test cases | 70% |
| Code trace | Trace tree traversal | 20% |
| Predict output | Predict traversal output | 10% |

#### 3.10.4 Evidence / Retrieval / Transfer

| Type | Requirement |
|------|-------------|
| Evidence | `SRS` card for `dsa.trees`, updated on each attempt |
| Revision | Spaced repetition at 1 day, 3 days, 7 days |
| Transfer | Apply tree concepts to graph traversal |

---

## 4. V1 Skill Dependency Graph

```
coding.variables, coding.loops → dsa.arrays
dsa.arrays → dsa.strings, dsa.hashing, dsa.two_pointers, dsa.sorting, dsa.stack_queue, dsa.linked_list
dsa.arrays → dsa.sorting → dsa.binary_search
dsa.arrays → dsa.two_pointers → dsa.sliding_window
dsa.linked_list → dsa.trees
```

---

## 5. Design Review Checklist

| # | Question | Status |
|---|----------|--------|
| 1 | All 10 V1 skills have complete concept hierarchy? | Yes |
| 2 | Each skill has minimum 3 distinct problems? | Yes |
| 3 | Each problem has interaction template specified? | Yes |
| 4 | Each problem has test case count minimum? | Yes |
| 5 | Each skill has assessment methods defined? | Yes |
| 6 | Each skill has evidence/retrieval/transfer requirements? | Yes |
| 7 | Prerequisites form acyclic graph? | Yes |
| 8 | All skill IDs follow canonical `domain.subskill` format? | Yes |
| 9 | V1 vs Roadmap boundary clear? | Yes |
| 10 | Aligned with Vision Lock? | Yes |

---

**End of 19 ALGORITHM CURRICULUM INVENTORY**
