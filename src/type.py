from typing import Literal

from pydantic import BaseModel, RootModel

GENDERS_TYPE = Literal["female", "male"]
EVENT_TYPE = Literal[
    "100m",
    "200m",
    "300m",
    "400m",
    "500m",
    "110mH",
    "400mH",
    "4x100m",
    "4x200m",
    "4x400m",
    "600m",
    "800m",
    "1000m",
    "1500m",
    "Mile",
    "2000m",
    "2000mSC",
    "3000m",
    "3000mSC",
    "2 Miles",
    "5000m",
    "10,000m",
    "5km",
    "10km",
    "15km",
    "10 Miles",
    "20km",
    "HM",
    "25km",
    "30km",
    "Marathon",
    "100km",
    "3kmW",
    "5kmW",
    "10kmW",
    "15kmW",
    "20kmW",
    "30kmW",
    "35kmW",
    "50kmW",
    "3000mW",
    "5000mW",
    "10,000mW",
    "15,000mW",
    "20,000mW",
    "30,000mW",
    "35,000mW",
    "50,000mW",
    "HJ",
    "PV",
    "LJ",
    "TJ",
    "SP",
    "DT",
    "HT",
    "JT",
    "Decathlon",
]


class Time(BaseModel):
    hours: int
    minutes: int
    seconds: float

    def __repr__(self) -> str:
        return f"{self.hours}h{self.minutes}min{self.seconds:.2f}s"

    def get_seconds(self) -> float:
        return self.hours * 3600 + self.minutes * 60 + self.seconds


class Coeff(RootModel[tuple[float, float, float]]):
    pass

    def get_iaaf_score(self, time: Time) -> int:
        performance = time.get_seconds()
        a, b, c = self.root
        points = round(a * performance**2 + b * performance + c)
        if points < 0:
            return 0
        if points > 1400:
            # if calculate_performance(self, 1400) < performance:
            #     return 0
            return 1400
        return points


class IaafModel(RootModel[dict[str, dict[str, Coeff]]]):
    pass

    def get_coeffs(self, gender: GENDERS_TYPE, event: EVENT_TYPE) -> Coeff:
        if gender not in self.root:
            raise ValueError(
                f"{gender=} not found. Genders available: {list(self.root.keys())}"
            )

        if event not in self.root[gender]:
            raise ValueError(
                f"{event=} not found in model[{gender}]. "
                f"Events available: {list(self.root[gender].keys())}"
            )
        return self.root[gender][event]
