import json
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from .iaaf import Event, Gender, IAAFCalculator
from .time_an_pace import Pace, Time


class Perf(BaseModel):
    time: Time
    distance: float
    date: datetime
    name_event: Optional[str] = None
    location: Optional[str] = None
    url_results: Optional[str] = None
    url_strava: Optional[str] = None
    iaaf_score: Optional[int] = None

    @property
    def pace(self) -> Pace:
        return Pace.from_time_distance(self.time, self.distance)

    def __str__(self) -> str:
        return f"{self.time} for {self.distance}km on {self.date.date()}"

    def get_event(self) -> Optional[Event]:
        """
        Retrieves the event corresponding to the distance of the current instance.

        Returns:
            Optional[Event]: An Event object if the distance is found in the mapping,
                otherwise None.
        """
        mapping: dict[float, Event] = {
            5: Event("5km"),
            10: Event("10km"),
            15: Event("15km"),
            16.09: Event("10 Miles"),
            20: Event("20km"),
            21.1: Event("HM"),
            25: Event("25km"),
            30: Event("30km"),
            42.2: Event("Marathon"),
            100: Event("100km"),
        }
        if self.distance not in mapping:
            print(f"Distance {self.distance} not in mapping")
            return None
        return mapping[self.distance]


class MainPerf(Perf):
    num_participants: Optional[int] = None
    rank: Optional[int] = None
    sub_perfs: dict[tuple[float, float], "SubPerf"] = {}

    @property
    def ratio(self) -> Optional[float]:
        if self.num_participants is None or self.rank is None:
            return None
        return self.rank / self.num_participants

    def add_sub_perf(self, list_sub_time: list[Time], sub_distance: float) -> None:
        """
        Adds sub-performance metrics to the performance tracker.

        This method takes a list of sub-times and a sub-distance, and calculates
        the sub-performance metrics for each segment. It ensures that the sum of
        the sub-times does not exceed the total time of the performance.

        Args:
            list_sub_time (list[Time]): A list of Time objects representing the
                sub-times for each segment of sub_distance.
            sub_distance (float): The distance for each sub-performance segment.

        """
        sum_time = sum(sub_time.get_seconds() for sub_time in list_sub_time)
        if sum_time > self.time.get_seconds():
            raise ValueError(
                "Sum of sub times cannot be greater than total"
                + f" time (sum sub time{sum_time} > time:{self.time})"
            )

        if sub_distance > self.distance:
            raise ValueError(
                "Sub distance cannot be greater than total distance"
                + f" (sub distance:{sub_distance} > distance:{self.distance})"
            )

        sub_section_length = self._create_each_sub_section_length(
            list_sub_time, sub_distance
        )

        for distance, list_sub_time in sub_section_length.items():
            print(f"{distance=}, {list_sub_time=}")

            for i, sub_time in enumerate(list_sub_time):
                begin_distance = i * sub_distance
                end_distance = begin_distance + distance
                sub_pref = self._create_sub_perf(sub_time, begin_distance, end_distance)
                if (begin_distance, end_distance) in self.sub_perfs:
                    raise ValueError(
                        f"SubPerf for {begin_distance}-{end_distance} already exists"
                    )
                self.sub_perfs[(begin_distance, end_distance)] = sub_pref
                print(f"Added sub_perf: {sub_pref}")

    def to_dict(self) -> dict[str, str | list[dict[str, str]]]:
        output: dict[str, str | list[dict[str, str]]] = {
            "time": str(self.time),
            "distance": str(self.distance),
            "date": str(self.date),
            "name_event": str(self.name_event),
            "location": str(self.location),
            "url_results": str(self.url_results),
            "url_strava": str(self.url_strava),
            "iaaf_score": str(self.iaaf_score),
            "num_participants": str(self.num_participants),
            "rank": str(self.rank),
            "sub_perfs": (
                [sub_perf.to_dict() for sub_perf in self.sub_perfs.values()]
                if self.sub_perfs
                else "None"
            ),
        }
        # remove None value
        return {k: v for k, v in output.items() if v != "None"}

    def _create_sub_perf(
        self, sub_time: Time, begin_distance: float, end_distance: float
    ) -> "SubPerf":
        """
        Creates a sub-performance (SubPerf) instance based on the given sub_time,
        begin_distance, and end_distance.

        Args:
            sub_time (Time): The time duration for the sub-performance.
            begin_distance (float): The starting distance for the sub-performance.
            end_distance (float): The ending distance for the sub-performance.

        Returns:
            SubPerf: A new SubPerf instance representing the sub-performance.
        """
        if begin_distance < 0:
            raise ValueError("Begin distance cannot be negative")
        if end_distance > self.distance:
            raise ValueError("End distance cannot be greater than total distance")
        if begin_distance > end_distance:
            raise ValueError("End distance must be greater than begin distance")
        if sub_time.get_seconds() > self.time.get_seconds():
            raise ValueError(
                "Sub time cannot be greater than total time"
                + f" (sub time:{sub_time} > time:{self.time})"
            )
        sub_data = deepcopy(self.__dict__)
        del sub_data["sub_perfs"]
        del sub_data["num_participants"]
        del sub_data["rank"]
        sub_data["time"] = sub_time
        sub_data["distance"] = end_distance - begin_distance
        sub_data["parent_perf"] = self
        sub_data["begin_distance"] = begin_distance
        sub_data["end_distance"] = end_distance
        return SubPerf(**sub_data)

    def _create_each_sub_section_length(
        self, list_sub_time: list[Time], sub_distance: float
    ) -> dict[float, list[Time]]:
        each_sub_section_length: dict[float, list[Time]] = {}
        step: int = 0
        step_distance: float = sub_distance
        while step_distance < self.distance:
            # print(f"{step=}, {step_distance=}")
            each_sub_section_length[step_distance] = []
            for i in range(len(list_sub_time) - step):
                # print(f"{i=}, {i + 1 + step=}")
                slice_time = list_sub_time[i : i + 1 + step]
                # print(f"{i=}, {slice_time=}")
                sum_time_seconds = sum(
                    sub_time.get_seconds() for sub_time in slice_time
                )
                each_sub_section_length[step_distance].append(
                    Time.from_total_seconds(sum_time_seconds)
                )
            step_distance += sub_distance
            step += 1
        return each_sub_section_length


class SubPerf(Perf):
    parent_perf: MainPerf
    begin_distance: float
    end_distance: float

    def __str__(self):
        return (
            f"SubPerf of {self.time} between {self.begin_distance} and "
            + f"{self.end_distance}km during {self.distance}km on {self.date.date()}"
        )

    def to_dict(self) -> dict[str, str]:
        output = {
            "time": str(self.time),
            "distance": str(self.distance),
            "iaaf_score": str(self.iaaf_score),
            "begin_distance": str(self.begin_distance),
            "end_distance": str(self.end_distance),
        }
        return {k: v for k, v in output.items() if v != "None"}


class PerfOfAllTime(BaseModel):
    perfs: list[Perf] = []
    gender: Optional[Gender] = None

    @property
    def iaaf(self) -> Optional[IAAFCalculator]:
        if self.gender is None:
            return None
        return IAAFCalculator()

    def __len__(self) -> int:
        return len(self.perfs)

    def add_perf(self, perf: Perf) -> None:
        """
        Adds a performance record to the tracker.

        If the performance record is an instance of MainPerf, its sub-performances
        are also added to the tracker.

        Args:
            perf (Perf): The performance record to be added.
        """
        self.perfs.append(perf)

        if isinstance(perf, MainPerf):
            for sub_perf in perf.sub_perfs.values():
                self.perfs.append(sub_perf)

    def get_personal_best(self, distance: float) -> Optional[Perf]:
        """
        Retrieves the personal best performance for a given distance.

        Args:
            distance (float): The distance for which to retrieve the personal best.

        Returns:
            Optional[Perf]: The personal best performance if found, otherwise None.
        """
        filtered_perfs = list(
            filter(lambda perf: perf.distance == distance, self.perfs)
        )
        if len(filtered_perfs) == 0:
            return None
        return min(filtered_perfs, key=lambda perf: perf.time)

    def get_all_personal_best(self) -> dict[float, Perf]:
        """
        Retrieves the personal best performance for each distance.

        Returns:
            dict[float, Perf]: A dictionary with the distance as key and the
                personal best performance as value.
        """
        all_pb = {
            distance: self.get_personal_best(distance)
            for distance in set(perf.distance for perf in self.perfs)
        }
        return {distance: perf for distance, perf in all_pb.items() if perf is not None}

    def compute_iaaf_scores(self) -> None:
        """
        Computes the IAAF scores for each performance in the `perfs` list.

        This method requires that the `iaaf` and `gender` attributes are set.
        If either is not set, the method returns without computing any scores.

        Returns:
            None
        """
        if self.iaaf is None or self.gender is None:
            print("IAAF scores cannot be computed without gender information")
            return None
        for perf in self.perfs:
            event = perf.get_event()
            if event is None:
                print(f"Event not found for distance {perf.distance}")
                continue
            iaaf_score = self.iaaf.get_iaaf_score(
                gender=self.gender, event=event, time=perf.time
            )
            perf.iaaf_score = iaaf_score
            print(f"IAAF score for {perf} is {iaaf_score}")

    def save_to_json(self, filepath: Path) -> None:
        main_perfs: list[MainPerf] = list(
            filter(lambda perf: isinstance(perf, MainPerf), self.perfs)
        )
        data = [perf.to_dict() for perf in main_perfs]
        json.dump(data, open(filepath, "w"), indent=4)
