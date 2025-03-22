from math import isclose
import pytest
from pydantic import ValidationError

from src.time_an_pace import Pace, Time


class TestTime:
    def test_get_minutes(self):
        t = Time(hours=1, minutes=25, seconds=20)
        assert t.get_minutes() == 85 + 1 / 3

    def test_get_seconds(self):
        t = Time(hours=1, minutes=25, seconds=20)
        assert t.get_seconds() == 5120

    def test_compare(self):
        t1 = Time(hours=1, minutes=25, seconds=20)
        t2 = Time(hours=1, minutes=25, seconds=21)
        assert t1 < t2
        assert t1 <= t2
        assert t2 > t1
        assert t2 >= t1

    def test_from_total_seconds(self):
        num_seconds = 5120
        t = Time.from_total_seconds(num_seconds)
        assert t.hours == 1
        assert t.minutes == 25
        assert t.seconds == 20

    def test_add(self):
        t1 = Time(hours=1, minutes=25, seconds=20)
        t2 = Time(minutes=35, seconds=40)
        t = t1 + t2
        assert t == Time(hours=2, minutes=1, seconds=0)

    @pytest.mark.parametrize(
        ("minutes", "seconds"),
        [
            (20, -30),
            (0, -30),
            (0, 0),
            (-10, -30),
        ],
    )
    def test_time_negative(self, minutes, seconds):
        with pytest.raises(ValidationError):
            Time(minutes=minutes, seconds=seconds)


class TestPace:
    def test_half_marathon(self):
        p = Pace.from_time_distance(Time(hours=1, minutes=25, seconds=22), 21)
        assert p.minutes == 4
        assert p.seconds == 3
        assert isclose(p.kmh, 14.81, rel_tol=1e-2)

    def test_10k(self):
        p = Pace.from_time_distance(Time(hours=1, minutes=0, seconds=0), 10)
        assert p.minutes == 6
        assert p.seconds == 0
        assert p.kmh == 10

    def test_5k(self):
        p = Pace.from_time_distance(Time(hours=0, minutes=17, seconds=30), 5)
        assert p.minutes == 3
        assert p.seconds == 30
        assert isclose(p.kmh, 17.14, rel_tol=1e-3)
