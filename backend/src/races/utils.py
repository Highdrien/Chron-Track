from datetime import timedelta
from decimal import ROUND_HALF_UP, Decimal

TWO_PLACES = Decimal("0.01")


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
