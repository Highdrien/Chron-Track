from pydantic import BaseModel
from typing_extensions import Self


class Time(BaseModel):
    hours: int
    minutes: int
    seconds: float

    @classmethod
    def from_total_seconds(cls, total_seconds: float) -> Self:
        """
        Initialize a Time object from a total amount of seconds.

        Args:
            total_seconds (float): The total amount of seconds to convert.

        Returns:
            Time: The Time object calculated from the total amount of seconds.
        """
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = total_seconds % 60
        return Time(hours=hours, minutes=minutes, seconds=seconds)

    @classmethod
    def from_str(cls, time_str: str) -> Self:
        """
        Initialize a Time object from a string.

        Args:
            time_str (str): The string representing the time in the format:
                "<hour>h<min>min<sec>s".

        Returns:
            Time: The Time object calculated from the string.
        """
        time_str = time_str.replace("h", ":").replace("min", ":").replace("s", "")
        hours, minutes, seconds = time_str.split(":")
        return Time(hours=int(hours), minutes=int(minutes), seconds=float(seconds))

    def __str__(self) -> str:
        return f"{self.hours}h{self.minutes}min{self.seconds:.2f}s"

    def get_minutes(self) -> float:
        """Convert time to minutes"""
        return self.hours * 60 + self.minutes + self.seconds / 60

    def get_seconds(self) -> float:
        """Convert time to seconds"""
        return self.hours * 3600 + self.minutes * 60 + self.seconds

    def __lt__(self, other: "Time") -> bool:
        """Less than comparison"""
        return self.get_seconds() < other.get_seconds()

    def __le__(self, other: "Time") -> bool:
        """Less than or equal comparison"""
        return self.get_seconds() <= other.get_seconds()

    def __gt__(self, other: "Time") -> bool:
        """Greater than comparison"""
        return self.get_seconds() > other.get_seconds()

    def __ge__(self, other: "Time") -> bool:
        """Greater than or equal comparison"""
        return self.get_seconds() >= other.get_seconds()

    def __add__(self, other: "Time") -> "Time":
        """Add two Time objects"""
        total_seconds = self.get_seconds() + other.get_seconds()
        return Time.from_total_seconds(total_seconds=total_seconds)

    def __sub__(self, other: "Time") -> "Time":
        """Subtract two Time objects"""
        if self.get_seconds() < other.get_seconds():
            raise ValueError("Cannot subtract a larger time from a smaller time")
        total_seconds = self.get_seconds() - other.get_seconds()
        return Time.from_total_seconds(total_seconds)


class Pace(BaseModel):
    minutes: int
    seconds: float

    @classmethod
    def from_time_distance(cls, time: Time, distance: float) -> Self:
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
