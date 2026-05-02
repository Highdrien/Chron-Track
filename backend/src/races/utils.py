"""Utilities for races."""

from __future__ import annotations

from datetime import timedelta
from decimal import ROUND_HALF_UP, Decimal
from functools import lru_cache
from typing import TYPE_CHECKING

from accounts.models import User

if TYPE_CHECKING:
    from races.models import Race

TWO_PLACES = Decimal("0.01")

DISTANCE_CATEGORIES: dict[str, tuple[Decimal, Decimal]] = {
    "5K": (Decimal("4.5"), Decimal("5.5")),
    "10K": (Decimal("9.5"), Decimal("10.5")),
    "20K": (Decimal("19.5"), Decimal("20.5")),
    "Semi": (Decimal("20.5"), Decimal("22.0")),
    "30K": (Decimal("29.5"), Decimal("30.5")),
    "Marathon": (Decimal("41.5"), Decimal("43.0")),
}


def calculate_speed(distance: Decimal, time: timedelta) -> Decimal:
    """Return speed in km/h from distance (km) and a timedelta."""
    total_seconds = Decimal(str(time.total_seconds()))
    if total_seconds <= 0:
        return Decimal("0")
    hours = total_seconds / Decimal("3600")
    return (distance / hours).quantize(TWO_PLACES, rounding=ROUND_HALF_UP)


def calculate_pace(distance: Decimal, time: timedelta) -> Decimal:
    """Return pace in min/km from distance (km) and a timedelta."""
    total_seconds = Decimal(str(time.total_seconds()))
    if distance <= 0:
        return Decimal("0")
    minutes = total_seconds / Decimal("60")
    return (minutes / distance).quantize(TWO_PLACES, rounding=ROUND_HALF_UP)


def get_record(user: User, category: str) -> Race | None:
    from races.models import Race

    if category not in DISTANCE_CATEGORIES:
        raise ValueError(f"Invalid category: {category}")

    low, high = DISTANCE_CATEGORIES[category]
    return (
        Race.objects.filter(user=user, distance__gte=low, distance__lte=high)
        .order_by("time")
        .first()
    )


@lru_cache(maxsize=1)
def get_list_categories() -> list[str]:
    return list(DISTANCE_CATEGORIES.keys())
