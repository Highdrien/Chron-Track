FROM python:3.13-slim-bookworm AS base

# Install uv (version fixed for reproducibility)
COPY --from=ghcr.io/astral-sh/uv:0.11.7 /uv /usr/local/bin/uv

# Set uv config and python config
ENV UV_PROJECT_ENVIRONMENT=/usr/local \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /backend-chron-track

# Copy project files
COPY pyproject.toml uv.lock ./

## ------------------------------- Development Stage -------------------------- ##
FROM base AS development

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

COPY src/ ./src

CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]

## ------------------------------- Production Stage --------------------------- ##
FROM base AS production

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev

COPY src/ ./src
COPY gunicorn.conf.py .

RUN python src/manage.py collectstatic --noinput

RUN useradd --create-home --shell /bin/bash appuser \
 && chown -R appuser:appuser /backend-chron-track
USER appuser

RUN gunicorn --config gunicorn.conf.py --chdir src --bind 0.0.0.0:8000

