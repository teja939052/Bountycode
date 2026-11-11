# Content Quality Policy — Student-Facing Path

## Principle
Students only see **curated, answer-verified, pattern-matched** items on the learning and mock path.
Volume without truth is waste.

## Student-facing sources (allow)
| Source | Use |
|--------|-----|
| `service_oa_problem_bank_part*.json` with `source_style: service_oa_original` | Service OA mocks |
| Lesson `assessment.questions` inside `data/lessons/*.json` | Academy mastery checks |
| Files listed in `COMPANY_CONTENT_STATUS.md` as **Verified / Registered** only after schema check | Company drills |

## Not student-facing by default (quarantine)
- Unverified scraped dumps
- Placeholder / broken option banks
- Items without `correct_index` or `explanation`
- Anything labeled only by rumor ("asked in 2019") without independent solve

Default public label: **"{Company}-pattern practice"** — never claim a real past paper without a dated primary source.

## Quality gates before publish
1. Exactly one correct option; distractors distinct
2. Explanation shows the method (not just the answer)
3. Topic maps to skill graph / sprint lesson
4. Time target realistic for service OA (~45–90s MCQ)
5. No duplicate stem with different answers

## Expansion method
Prefer **parametric generators** (quant, pseudocode) where a script computes the answer, then human-review the stem.
Verbal RC remains human-authored.

## Wiring
- Mocks: `service_oa_mocks` loads all `service_oa_problem_bank_part*.json`
- Study today: sprint lessons + weak-skill remediation — not random bank dumps
