# Activity

**Path:** `backend/src/activity/`

## Purpose

Stores and manages running activities imported from fitness device files. Parses Garmin FIT files (`.fit` / `.fit.gz`) into `Activity` and `ActivityLap` records with heart rate, cadence, elevation, and pace data. Provides a Django management command for CLI imports and a Django Admin interface for browsing activities.

## Interface

- `Activity` model (`activity.models`): FK to user, fields for name, sport_type, start_time, duration, distance (meters), elevation, HR, cadence, calories. Computed properties: `distance_km`, `pace`, `speed_kmh`. Uniqueness on `(user, start_time)` and `external_id`.
- `ActivityLap` model (`activity.models`): FK to Activity, per-lap distance, duration, HR, cadence, elevation. Computed properties: `distance_km`, `pace`.
- `parse_fit(source)` (`activity.parser`): Parses a FIT file (path, gzip path, or binary stream) into an `ActivityData` dataclass. No Django dependency.
- `import_fit_file(user, source)` (`activity.services`): Parses and saves a FIT file. Raises `ActivityAlreadyExists` on duplicate `external_id`.
- `manage.py import_fit <path> <user_id>`: CLI command wrapping `import_fit_file`.

## Internal structure

- `parser/fit.py` — FIT parsing via `fitparse`. Extracts session, lap, file_id, and sport messages. Generates `external_id` from device serial number + timestamp.
- `shemas.py` — `ActivityData` and `LapData` dataclasses used as intermediate representation between parsers and the service layer.
- `services.py` — Orchestrates parsing and DB writes. Uses `bulk_create` for laps.
- `utils.py` — `format_duration` and `format_pace` helpers shared between admin and future API.
- `admin.py` — `ActivityAdmin` with `ActivityLapInline`, fieldsets, computed display fields.

## Dependencies

- [accounts](accounts.md) (User model via `settings.AUTH_USER_MODEL`)
- `fitparse` (FIT file parsing)
- `gzip` (stdlib, for `.fit.gz` support)

## Gotchas

- Distances are stored in **meters** (not km), unlike the `races` module which uses km. Properties `distance_km`, `pace`, `speed_kmh` convert on read.
- `external_id` format is `fit_{serial}_{timestamp}` (e.g. `fit_3467968002_20250309T070158`). Duplicate detection relies on this — reimporting the same file is a no-op.
- `fitparse` returns naive UTC datetimes; `parser/fit.py` makes them aware via `_make_aware()` before returning. Django's `USE_TZ = True` would warn otherwise.
- The `(user, start_time)` constraint is a secondary guard against duplicates from different sources. The primary guard is `external_id`.
