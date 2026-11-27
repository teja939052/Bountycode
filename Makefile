# BountyCode — platform validation Makefile
#
# Targets:
#   make test                # complete validation suite (all stages)
#   make test-backend-unit   # fast unit tests (no external services)
#   make test-backend-integration # integration tests with real DB
#   make test-e2e            # end-to-end learner lifecycle tests
#   make test-frontend       # TypeScript typecheck + build
#   make test-content        # content contract validation
#
# Stages run in CI; locally you can run any subset.

PYTHON ?= python
PYTEST ?= $(PYTHON) -m pytest
NPM ?= npm

BACKEND_DIR := backend
FRONTEND_DIR := frontend

# PostgreSQL database used by local migration tests.
export SUPABASE_DB_URL := postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/bountycode

.PHONY: test test-backend-unit test-backend-integration test-e2e test-frontend test-content test-backend clean

test: test-backend-unit test-backend-integration test-e2e test-content
	@echo "=== All backend stages passed ==="

# ── Unit stage ──────────────────────────────────────────────────────────
# Fast, deterministic tests that do not require an external database.
test-backend-unit:
	cd $(BACKEND_DIR) && $(PYTEST) tests/ -q --tb=short \
		--ignore=tests/test_e2e_learner_journey.py \
		--ignore=tests/test_e2e_core_loop.py \
		--ignore=tests/test_oa_repair_loop_evidence.py \
		--ignore=tests/test_compiler_service.py \
		--ignore=tests/test_world_complete_xp.py

# ── Integration stage ───────────────────────────────────────────────────
# Integration tests requiring a real PostgreSQL schema.
test-backend-integration:
	cd $(BACKEND_DIR) && $(PYTEST) tests/test_compiler_service.py tests/test_oa_repair_loop_evidence.py tests/test_world_complete_xp.py tests/test_postgres_academy.py tests/test_postgres_exam.py -q --tb=short

# ── E2E stage ───────────────────────────────────────────────────────────
# The definitive learner lifecycle test. Runs in its own pytest process
# against an isolated test database (production data is never touched).
test-e2e:
	cd $(BACKEND_DIR) && $(PYTEST) tests/test_e2e_core_loop.py tests/test_e2e_learner_journey.py -q --tb=short

# ── Content stage ───────────────────────────────────────────────────────
# Content contract validation: question store trust gate, servable counts.
test-content:
	cd $(BACKEND_DIR) && $(PYTEST) tests/test_quiz_session_integrity.py tests/test_quiz_time_limits.py tests/test_core.py -q --tb=short

# ── Frontend stage ──────────────────────────────────────────────────────
test-frontend:
	cd $(FRONTEND_DIR) && $(NPM) run typecheck
	cd $(FRONTEND_DIR) && $(NPM) run build

clean:
	cd $(BACKEND_DIR) && rm -rf .pytest_cache __pycache__ app/**/__pycache__ tests/__pycache__ 2>/dev/null || true
	cd $(FRONTEND_DIR) && rm -rf node_modules/.cache dist 2>/dev/null || true
