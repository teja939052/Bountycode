# Contributing to PlacementPro

Thank you for your interest in contributing! This document provides guidelines and best practices for contributing to the PlacementPro codebase.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Development Setup](#development-setup)
- [Code Conventions](#code-conventions)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Feature Flags](#feature-flags)

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Respect differing viewpoints and experiences

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/placementpro.git`
3. Create a feature branch: `git checkout -b feature/my-new-feature`
4. Make your changes
5. Run tests: `pytest backend/tests/`
6. Run linting: `pre-commit run --all-files`
7. Commit and push: `git push origin feature/my-new-feature`
8. Open a Pull Request

## Project Structure

```
placementpro/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI app, routers, middleware
│   │   ├── config.py         # Pydantic settings (env vars)
│   │   ├── database.py       # Motor client, collections, indexes
│   │   ├── models/           # Pydantic request/response models
│   │   ├── routes/           # One route file per feature domain
│   │   ├── services/         # Business logic, AI, execution engines
│   │   ├── middleware/       # Auth, rate limiting, logging
│   │   └── utils/            # Shared utilities
│   ├── tests/                # Backend tests (pytest + async)
│   ├── requirements.txt      # Production dependencies
│   └── requirements-dev.txt  # Dev/test dependencies
├── frontend/
│   ├── src/
│   │   ├── App.tsx           # Router, global state providers
│   │   ├── pages/            # One page per route (lazy-loaded)
│   │   ├── components/       # Reusable UI components
│   │   ├── services/api/     # Typed API client modules
│   │   ├── store/            # Zustand global state
│   │   ├── utils/            # Frontend utilities
│   │   └── hooks/            # Custom React hooks
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
├── docker-compose.yml        # MongoDB, Redis, backend, frontend
├── .pre-commit-config.yaml   # Linting, formatting hooks
└── AGENTS.md                 # Project overview and conventions
```

## Development Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- MongoDB 7+ (or Docker)
- Redis 7+ (optional, falls back to in-memory)

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env   # Fill in values
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Docker (Recommended)

```bash
docker-compose up --build
```

## Code Conventions

### Backend (Python)

- **Async everywhere**: All routes must use `async def` with `await` for I/O
- **Type hints**: Required for all function signatures
- **Docstrings**: Required for all public functions/classes
- **Error handling**: Raise `HTTPException(status_code=..., detail=...)` for API errors
- **Auth**: Use `Depends(get_current_user)` for protected routes
- **Database**: Use `motor` async driver, never `pymongo` sync
- **AI calls**: Use `chat_completion()` from `app.services.ai`, with retry/circuit breaker
- **Config**: Use `get_settings()` from `app.config`, never hardcode secrets
- **Logging**: Use `logger` from `app.services.structured_logging`, include correlation IDs
- **Models**: Pydantic v2 models in `app/models/` for request/response validation
- **Routes**: One feature per file, prefix with `/api/v1/<feature>`
- **Services**: Business logic in `app/services/`, keep routes thin

### Frontend (TypeScript/React)

- **TypeScript strict mode**: Enabled (`tsconfig.json` has `"strict": true`)
- **Functional components**: Use hooks, no class components
- **State management**: Zustand for global state (auth, theme only)
- **API calls**: Use `services/api/index.ts` aggregated client
- **Routing**: React Router v6, wrap authenticated pages in `ProtectedRoute`
- **Code splitting**: All pages must be lazy-loaded with `React.lazy()`
- **Styling**: Tailwind CSS utility classes, no component library
- **Animations**: Framer Motion for page transitions, GSAP for complex sequences
- **Error handling**: Use `ErrorBoundary` for component errors

### Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Python files | `snake_case` | `feature_flags.py` |
| Python functions | `snake_case` | `check_and_reset_monthly_usage` |
| Python classes | `PascalCase` | `CircuitBreaker` |
| TypeScript files | `PascalCase` for components, `camelCase` for utils | `AuthLayout.tsx`, `featureFlags.ts` |
| React components | `PascalCase` | `Dashboard.tsx` |
| API routes | `kebab-case` URL, `snake_case` function | `/api/v1/company-prep` |
| MongoDB collections | `snake_case` plural | `users_collection`, `gamification_collection` |

## Testing

### Backend Tests

```bash
# Run all tests
pytest backend/tests/

# Run specific test file
pytest backend/tests/test_feature_flags.py -v

# Run with coverage
pytest backend/tests/ --cov=app --cov-report=term-missing
```

**Test requirements:**
- All new features must include tests
- Unit tests for pure logic (no DB)
- Integration tests for API endpoints (use `AsyncClient`)
- Mock external APIs (OpenRouter, Piston) in tests
- Use `pytest-asyncio` for async tests
- Test files must be named `test_*.py`

### Frontend Tests

```bash
# Smoke tests (requires backend)
npm run smoke

# Type check
npm run check:ts
```

**Test requirements:**
- All new pages/components must render without crash
- Critical user flows should have smoke tests
- TypeScript must pass strict mode (`noUnusedLocals`, `noUnusedParameters`)

## Pull Request Process

1. **One feature per PR**: Keep changes focused and reviewable
2. **Update docs**: Update `AGENTS.md` if adding new features or changing architecture
3. **Add tests**: Include tests for new functionality
4. **Run checks**: Ensure `pytest` passes and `npm run check:ts` passes
5. **Update CHANGELOG**: Add entry describing the change
6. **Request review**: Assign at least one reviewer

### PR Checklist

- [ ] Code follows conventions above
- [ ] Tests added/updated
- [ ] `pytest backend/tests/` passes
- [ ] `npm run check:ts` passes
- [ ] No secrets or API keys committed
- [ ] `AGENTS.md` updated if needed
- [ ] CHANGELOG updated

## Feature Flags

The codebase uses feature flags to manage 50+ features. This enables gradual rollouts, A/B testing, and plan-based gating.

### Backend

```python
from app.services.feature_flags import is_feature_enabled

if is_feature_enabled("dsa_visualizer", user["plan"]):
    return {"message": "Feature enabled"}
```

### Frontend

```typescript
import { features, isFeatureEnabled } from "@/utils/featureFlags";

if (isFeatureEnabled("dsaVisualizer", user.plan)) {
  // Show feature
}
```

### Adding a New Feature Flag

1. Add entry to `FEATURE_FLAGS` in `backend/app/services/feature_flags.py`
2. Add entry to `features` in `frontend/src/utils/featureFlags.ts`
3. Use `is_feature_enabled()` / `isFeatureEnabled()` in your code
4. Set `allowed_plans` if the feature is plan-gated

## Architecture Decisions

- **MongoDB**: Chosen for flexible schema with 50+ collections
- **Motor**: Async MongoDB driver for FastAPI compatibility
- **Redis**: Optional cache layer with in-memory fallback
- **OpenRouter**: AI provider with 4-model fallback chain
- **Piston API**: Code execution with Docker sandbox fallback
- **JWT + httpOnly cookies**: XSS-proof authentication
- **Circuit breaker**: Prevents cascade failures from external APIs
- **Structured logging**: JSON logs with correlation IDs for tracing

## Security

- Never commit secrets, API keys, or passwords
- Use environment variables for all configuration
- Validate all user input with Pydantic models
- Rate limit all public endpoints
- Sanitize error messages before returning to client

## Questions?

- Check `AGENTS.md` for project overview and known issues
- Check `FUTURE.md` for the product roadmap
- Open an issue for bugs or feature requests
