from pydantic import BaseModel
from typing_extensions import Self


class Time(BaseModel):
    hours: int
    minutes: int
    seconds: float

    def __str__(self) -> str:
        return f"{self.hours}h{self.minutes}min{self.seconds:.2f}s"

    def get_minutes(self) -> float:
        """Convert time to minutes"""
        return self.hours * 60 + self.minutes + self.seconds / 60

    def get_seconds(self) -> float:
        """Convert time to seconds"""
        return self.hours * 3600 + self.minutes * 60 + self.seconds


class Pace(BaseModel):
    minutes: int
    seconds: float

    @classmethod
    def from_time_distance(cls, time: Time, distance: int) -> Self:
        """
        Initialize a Pace object from a Time object and a distance.

        Args:
            time (Time): The Time object representing the performance time.
            distance (int): The distance covered in kilometers.

        Returns:
            Pace: The Pace object calculated from the Time and distance
        """
        pace = time.get_minutes() / distance
        minutes = int(pace)
        secondes = int((pace - minutes) * 60)
        return Pace(minutes=minutes, seconds=secondes)

    @property
    def kmh(self) -> float:
        """Calculate the speed in km/h"""
        return 60 / (self.minutes + self.seconds / 60)

    def __str__(self) -> str:
        pace_str = f"{self.minutes:02d}'{self.seconds:02.0f}"
        speed_str = f"{self.kmh:.2f}"
        return f"Pace: {pace_str} min/km (={speed_str} km/h)"
