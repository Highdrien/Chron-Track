from pydantic import BaseModel

from typing import Literal

GENDERS_TYPE = Literal["female", "male"]
EVENT_TYPE = Literal['100m', '200m', '300m', '400m', '500m', '110mH', '400mH', '4x100m', '4x200m', '4x400m', '600m', '800m', '1000m', '1500m', 'Mile', '2000m', '2000mSC', '3000m', '3000mSC', '2 Miles', '5000m', '10,000m', '5km', '10km', '15km', '10 Miles', '20km', 'HM', '25km', '30km', 'Marathon', '100km', '3kmW', '5kmW', '10kmW', '15kmW', '20kmW', '30kmW', '35kmW', '50kmW', '3000mW', '5000mW', '10,000mW', '15,000mW', '20,000mW', '30,000mW', '35,000mW', '50,000mW', 'HJ', 'PV', 'LJ', 'TJ', 'SP', 'DT', 'HT', 'JT', 'Decathlon']


class TIME(BaseModel):
    hours: int
    minutes: int
    seconds: float

    def __repr__(self) -> str:
        return f"{self.hours}h{self.minutes}min{self.seconds:.2f}s"
    
    def get_seconds(self) -> float:
        return self.hours * 3600 + self.minutes * 60 + self.seconds
    

class COEFFS(BaseModel):
    a: float
    b: float
    c: float

    def get_iaaf_score(self, time: TIME) -> int:
        performance = time.get_seconds()
        points = round(self.a * performance**2 + self.b * performance + self.c)
        if points < 0:
            return 0
        if points > 1400:
            # if calculate_performance(self, 1400) < performance:
            #     return 0
            return 1400
        return points

class IAAFMODEL_GENDER(BaseModel):
    model : dict[EVENT_TYPE, COEFFS]

    def get_coeffs(self, event: EVENT_TYPE) -> COEFFS:
        if event not in self.model:
            raise ValueError(f"{event} not found in model: {self.model.keys()}")
        return self.model[event]

class IAAFMODEL(BaseModel):
    female: IAAFMODEL_GENDER
    male: IAAFMODEL_GENDER

    def __repr__(self):
        return f"IAAFMODEL(\n{self.female}\n{self.male}\n)"