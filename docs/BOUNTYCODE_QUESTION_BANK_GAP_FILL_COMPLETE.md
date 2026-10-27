# BOUNTYCODE_QUESTION_BANK_GAP_FILL_COMPLETE.md

**Version:** 1.1 (Curation Complete — checklist corrected against live code)
**Effective Date:** 2026-09-23
**Governed By:** `docs/BOUNTYCODE_VISION_LOCK.md`, `docs/PRD_SERVICE_BASED_V1.md`, `AGENTS.md` (Content Trust + No-LLM Bank rules)

---

## 0. What Was Added (verified against repo)

**Backend (1 file):**
- `backend/app/data/verified_question_bank.json` — **43 curation candidates** with `source_bank: "exam_pattern_2026_gap_fill"`

**Metadata (all 43 entries):**
- `trust_status: "automated_checked"` (not human-reviewed yet)
- `provenance: "2025-2026 exam pattern gap-fill candidate — awaiting human review"` (UTF-8 em dash; auditable)

**Coverage (verified counts by id prefix):**

| Segment | IDs | Count | Types |
|---------|-----|-------|-------|
| TCS NQT 2026 | `tcs26-pseudo-001`…`015`, `tcs26-adv-reason-001`…`005` | 20 | aptitude / cs_fundamentals |
| Infosys InfyTQ 2026 | `infy26-puzzle-001`…`005` | 5 | aptitude |
| Cognizant GenC Next 2026 | `cogn26-prog-001`…`010` | 10 | cs_fundamentals |
| Accenture 2026 | `accenture26-ai-001`…`005` | 5 | cs_fundamentals |
| Coding gaps | `exam26-code-001`…`003` | 3 | coding |
| **Total** | | **43** | aptitude 25, cs_fundamentals 15, coding 3 |

**Quarantine (verified live):**
- All 43 load into `question_store` (`source_bank` present, `_is_executable` = 43/43)
- **0/43 servable** — `_is_servable()` requires `trust_status in ("verified", "reviewed")`
- Bank snapshot: `total_stored=22823`, `total_servable=9106` (`verified` 8532 + `reviewed` 574)

**Tests:** `pytest tests/test_os_features.py tests/test_rank_badge.py` → **13 passed** (2026-09-23).

---

## 1. Trust statuses — CORRECTED (do not use `human_verified`)

The repo has **no** `human_verified` status. Writing it would leave questions **unservable**.

```
unverified → automated_checked → reviewed → verified
                 (quarantined)    (servable)  (servable, full promotion)
```

| Status | Servable? | Meaning |
|--------|-----------|---------|
| `automated_checked` | **No** | Passed deterministic auto checks; awaiting human review |
| `reviewed` | **Yes** | Human sign-off (`reviewed_by` + `reviewed_at`) |
| `verified` | **Yes** | Independent verification + promotion path |
| `quarantined` / `unverified` / `needs_review` | **No** | Blocked |

Gate: `question_store._is_servable()` → `status not in ("verified", "reviewed") → False`.

Canonical human stamp for JSON-bank candidates: set `trust_status: "reviewed"` with reviewer identity (same stamp as `POST /api/v1/admin/content/tranches/{id}/approve`).

---

## 2. Human Review Checklist (promote `automated_checked` → `reviewed`)

### Step 1 — List candidates for review

```bash
cd backend
venv\Scripts\python.exe scripts/review_gap_fill_candidates.py --list
```

Expected: **43 awaiting review**, 0 already reviewed, 0 servable.

### Step 2 — Review each question (quality gate)

For each id, verify:
- [ ] Question text clear (no typos, no ambiguity)
- [ ] Options plausible; correct answer independently checked
- [ ] Explanation accurate (step-by-step, no errors)
- [ ] Difficulty tag matches actual difficulty
- [ ] Tags/topic accurate
- [ ] Coding: visible + hidden test cases cover edge cases
- [ ] Provenance still `2025-2026 exam pattern gap-fill candidate — awaiting human review`
- [ ] No fabricated company claims (pattern-relevant only unless provenance proves otherwise)

### Step 3 — Promote a reviewed batch (human identity required)

```bash
cd backend
venv\Scripts\python.exe scripts/review_gap_fill_candidates.py ^
  --promote tcs26-pseudo-001,tcs26-pseudo-002,infy26-puzzle-001 ^
  --reviewer "Your Name <you@example.com>"
```

Rules enforced by the script:
- Only ids already in the gap-fill set
- Only current status `automated_checked` → `reviewed` (never skips to a fake status)
- Writes `reviewed_by`, `reviewed_at` (UTC ISO), `review_method: "human_review_gap_fill_v1"`
- Requires non-empty `--reviewer` (not `pipeline` / `system` / `auto`)
- Refuses dry-run-less bulk promote of all 43 without explicit ids or `--all` + `--i-reviewed-every-question`

**Restart backend after promote** (`question_store.load_all()` is once-per-process).

### Step 4 — Verify servability

```bash
cd backend
venv\Scripts\python.exe scripts/review_gap_fill_candidates.py --list
```

Expected after promoting N ids:
- `servable_gap_fill: N` (was 0)
- `total_servable: 9106 + N`

Do **not** assert absolute totals like `12,809` — those numbers are not this bank.

---

## 3. Why this process wins

| Quantity path | Trust path (this work) |
|---------------|------------------------|
| Dump thousands → serve all → trust erodes | 43 candidates → quarantine → human review → `reviewed` → serve |
| No provenance | `source_bank` + `provenance` on every row |
| LLM self-promotion forbidden | Machine may set `automated_checked` only; human sets `reviewed` |
| Big-bang release | Promote in reviewed batches; each batch restart-verifiable |

Compliance:
- **Content Trust:** `UNVERIFIED → AUTOMATED_CHECKED → HUMAN_REVIEWED → TRUSTED` (statuses map: `unverified` / `automated_checked` / `reviewed` / `verified`)
- **No-LLM Bank Rule:** no LLM authoring/tagging/promotion of these rows
- **Residency:** content stays in `backend/app/data/`, never Mongo

---

## 4. Next steps

### Phase 1 — Human review of the 43 (now)
- [ ] Review TCS NQT 2026 (15 pseudo + 5 advanced reasoning)
- [ ] Review Infosys InfyTQ 2026 (5 puzzles)
- [ ] Review Cognizant GenC Next 2026 (10 programming MCQs)
- [ ] Review Accenture 2026 (5 AI Foundations)
- [ ] Review coding gaps (3 OA patterns)
- [ ] Promote via `review_gap_fill_candidates.py --promote … --reviewer …`
- [ ] Restart backend; confirm `servable_gap_fill` matches promoted count

### Phase 2 — More gap-fill candidates (only after Phase 1 lands)
- [ ] Identify real coverage gaps (do not bulk-generate)
- [ ] Append new candidates with same provenance schema, `automated_checked`
- [ ] Same human review loop — never skip to `reviewed`

### Phase 3 — Quality metrics (after serve)
- [ ] Track first-try acceptance rate per id
- [ ] Track upvotes/downvotes
- [ ] Hide / quarantine on poor community signal (existing `served_quarantine` path)

---

## 5. Bottom line

- **43 candidates** present, executable, **0 servable** — quarantine works.
- **Provenance explicit** on every row.
- **Human review is mandatory** before any student sees them.
- **Correct promote target is `reviewed`**, not `human_verified` (that status does not exist and would not unlock serving).
- Tooling: `backend/scripts/review_gap_fill_candidates.py` enforces the real gate.

**Blocked on:** a human reviewer identity + batch sign-off. Machine must not self-promote.
