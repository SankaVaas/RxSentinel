.PHONY: up down logs migrate test eval lint fmt

up:
	docker compose up --build

down:
	docker compose down -v

logs:
	docker compose logs -f backend

migrate:
	docker compose exec backend alembic upgrade head

test:
	docker compose exec backend pytest -v

eval:
	docker compose exec backend python /app/../eval/run_eval.py

lint:
	docker compose exec backend ruff check src tests

fmt:
	docker compose exec backend ruff format src tests
