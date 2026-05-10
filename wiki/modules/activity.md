# Activity

**Path:** `backend/src/activity/`

## Purpose

Stores and manages running activities imported from fitness device files. Parses Garmin FIT files (`.fit` / `.fit.gz`) into `Activity` and `ActivityLap` records with heart rate, cadence, elevation, and pace data. Provides a Django management command for CLI imports and a Django Admin interface for browsing activities.

## Interface

- `Activity` model (`activity.models`): FK to user, fields for name, sport_type, start_time, duration, distance (meters), elevation, HR, cadence, calories. Computed properties: `distance_km`, `pace`, `speed_kmh`. Uniqueness on `(user, start_time)` and `external_id`.
- `ActivityLap` model (`activity.models`): FK to Activity, per-lap distance, duration, HR, cadence, elevation. Computed properties: `distance_km`, `pace`.
- `parse_fit(source)` (`activity.parser`): Parses a FIT file (path, gzip path, or binary stream) into an `ActivityData` dataclass. Rejects non-running activities with `ValueError`. No Django dependency.
- `parse_strava_csv(csv_path)` (`activity.parser.strava_csv`): Reads a Strava `activities.csv` export, returns only "Course à pied" entries with their title and FIT filename.
- `import_fit_file(user, source, *, name=None)` (`activity.services`): Parses and saves a FIT file. Optional `name` overrides the auto-generated title. Raises `ActivityAlreadyExists` on duplicate `external_id`.
- `manage.py import_fit <path> <user_id>`: Import a single FIT file.
- `manage.py bulk_import_fit <export_dir> <user_id>`: Bulk import from a Strava export directory (reads `activities.csv` to get titles and filter running activities, then imports each FIT file).

## Internal structure

- `parser/fit.py` — FIT parsing via `fitparse`. Extracts session, lap, file_id, and sport messages. Rejects non-running sports. Auto-generates descriptive names from distance/duration. Generates `external_id` from device serial number + timestamp.
- `parser/strava_csv.py` — Reads Strava's `activities.csv` export. Filters by "Course à pied" and returns `StravaCsvEntry` dataclasses with activity name and FIT filename.
- `shemas.py` — `ActivityData` and `LapData` dataclasses used as intermediate representation between parsers and the service layer.
- `services.py` — Orchestrates parsing and DB writes. Uses `bulk_create` for laps. Accepts optional name override from CSV.
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
- FIT files don't contain the user-facing activity title (only the sport type in the device language, e.g. "Course"). When importing via `bulk_import_fit`, the real title comes from Strava's `activities.csv`. When importing a single file via `import_fit`, a descriptive name is auto-generated from distance and duration (e.g. "Semi-marathon - 1h25").
- Only running activities are imported. `parse_fit` raises `ValueError` for non-running sports (swimming, cycling, etc.). `bulk_import_fit` pre-filters at the CSV level for efficiency.
