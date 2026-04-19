from datetime import date, timedelta
from decimal import Decimal

import pytest

from races.models import Race
from races.utils import calculate_pace, calculate_speed


class TestRaceSave:
    def test_speed_and_pace_computed_on_create(self, race):
        expected_speed = calculate_speed(race.distance, race.time)
        expected_pace = calculate_pace(race.distance, race.time)
        assert race.speed == expected_speed
        assert race.pace == expected_pace

    def test_speed_and_pace_recomputed_on_update(self, race):
        race.distance = Decimal("42.00")
        race.time = timedelta(hours=3, minutes=45)
        race.save()
        race.refresh_from_db()

        expected_speed = calculate_speed(
            Decimal("42.00"), timedelta(hours=3, minutes=45)
        )
        expected_pace = calculate_pace(Decimal("42.00"), timedelta(hours=3, minutes=45))
        assert race.speed == expected_speed
        assert race.pace == expected_pace

    def test_str(self, race):
        assert str(race) == "Trail des Templiers"

    def test_ordering(self, user):
        Race.objects.create(
            user=user,
            name="Race A",
            date=date(2026, 1, 1),
            distance=Decimal("10"),
            time=timedelta(hours=1),
        )
        Race.objects.create(
            user=user,
            name="Race B",
            date=date(2026, 6, 1),
            distance=Decimal("10"),
            time=timedelta(hours=1),
        )
        races = list(Race.objects.filter(user=user).values_list("name", flat=True)[:2])
        assert races[0] == "Race B"


class TestValidation:
    def test_full_clean_passes_with_valid_data(self, race):
        race.full_clean()

    def test_full_clean_rejects_negative_time(self, user):
        r = Race(
            user=user,
            name="Bad",
            date=date(2026, 1, 1),
            distance=Decimal("10"),
            time=timedelta(seconds=-1),
        )
        r.speed = Decimal("0")
        r.pace = Decimal("0")
        with pytest.raises(Exception):
            r.full_clean()


class TestCalculations:
    def test_speed_10km_1h(self):
        result = calculate_speed(Decimal("10"), timedelta(hours=1))
        assert result == Decimal("10.00")

    def test_speed_42km_3h30(self):
        result = calculate_speed(Decimal("42.195"), timedelta(hours=3, minutes=30))
        assert result == Decimal("12.06")

    def test_pace_10km_1h(self):
        result = calculate_pace(Decimal("10"), timedelta(hours=1))
        assert result == Decimal("6.00")

    def test_pace_42km_3h30(self):
        result = calculate_pace(Decimal("42.195"), timedelta(hours=3, minutes=30))
        assert result == Decimal("4.98")

    def test_speed_zero_time(self):
        result = calculate_speed(Decimal("10"), timedelta(seconds=0))
        assert result == Decimal("0")

    def test_pace_zero_distance(self):
        result = calculate_pace(Decimal("0"), timedelta(hours=1))
        assert result == Decimal("0")
