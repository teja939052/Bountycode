# Intake candidates (not served)

These files are a review queue, not student-facing content. They are not
loaded by `question_store`; every question/task candidate is marked
`trust_status: "unverified"`. Do not add this directory to a serving loader.

| File | Items | Purpose | Trust boundary |
| --- | ---: | --- | --- |
| `aptitude_generated_v2.json` | 250 | Aptitude and logical series | Computed and independently recomputed; still unverified |
| `pseudocode_generated_v2.json` | 60 | Code-tracing / pseudocode | Execution-derived output; human review still required |
| `verbal_generated_v2.json` | 120 | Six verbal subtypes, 20 each | Human review required |
| `essay_prompts_v2.json` | 28 prompts + rubric | Essay practice | Draft rubric; calibrate against 30 human-scored essays before any readiness use |
| `spoken_english_tasks_v2.json` | 30 | Read-aloud, repeat and short-answer practice | Practice only; no readiness scoring |
| `company_blueprints_additions.json` | 4 drafts | Cognizant GenC, Tech Mahindra, LTIMindtree and Infosys general pseudocode | Unofficial sources with recorded conflicts; not confirmed formats |

The 80 verified option repairs are maintained separately in
`app/data/verified_mcq_option_overrides.json`. The normal question-store load
applies them before deduplication and never changes `trust_status`. Rebuild
that small overlay with `python scripts/restore_mcq_options.py`.

Run `python scripts/validate_intake_v2.py` from `backend/` to check candidate
file structure, unique IDs, answer-key alignment and trust state. This is a
structural check, not proof of content quality or independent ground truth.

Seeded generators:
- `python scripts/gen_aptitude_items.py`
- `python scripts/gen_pseudocode_items.py`
- `python scripts/gen_verbal_items.py`
- `python scripts/gen_communication_items.py`

The existing `lint_intake.py`, `ground_truth_sweep.py` and `promote_tranche.py`
do not consume this directory: they audit the loaded store, served coding
questions, and existing parametric/autocheck banks respectively.

Promotion gate: re-run the generators and structural validator, review
wording, distractors, explanations and tags in batches, inspect pseudocode
and every distractor, calibrate the essay rubric, and independently verify
company-specific formats. Promote only through a separate audited human-review
path. No candidate is served or used for readiness in this commit.
