# Deployment

## What it is

Docker Compose orchestration for local development, with multi-stage Dockerfiles for production builds.

## How it works

**Development** (`docker-compose.yml`):
- `db`: Postgres 18 with healthcheck (`pg_isready`). Data persisted in `postgres_data` volume.
- `backend`: Builds `development` target. Runs `migrate` then `runserver`. Source mounted for hot reload. Healthcheck hits `/api/health`. Depends on `db` being healthy.
- `frontend`: Builds `development` target. Vite dev server on port 5173. Source mounted. Depends on `backend` being healthy.

**Backend Dockerfile** (multi-stage):
- `base`: Python 3.13-slim + uv 0.11.7. Installs deps from `pyproject.toml` + `uv.lock`.
- `development`: Full deps, runs `manage.py runserver`.
- `production`: No dev deps, runs `collectstatic`, creates non-root `appuser`, starts gunicorn.

**Frontend Dockerfile** (multi-stage):
- `development`: Node-based, Vite dev server.
- `production`: Build step, then nginx serving static files with SPA fallback.

## Key constraints

- `MODE` detection in `chron_track/utils.py` checks `sys.argv` and `sys.modules` to switch between testing (SQLite), development (Postgres via runserver), and production (Postgres via gunicorn).
- Backend `.env` is required (contains `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`). Docker Compose also sets DB credentials via environment.
- CORS allows only `http://localhost:5173` — must be updated for production.
