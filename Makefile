.PHONY: help dev db-up db-down test lint backend frontend

help:
	@echo "AgentArena Developer Commands:"
	@echo "  make db-up       - Start isolated PostgreSQL (5433) and Redis (6380) containers"
	@echo "  make db-down     - Stop containers"
	@echo "  make dev         - Run both backend and frontend concurrently"
	@echo "  make backend     - Run FastAPI backend on port 8000"
	@echo "  make frontend    - Run Next.js frontend on port 3000"
	@echo "  make test        - Run test suite"
	@echo "  make lint        - Run ruff and type checks"

db-up:
	docker compose up -d

db-down:
	docker compose down

backend:
	cd apps/backend && uvicorn app.main:app --reload --port 8000

frontend:
	cd apps/frontend && npm run dev

test:
	cd apps/backend && pytest -v

lint:
	cd apps/backend && ruff check .
