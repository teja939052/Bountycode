# Bountycode Lesson & Learning-Loop Audit

**Date:** 2026-11-06 · **Branch under audit:** `feat/coding-aptitude-learning-engine` (HEAD `7bd1e0b`) · **Base for comparison:** `origin/main` = `05b3ebf`

Scope: audited the learning/lesson system that is actually in the working tree, plus the working-tree state itself. No content was changed during this audit. All numbers below were computed from the code in this checkout; the per-lesson inventory is `docs/learning/LESSON_INVENTORY.csv` (+ `_summary.json`).

⚠️ **Alignment note for the master brief:** the brief describes the *Academy* architecture (69 × `backend/app/data/lessons/*.json`, `routes/company_lessons.py`, `routes/academy_plan.py`, `test_lesson_content_quality.py` …). In this checkout that architecture exists only partially on `origin/main` (under 10 lesson JSONs + `company_lessons.py`; no `academy_plan.py`, no quality tests). The current branch instead ships a **second, divergent lesson system** (`backend/app/services/lessons/*.py` + `lesson_service.py` + `routes/lessons.py`). PR #3's full 69-lesson library is not present on any local or remote ref here. Before investing content effort, confirm which architecture is canonical; building on top of both would be exactly the duplicate-system failure mode the brief forbids.

---

## 1. Working-tree state (checked before anything else)

`git status` shows the tree is **broken and littered in both directions**:

| Problem | Evidence | Impact |
|---|---|---|
| `backend/app/services/lessons/__init__.py` deleted (unstaged) | `git status`: ` D` | Package is no longer a real package; `from app.services.lessons import _LESSONS` fails or resolves to nothing |
| `backend/app/services/lessons/python.py` deleted (unstaged) | `git status`: ` D` | HEAD's `__init__.py` imports `.python`; even restoring `__init__.py` won't fix — an updated `__init__.py` must also come back |
| Stray untracked `app/` dir at repo root | `app/services/lessons/{__init__.py, dsa.py}` | A scratch script was run from the wrong cwd; contains a *better* `__init__.py` (imports `python_content`) than the deleted one. Probe the wrong-path copy; it should not exist at repo root |
| ~15 uncommitted scratch scripts | `add_java_api.py`, `append_dsa_final.py`, `remove_python.py`, `backend/remove_python.py`, `backend/app/services/lessons/_add_*.py`, `*_append*.py`, `backend/temp.txt`, `backend/test_file.txt`, `frontend/vite_output.txt` … | Exactly the "template-based" tooling that produced the filler content; none should be committed |
| Backend does not start | `import app.main` → `RuntimeError: Failed to import 1 route module(s): lessons (ImportError: cannot import name '_LESSONS' …)`; `pytest --collect-only` fails on this too | **App and whole backend test suite are un-runnable right now** |
| Frontend has 47 typecheck errors; 3 files structurally mangled | `GamificationDashboard.tsx`, `LessonView.tsx` are mangled in **committed HEAD** (streak-tab JSX spliced incorrectly); uncommitted `SkillMap.tsx` draft is truncated mid-JSX (no `useNavigate` import, broken ends) | `npm run typecheck` ❌; production build will fail |

## 2. The lesson catalog — real numbers (simulated aggregation in execution order of the intended `__init__.py`)

- **1,239 lesson objects defined → 1,112 unique IDs → 60 IDs silently overwritten** by later modules (e.g. `cs1`–`cs4` defined 4×, `dsa-arrays-1` 4×). `__init__.py` does blind `_LESSONS[id] = lesson` with no conflict detection.
- Hand-authored tracks are **tiny**: aptitude 7, logical 5, verbal 4, dbms 5, os 3, networks 3, oop 4, company_prep 8, python 17, java 12, cpp 13.
- The "triple content / 14,800+ lessons" commits padded the catalog with **1,023 template-filler lessons (92%)**, of which **1,031 sit in the DSA track** (only ±28 are real self-extended/bst/etc. content).
- Orphaned modules: `java_extra.py`, `cpp_extra.py`, `dsa.py`-dead-blocks are **never imported** — dead payload (~1.5 MB).
- `dsa.py` alone is **1.65 MB / 1,462 lines** and contains **4 redefinitions** of `EXTRA_DSA_LESSONS`; three extend into `DSA_LESSONS` (dead weight kept in memory) and only the last is live.
- **1,013 broken prerequisite links** in the final catalog (generator used offsets like `dsa-strings-0`, `dsa-linked_lists-1` — lessons that were never defined). Per-inventory CSV: 1,013 rows flagged.
- Template filler is recognisable by its fingerprints — every generated lesson is `"Learn about X in dsa with hands-on examples"`, `code: "# Example of X\n# Example code here"`, `output: "// Example output"` (Python comments declaring C++-style output!), and a quiz `"What is the primary purpose of X?"` with `correctIndex: 3` (`"All of the above"`) — 1,150 occurrences of that exact quiz. Several steps' quizzes have **identical` options/titles across different topics** because only the topic placeholder changes.

## 3. Lesson contract & grading-truth table (what the renderer + backend actually do)

Step types found in data: `explain`, `quiz`, `exercise` only (the brief's recommended set — predict-the-output, reorder, fill-in, debug, SQL lab — is not implemented in this system).

| Step type | Render | Client-side validation | Server grading | XP/mastery contribution |
|---|---|---|---|---|
| `explain` | content+code+output; user clicks Run (`/compiler/execute`, always Python) | none | **No grading at all** — complete_step records it | Counts toward "lesson complete" despite no checks |
| `quiz` | options; `correctIndex` is **sent to the browser in the GET payload** | `selectedOption === correctIndex` in LessonPlayer; server only asked to mark step complete | Nothing (answers exposed; verdicts never verified) | XP if correct per client claim; progress persisted on client assertion |
| `exercise` | editor + Run; Click submit → `/lessons/step` | runs Piston via `/api/compiler/execute` (Python hardcoded, unverified claim in brief about the Worker sandbox) | `score_question(question_type="code")` → **exact string equality** vs the reference `solution` | Any formatted-differently correct code is marked wrong; wrong answers are *not* blocked from completion — `complete_step` records completion with `is_correct` but never requires correctness |

Trust-model violations against the brief, quantified:

- **Every answer key lives client-side for quizzes** (brief §8 forbids it): 1,082 quiz steps.
- **Every exercise's "solution" is the grading key as a string** (1,109 exercise steps) — even a correct implementation that uses other names/spacing is failed; conversely a cheat could paste the reference. The `tests` field (`check: implements_bst_search`, or generated filler's `check: student_attempted`) is **never executed** anywhere — dead field.
- `complete_step` doesn't distinguish correctness: lesson is "complete" if a user clicked through every step of an `explain` lesson (mastery-from-nothing).
- Skill-score updates always record `score=1.0, is_correct=True` in `category="dsa"` regardless of the real track (`lesson["track"]` may be `python`, aptitude, …); weak-skill evidence is therefore fabricated across the board. `decide_next_action` is called with hardcoded `mastery=0.5, weakness_tier="weak"` instead of the real skill graph it just fetched.
- Exercise completion also never requires a *passed* assessment: wrong exercise answers are persisted as "completed".
- `next_lesson` iterates over the `_LESSONS.values()` in dict-insertion order (module order) — not the skill graph and not the plan; master brief's "next action must depend on progress, not static links" isn't observable here either way — there is no plan next for this branch (a plan engine exists on `origin/main` only, per `academy_plan.py`).

## 4. XP/progress economics

- `xpReward` is hardcoded per lesson (50 beginner, 90 advanced filler); everything goes through a single `lesson_progress` collection keyed `lesson_id:step_id`. Quiz XP awarded on the client's say-so; exercise XP on exact-match.
- Boss battles / spaced revision / company applications / remediation links: **none implemented on this branch's lesson system.**

## 5. Tests & validation observed

| Command (per AGENTS.md / brief) | Result |
|---|---|
| `pytest --collect-only -q` (`backend`) | ❌ collection error (broken lesson import — see §1) |
| `python -c "import app.main"` | ❌ refuses to start |
| `python -m compileall app/ -q` | not yet rerun this session; staging cleanup first |
| `npm run typecheck` (frontend) | ❌ 47 errors; `GamificationDashboard.tsx` & `LessonView.tsx` mangled **in committed HEAD**, `SkillMap.tsx` uncommitted draft truncated |
| `npm run build` | expected to fail (typecheck gate) |
| Learning-specific suites the brief names (`test_lesson_content_quality.py`, `test_academy_plan.py`, `test_company_lesson_placement_loop.py`) | **Not present on this branch** — they belong to the divergent Academy system |

## 6. What is actually good (preserve, don't rewrite)

- `lesson_service.py`'s record shape (`lesson_progress` keyed `lesson:step`) reuses `skill_assessment`, `path_generator`, `scoring`, `gamification` — the layering is sane; the wiring/bars are what to fix, not the architecture.
- Hand-written lessons exist: the ~24 original DSA lessons (arrays intro, BST search, etc. with real C++ code), `python_content.py` (17 curated lessons incl. 3 projects + quizzes with explanations), and the small aptitude/logical/verbal/SQL tracks are real content.
- Code-lab runs go through the existing Piston `/api/compiler/execute` route; contract already exists, just misused (language hardcoded to Python, no source-vs-execution verification).
- Frontend has a working `LessonPlayer` shell covering all three step types; no renderer additions are needed for the current contract — content-grade/interactivity bar needs them.

## 7. Findings ranked (P0 → P3)

**P0 — correctness / broken product**

1. Backend won't start: deleted `__init__.py` + deleted `python.py`; must be re-created importing `python_content` (a correct copy already exists, ironically, at stray `app/services/lessons/__init__.py`) and `*_extra` modules excluded or imported deliberately.
2. 60 silent overwrite collisions defeat catalog determinism.
3. 1,013 broken prerequisite links make the catalog's progression chains dead-on-arrival.
4. 1,023 template-filler lessons (92%) masquerading as "content" — should **not** be prolonged live; they award XP for repeated, always-"All of the above"-quiz answers and are a school-grade indefensible product surface. Delete or replace wholesale with a real sourcing pipeline.
5. Client-side quiz grading with answer keys in the payload (1,082 steps).
6. Exercise grading is exact-string match vs a reference solution (defeats correct-but-different code; simultaneously dead `tests` field means no real validation).
7. `explain`-only lessons are completable, granting "mastery" for reading.
8. Frontend `GamificationDashboard.tsx` + `LessonView.tsx` are JSX-mangled in committed HEAD (found in the typecheck pass, not solely the uncommitted skill-map draft); `SkillMap.tsx` is a truncated uncommitted draft.

**P1 — learning quality**

9. No remediation links, no assessment gating (score threshold), no spaced-revision hook into lesson completion, next-lesson isn't plan-driven.
10. Skill-graph update is hardcoded (`category="dsa"`, `score=1.0` regardless of performance or track) — all personalization evidence downstream (D-SA fingerprint, weak skills, adaptive plans) is polluted.
11. Non-DSA non-programming tracks have ≤17 lessons combined pieces (aptitude 7, logical 5, verbal 4, DBMS 5, OS 3, networks 3, OOP 4) against the brief's P1 plan of full curricula.
12. No content-quality schema/tests for this system (the brief's `test_lesson_content_quality.py` covers the other architecture).

**P2 — hygiene/architecture**

13. Repo root `app/` directory; ~15 scratch scripts; `python.py` deleted vs `python_content.py` ambiguous precedence; dead 1.5 MB `dsa.py` blocks; `_extra` modules unreachable.
14. Branch's lesson system diverges from the Academy architecture the brief treats as canonical — one source of truth must be chosen before content investment scales up.

## 8. Recommended Phase-A fix order (already-sized, minimal diffs)

1. Restore `backend/app/services/lessons/__init__.py` importing `python_content` instead of the deleted `python`, and delete/mothball its dead blocks in one content-hygiene commit (no content change to the 89 real lessons across python/java/cpp/aptitude/logical/verbal/dbms/os/networks/oop/company_prep).
2. Decide the filler question explicitly (keep fixtures/quality-flagged subset vs purge): delete the 1,012 template `EXTRA_DSA_LESSONS` items and the ~1031 filler rows from `dsa.py` (leaves the ±28 real lessons), or tag every filler as `needs_review` in the inventory rather than live. The default recommendation is **purge** — the whole generator produced content under a deliberate fill-the-catalog goal.
3. Server-side grading for quiz/exercise: add an `assessment_id`+`correct_index` server-only key (never send `correctIndex` in GET) and switch exercise grading to a bounded, deterministic runner (run both reference and user code against declared test cases, or at minimum keep exact-match while declaring that in UI), then gate XP/mastery and completion on a passed final assessment with a threshold.
4. Fix the 3 structurally broken frontend pages (2 committed + 1 uncommitted draft), then rebuild.
5. Then, and only then, resume content work against the contract in the brief.

## 9. Next single highest-value task

**Restore `backend/app/services/lessons/__init__.py` (importing `python_content`) and decide/purge the 1,012 items of template `EXTRA_DSA_LESSONS` filler in `dsa.py` in a single hygiene commit.** This unblocks `app.main`, the entire backend test suite, and ends the practice-award-for-nothing surface in one smallest-useful slice — every other item in the brief depends on the backend being importable and the catalog being honest.
