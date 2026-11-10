# Service-company content quality audit

**Snapshot date:** 10 November 2026  
**Scope:** Existing Bountycode company banks, general aptitude/verbal/reasoning banks, step-based lessons and content loader.  
**Disposition:** Findings are review candidates. This report does not change or delete existing question records.

## 1. Inventory is not quality

The existing report at backend/app/data/COMPANY_CONTENT_STATUS.md states 2,977 generated questions and 2,689 serveable questions across TCS NQT, Infosys InfyTQ, Wipro NLTH, Cognizant GenC and Capgemini/Accenture banks.

Those figures are useful inventory indicators only. "Generated" and "serveable" do not prove:
- the prompt matches the solution's input contract;
- the expected output is correct;
- the distractors are unambiguous;
- the explanation teaches a transferable method;
- company attribution has a current source;
- the item has independent human review.

Do not use the 2,689 count as a quality or readiness metric.

## 2. Concrete defects found in sampled files

### A. Cognizant generated coding bank

File: backend/app/data/cognizant_genc_verified.json

Sample item IDs:
- cognizant_coding_001 — "Two Sum"
- cognizant_coding_002 — "Reverse Array"
- cognizant_coding_003 — "Check Prime"

Observed issues:
1. The "Two Sum" record uses scalar test inputs 0, 1 and 5 with scalar outputs 1, 1 and 8. Its solution expects an array and target. These test cases do not exercise the stated problem contract.
2. "Reverse Array" has the same generic scalar testcases (0→1, 1→1, 5→8), not arrays and expected reversed arrays.
3. "Check Prime" has a test case input 1 with expected true, while the supplied solution explicitly returns false for n <= 1. This is a direct answer/test-oracle contradiction.
4. Explanations such as "Solve two sum using an efficient approach", hints such as "Hint 1 for two sum", and reasoning steps such as "Understand problem. Choose approach. Implement. Test. Return result." are templates, not useful pedagogical scaffolding.
5. The file labels items trust_status=verified and verification_version=automated_checked_v1. That is not itself evidence of human review or a complete independent correctness review.

**Action:** Quarantine these item IDs from trusted mocks until each problem statement, function contract, examples, visible/hidden cases, solution and explanation are reviewed as one unit. Do not delete them in this audit PR.

### B. Logical reasoning bank

File: backend/app/data/content/reasoning/logical_reasoning.json

Sample item ID: LR-PRACTICE-001

The prompt is "Continue: A2B4C6D8E_". The options do not contain the next pair F12. The answer key chooses "10F", while the explanation itself says the coherent next pair should be F12 and then attempts to rationalize the reversed option. The item is internally inconsistent and should not be served as a trusted question.

**Action:** Replace only after a human reviewer approves a corrected sequence, answer key and explanation. Otherwise quarantine the item.

### C. Verbal bank

File: backend/app/data/content/verbal/verbal_ability.json

Sample item ID: VB-001

The stem "The earth is in great danger because of ____ pollution" with an option "all" is not a well-formed single-blank sentence: "all pollution" is not the grammatical completion. The explanation states a broad opinion rather than explaining a language/reading skill.

**Action:** Rewrite as a precise grammar, vocabulary-in-context or reading-inference task; then review its distractors and explanation.

### D. Lesson authoring quality

File: backend/app/data/lessons/flowchart_basics.json

The iteration-count explanation contains an editorial self-correction ("Wait - let me re-read"). The final count is correct, but an internal drafting note should not appear in the student-facing explanation.

**Action:** Replace with a clean state trace and independently check the loop's exact condition and increment order.

## 3. Trust-loader defect

File: backend/app/services/content_loader.py

Before this branch, each loaded item was unconditionally assigned:
- trust_status = human_reviewed
- source = bountycode_original (when the item did not provide a source)

This allowed missing trust evidence and missing provenance to be silently upgraded by the loader.

The branch changes this behavior:
- absent/unknown trust labels remain unverified;
- human_reviewed/reviewed labels map to reviewed only when reviewer, reviewed_at and decision=approved are recorded;
- verified/trusted labels map to verified only when both human review and independent validation evidence are recorded;
- source defaults to "unspecified", never a fabricated Bountycode-original provenance claim.

This records an approval trail; it does not prove the human review took place. The review evidence must refer to real review work.

## 4. Canonical curriculum alignment

The latest mainline defines `docs/SERVICE_COMPANY_CURRICULUM.md` as the canonical ordered service-company curriculum and `docs/learning/LEARNING_EXPERIENCE_STANDARD.md` as the lesson-quality standard. This branch was rebuilt from mainline commit `40b01f5926b9af5eb3c5ab4fd4080fa146634099` after those documents were added.

The mainline content status snapshot (`docs/SERVICE_COMPANY_CONTENT_STATUS.md`, updated 7 November 2026) reports Quant and Logical core/depth complete and Verbal core live. Treat those as reported inventory/status, not independent proof of every item’s correctness.

The new 17-object pack is an editorial review queue. Where it touches already-covered topics (percentages, time/work, direction reasoning and syllogisms), its intent is to supply alternate transfer scenarios and expose review gaps—not create duplicate playable lessons. Do not register it as another world or lesson registry.

## 5. Existing lesson and pattern inventory

The repository already has step-based lessons for many first-wave topics: percentages, ratios, profit/loss, averages, time & work, time/distance, probability, number series, blood relations, directions, syllogisms, coding-decoding, grammar, reading comprehension, para-jumbles, arrays, strings, hashing, sorting/searching, two pointers, sliding window, stacks/queues, recursion, trees, SQL, DBMS, OOP, operating systems and computer networks.

The highest-value next content work is not duplicating those slugs. It is:
- richer pseudocode and variable-state traces;
- data interpretation with proper tables and weighted denominators;
- better business/professional communication and email scenarios;
- practical HTTP/API, Git, testing and debugging foundations;
- stronger transfer items and diagnostic distractor feedback;
- rigorous review of legacy company banks before increasing their serveable count.

## 6. Candidate content added in this branch

File: backend/app/data/candidates/service_company_patterns_v1.json

Seventeen original learning-object candidates cover:
1. successive percentage change;
2. combined work rates;
3. service-desk data interpretation;
4. syllogism and the converse trap;
5. evidence-based reading inference;
6. professional status email;
7. nested-loop pseudocode tracing;
8. first non-repeating character;
9. HTTP idempotency and retry safety;
10. boundary-value testing;
11. average speed over equal distances;
12. coordinate-based direction reasoning;
13. subject–verb agreement with intervening phrases;
14. sequential array mutation tracing;
15. second-largest distinct array value;
16. OOP runtime method dispatch;
17. Git feature-branch and pull-request workflow.

They use the existing Learning Object shape, stable IDs, worked reasoning, recognition signals, anti-patterns, hint ladders, test/assessment examples and explicit provenance notes.

**Important:** All seventeen are authored as AI-generated, synthetic, draft, unverified candidates. They are not registered with question_store or the student lesson player. They must not be promoted until independently checked by a human reviewer.

## 7. Recommended remediation order

| Priority | Work | Acceptance evidence |
|---|---|---|
| P0 | Quarantine contradictory coding or MCQ oracles | Exact IDs blocked from trusted mocks; regression test proves exclusion |
| P0 | Repair content-loader trust upgrades | Tests show metadata-only labels remain unverified |
| P1 | Human-review the 17 candidate learning objects | Reviewer identity, date, decision, answer/explanation checks |
| P1 | Build World 4 pseudocode trace lessons deeply | Trace tables, predict steps, code labs, edge cases, transfer and server-recorded evidence |
| P1 | Expand data interpretation and verbal/communication | Multiple datasets/passages, carefully justified options, evidence-based explanations |
| P2 | Add role-targeted technical foundations (HTTP, Git, testing, APIs) | Real scenario tasks, not recall-only question dumps |
| P2 | Version company blueprints separately from question items | Source URL, checked date, scope, effective date and item versions per attempt |

## 8. Re-running the audit

Run from the repository root:

```bash
python backend/scripts/audit_service_company_content.py
python backend/scripts/audit_service_company_content.py --format json
```

The script is read-only. A low issue count is not proof of correctness; all high-stakes answers and company claims still require independent review.
