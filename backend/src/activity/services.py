from __future__ import annotations

from pathlib import Path
from typing import BinaryIO

from accounts.models import User
from activity.models import Activity, ActivityLap
from activity.parser import parse_fit
from activity.shemas import ActivityData


class ActivityAlreadyExists(Exception):
    def __init__(self, activity: Activity):
        self.activity = activity
        super().__init__(
            f"Activity already exists: {activity.name} ({activity.start_time})"
        )


def _save_activity(user: User, data: ActivityData) -> Activity:
    if data.external_id:
        existing = Activity.objects.filter(external_id=data.external_id).first()
        if existing:
            raise ActivityAlreadyExists(existing)

    activity = Activity.objects.create(
        user=user,
        source=Activity.Source.FIT,
        external_id=data.external_id,
        name=data.name,
        sport_type=data.sport_type,
        start_time=data.start_time,
        duration=data.duration,
        distance=data.distance,
        elevation_gain=data.elevation_gain,
        elevation_loss=data.elevation_loss,
        avg_hr=data.avg_hr,
        max_hr=data.max_hr,
        avg_cadence=data.avg_cadence,
        calories=data.calories,
    )

    laps = [
        ActivityLap(
            activity=activity,
            lap_number=lap.lap_number,
            distance=lap.distance,
            duration=lap.duration,
            start_time=lap.start_time,
            avg_hr=lap.avg_hr,
            max_hr=lap.max_hr,
            avg_cadence=lap.avg_cadence,
            elevation_gain=lap.elevation_gain,
            calories=lap.calories,
        )
        for lap in data.laps
    ]
    if laps:
        ActivityLap.objects.bulk_create(laps)

    return activity


def import_fit_file(user: User, source: str | Path | BinaryIO) -> Activity:
    """Parse a FIT file and save it as an Activity.

    Raises:
        ActivityAlreadyExists: if an activity with the same external_id exists.
        ValueError: if the FIT file is invalid or missing required data.
        FileNotFoundError: if the file path doesn't exist.
    """
    data = parse_fit(source)
    return _save_activity(user, data)
