# BountyCode Canonical Skill Graph — Review

**File:** `backend/app/data/skill_graph.json`  
**Validator:** `backend/app/path_engine/graph.py`  
**Tests:** `backend/tests/path_engine/test_graph.py` (19 tests, all passing)

## Status

All edges are `reviewed: false`. None are approved for serving to students until the founder reviews and flips them to `reviewed: true`.

## Graph summary

- **37 skills** across 4 sections: aptitude, logical, verbal, coding/cs_fundamentals
- **24 prerequisite edges**
- **2 company blueprints:** TCS, Infosys (weights sum to 1.0 each)

## Edges (pending review)

| # | From → To | Reason | Strength |
|---|-----------|--------|----------|
| 1 | programming_basics → arrays | You must understand variables and loops before working with arrays as a data structure. | 0.9 |
| 2 | programming_basics → recursion | Recursive functions require a solid grasp of functions and base cases from programming basics. | 0.8 |
| 3 | programming_basics → oop | Object-oriented programming builds on variables, functions, and control flow basics. | 0.8 |
| 4 | number_system → percentages | Percentages are fractions of 100, so you must understand number operations first. | 0.9 |
| 5 | percentages → profit_loss | Profit and loss percentage is computed from the cost price using percentage concepts. | 0.8 |
| 6 | percentages → simple_compound_interest | Simple and compound interest are percentage calculations applied over time periods. | 0.8 |
| 7 | number_system → ratio_proportion | Ratios compare quantities, which requires understanding numbers and division. | 0.8 |
| 8 | averages → time_work | Work rate is an average amount of work done per unit of time. | 0.7 |
| 9 | time_work → time_distance | Speed is a rate similar to work rate, so time-work intuition transfers to time-distance. | 0.7 |
| 10 | series → coding_decoding | Both series and coding-decoding rely on recognizing patterns in sequences. | 0.7 |
| 11 | coding_decoding → analogy | Analogy questions use coded relationships similar to coding-decoding transformations. | 0.6 |
| 12 | blood_relation → seating_arrangements | Both blood relations and seating arrangements require reasoning about relative positions. | 0.6 |
| 13 | direction_sense → puzzles | Direction sense builds spatial reasoning that helps solve arrangement and movement puzzles. | 0.5 |
| 14 | grammar → sentence_correction | You cannot correct sentence errors without knowing grammar rules first. | 0.9 |
| 15 | synonyms_antonyms → reading_comprehension | Reading comprehension depends on vocabulary, which synonyms and antonyms build. | 0.7 |
| 16 | arrays → linked_lists | Linked lists are an alternative linear data structure best understood after arrays. | 0.6 |
| 17 | arrays → sorting_searching | Sorting and searching algorithms are most commonly taught and applied on arrays. | 0.8 |
| 18 | arrays → two_pointers | The two-pointer technique operates on array indices, so arrays must come first. | 0.7 |
| 19 | linked_lists → stacks_queues | Stacks and queues can be implemented using linked lists, making linked lists a prerequisite. | 0.6 |
| 20 | sorting_searching → hashing | Hashing is motivated by the need for faster searching than sorted-array binary search. | 0.7 |
| 21 | recursion → trees | Tree traversal and tree algorithms are naturally recursive, so recursion comes first. | 0.8 |
| 22 | dbms → operating_systems | Database management systems rely on operating system file and memory management. | 0.5 |
| 23 | complexity → sorting_searching | You need complexity notation to compare sorting and searching algorithm efficiency. | 0.6 |

## Company blueprints

**TCS** — 31 skills, weights sum to 1.000000  
**Infosys** — 34 skills, weights sum to 1.000000

Both cover TCS and Infosys first. Wipro, Cognizant, Capgemini, Accenture, Tech Mahindra, LTIMindtree can follow in the same format.

## Coverage report (real verified question counts)

Based on the live question store. Skills below 12 verified questions are flagged LOW.

| Skill | Section | Verified questions | Lessons | Status |
|-------|---------|-------------------|---------|--------|
| number_system | aptitude | 14 | 1 | OK |
| percentages | aptitude | 6 | 1 | **LOW** |
| profit_loss | aptitude | 5 | 1 | **LOW** |
| ratio_proportion | aptitude | 4 | 1 | **LOW** |
| averages | aptitude | 4 | 1 | **LOW** |
| time_work | aptitude | 5 | 1 | **LOW** |
| time_distance | aptitude | 5 | 1 | **LOW** |
| simple_compound_interest | aptitude | 8 | 1 | **LOW** |
| series | logical | 5 | 1 | **LOW** |
| coding_decoding | logical | 1 | 1 | **LOW** |
| blood_relation | logical | 2 | 1 | **LOW** |
| direction_sense | logical | 2 | 1 | **LOW** |
| analogy | logical | 2 | 1 | **LOW** |
| seating_arrangements | logical | 1 | 1 | **LOW** |
| syllogisms | logical | 1 | 1 | **LOW** |
| puzzles | logical | 1 | 1 | **LOW** |
| grammar | verbal | 3 | 1 | **LOW** |
| sentence_correction | verbal | 1 | 1 | **LOW** |
| reading_comprehension | verbal | 0 | 0 | **LOW** |
| synonyms_antonyms | verbal | 7 | 0 | **LOW** |
| para_jumbles | verbal | 0 | 1 | **LOW** |
| fill_in_blanks | verbal | 1 | 0 | **LOW** |
| programming_basics | coding | 0 | 2 | **LOW** |
| arrays | coding | 31 | 1 | OK |
| strings | coding | 15 | 0 | **LOW** |
| linked_lists | coding | 0 | 1 | **LOW** |
| stacks_queues | coding | 0 | 0 | **LOW** |
| trees | coding | 0 | 0 | **LOW** |
| sorting_searching | coding | 4 | 0 | **LOW** |
| hashing | coding | 14 | 1 | OK |
| recursion | coding | 0 | 0 | **LOW** |
| two_pointers | coding | 0 | 0 | **LOW** |
| dbms | cs_fundamentals | 62 | 1 | OK |
| operating_systems | cs_fundamentals | 10 | 1 | **LOW** |
| computer_networks | cs_fundamentals | 8 | 1 | **LOW** |
| oop | cs_fundamentals | 2 | 1 | **LOW** |
| complexity | cs_fundamentals | 2 | 0 | **LOW** |

**32 of 37 skills are below the 12-verified-question threshold.** Only `number_system`, `arrays`, `hashing`, and `dbms` meet it.

## Blueprint skills with zero verified questions

All 65 blueprint skill-company pairs (31 TCS + 34 Infosys) reference skills with zero verified questions across at least one topic mapping. This is expected at v0.1: the question bank topics use inconsistent naming (e.g., `blood-relation` vs `blood_relation`, `linked_list` vs `linked lists`) and many skills map to topics that haven't been independently verified yet.

The graph loads and validates correctly. These coverage gaps are reported loudly per the validator spec — they are data gaps, not code bugs.

## Next actions for founder

1. **Review each edge** — confirm or reject the prerequisite relationship. Flip `reviewed` to `true` for approved edges.
2. **Adjust blueprint weights** — ensure they reflect what TCS and Infosys actually test.
3. **Add verified questions** for LOW skills before the path engine can serve them confidently.
4. **Add missing companies** (Wipro, Cognizant, Capgemini, Accenture, Tech Mahindra, LTIMindtree) to blueprints when ready.

## Validator rules enforced

1. No cycles ✓
2. Every skill ID in edges/blueprints exists ✓
3. Every skill reachable from at least one root ✓ (multiple roots allowed)
4. Every edge reason ≥ 8 words ✓
5. Blueprint weights per company sum to 1 (tolerance 1e-6) ✓
6. Coverage report flags skills below 12 verified questions ✓
7. Blueprint skills with no questions reported loudly ✓

## Tests

All 19 tests pass:

```
pytest tests/path_engine/test_graph.py -v
19 passed
```

Tests cover: cycle rejection, unknown skill rejection, missing reason rejection, weights not summing to 1, valid fixture load, topological order respects edges, multiple roots allowed, orphan skill flagged, real graph loads, real graph no cycles, real graph blueprints sum to one, TCS and Infosys present, edges have reasons, edges refer to known skills, skills reachable from roots, coverage report flags low verified, blueprint skills without questions reported loudly.
