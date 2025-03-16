from math import isclose

from src.time_an_pace import Pace, Time


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
