from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal
from typing import TYPE_CHECKING

from django.conf import settings
from django.db import models

if TYPE_CHECKING:
    from accounts.models import User


class Activity(models.Model):
    class Source(models.TextChoices):
        FIT = "fit"
        GPX = "gpx"
        TCX = "tcx"
        STRAVA_API = "strava_api"
        GARMIN_API = "garmin_api"

    class SportType(models.TextChoices):
        RUNNING = "running"
        TRAIL = "trail"
        TRACK = "track"
        TREADMILL = "treadmill"

    user: User = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="activities",
    )
    source: str = models.CharField(max_length=20, choices=Source.choices)
    external_id: str | None = models.CharField(
        max_length=255, unique=True, null=True, blank=True
    )

    name: str = models.CharField(max_length=255)
    sport_type: str = models.CharField(
        max_length=25, choices=SportType.choices, default=SportType.RUNNING
    )
    start_time: datetime = models.DateTimeField()
    duration: timedelta = models.DurationField()
    distance: Decimal = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Distance in meters"
    )
    elevation_gain: Decimal | None = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True, help_text="In meters"
    )
    elevation_loss: Decimal | None = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True, help_text="In meters"
    )

    avg_hr: int | None = models.PositiveSmallIntegerField(null=True, blank=True)
    max_hr: int | None = models.PositiveSmallIntegerField(null=True, blank=True)
    avg_cadence: int | None = models.PositiveSmallIntegerField(null=True, blank=True)
    calories: int | None = models.PositiveIntegerField(null=True, blank=True)

    created_at: datetime = models.DateTimeField(auto_now_add=True)

    if TYPE_CHECKING:
        id: int
        laps: models.Manager[ActivityLap]

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"
        ordering = ["-start_time"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "start_time"],
                name="unique_user_start_time",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.start_time:%Y-%m-%d})"

    @property
    def distance_km(self) -> Decimal:
        return (self.distance / Decimal("1000")).quantize(Decimal("0.01"))

    @property
    def pace(self) -> timedelta | None:
        """Average pace as timedelta (min/km)."""
        km = self.distance_km
        if not km or km <= 0:
            return None
        total_seconds = self.duration.total_seconds()
        seconds_per_km = total_seconds / float(km)
        return timedelta(seconds=seconds_per_km)

    @property
    def speed_kmh(self) -> Decimal | None:
        """Average speed in km/h."""
        hours = Decimal(str(self.duration.total_seconds())) / Decimal("3600")
        if hours <= 0:
            return None
        return (self.distance_km / hours).quantize(Decimal("0.01"))


class ActivityLap(models.Model):
    activity: Activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, related_name="laps"
    )
    lap_number: int = models.PositiveSmallIntegerField()
    distance: Decimal = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="In meters"
    )
    duration: timedelta = models.DurationField()
    start_time: datetime | None = models.DateTimeField(null=True, blank=True)

    avg_hr: int | None = models.PositiveSmallIntegerField(null=True, blank=True)
    max_hr: int | None = models.PositiveSmallIntegerField(null=True, blank=True)
    avg_cadence: int | None = models.PositiveSmallIntegerField(null=True, blank=True)
    elevation_gain: Decimal | None = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )
    calories: int | None = models.PositiveIntegerField(null=True, blank=True)

    if TYPE_CHECKING:
        id: int

    class Meta:
        verbose_name = "Activity Lap"
        verbose_name_plural = "Activity Laps"
        ordering = ["activity", "lap_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["activity", "lap_number"],
                name="unique_activity_lap_number",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.activity.name} - Lap {self.lap_number}"

    @property
    def distance_km(self) -> Decimal:
        return (self.distance / Decimal("1000")).quantize(Decimal("0.01"))

    @property
    def pace(self) -> timedelta | None:
        km = self.distance_km
        if not km or km <= 0:
            return None
        seconds_per_km = self.duration.total_seconds() / float(km)
        return timedelta(seconds=seconds_per_km)
