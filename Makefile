.PHONY: up down logs ps test lint build clean

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f

ps:
	docker compose ps

build:
	docker compose build

test:
	docker compose run --rm --no-deps -e DATABASE_URL=sqlite:///:memory: api pytest -q

lint:
	docker compose run --rm --no-deps api ruff check .

clean:
	docker compose down -v
