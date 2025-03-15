

from src.basic_class import Time, Pace

class TestPace:
    def test_half_marathon(self):
        p = Pace.from_time_distance(Time(hours=1, minutes=25, seconds=22), 21)
        assert p.minutes == 4
        assert p.seconds == 3

    def test_10k(self):
        p = Pace.from_time_distance(Time(hours=1, minutes=0, seconds=0), 10)
        assert p.minutes == 6
        assert p.seconds == 0
    
    def test_5k(self):
        p = Pace.from_time_distance(Time(hours=0, minutes=17, seconds=30), 5)
        assert p.minutes == 3
        assert p.seconds == 30