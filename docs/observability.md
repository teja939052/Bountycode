# BountyCode Observability (Phase 8A)

Production-grade structured logging, error monitoring, request correlation,
and developer notifications for the BountyCode backend and frontend.

Free-tier friendly — no paid infrastructure required. Sentry is optional and
env-gated; the application runs normally without it.

---

## Architecture

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│   Frontend      │      │    Backend      │      │    Sentry         │
│  (React + Vite) │      │  (FastAPI +     │      │  (optional)       │
│                 │      │   SQLAlchemy)   │      │                     │
│  ErrorBoundary  │──────│ Logging Middleware│────▶│ Error dashboard   │
│  @sentry/react  │─────▶│ structured_logging│────▶│ Stack traces      │
│                 │      │ Request ID MW     │────▶│ Email alerts      │
└─────────────────┘      └─────────────────┘      └─────────────────┘
                                                    ▲
                                                    │
                                              Local logs
                                              backend/logs/
```

---

## What is instrumented

| Module | Events logged |
|--------|--------------|
| Authentication | Registration, login, token refresh, password reset |
| Database | Connection open/close, pool checkout/checkin, slow queries, transaction begin/commit/rollback, errors |
| Learning | Attempt recorded, mastery updated, review scheduled |
| Gamification | XP awarded, duplicate reward rejected |
| Assessments | Submission received, evaluation failed |
| AI Gateway | Provider, model, latency, retry count, fallback selection, circuit breaker |
| Background jobs | Job started, completed, failed |

---

## What is NEVER logged

- Passwords, password hashes, access tokens, refresh tokens, JWTs
- OAuth credentials, authorization headers, cookies, API keys
- Database passwords, connection strings, reset tokens, verification tokens
- Full resumes, uploaded file contents, student source code
- Hidden test cases, assessment answer keys, private interview transcripts
- AI prompts and completions
- Raw request/response bodies

---

## Getting started

### 1. Start the backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
cp .env.example .env           # Fill in values
uvicorn app.main:app --reload  # Hot reload on port 8000
```

Logs appear in the VS Code integrated terminal and in `backend/logs/BountyCode.log`.

### 2. Local logs

- Directory: `backend/logs/`
- File: `BountyCode.log` (rotating, 10 MB max, 5 backups)
- Format: JSON (machine-searchable) in production, human-readable in development
- Git-ignored: `*.log` and `BountyCode.log` are in `.gitignore`

### 3. Changing log level

Set `LOG_LEVEL` in `.env`:
```
LOG_LEVEL=DEBUG   # verbose
LOG_LEVEL=INFO    # normal (default)
LOG_LEVEL=WARNING # errors only
```

### 4. Finding an error by request ID

Every HTTP response includes `X-Request-ID`. Search logs for that ID:

```bash
# In backend/logs/BountyCode.log, grep for the request ID
grep "bc-7a91..." backend/logs/BountyCode.log
```

Or in the VS Code terminal, search for the request ID string.

### 5. Sentry setup (optional)

1. Create a free account at https://sentry.io/signup
2. Create a **backend** project (Python/FastAPI) — copy the DSN
3. Create a **frontend** project (React/Vite) — copy the DSN
4. Add DSNs to `.env`:
   ```
   SENTRY_BACKEND_DSN=https://xxx@sentry.io/yyy
   SENTRY_FRONTEND_DSN=https://xxx@sentry.io/yyy
   SENTRY_ENABLED=true
   SENTRY_ENVIRONMENT=development
   ```
5. Configure email issue alerts in Sentry (Project Settings → Alerts)

### 6. Frontend error experience

When a React component crashes:
- The ErrorBoundary shows a polished fallback with an error reference ID
- Students can copy the error ID and refresh the page
- Internal stack traces are never shown to students
- Errors are captured in Sentry (if configured)

---

## Configuration reference

| Variable | Default | Description |
|----------|---------|-------------|
| `LOG_LEVEL` | `INFO` | Python log level (DEBUG, INFO, WARNING, ERROR) |
| `LOG_FILE` | `BountyCode.log` | Log filename under `backend/logs/` |
| `LOG_ROTATION_MAX_BYTES` | `10485760` | Max log file size before rotation (10 MB) |
| `LOG_ROTATION_BACKUP_COUNT` | `5` | Number of rotated log files to keep |
| `SENTRY_BACKEND_DSN` | `""` | Sentry DSN for backend (empty = disabled) |
| `SENTRY_FRONTEND_DSN` | `""` | Sentry DSN for frontend (empty = disabled) |
| `SENTRY_ENVIRONMENT` | `development` | Environment name for Sentry grouping |
| `SENTRY_TRACES_SAMPLE_RATE` | `0.1` | Percentage of transactions traced (0.0-1.0) |
| `SENTRY_ENABLED` | `false` | Master switch for Sentry |

---

## Developer workflow

1. **See an error in production** → Sentry email notification with error ID
2. **Search logs by request ID** → `grep <request_id> backend/logs/BountyCode.log`
3. **Reproduce locally** → Run with `LOG_LEVEL=DEBUG`, watch terminal + log file
4. **Check Sentry dashboard** → Stack trace, breadcrumbs, environment, release
5. **Fix and deploy** → No database schema changes required

---

## File layout

```
backend/
├── app/
│   ├── services/
│   │   ├── structured_logging.py   # JSON formatter, redaction, Sentry init
│   │   └── ai_core.py              # AI Gateway observability logging
│   ├── observability/
│   │   ├── __init__.py
│   │   └── db_instrumentation.py   # SQLAlchemy slow query/transaction logging
│   ├── middleware/
│   │   └── logging.py              # Request/response timing middleware
│   └── main.py                     # Sentry init, exception handlers
├── logs/
│   └── BountyCode.log              # Rotating log file (Git-ignored)
├── tests/
│   └── test_observability.py       # Observability tests
└── .env.example                    # Sentry + log config placeholders

frontend/
├── src/
│   ├── observability/
│   │   └── sentry.ts               # Frontend Sentry init
│   ├── components/
│   │   └── ErrorBoundary.tsx       # Polished error fallback with error ID
│   ├── services/
│   │   └── errorTracker.ts         # Window error/unhandledrejection tracking
│   └── main.tsx                    # Sentry initialization
└── package.json                    # @sentry/react dependency
```

---

## Restrictions

- No database schema changes for logging
- No logs table in Supabase or MongoDB
- No paid service required
- No external monitoring required for local development
- No `.env` files or DSNs committed to Git
- No credentials or private student data in logs
- Sentry failures never crash the application
- Golden Hour frontend redesign is kept separate
