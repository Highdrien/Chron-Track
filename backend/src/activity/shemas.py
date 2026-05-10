from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal

# Schemas of Activity and Lap django models


@dataclass
class LapData:
    lap_number: int
    distance: Decimal
    duration: timedelta
    start_time: datetime | None = None
    avg_hr: int | None = None
    max_hr: int | None = None
    avg_cadence: int | None = None
    elevation_gain: Decimal | None = None
    calories: int | None = None


@dataclass
class ActivityData:
    name: str
    sport_type: str
    start_time: datetime
    duration: timedelta
    distance: Decimal
    elevation_gain: Decimal | None = None
    elevation_loss: Decimal | None = None
    avg_hr: int | None = None
    max_hr: int | None = None
    avg_cadence: int | None = None
    calories: int | None = None
    external_id: str | None = None
    laps: list[LapData] = field(default_factory=list)
