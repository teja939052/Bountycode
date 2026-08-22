.PHONY: help dev backend frontend test lint typecheck clean docker-up docker-down

help:
	@echo "PlacementPro Development Commands"
	@echo "  make dev          - Start both backend and frontend"
	@echo "  make backend      - Start backend dev server"
	@echo "  make frontend     - Start frontend dev server"
	@echo "  make test         - Run backend tests"
	@echo "  make lint         - Run linters (black, flake8, isort)"
	@echo "  make typecheck    - Run TypeScript type checking"
	@echo "  make check        - Run lint + typecheck"
	@echo "  make clean        - Remove build artifacts"
	@echo "  make docker-up    - Start services with Docker Compose"
	@echo "  make docker-down  - Stop Docker Compose services"

dev:
	@echo "Starting PlacementPro development environment..."
	@docker-compose up mongodb redis -d
	@$(MAKE) backend &
	@$(MAKE) frontend

backend:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

frontend:
	cd frontend && npm run dev

test:
	cd backend && pytest tests/ -v

lint:
	@echo "Running Python linters..."
	cd backend && black . && isort . && flake8 app/ tests/ --max-line-length=127 --extend-ignore=E203,W503
	@echo "Running pre-commit..."
	pre-commit run --all-files || true

typecheck:
	cd frontend && npm run check:ts

check: lint typecheck

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name node_modules -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name dist -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name build -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	find . -name ".coverage" -delete 2>/dev/null || true

docker-up:
	docker-compose up --build

docker-down:
	docker-compose down
