.PHONY: up down restart build migrate seed logs shell test clean

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose restart

build:
	docker compose build

migrate:
	docker compose exec backend alembic upgrade head

seed:
	docker compose exec backend python scripts/seed_data.py

logs:
	docker compose logs -f

shell:
	docker compose exec backend bash

test:
	docker compose exec backend pytest -q

clean:
	docker compose down -v --remove-orphans
