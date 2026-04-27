# Project 1 — Dockerized 3-Tier Web Stack with CI

[![CI](https://github.com/AlexCraescu/dockerized-web-stack/actions/workflows/ci.yml/badge.svg)](https://github.com/AlexCraescu/dockerized-web-stack/actions/workflows/ci.yml)

A reproducible local web stack — **Nginx → Flask API → Postgres** — orchestrated with Docker Compose, tested in GitHub Actions, and runnable on any machine that has Docker.

> No AWS, no paid cloud, no public deployment. Everything runs on `localhost`.

---

## GCAO

### Goal
Show that I can take a small web application from source code to a reproducible, container-orchestrated local stack with a working CI pipeline that runs on every push.

### Context
A junior DevOps engineer is expected to dockerize apps, write `docker-compose.yml` files for multi-service stacks (web/API/DB), and wire up basic CI. The stack must run on any laptop with Docker installed — no cloud account needed. The project also has to demonstrate fundamentals: multi-stage Dockerfiles, healthchecks, named volumes for data persistence, and a non-root container user.

### Action
- A small Flask API with two endpoints: `GET /health` and `GET /items` (reads from Postgres).
- Multi-stage `Dockerfile` producing a small, non-root runtime image.
- `docker-compose.yml`: `nginx` reverse proxy → `api` (Flask + gunicorn) → `db` (Postgres) with healthchecks and a named volume.
- `pytest` unit tests with a stubbed DB; `ruff` for linting.
- GitHub Actions: lint → test → `docker compose build` on every push.
- `Makefile` for one-command UX.

### Outcome
A reproducible local stack that boots with `make up`, has a green CI badge, and can be cloned and run by anyone with Docker installed in under two minutes.

---

## Architecture

```
                 ┌───────────────────────────────────────────┐
                 │                Docker host                │
                 │                                           │
   localhost ───►│  nginx :8080  ──►  api :5000  ──►  db :5432
                 │   (reverse           (Flask +         (Postgres
                 │    proxy)            gunicorn)        + volume)
                 │                                           │
                 └───────────────────────────────────────────┘
```

All inter-service traffic stays on a private Docker network. Only Nginx is exposed to the host on port `8080`.

---

## Quick start

Prerequisites: Docker Desktop (or Docker Engine + Compose v2) and `make`.

```bash
git clone https://github.com/AlexCraescu/dockerized-web-stack.git
cd dockerized-web-stack
cp .env.example .env
make up
curl http://localhost:8080/health      # {"status":"ok"}
curl http://localhost:8080/items       # [{"id":1,"name":"hello"}, ...]
make logs                              # follow service logs
make down                              # tear down
```

## Common tasks

| Command       | What it does                                |
|---------------|---------------------------------------------|
| `make up`     | Build and start all services in the background |
| `make down`   | Stop and remove all services and the network  |
| `make logs`   | Follow logs from all services                 |
| `make ps`     | Show running services                         |
| `make test`   | Run pytest inside the api container           |
| `make lint`   | Run ruff lint                                 |
| `make clean`  | `make down` + remove the named DB volume      |

## CI

Every push to `main` triggers `.github/workflows/ci.yml`, which runs:

1. **lint** — `ruff check`
2. **test** — `pytest`
3. **build** — `docker compose build`

If you want CI to also run integration tests against a live stack, uncomment the `integration` job in `ci.yml`.

---

## Repository layout

```
.
├── README.md
├── Makefile
├── docker-compose.yml
├── .env.example
├── .gitignore
├── .dockerignore
├── pyproject.toml
├── api/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app.py
│   ├── db.py
│   └── tests/
│       ├── __init__.py
│       └── test_app.py
├── nginx/
│   ├── Dockerfile
│   └── nginx.conf
├── db/
│   └── init.sql
└── .github/workflows/ci.yml
```

---

## Publishing this project

```bash
gh auth login                                     # one-time, browser-based
gh repo create AlexCraescu/dockerized-web-stack --public --source=. --push
```

GoDaddy / `bliat.club` is **not** used here — the project intentionally has no public deployment.
