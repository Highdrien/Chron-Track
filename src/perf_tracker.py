from pydantic import BaseModel, model_validator
from datetime import datetime
from typing import Optional

from .basic_class import Time, Pace

class Perf(BaseModel):
    time: Time
    distance: int
    date: datetime
    event: Optional[str] = None
    location: Optional[str] = None

    @property
    def pace(self) -> Pace:
        return Pace.from_time_distance(self.time, self.distance)
    
    def __repr__(self) -> str:
        return f"{self.time} for {self.distance}m on {self.date}"
