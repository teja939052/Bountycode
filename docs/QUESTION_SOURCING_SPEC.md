# BountyCode — Question Sourcing & Seeding Spec (for future content work)

Context: `intake_lint.py` now blocks obvious filler (stubs, formatters, malformed MCQs) at
submission time, and the 26-question self-stamping incident proved that execution
verification alone can pass a wrong solution against wrong-but-matching test cases. Every
rule below exists to stop that specific failure from recurring at larger volume, since new
sourcing is exactly when volume pressure tempts someone to skip a step.

---

## 1. The non-negotiable pipeline for any new batch

**No new question reaches a student without passing through all of these, in order —
no shortcuts for "this batch is small" or "this source is trusted":**

1. `intake_lint.py` at submission (already wired) — rejects stubs/formatters/malformed
   MCQs automatically. This catches *content that's obviously fake*, not content that's
   *subtly wrong*.
2. Deterministic verification (`verify_question`) — runs the solution against test cases.
   Passing this only proves internal consistency (solution matches its own test cases),
   **not correctness** — this is the exact gap the 26-question incident exploited.
3. **An independent sanity check per question**, separate from whoever authored the
   solution+test cases (`ground_truth.py` cross-check + tranche gate). Concretely: for
   coding questions, a second independently-derived solution (or independently-sourced
   expected outputs) must agree with the stored test cases exactly. This is the actual
   fix for the self-stamping gap — lint and execution verification both check internal
   consistency, never ground truth.
4. Tranche staging → human review (existing ~11-min/tranche rhythm) → promotion.
5. Only after promotion does `trust_status` move past `automated_checked`.

**Rule of thumb:** if a new batch is large enough that step 3 feels like it'd slow things
down too much to bother, that's the volume warning sign, not a reason to skip it — smaller,
independently-checked batches beat larger, self-consistent-only ones every time. This is
the same principle as the GD/aptitude decision from earlier: quality over volume, because
volume with a self-stamping gap is how you got 26 fake questions served in the first place.

---

## 2. What to prioritize sourcing (tied to the actual product strategy)

Don't source generically. Prioritize by what's both high-demand and currently thin:

- **GD (group discussion) topics** — currently at 0 content, target ~150-200 human-
  reviewed topics across current-affairs / abstract / case-study / controversial-but-safe.
  This is the identified market differentiator; it should be sourced and reviewed first,
  not last.
- **Company-specific aptitude/OA content for TCS/Infosys/Wipro-style formats** — the
  `prioritized_verify_queue.py` scoring (TCS/Infosys/Wipro +100, FAANG +50) already tells
  you where real demand concentrates. New sourcing should follow that same weighting:
  Arrays, Graphs, DP-1D, Trees were the top patterns by demand — fill gaps there first.
- **SQL, with schema metadata from day one** — any new SQL question MUST ship with
  `sql_schema` (schema_ddl, seed_inserts, expected_query) at authoring time, not added
  later. The 932 currently-quarantined SQL questions are quarantined specifically because
  this was skipped originally — don't repeat that mistake on new ones.
- **Editorials / written walkthroughs** — flagged as "live but basic" (raw reference
  solution, not real explanation). If sourcing effort is available, upgrading existing
  high-traffic questions' editorials is higher-value than adding net-new questions in a
  pattern that's already well-covered.

---

## 3. Deduplication and metadata requirements for every new question

- Run through `_dedupe_and_filter()`'s normalized-title collapse before anything else —
  don't let a new batch reintroduce duplicates that were already cleaned out.
- **Company tags only when genuinely verified against a real, current pattern** — per the
  standing rule from the OA-fidelity work. A question tagged "Amazon" because it's
  DSA-flavored and Amazon asks DSA questions is not verified; it needs to trace to an
  actual known platform or source.
- Pattern/topic tags (Striver pattern list) required on every coding question — this is
  what the prioritized-queue scoring and the "similar questions" feature both depend on.
  An untagged question is invisible to both systems.
- `last_verified_at` — required if the question is company/pattern-specific and could go
  stale (hiring formats change season to season).

---

## 4. What NOT to do when sourcing at volume

- **Never let an LLM generate both the solution and the test cases for the same
  question.** This is structurally the same failure as the 26-stub incident — a single
  source that's internally consistent but never checked against ground truth. If LLM
  drafting is used at all (per the existing `llm_draft_5000`-style intake), the test
  cases must come from an independent, deterministic source (the reference platform, a
  second author, or execution against a *separately human-verified* solution) — never
  from the same generation pass as the solution.
- **Never promote past `automated_checked` without the tranche human-review step**,
  regardless of how confident automated checks look. This has been the standing rule all
  thread; new sourcing doesn't get an exception because it's "obviously fine."
- **Never batch-import a large external question set without running it through
  `intake_lint.py` first**, even if the source seems reputable. Reputable sources still
  contain filler, mislabeled content, and formatting mismatches with your executor's
  calling conventions.
- **Don't chase 100% servability as a target.** Per the standing gap-analysis rule:
  structurally broken content (no test cases, no example, no real solution) goes to a
  "needs authoring" list, not an automation queue. Authoring effort should go toward the
  high-demand gaps in section 2, not toward salvaging low-value stub content.

---

## 5. Recurring maintenance, not a one-time pass

- **Re-run `lint_intake.py`'s spot-check periodically**, not just once — it's a scan
  tool as much as a gate, and periodic re-runs catch anything that slipped through before
  the lint existed, or through any future ingestion path that bypasses the submit
  endpoint (a direct bank-file edit, for instance).
- **Track servable % as a trend, reviewed regularly** — not a number you compute once
  and stop watching. A new content source, a new judge version, or a schema change can
  all quietly shift it.
- **Every quarantine action should leave a reason in `served_quarantine.json`'s
  metadata** (already the case for the 26-stub batch) — future reviewers need to know
  *why* something was pulled, not just that it was.

---

## One-line summary for whoever sources the next batch

**Internal consistency (solution matches its own test cases) is not correctness. Every
new question needs a ground-truth check from a source independent of whoever wrote the
solution — that's the one rule this whole spec exists to enforce.**
