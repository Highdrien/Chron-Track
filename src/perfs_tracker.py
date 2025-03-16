from datetime import datetime
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

    @property
    def pace(self) -> Pace:
        return Pace.from_time_distance(self.time, self.distance)

    def __str__(self) -> str:
        return f"{self.time} for {self.distance}km on {self.date}"

    def get_event(self) -> Optional[Event]:
        """
        Retrieves the event corresponding to the distance of the current instance.

        Returns:
            Optional[Event]: An Event object if the distance is found in the mapping,
                otherwise None.
        """
        mapping: dict[int, Event] = {
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


class PerfOfAllTime(BaseModel):
    perfs: list[Perf]
    gender: Optional[Gender] = None

    @property
    def iaaf(self) -> Optional[IAAFCalculator]:
        if self.gender is None:
            return None
        return IAAFCalculator()

    def __len__(self) -> int:
        return len(self.perfs)

    def add_perf(self, perf: Perf) -> None:
        self.perfs.append(perf)

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
            dict[float, Perf]: A dictionary with the distance as key and the personal best
                performance as value.
        """
        all_distances = set(perf.distance for perf in self.perfs)
        output = {
            distance: self.get_personal_best(distance)
            for distance in set(perf.distance for perf in self.perfs)
        }
        return output
