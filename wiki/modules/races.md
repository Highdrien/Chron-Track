# Races

**Path:** `backend/src/races/`

## Purpose

Core domain module. Stores race results per user with auto-computed speed and pace. Provides full CRUD API with filtering, pagination, and personal records by distance category.

## Interface

- `Race` model (`races.models`): FK to `AUTH_USER_MODEL`, fields for name, edition, date, distance, elevation_gain, time, speed (computed), pace (computed), strava_url, results_url, location, ranking fields. Ordered by `-date`.
- `GET /api/races/` — list own races, paginated (limit/offset), filterable by name, edition, location, date range, distance range.
- `POST /api/races/` — create race (speed/pace auto-computed on save).
- `GET /api/races/{id}` — retrieve own race.
- `PUT /api/races/{id}` — full update.
- `PATCH /api/races/{id}` — partial update (recalculates speed/pace).
- `DELETE /api/races/{id}` — delete own race.
- `GET /api/races/records` — personal records per distance category.

## Dependencies

- [accounts](accounts.md) (User model via `settings.AUTH_USER_MODEL`)
- `django-ninja` (Router, ModelSchema, FilterSchema, pagination)
- `races.utils` — `calculate_speed`, `calculate_pace`, `get_record`, `get_list_categories`, `DISTANCE_CATEGORIES`

## Gotchas

- `speed` and `pace` are `editable=False` — computed in `Race.save()` via `utils.calculate_speed` / `utils.calculate_pace`. Never set them directly.
- `DISTANCE_CATEGORIES` defines bucket ranges (e.g. "5K" = 4.5–5.5 km). Records use the fastest time within each bucket, not exact distance matching.
- `get_record` does a lazy import of `Race` to avoid circular imports with `utils.py`.
