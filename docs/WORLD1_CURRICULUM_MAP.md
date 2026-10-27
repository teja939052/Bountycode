# World 1 Curriculum Map — "I Can Think in Code"

**Purpose.** India has placement-prep breadth everywhere: huge question banks, mocks,
company tracks, readiness scores (takeUforward, StudyBench, placd). Our wedge is
**capability, not content volume**. World 1 is the flagship proof: *"I can think in code."*

**The one metric.** After World 1, the percentage of true beginners who can solve an
unseen, basic coding problem **unaided** and **explain their solution**. If that number
moves meaningfully, we have something no question bank can copy.

**Unit of learning.** One interactive mission, not a video. Every lesson runs the same
loop — `Discover → Manipulate → Predict → Explain → Build → Break → Debug → Retrieve →
Transfer → Mastery` — with an executable prediction, a small build, a seeded believable
mistake, a hint ladder, a delayed retrieval check, and a transfer task. A video may exist
only as optional rescue material.

**Reuse commitment.** The eight authored Phase B lessons are the live seed of this map
(marked ★). They already implement the full loop, real student-state writes, and
pass the contract verifier (`backend/scripts/verify_concept_clarity.py`). Every new lesson
below is authored to the **same schema**, registered in
`backend/app/content/curriculum/registry.py`, and must pass the same verifier + the
trust pipeline before it is served.

---

## 1. The Capability Ladder → Chapter Map

| # | Capability | What the student can do | Chapter |
|---|---|---|---|
| 1 | **Read** | State values, variables, and output of code they did not write | Ch. 1 |
| 2 | **Predict** | Trace execution before running | Ch. 1–4 |
| 3 | **Build** | Write expressions, conditions, loops, functions from intent | Ch. 2–5 |
| 4 | **Break** | Recognize believable misconceptions planted in code | Ch. 2–5 (every lesson) |
| 5 | **Debug** | Locate, explain, and repair a defect independently | Ch. 2–5 debug lessons |
| 6 | **Retrieve** | Recall concepts after time has passed (SRS-driven) | Throughout (Ch. 2 onward) |
| 7 | **Transfer** | Solve an unseen problem without copying a pattern | Every lesson (graded) |
| 8 | **Perform** | Solve timed placement-style tasks and explain reasoning | Ch. 5 (capstone) |

Chapter accents:

| Chapter | Title | Lessons | Capability accent |
|---|---|---|---|
| 1 | The Program | 1–7 | Read + trace state |
| 2 | Choice | 8–14 | Booleans, decisions, condition debugging |
| 3 | Repetition | 15–21 | Loops, accumulators, loop debugging |
| 4 | Collections | 22–28 | Lists, mutation, traversal, list debugging |
| 5 | Express & Perform | 29–35 | Functions, placement-depth topics, timed capstone |

---

## 2. The Learning Loop — Graded Artifact Per Stage

| Stage | Student does | Graded artifact | Pass rule |
|---|---|---|---|
| Discover | Watch a worked example animate | none | — |
| Manipulate | Edit a live snippet and run it | produced output | no grade, explore only |
| Predict | Trace an unseen snippet **before** running | exact predicted output | exact match; hint ladder (2 hints), retries allowed |
| Explain | Explain a just-learned concept in their own words | free text | ≥1 keyword cluster **and** ≥8 words; model answer shown on fail |
| Build | Write the function from tests + prompt | code vs visible tests | ≥70% visible, then **100% hidden** |
| Break | Diagnose a seeded misconception, then fix it | diagnosis option + one-line fix | diagnosis id exact **and** whitespace-normalized fix exact |
| Debug | Locate + repair an unseeded defect | fix (or diagnosis+fix) | exact match on normalized fix |
| Retrieve | Replay an **older** concept (SRS card) | recall answer | exact/keyword match; feeds SRS state |
| Transfer | Solve an unseen problem unaided | hidden tests + 1 short explain | 100% hidden; explain keyword-cluster |
| Mastery | Concept-recall quiz | 3 MCQs (2 variants) | ≥70 (current `mastery_threshold`) |

World 1 gate (AGENTS.md Acceptance Gate 2): **all 35 lessons must demonstrate this
complete loop, with transfer as required evidence** — not "lesson watched."

---

## 3. The 35 Lessons — Master Table

Legend: ★ = already authored Phase B lesson (reuse, no re-platforming). C# = chapter.

| # | Slug | Title (node) | Capability | Key misconception seeded | Star |
|---|---|---|---|---|---|
| 1 | `program_io` | What a Program Does | Read | Output happens where I expect it to | |
| 2 | `assignment_boxes` | Variables as Named Boxes | Read | The name is the value; `=` means equality | |
| 3 | `variables_state` | The Memory Palace — State Changes | Read/Predict | A later assignment changes the first value everywhere | ★ |
| 4 | `types_values` | Values, Types, and Type Errors | Read | Everything is a string / "+ is always addition" | |
| 5 | `expressions_order` | Order of Evaluation | Predict | Left-to-right overrides precedence | |
| 6 | `strings_words` | The Stringed Loom — Text as Data | Read/Build | Strings are mutable | ★ |
| 7 | `trace_mini` | Chapter Transfer: Read the Whole | Transfer | — | |
| 8 | `booleans_compare` | Booleans and Comparisons | Read/Predict | `=` vs `==`; reversing comparison direction | |
| 9 | `control_flow` | The Forking Path — One Condition, Two Paths | Predict/Build | A condition must cover the "no" case | ★ |
| 10 | `elif_chain` | Ordered Decisions | Build | First match wins; unreachable branches | |
| 11 | `logic_combo` | and / or / not | Predict | "or" means inclusive; negating a comparison | |
| 12 | `condition_bugs` | Break: Wrong Condition | Debug | Inverted logic, off-by-one boundary | |
| 13 | `condition_spec` | Transfer: Eligibility Spec → Code | Transfer | — | |
| 14 | `decision_oa` | Timed Placement: Decide + Loop | Perform | — | |
| 15 | `while_loop` | Controlled Repetition | Predict/Build | Infinite loop = guaranteed termination | |
| 16 | `loops` | The Lantern Row — for/range | Predict/Build | `range(n)` includes n | ★ |
| 17 | `accumulate_run` | Accumulators: Sum and Count | Predict | Accumulator must start before the loop | |
| 18 | `string_walk` | Walk a String | Build | Indexing vs character; digit-as-number | |
| 19 | `loop_stop` | Break, Continue, Nested Loops | Predict/Build | break exits all nested loops | |
| 20 | `loop_bugs` | Break: The Off-by-One and the Infinite | Debug | Stop-boundary; resetting accumulator inside loop | |
| 21 | `loop_transfer` | Timed Transfer: Sum Even Digits | Transfer | — | |
| 22 | `arrays` | The Warehouse Stack — Indexing | Read/Predict | Index 1 = first; negative indexes | ★ |
| 23 | `list_mutate` | Mutate in Place vs Rebind | Read/Build | Reassigning = mutating; `b = a` copies | |
| 24 | `list_walk` | Traverse a List | Predict/Build | "for x in l" visits boxes or values? | |
| 25 | `list_build` | Build New Lists | Build | Modify-in-place vs accumulate-new | |
| 26 | `list_copy` | Slicing, Aliasing, Copying | Predict/Read | Slices alias the original | |
| 27 | `list_bugs` | Break: Index, Boundary, Alias | Debug | Mutating while iterating; off-by-one index | |
| 28 | `list_transfer` | Timed Transfer: Second-Largest | Transfer | — | |
| 29 | `functions` | The Function Forge — return vs print | Read/Build | `print` returns a value | ★ |
| 30 | `scope_rules` | Locals, Globals, Parameter Copies | Predict|Read | Inside changes leak outside | |
| 31 | `compose_reuse` | Compose Small Functions | Build | One big function is easier than many small | |
| 32 | `function_bugs` | Break: The Silent Forge | Debug | Missing return; wrong arg order; shadowing | |
| 33 | `sorting` | The Sorting Bazaar — One Pass at a Time | Predict/Read | One pass fully sorts | ★ |
| 34 | `complexity` | The Word learns Scale (reading only) | Predict/Read | "It feels fast" ≈ fast; nested = linear | ★ |
| 35 | `capstone_oa` | World-1 Exam: Perform + Explain | Perform | — | new |

**Content trust note.** ★ lessons are AUTOMATED_CHECKED today (expected outputs executed by
`verify_concept_clarity.py`). Before World 1 ships, every lesson — and every transfer /
break / assessment item — must reach **TRUSTED** per the `UNVERIFIED → AUTOMATED_CHECKED →
HUMAN_REVIEWED → TRUSTED` pipeline. Compile-passes are not evidence; executed expected
outputs are.

---

## 4. Per-Lesson Detail Blocks

Compact key per block: **Objective** (capability), **Misconceptions** (become the break
diagnosis options + `user_weaknesses` tags), **Transfer** (the graded unseen task),
**Mastery** (assessment criteria + threshold), **State** (concept_id + writes beyond the
shared contract; `S` = shared complete-write, `E` = per-stage event log, `W` = weakness
signal on failed break/explain).

### Chapter 1 — The Program (Read + trace state)

**L1 · `program_io` — What a Program Does**
- Objective: Read a 4–8 line program as *input → state → output*; state the output.
- Misconceptions: `output_where_expected` (thinking print output is not the program's result), `top_to_bottom_only` (ignoring reordering), `magic_input`.
- Transfer: After only two new concepts, trace an unseen mixed program (input + arithmetic + prints) and produce exact output.
- Mastery: predict exact, then explain "what changed between line X and line Y" (≥1 keyword cluster). Assess 70.
- State: concept `variables`; S, E.

**L2 · `assignment_boxes` — Variables as Named Boxes**
- Objective: Model `x = 5` as putting 5 in a box named x; read boxes after a few assignments.
- Misconceptions: `name_is_value` (the name *is* the value), `eq_is_equality` (`=` means equal), `box_reuse_confusion`.
- Transfer: Given 3 boxes and 4 assignments, predict the value in each box (unseen layout).
- Mastery: predict exact; build one line "put 3 into total". Assess 70.
- State: concept `variables`; S, E.

**L3 · `variables_state` — The Memory Palace: State Changes** ★
- Objective: A name holds *one* current value; later assignment replaces it; order matters.
- Misconceptions: `first_assignment_wins`, `cross_contamination`, `swap_without_temp`.
- Transfer: `a = 2; b = a; a = 5` — predict `(a, b)`; then the Poisoned Swap break (`a, b = b, a`, expected `2 5`).
- Mastery: verifier PASS today; assess 70. State: `programming_fundamentals:variables`; S, E, W(`swap_without_temp`).

**L4 · `types_values` — Values, Types, and Type Errors**
- Objective: Classify `int/float/str/bool`; read `type()` output; predict `TypeError` outcomes.
- Misconceptions: `everything_strings`, `plus_confusion` (str+int), `integer_division_confusion` (`/` vs `//`).
- Transfer: Predict which of 4 expressions raise and which print; unseen expression mix.
- Mastery: predict exact + one explain. Assess 70.
- State: concept `types`; S, E, W(`plus_confusion`).

**L5 · `expressions_order` — Order of Evaluation**
- Objective: Use precedence `() > ** > * / // % > + -` to read/write compound expressions.
- Misconceptions: `left_to_right` (precedence ignored), `parentheses_always`, `remainder_sign`.
- Transfer: Given a spec in words ("seven less than three times x"), produce the expression that evaluates hidden-test cases.
- Mastery: build hidden 100 + predict exact. Assess 70.
- State: concept `expressions`; S, E, W(`left_to_right`).

**L6 · `strings_words` — The Stringed Loom: Text as Data** ★
- Objective: Concatenate, repeat, index, `len`; read string code.
- Misconceptions: `strings_mutable` (written-over strategies), `index_start_one`, `char_tokenization`.
- Transfer: The Uncuttable Thread break (`word[0] = ...` TypeError → `word[0].upper() + word[1:]`, expected `Hello`).
- Mastery: verifier PASS today; assess 70. State: `programming_fundamentals:strings`; S, E, W(`strings_mutable`).

**L7 · `trace_mini` — Chapter Transfer: Read the Whole**
- Objective: Trace a 7–10 line program mixing L1–L6 **without running it first**.
- Misconceptions: none in this lesson (pure transfer); hint ladder only.
- Transfer: Two unseen programs; exact output + one-sentence "why" per program (keyword-graded).
- Mastery: both exact, both explains pass, assess 70. This is snapshot #1 of the north-star trace skill.
- State: concept `chapter1_read`; S, E.

### Chapter 2 — Choice (booleans and decisions)

**L8 · `booleans_compare` — Booleans and Comparisons**
- Objective: Read/correctly use `== != < > <= >=`; know `=` is assignment.
- Misconceptions: `single_equals_compare`, `comparison_direction`, `bool_as_string`.
- Transfer: Given an unseen sorting rule, produce the correct comparison expression.
- Mastery: build hidden 100; predict exact. Assess 70.
- State: concept `booleans`; S, E, W(`single_equals_compare`).

**L9 · `control_flow` — The Forking Path** ★
- Objective: `if`/`else` picks one and only one path; the "no" case is handled.
- Misconceptions: `missing_else`, `condition_overlook` (condition never true), `indentation_ignored`.
- Transfer: The Faulty Guard break (`if age < 12 = True:` SyntaxError → `if age < 12:`, expected `child`).
- Mastery: verifier PASS today; assess 70. State: `programming_fundamentals:control_flow`; S, E, W(`missing_else`).

**L10 · `elif_chain` — Ordered Decisions**
- Objective: Model elif as *first true branch runs*; order conditions low→high.
- Misconceptions: `first_match_confusion`, `unreachable_branch`, `all_conditions_evaluated`.
- Transfer: Grade boundaries (A/B/C/F) — reorder an unseen correct chain to be wrong-free.
- Mastery: build hidden 100 (grade function). Assess 70.
- State: concept `decisions`; S, E, W(`unreachable_branch`).

**L11 · `logic_combo` — and / or / not**
- Objective: Reason truth tables for `and/or/not`; read compound conditions aloud.
- Misconceptions: `or_means_either_but_not_both`, `negated_comparison` (need De Morgan at intuition level), `operator_precedence_bool`.
- Transfer: Convert an English "unless / otherwise" rule (e.g., "discount if Saturday or sale") into a compound boolean.
- Mastery: build hidden 100. Assess 70.
- State: concept `booleans`; S, E, W(`or_means_not_both`).

**L12 · `condition_bugs` — Debug the Wrong Condition**
- Objective: Find why a condition is inverted, off-by-one, or misses an edge.
- Misconceptions to *spot* (not hold): `inverted_logic`, `boundary_open_vs_closed`, `negate_forgot`.
- Transfer: Three seeded defects, each with a failing test — locate, explain, repair (normalized-fix graded).
- Mastery: all 3 fixes exact + explanation passes; assess 70. Feeds repair when failed.
- State: concept `control_flow`; S, E, W(repaired-from tags).

**L13 · `condition_spec` — Eligibility Spec → Code**
- Objective: Parse an English rule with multiple clauses into one correct condition, test it.
- Misconceptions: `missing_clause`, `range_boundary`, `logic_order_irrelevant`.
- Transfer: "Pass if 18–60 and member or staff" — hidden tests on all clause combinations.
- Mastery: hidden 100 + explain. Assess 70.
- State: concept `decisions`; S, E.

**L14 · `decision_oa` — Timed Placement: Decide + Loop**
- Objective: Solve 2 timed decision problems (e.g., leap year, ticket price) with loop seasoning.
- Misconceptions: performance-pressure misreads; hint ladder, no spy.
- Transfer: unseen items, mixed difficulty. Explain one choice.
- Mastery: 2/2 hidden passes; 80. State: `oa` event + weakness profile.
- State: concept `decisions`; S, E, OA result row.

### Chapter 3 — Repetition (controlled loops)

**L15 · `while_loop` — Controlled Repetition**
- Objective: `while` needs a condition that *changes*; counters and sentinels.
- Misconceptions: `guaranteed_termination`, `condition_once`, `sentinel_forgot`.
- Transfer: Predict loop passes for an unseen counter/sentinel loop. Build a while reading until `-1`.
- Mastery: predict exact + build hidden 100. Assess 70.
- State: concept `loops`; S, E, W(`guaranteed_termination`).

**L16 · `loops` — The Lantern Row: for/range** ★
- Objective: `for i in range(...)`; `range(n)` = 0..n-1; manipulate to change behavior.
- Misconceptions: `range_includes_stop`, `loop_variable_leaks`, `accumulator_start_zero`.
- Transfer: The Summing Crime break (`range(1,3)` sums 3 → `for i in range(1, 4):`, expected `6`).
- Mastery: verifier PASS today; assess 70. State: `programming_fundamentals:loops`; S, E, W(`range_includes_stop`).

**L17 · `accumulate_run` — Accumulators: Sum and Count**
- Objective: Sum/count/track running total; predict running totals mid-loop.
- Misconceptions: `accumulator_inside_loop` (reset each pass), `off_by_one_last_pass`, `product_product`.
- Transfer: Predict printed running total after pass 3 (unseen data). Build "how many even numbers in a range".
- Mastery: predict exact + hidden 100. Assess 70.
- State: concept `loops`; S, E, W(`accumulator_inside_loop`).

**L18 · `string_walk` — Walk a String**
- Objective: Iterate characters; accumulate digit sums / vowel counts; convert char→int.
- Misconceptions: `char_is_number`, `index_vs_char`, `modifying_while_walking`.
- Transfer: Build `sum of digits of "1a2b3"`-style unseen prompt.
- Mastery: hidden 100. Assess 70.
- State: concept `strings`; S, E, W(`char_is_number`).

**L19 · `loop_stop` — Break, Continue, Nested Loops**
- Objective: `break` exits the *innermost* loop; `continue` skips one pass.
- Misconceptions: `break_exits_all`, `continue_skips_rest_of_program`, `nested_counter_fusion`.
- Transfer: Predict which numbers print for an unseen nested/break puzzle.
- Mastery: predict exact + build hidden 100. Assess 70.
- State: concept `loops`; S, E, W(`break_exits_all`).

**L20 · `loop_bugs` — The Off-by-One and the Infinite**
- Objective: Debug stop-boundary, wrong accumulator, infinite-loop risk.
- Misconceptions to spot: `range_off_by_one`, `accumulator_wrong_place`, `loop_termination`.
- Transfer: Three seeded loop defects with failing outputs — locate, explain, repair.
- Mastery: 3/3 fixes exact; assess 70. Feeds repair.
- State: concept `loops`; S, E, W.

**L21 · `loop_transfer` — Timed: Sum Every Even Digit**
- Objective: Parse a timed prompt, plan, build, test the hidden cases.
- Misconceptions: digit-vs-number; boundary of "even digit"; zero handling.
- Transfer: unseen digit-filter prompt; hidden tests 100 + short explain.
- Mastery: 80. State: concept `loops`; S, E.

### Chapter 4 — Collections (lists)

**L22 · `arrays` — The Warehouse Stack** ★
- Objective: Indexing `l[0]`, negatives `l[-1]`, `len`; reading list code.
- Misconceptions: `index_start_one`, `negative_index_mystery`, `last_index_is_len`.
- Transfer: The Vanished Crate break (`i = len(nums)` IndexError → `i = len(nums) - 1`, expected `3`).
- Mastery: verifier PASS today; assess 70. State: `programming_fundamentals:arrays`; S, E, W(`index_start_one`).

**L23 · `list_mutate` — Mutate in Place vs Rebind**
- Objective: `append/insert/remove`, `l[i] = v`; distinguish in-place change from rebinding `l = [...]`.
- Misconceptions: `assign_copies_list`, `index_overwrite_appends`, `removing_while_indexing`.
- Transfer: Decide which statements change a list vs rebind (unseen sequence of ops → final list).
- Mastery: predict exact + build hidden 100. Assess 70.
- State: concept `arrays`; S, E, W(`assign_copies_list`).

**L24 · `list_walk` — Traverse a List**
- Objective: Sum/max/count over a list; `for x in l`, `enumerate`.
- Misconceptions: `element_vs_index`, `max_initialised_zero` (fails for negatives), `off_by_one_last`.
- Transfer: Build "max of list handling negatives" against hidden tests; predict hand-run total.
- Mastery: hidden 100 + predict exact. Assess 70.
- State: concept `arrays`; S, E, W(`max_initialised_zero`).

**L25 · `list_build` — Build New Lists**
- Objective: Filter/transform via explicit loops into a *new* list (comprehension intuition, not syntax).
- Misconceptions: `modify_during_build`, `filter_means_delete`, `sharing_new_list`.
- Transfer: Build "all scores above 60 in order" for unseen data.
- Mastery: hidden 100. Assess 70.
- State: concept `arrays`; S, E.

**L26 · `list_copy` — Slicing, Aliasing, Copying**
- Objective: `l[:n]` copies the *slice*; `b = a` aliases; `list(a)`/slices copy.
- Misconceptions: `slice_aliases`, `append_affects_copy`, `copy_is_shallow_enough`.
- Transfer: Predict which lists change when `b = a` vs `b = a[:]` (unseen mutate-after).
- Mastery: predict exact. Assess 70.
- State: concept `arrays`; S, E, W(`slice_aliases`).

**L27 · `list_bugs` — Index, Boundary, Alias**
- Objective: Debug wrong index, boundary, mutation-during-iteration, alias surprise.
- Misconceptions to spot: `index_off_by_one`, `mutate_while_iterating`, `alias_mutation_leak`.
- Transfer: Three seeded list defects with failing tests — locate, explain, repair.
- Mastery: 3/3 fixes exact; assess 70. Feeds repair.
- State: concept `arrays`; S, E, W.

**L28 · `list_transfer` — Timed: Second-Largest**
- Objective: Parse + plan + build a list problem with edge cases (duplicates, negatives, single-element).
- Misconceptions: `second_max_via_sort`, `dup_collapse`, `singleton_crash`.
- Transfer: Second-largest hidden tests incl. [5,5,4]; explain your plan first.
- Mastery: 80. State: concept `arrays`; S, E.

### Chapter 5 — Express & Perform (functions → placement)

**L29 · `functions` — The Function Forge** ★
- Objective: `def`, parameters, `return` vs `print`; call/reuse a function.
- Misconceptions: `print_returns`, `missing_return_none`, `args_match_required`.
- Transfer: The Silent Forge break (`print` instead of `return` → `return result`, expected `10`).
- Mastery: verifier PASS today; assess 70. State: `programming_fundamentals:functions`; S, E, W(`print_returns`).

**L30 · `scope_rules` — Locals, Globals, Copies**
- Objective: Locals die at `return`; globals don't change inside; parameters are copies.
- Misconceptions: `inside_changes_leak`, `global_always_readable_as_writable`, `parameter_pointer`.
- Transfer: Predict output of a function that returns while a global looks unchanged (unseen).
- Mastery: predict exact + explain. Assess 70.
- State: concept `functions`; S, E, W(`inside_changes_leak`).

**L31 · `compose_reuse` — Compose Small Functions**
- Objective: Factor repetition into helpers; named intermediate values; read a 2-function pipeline.
- Misconceptions: `one_big_function`, `recompute_is_fine`, `copy_paste_reuse`.
- Transfer: Build `is_valid(...)` composed from two unseen small helpers.
- Mastery: hidden 100. Assess 70.
- State: concept `functions`; S, E.

**L32 · `function_bugs` — Debug the Silent Forge**
- Objective: Debug missing return, wrong arg order, shadowing, parameter mutation.
- Misconceptions to spot: `missing_return`, `wrong_arg_order`, `shadow_global`.
- Transfer: Three seeded function defects with failing outputs — locate, explain, repair.
- Mastery: 3/3 fixes exact; assess 70. Feeds repair.
- State: concept `functions`; S, E, W.

**L33 · `sorting` — The Sorting Bazaar** ★
- Objective: Selection/bubble *one pass at a time*; predict the list after each pass. Placement vocabulary, beginner depth.
- Misconceptions: `one_pass_sorts`, `swap_without_temp`, `sorted_is_destructive`.
- Transfer: The Vanishing Crate Swap break (`nums[i], nums[j] = nums[j], nums[i]`, expected `[2, 1]`).
- Mastery: verifier PASS today; assess 70. State: `programming_fundamentals:sorting`; S, E, W(`one_pass_sorts`).

**L34 · `complexity` — The Observatory: Reading Scale** ★
- Objective: Read, not derive: does the work double when input doubles? (linear vs nested vs constant).
- Misconceptions: `feels_fast_is_fast`, `nested_is_linear`, `dropped_constant_ignored`.
- Transfer: The Accidental Bombard break (nested when single intended → `for i in range(n): total += 1`, expects `True`).
- Mastery: verifier PASS today; assess 70. State: `programming_fundamentals:complexity`; S, E, W(`nested_is_linear`).

**L35 · `capstone_oa` — World-1 Performance** ★(new assessment + repair stage)
- Objective: Solve 4 unseen timed placement-style problems **unaided**, then explain one solution aloud; the World-1 metric.
- Misconceptions: none hosted — performance measurement only.
- Transfer: unseen item set across L1–L34 competencies (read, decide, loop, list, function); hidden tests 100 = "solved"; explanation keyword-cluster = "explained".
- Mastery: **World-1 metric = (% true beginners who solve + explain ≥1 unseen problem).** Per-problem competency tagging enables repair.
- State: `oa_sessions` row (per-problem results, time, hints used, all-or-nothing code pass); weakness profile → `repair_missions` per failed competency; gamification only via `record_practice` (Gamification Law).

---

## 5. Student-State Write Contract

Server state only. Frontend never computes level/score. Question/lesson content never in
Mongo (Question Bank Residency Rule — lessons are content files; DB holds *student state*).

### Shared writes (every lesson; implemented today in `LessonService.complete_lesson`)
| Collection | Document/fields | Notes |
|---|---|---|
| `gamification` | `completed_competencies["code_foundations:<competency_id>"]` = {`completed`, `score`, `best_score` (ratchet, atomic claim), `attempts`, `completed_at`} | Idempotent; improvement-only Diamond award |
| `gamification` | `last_practice_date` touch on replay (streak protection, zero other mutation) | |
| `gamification` + ledger | `record_practice(activity_type="lesson", score/10, metadata={lesson_id,time_spent})` | **Only XP/level/streak writer**; one immutable `gamification_events` row; `profile.xp` reconciles |
| `srs_states` | First card on mastery: `{concept_id, interval, repetitions, ease_factor, next_review, learning_step, totals, key_points, spaced_fields}` | Only SRS writer is `SpacedRepetitionEngine` (`create_new_card`) |

Per-lesson `concept_id`s (registry truth): `variables`·`control_flow`·`loops`·`arrays`·
`strings`·`functions`·`sorting`·`complexity` (all `programming_fundamentals:*`) + new
`types`·`expressions`·`booleans`·`decisions` for L4/5/8/10–14.

### Writes to ADD before World 1 ships (gaps vs today's lesson engine)
| # | Gap | Required write | Purpose |
|---|---|---|---|
| G1 | Per-stage attempts are not persisted | `learning_events` append-only row per graded stage (`predict/explain/build/break_diagnosis/break_fix/transfer/assess`): `{user_id, lesson_id, stage, correct, time_ms, ts}` | Traces *capability trajectory*, not just completion; feeds dashboard + AI Interview memory |
| G2 | No misconception signal | `user_weaknesses`: `{concept_id, misconception_id, count}` upsert on failed break/explain | Repair pipeline (intelligent failure, AGENTS gate 3) — a *specific* repair path, not "wrong answer" |
| G3 | Delayed retrieval not wired | SRS `retrieve` stage replays prior cards (spaced_fields); lesson `retrieve` phase calls SRS review API | Capability 6; drives engagement + durability |
| G4 | Capstone report/repair missing | `oa_sessions` per-problem result row (L35) → weakness profile → `repair_missions` per failed competency | AGENTS gate 3 (mock-OA → specific repair path); north-star denominator/numerator |
| G5 | Per-lesson lesson_id ≠ competency for new nodes | New lessons set `world_progression.competency_id` + `unlocks_next` graph chaining 1→35 | Progress serialization in World 1 → Journey |

New lesson modules: `backend/app/content/curriculum/world1_*.py` (chunks of ~7 for
reviewability), registered in `registry.py`, validated by extending
`backend/scripts/verify_concept_clarity.py` (same contract as the ★ set).

---

## 6. North-Star Measurement (Capability gained per student)

Instrumented at L35, logged per student, rolled up per cohort:

**Denominator.** True beginners (self-assessed ≤1 on "can you write a 5-line program?") who
commence L1 **and** reach L35.
**Numerator.** At L35, solve ≥1 unseen problem with **0 hints**, **100% hidden tests**,
**and** a keyword-cluster-passing explanation of their approach.

Report the conversion rate and the gap (solved-but-cannot-explain vs
solved+explained) — the second number is the differentiator no question bank offers.

Milestone snapshots to catch mid-course drop-off: L7 (chapter read-transfer), L14,
L21, L28, then L35.

---

## 7. World 1 Quality Gates (binding, maps to AGENTS.md)

1. **Content correctness (Gate 1):** no lesson served until its transfer/break/assessment
   expected outputs are *executed*, not authored — `AUTOMATED_CHECKED` then `HUMAN_REVIEWED`
   before promotion; quarantine on doubt.
2. **Complete loop (Gate 2):** each of the 35 lessons proves transfer with real executed
   evidence in its verifier report — "completion is not mastery."
3. **Repair (Gate 3):** failing L35 competencies produce named `repair_missions` with a
   concrete fix path (specific misconception → guided practice → retest).
4. **AI Interview memory (Gate 4):** interview consumes `learning_events` + `user_weaknesses`
   + `oa_sessions` — a transcript personalized by actual student state.
5. **No gaming the metric:** L35 numerator requires *unaided* pass (hints recorded and
   excluded); `record_practice` remains the sole XP writer throughout.