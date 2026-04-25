from datetime import timedelta
from typing import TYPE_CHECKING

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from races import utils


class Race(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="races",
        verbose_name="User",
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Name",
        help_text="Name of the race",
    )
    edition = models.CharField(
        max_length=255,
        verbose_name="Edition",
        help_text="Edition of the race",
        blank=True,
        null=True,
        default=None,
    )
    date = models.DateField(
        verbose_name="Date",
        help_text="Date of the race",
    )
    distance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Distance",
        help_text="Distance of the race (in kilometers)",
        validators=[MinValueValidator(0)],
    )
    elevation_gain = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        default=None,
        verbose_name="Elevation gain",
        help_text="Elevation gain of the race (in meters)",
        validators=[MinValueValidator(0)],
    )
    time = models.DurationField(
        verbose_name="Time",
        help_text="Time of the race",
        validators=[MinValueValidator(timedelta(0))],
    )
    speed = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Speed",
        help_text="Speed of the race (in km/h)",
        validators=[MinValueValidator(0)],
        editable=False,
    )
    pace = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Pace",
        help_text="Pace of the race (in min/km)",
        validators=[MinValueValidator(0)],
        editable=False,
    )
    strava_url = models.URLField(
        verbose_name="Strava URL",
        help_text="URL of the race on Strava",
        blank=True,
        null=True,
    )
    results_url = models.URLField(
        verbose_name="Results URL",
        help_text="URL of the race results",
        blank=True,
        null=True,
    )
    location = models.CharField(
        max_length=255,
        verbose_name="Location",
        help_text="Location of the race",
        blank=True,
        null=True,
        default=None,
    )
    number_of_participants = models.IntegerField(
        verbose_name="Number of participants",
        help_text="Number of participants in the race",
        blank=True,
        null=True,
        default=None,
    )
    global_ranking = models.IntegerField(
        verbose_name="Global ranking",
        help_text="Global ranking of the race",
        blank=True,
        null=True,
        default=None,
    )
    category_ranking = models.IntegerField(
        verbose_name="Category ranking",
        help_text="Category ranking of the race",
        blank=True,
        null=True,
        default=None,
    )

    if TYPE_CHECKING:
        id: int

    class Meta:
        verbose_name = "Race"
        verbose_name_plural = "Races"
        ordering = ["-date"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(speed__gte=0),
                name="race_speed_positive",
            ),
            models.CheckConstraint(
                condition=models.Q(pace__gte=0),
                name="race_pace_positive",
            ),
            models.CheckConstraint(
                condition=models.Q(distance__gte=0),
                name="race_distance_positive",
            ),
        ]

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.speed = utils.calculate_speed(self.distance, self.time)
        self.pace = utils.calculate_pace(self.distance, self.time)
        super().save(*args, **kwargs)
