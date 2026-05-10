# Django Ninja as API framework

**Date:** 2026-04-19
**Status:** active

## Context

The project needs a REST API for a React SPA. Django alone provides templates and basic views, but not a modern, typed API layer with auto-generated docs.

## Options considered

1. **Django REST Framework (DRF)** — mature, large ecosystem, serializer-based. Verbose configuration.
2. **Django Ninja** — Pydantic-based schemas, function views, automatic OpenAPI docs at `/docs`. Lighter, more Pythonic.

## Choice

Django Ninja with `django-ninja-jwt` for authentication. Routers per domain (`accounts/api.py`, `races/api.py`) mounted on a single `NinjaAPI` instance in `urls.py`.

## Consequences

- Schemas are Pydantic models (`Schema`, `ModelSchema`, `FilterSchema`), not DRF serializers. Validation happens via type hints.
- OpenAPI docs auto-generated at `/docs`.
- `ninja_jwt` provides token obtain/refresh/verify routers that plug directly into the Ninja API.
- Less community resources compared to DRF, but simpler codebase.
