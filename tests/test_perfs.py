from src.perfs_tracker import Perf, PerfOfAllTime
from src.time_an_pace import Time, Pace

from datetime import datetime


perfs: dict[int, Time] = {
    6: Time(hours=0, minutes=47, seconds=28),
    10: Time(hours=1, minutes=45, seconds=0),
    21.1: Time(hours=0, minutes=25, seconds=0),
}


class TestPerf:
    def test_10km(self):
        distance = 10
        time = perfs[distance]
        perf = Perf(
            time=time,
            distance=distance,
            name="10km in Paris",
            date="2021-10-10",
            location="Paris",
        )
        expected_pace = Pace.from_time_distance(time, 10)
        assert perf.pace == expected_pace
        assert perf.get_event().name == "e10km"

    def test_half_marathon(self):
        distance = 21.1
        time = perfs[distance]
        perf = Perf(time=time, distance=distance, name="HM in NY", date="2023-01-28")
        expected_pace = Pace.from_time_distance(time, distance)
        assert perf.pace == expected_pace
        assert perf.get_event().name == "eHM"

    def test_6km(self):
        distance = 6
        time = perfs[distance]
        perf = Perf(
            time=time, distance=distance, name="one lap at backyard", date="2024-12-25"
        )
        expected_pace = Pace.from_time_distance(time, 6)
        assert perf.pace == expected_pace
        assert perf.get_event() == None


class TestPerfOfAllTime:
    def setup_method(self):
        self.test_perfs: list[Perf] = []
        for distance, time in perfs.items():
            perf = Perf(
                time=time,
                distance=distance,
                date=datetime.now(),
                name_event=f"test {distance}km on {time}",
            )
            self.test_perfs.append(perf)

        # Add also a 10km perf
        self.test_perfs.append(
            Perf(
                time=Time(hours=0, minutes=40, seconds=0),
                distance=10,
                date=datetime.now(),
                name_event="10km pb",
            )
        )
        self.perfs_of_all_time = PerfOfAllTime(perfs=self.test_perfs)

    def test_len(self):
        assert len(self.perfs_of_all_time) == len(self.test_perfs)

    def test_add_perf(self):
        new_perf = Perf(
            time=Time(hours=0, minutes=30, seconds=0),
            distance=5,
            date=datetime.now(),
            name_event="5km in the park",
        )
        self.perfs_of_all_time.add_perf(new_perf)
        assert len(self.perfs_of_all_time) == len(self.test_perfs) + 1
        assert self.perfs_of_all_time.perfs[-1] == new_perf

    def test_find_pb_only_one_race(self):
        best_perf_on_21_1 = self.perfs_of_all_time.get_personal_best(21.1)
        assert best_perf_on_21_1.time == perfs[21.1]

    def test_find_pb_multiple_races(self):
        best_perf_on_10 = self.perfs_of_all_time.get_personal_best(10)
        assert best_perf_on_10 == self.test_perfs[-1]

    def test_find_pb_on_inexistent_distance(self):
        best_perf_on_5 = self.perfs_of_all_time.get_personal_best(5)
        assert best_perf_on_5 == None

    def test_get_all_pb(self):
        all_pb = self.perfs_of_all_time.get_all_personal_best()
        expected_perfs: dict[str, Time] = {
            6: perfs[6],
            10: self.test_perfs[-1].time,
            21.1: perfs[21.1],
        }
        assert len(all_pb) == len(expected_perfs)
        for distance, perf in all_pb.items():
            assert perf.time == expected_perfs[distance]
