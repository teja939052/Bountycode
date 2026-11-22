# Recovered legacy lesson candidates

**Status: CANDIDATE / NOT STUDENT-SERVING**

These five lesson drafts were recovered from the historical branch
`bountycode/academy-unification-and-resume` on 2026-11-19.

They are stored here rather than in `backend/app/data/lessons/` because
`app/routes/company_lessons.py` discovers and serves JSON files from that
live directory. Moving them into the candidate directory prevents accidental
publication before human content review and canonical skill mapping.

| Slug | Purpose | Automated structural review |
|---|---|---|
| data_interpretation | Quantitative aptitude / data interpretation | Step and assessment answer-key shape passed |
| loops_code_lab | Programming / loop code lab | Assessment shape passed; interactive/code-lab step needs manual contract review |
| percentages | Quantitative aptitude / percentage foundations | Step and assessment answer-key shape passed |
| pseudocode_trace | Pseudocode output tracing | Assessment shape passed; output-tracing step needs manual contract review |
| seating_arrangement | Logical reasoning / seating arrangements | Step and assessment answer-key shape passed |

Automated checks only establish basic structure. They do **not** prove mathematical
correctness, answer-key correctness, pedagogical quality, accessibility, or
compatibility with the current lesson player.

Before promotion:
1. Have a human reviewer solve every worked example and question independently.
2. Verify all answer keys, edge cases, explanations and hints.
3. Validate special step types against the current player and server grader.
4. Map each lesson to a canonical skill ID and prerequisite set.
5. Add tests and explicit serving/registry integration.
6. Move approved files to the live lesson directory in a separate reviewed change.

No question-trust or lesson-publication status is promoted by this recovery.
