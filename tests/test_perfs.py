from datetime import datetime

from src.iaaf import Event, Gender
from src.perfs_tracker import MainPerf, PerfOfAllTime, SubPerf
from src.time_an_pace import Pace, Time

perfs: dict[float, Time] = {
    6: Time(hours=0, minutes=47, seconds=28),
    10: Time(hours=1, minutes=45, seconds=0),
    21.1: Time(hours=1, minutes=25, seconds=0),
}

sub_perfs_10k: list[Time] = [
    Time(hours=0, minutes=21, seconds=0),
    Time(hours=0, minutes=19, seconds=0),
]
sub_perfs_21k: list[Time] = [
    Time(hours=0, minutes=22, seconds=0),
    Time(hours=0, minutes=20, seconds=30),
    Time(hours=0, minutes=19, seconds=30),
    Time(hours=0, minutes=18, seconds=0),
]


class TestPerf:
    def test_10km(self) -> None:
        distance = 10
        time = perfs[distance]
        perf = MainPerf(
            time=time,
            distance=distance,
            name="10km in Paris",
            date="2021-10-10",
            location="Paris",
        )
        expected_pace = Pace.from_time_distance(time, 10)
        assert perf.pace == expected_pace
        assert perf.get_event() == Event("10km")

    def test_half_marathon(self):
        distance = 21.1
        time = perfs[distance]
        perf = MainPerf(
            time=time, distance=distance, name="HM in NY", date="2023-01-28"
        )
        expected_pace = Pace.from_time_distance(time, distance)
        assert perf.pace == expected_pace
        assert perf.get_event() == Event("HM")

    def test_6km(self):
        distance = 6
        time = perfs[distance]
        perf = MainPerf(
            time=time, distance=distance, name="one lap at backyard", date="2024-12-25"
        )
        expected_pace = Pace.from_time_distance(time, 6)
        assert perf.pace == expected_pace
        assert perf.get_event() is None

    def test_sub_perfs_10(self):
        distance = 10
        time = perfs[distance]
        perf = MainPerf(
            time=time,
            distance=distance,
            date="2021-10-10",
        )
        perf.add_sub_perf(sub_perfs_10k, 5)
        assert len(perf.sub_perfs) == len(sub_perfs_10k)
        for sub_perf in perf.sub_perfs.values():
            assert sub_perf.time in sub_perfs_10k

    def test_sub_perfs_21(self):
        distance = 21.1
        time = perfs[distance]
        perf = MainPerf(
            time=time,
            distance=distance,
            date="2021-10-10",
        )
        perf.add_sub_perf(sub_perfs_21k, 5)
        assert len(perf.sub_perfs) == 4 + 3 + 2 + 1
        # check that all 5k splits are in the sub_perfs
        for i in range(4):
            begin = 5 * i
            end = begin + 5
            assert (begin, end) in perf.sub_perfs

        # check that all 10k splits are in the sub_perfs
        for i in range(3):
            begin = 5 * i
            end = begin + 10
            assert (begin, end) in perf.sub_perfs

        # check that all 15k splits are in the sub_perfs
        for i in range(2):
            begin = 5 * i
            end = begin + 15
            assert (begin, end) in perf.sub_perfs

        # check that all 20k splits are in the sub_perfs
        assert (0, 20) in perf.sub_perfs


class TestPerfOfAllTime:
    def setup_method(self):
        self.test_perfs: list[MainPerf] = []
        for distance, time in perfs.items():
            perf = MainPerf(
                time=time,
                distance=distance,
                date=datetime.now(),
                name_event=f"test {distance}km on {time}",
            )
            self.test_perfs.append(perf)

        # Add also a 10km perf
        self.test_perfs.append(
            MainPerf(
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
        new_perf = MainPerf(
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
        assert best_perf_on_21_1 is not None
        assert best_perf_on_21_1.time == perfs[21.1]

    def test_find_pb_multiple_races(self):
        best_perf_on_10 = self.perfs_of_all_time.get_personal_best(10)
        assert best_perf_on_10 is not None
        assert best_perf_on_10 == self.test_perfs[-1]

    def test_find_pb_on_inexistent_distance(self):
        best_perf_on_5 = self.perfs_of_all_time.get_personal_best(5)
        assert best_perf_on_5 is None

    def test_get_all_pb(self):
        all_pb = self.perfs_of_all_time.get_all_personal_best()
        expected_perfs: dict[float, Time] = {
            6: perfs[6],
            10: self.test_perfs[-1].time,
            21.1: perfs[21.1],
        }
        assert len(all_pb) == len(expected_perfs)
        for distance, perf in all_pb.items():
            assert perf.time == expected_perfs[distance]

    def test_get_iaaf(self):
        self.perfs_of_all_time.gender = Gender("female")
        self.perfs_of_all_time.compute_iaaf_scores()
        pb_10k = self.perfs_of_all_time.get_personal_best(10)
        assert pb_10k is not None
        assert pb_10k.iaaf_score == 755
        pb_hm = self.perfs_of_all_time.get_personal_best(21.1)
        assert pb_hm is not None
        assert pb_hm.iaaf_score == 843
        pb_6k = self.perfs_of_all_time.get_personal_best(6)
        assert pb_6k is not None
        assert pb_6k.iaaf_score is None

    def test_find_pb_on_sub_split(self):
        # Add a 10km perf with sub splits
        perf10k = MainPerf(time=perfs[10], distance=10, date=datetime.now())
        perf10k.add_sub_perf(sub_perfs_10k, 5)
        self.perfs_of_all_time.add_perf(perf10k)

        # Add a HM perf with sub splits of 5km
        perf21k = MainPerf(time=perfs[21.1], distance=21.1, date=datetime.now())
        perf21k.add_sub_perf(sub_perfs_21k, 5)
        self.perfs_of_all_time.add_perf(perf21k)

        # Test the best perf on 5km
        # best perf on 5km must be the last 5k of the HM
        best_perf_on_5 = self.perfs_of_all_time.get_personal_best(5)
        print(best_perf_on_5)
        assert best_perf_on_5 is not None
        assert isinstance(best_perf_on_5, SubPerf)
        assert best_perf_on_5.parent_perf == perf21k
        assert best_perf_on_5.begin_distance == 15
        assert best_perf_on_5.end_distance == 20

        # Test the best perf on 10km
        # best perf on 10km must be the last 10k of the HM
        best_perf_on_10 = self.perfs_of_all_time.get_personal_best(10)
        assert best_perf_on_10 is not None
        assert isinstance(best_perf_on_10, SubPerf)
        assert best_perf_on_10.parent_perf == perf21k
        assert best_perf_on_10.begin_distance == 10
        assert best_perf_on_10.end_distance == 20

    def test_get_iaaf_on_splited_race(self):
        # Add a HM perf with sub splits of 5km
        perf21k = MainPerf(time=perfs[21.1], distance=21.1, date=datetime.now())
        perf21k.add_sub_perf(sub_perfs_21k, 5)
        self.perfs_of_all_time.add_perf(perf21k)

        self.perfs_of_all_time.gender = Gender("male")
        self.perfs_of_all_time.compute_iaaf_scores()
        pb_10k = self.perfs_of_all_time.get_personal_best(10)
        assert pb_10k is not None
        assert pb_10k.iaaf_score is not None
        assert pb_10k.iaaf_score == 424
