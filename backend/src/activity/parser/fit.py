from __future__ import annotations

import gzip
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import BinaryIO

import fitparse

from activity.shemas import ActivityData, LapData


def _get_field(record: fitparse.DataMessage, name: str):
    """Safely extract a field value from a FIT record."""
    field = record.get(name)
    if field is None:
        return None
    return field.value


def _make_aware(dt: datetime | None) -> datetime | None:
    """Ensure datetime is timezone-aware (UTC). fitparse returns naive UTC datetimes."""
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=UTC)
    return dt


RUNNING_SPORTS: set[str] = {"running"}

RUNNING_SUB_SPORT_MAP: dict[str, str] = {
    "generic": "running",
    "trail_running": "trail",
    "track": "track",
    "treadmill": "treadmill",
    "indoor_running": "treadmill",
}

DISTANCE_LABELS = [
    (42000, "Marathon"),
    (21000, "Semi-marathon"),
    (15000, "15 km"),
    (10000, "10 km"),
    (5000, "5 km"),
]


def _build_name(distance: Decimal, start_time: datetime, duration: timedelta) -> str:
    for threshold, label in DISTANCE_LABELS:
        if distance >= threshold * Decimal("0.95"):
            total_s = int(duration.total_seconds())
            h, rem = divmod(total_s, 3600)
            m, s = divmod(rem, 60)
            time_str = f"{h}h{m:02d}" if h else f"{m}min{s:02d}s"
            return f"{label} - {time_str}"

    km = (distance / Decimal("1000")).quantize(Decimal("0.1"))
    return f"Course {km} km - {start_time:%d/%m/%Y}"


def _build_external_id(
    serial_number: int | None,
    start_time: datetime,
) -> str:
    ts = start_time.strftime("%Y%m%dT%H%M%S")
    if serial_number:
        return f"fit_{serial_number}_{ts}"
    return f"fit_{ts}"


def _parse_session(fit: fitparse.FitFile) -> ActivityData:
    sessions = list(fit.get_messages("session"))
    if not sessions:
        raise ValueError("No session message found in FIT file")
    session = sessions[0]

    serial_number = None
    for file_id in fit.get_messages("file_id"):
        serial_number = _get_field(file_id, "serial_number")
        break

    raw_sport = str(_get_field(session, "sport") or "")
    if raw_sport not in RUNNING_SPORTS:
        raise ValueError(f"Not a running activity (sport={raw_sport}), skipping")

    raw_sub_sport = str(_get_field(session, "sub_sport") or "generic")
    sport_type = RUNNING_SUB_SPORT_MAP.get(raw_sub_sport, "running")

    start_time = _make_aware(_get_field(session, "start_time"))
    if start_time is None:
        raise ValueError("No start_time in session")

    total_time = _get_field(session, "total_timer_time") or _get_field(
        session, "total_elapsed_time"
    )
    if total_time is None:
        raise ValueError("No total_timer_time in session")
    duration = timedelta(seconds=float(total_time))

    distance_m = _get_field(session, "total_distance")
    if distance_m is None:
        raise ValueError("No total_distance in session")
    distance = Decimal(str(distance_m)).quantize(Decimal("0.01"))

    name = _build_name(distance, start_time, duration)

    elevation_gain = _get_field(session, "total_ascent")
    elevation_loss = _get_field(session, "total_descent")

    return ActivityData(
        name=name,
        sport_type=sport_type,
        start_time=start_time,
        duration=duration,
        distance=distance,
        elevation_gain=Decimal(str(elevation_gain))
        if elevation_gain is not None
        else None,
        elevation_loss=Decimal(str(elevation_loss))
        if elevation_loss is not None
        else None,
        avg_hr=_get_field(session, "avg_heart_rate"),
        max_hr=_get_field(session, "max_heart_rate"),
        avg_cadence=_get_field(session, "avg_running_cadence"),
        calories=_get_field(session, "total_calories"),
        external_id=_build_external_id(serial_number, start_time),
    )


def _parse_laps(fit: fitparse.FitFile) -> list[LapData]:
    laps: list[LapData] = []
    for i, record in enumerate(fit.get_messages("lap")):
        total_time = _get_field(record, "total_timer_time") or _get_field(
            record, "total_elapsed_time"
        )
        if total_time is None:
            continue

        distance_m = _get_field(record, "total_distance")
        if distance_m is None:
            continue

        elevation_gain = _get_field(record, "total_ascent")

        laps.append(
            LapData(
                lap_number=i + 1,
                distance=Decimal(str(distance_m)).quantize(Decimal("0.01")),
                duration=timedelta(seconds=float(total_time)),
                start_time=_make_aware(_get_field(record, "start_time")),
                avg_hr=_get_field(record, "avg_heart_rate"),
                max_hr=_get_field(record, "max_heart_rate"),
                avg_cadence=_get_field(record, "avg_running_cadence"),
                elevation_gain=Decimal(str(elevation_gain))
                if elevation_gain is not None
                else None,
                calories=_get_field(record, "total_calories"),
            )
        )
    return laps


def parse_fit(source: str | Path | BinaryIO) -> ActivityData:
    """Parse a .fit or .fit.gz file and return structured activity data.

    Args:
        source: Path to a .fit/.fit.gz file, or an open binary stream.

    Returns:
        ActivityData with laps populated.

    Raises:
        ValueError: If the file is missing required data (session, distance, etc.)
        FileNotFoundError: If the path doesn't exist.
    """
    if isinstance(source, (str, Path)):
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"FIT file not found: {path}")

        if path.suffix == ".gz" or path.name.endswith(".fit.gz"):
            with gzip.open(path, "rb") as f:
                data = f.read()
            fit = fitparse.FitFile(data)
        else:
            fit = fitparse.FitFile(str(path))
    else:
        fit = fitparse.FitFile(source)

    activity = _parse_session(fit)
    activity.laps = _parse_laps(fit)
    return activity
