# Mock OA frontend integration — implementation contract

## Current verified repository shape

- The authenticated frontend route `/mock-oa` renders `frontend/src/pages/MockOA.tsx`.
- The page currently starts an aptitude test through legacy flattened `startAptitudeTest` helpers, submits by question index, and calls `completeAptitudeTest`.
- `frontend/src/services/api/companyPrep.ts` exposes `companyMocksApi.getCompanies`, `getConfig`, `start`, `getStatus`, and `getResults`; it has no answer or completion method.
- `backend/app/routes/company_mocks.py` exposes only:
  - `GET /api/v1/company-mocks/companies`
  - `GET /api/v1/company-mocks/{company_id}/config`
  - `POST /api/v1/company-mocks/{company_id}/start`
  - `GET /api/v1/company-mocks/{session_id}/status`
  - `GET /api/v1/company-mocks/{session_id}/results`
- The start route currently populates `all_questions` only for rounds whose `type` is `coding`. Configurations advertise aptitude, logical, verbal, CS fundamentals, system design, and behavioral rounds as well, but these are not currently materialized as questions by this route.
- No answer-submission or completion endpoint exists in `company_mocks.py`.

## Required product contract

Do not route company-mock submissions through the standalone aptitude API. A company mock must have its own session-owned answer lifecycle.

1. Start returns session id, safe question payloads, rounds, deadlines and a sanitized session summary. Correct answers and hidden tests must remain server-side.
2. Answer submission accepts a stable question id and an answer payload. It authenticates user ownership, confirms session is in progress, confirms question belongs to session and has not already been submitted, then grades using the server-side question bank or relevant trusted evaluator.
3. For coding questions, accept source code/language and use the existing trusted coding submission service; do not trust a client score or passed count.
4. For MCQ questions, grade with the server-side answer key, never a client-supplied correct answer.
5. Completion is idempotent, freezes further submissions, computes results from persisted graded answers, and records evidence through the existing canonical learning-event pathway where supported.
6. Status and results must enforce ownership and validate malformed IDs consistently.
7. Frontend uses `companyMocksApi` exclusively for this flow, persists recoverable session id locally if product policy allows, and supports resume/status/results.

## Scope and release gates

- First ship a truthful coding-only mock if only coding question materialization is available. Do not show unserved rounds as active questions.
- Add other section types only when their authored question sources and server-side grading paths exist.
- Add backend API tests for owner isolation, invalid/unknown questions, duplicate submissions, idempotent completion, score calculation, and timeout behaviour.
- Add frontend tests for start, navigation, retry/error, submission state, resume and results.
- Verify company mocks with a seeded test bank and two users before release.
- Do not claim CI, local browser QA or end-to-end tests passed unless actually run.

## Current finding

The current page and backend are not connected end to end. This document records the inspected contract so implementation can proceed without conflating standalone aptitude sessions with company mock sessions.
