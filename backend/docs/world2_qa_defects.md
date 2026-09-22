# World 2 Runtime QA — Defect Table

## Defects Found

| ID | Severity | File | Issue | Impact |
|----|----------|------|-------|--------|
| D-01 | P1 | `frontend/src/pages/LessonPage.tsx:1044` | `DiscoveryStepView` only renders `interaction.type === "reveal_value"`. World 2 uses `interaction="select-value"` with `values[]` and `answer`. The multiple-choice buttons never render. | Manipulate/discover interactive choices are invisible. Student sees a blank or generic button instead of the actual choices. |
| D-02 | P2 | `frontend/src/pages/LessonPage.tsx` | No explicit "break" or "debug" phase in `LessonPage`. Break/debug content is only embedded in assessment questions, not experienced as deliberate failure/debugging steps. | Students don't get the intended "break it → debug it" learning loop. |
| D-03 | P2 | `frontend/src/pages/LessonPage.tsx` | No explicit "retrieve" phase. SRS enrollment happens in backend (`_ensure_srs_card`), but there's no retrieval practice UI in the lesson flow. | Students don't experience spaced retrieval during the lesson. |
| D-04 | P2 | `frontend/src/pages/LessonPage.tsx:979` | `handleComplete` calls `window.location.reload()` instead of navigating via router. | Full page reload on completion; loses SPA state, feels jarring. |
| D-05 | P3 | `frontend/src/pages/LessonPage.tsx:805` | Transfer retry logic: `stepAttempts < (lesson.transfer_challenge.passing_score ? 3 : (lesson.transfer_challenge.max_attempts || 3))`. `passing_score` (e.g., 70) is used as a truthy boolean to force max attempts to 3, ignoring actual `max_attempts`. | If `passing_score` is set, `max_attempts` is ignored. |
| D-06 | P3 | `backend/app/services/lesson.py:377` | Debug assessment grading uses exact string match: `correct = actual == expected_fix.strip()`. | Students with semantically equivalent but differently-formatted fixes are marked wrong. |
| D-07 | P3 | `frontend/src/pages/LessonPage.tsx` | Debug steps in `guided_build` show a code editor but don't render the `buggy_code` as read-only. Students see a blank editor instead of the broken code. | Debug step doesn't show what needs fixing. |
| D-08 | P3 | `frontend/src/pages/LessonPage.tsx` | Editor heights are fixed (`h-64`, `h-80`). On small mobile screens (320-430px), this can cause vertical overflow or cramped layout. | Mobile UX degradation. |
| D-09 | P3 | `backend/app/content/world2_problem_solver.py` | Content uses `step_type="break"` but `LevelBase` model field is `break_step` (alias `break`). Works via LessonPage adapter, but would break if ever consumed by `LevelPlayer`. | Architectural inconsistency; future integration risk. |

## Verified Working

- Backend lesson routes: `GET /api/v1/lesson/{slug}`, `POST /build`, `POST /transfer`, `POST /predict`, `POST /assess`, `POST /complete`
- Backend `LessonService` methods: `submit_build_step`, `check_prediction`, `check_assessment`, `complete_lesson`
- `world2_bridge.py` adapter correctly maps `LessonDefinition` → rich `LessonContent`
- World 2 lessons are accessible via `/lesson/arrays-1` through `/lesson/arrays-boss`
- Backend compiles clean
- Frontend builds clean

## Not Tested (requires browser)

- D-01: select-value rendering at 390px/430px
- D-02/D-03: break/debug/retrieve phase rendering
- D-04: completion reload behavior
- D-05: transfer retry limit behavior
- D-06: debug grading tolerance
- D-07: debug step buggy_code visibility
- D-08: mobile editor overflow
- End-to-end: story → discover → predict → build → transfer → assess → complete
- XP awarded exactly once
- SRS enrollment persistence
- Refresh/back navigation safety
