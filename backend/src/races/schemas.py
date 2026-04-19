from datetime import date as date_type
from datetime import timedelta
from decimal import Decimal
from typing import Annotated, Optional

from ninja import Field, FilterLookup, FilterSchema, ModelSchema, Schema

from races.models import Race


class RaceOut(ModelSchema):
    class Meta:
        model = Race
        fields = (
            "id",
            "user",
            "name",
            "edition",
            "date",
            "distance",
            "elevation_gain",
            "time",
            "speed",
            "pace",
            "strava_url",
            "results_url",
            "location",
            "number_of_participants",
            "global_ranking",
            "category_ranking",
        )


class RaceIn(Schema):
    name: str = Field(..., max_length=255)
    date: date_type
    distance: Decimal
    time: timedelta
    edition: str | None = Field(default=None, max_length=255)
    elevation_gain: Decimal | None = None
    strava_url: str | None = None
    results_url: str | None = None
    location: str | None = Field(default=None, max_length=255)
    number_of_participants: int | None = None
    global_ranking: int | None = None
    category_ranking: int | None = None


class RacePatch(Schema):
    name: str | None = Field(default=None, max_length=255)
    date: date_type | None = None
    distance: Decimal | None = None
    time: timedelta | None = None
    edition: str | None = Field(default=None, max_length=255)
    elevation_gain: Decimal | None = None
    strava_url: str | None = None
    results_url: str | None = None
    location: str | None = Field(default=None, max_length=255)
    number_of_participants: int | None = None
    global_ranking: int | None = None
    category_ranking: int | None = None


class RaceFilter(FilterSchema):
    name: Annotated[Optional[str], FilterLookup(q="name__icontains")] = None
    edition: Annotated[Optional[str], FilterLookup(q="edition__icontains")] = None
    location: Annotated[Optional[str], FilterLookup(q="location__icontains")] = None
    date_from: Annotated[Optional[date_type], FilterLookup(q="date__gte")] = None
    date_to: Annotated[Optional[date_type], FilterLookup(q="date__lte")] = None
    min_distance: Annotated[Optional[Decimal], FilterLookup(q="distance__gte")] = None
    max_distance: Annotated[Optional[Decimal], FilterLookup(q="distance__lte")] = None


class Message(Schema):
    detail: str
