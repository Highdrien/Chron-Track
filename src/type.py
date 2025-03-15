from enum import Enum

from pydantic import BaseModel, RootModel


class Gender(str, Enum):
    male = "male"
    female = "female"


class Event(str, Enum):
    e100m = "100m"
    e200m = "200m"
    e300m = "300m"
    e400m = "400m"
    e500m = "500m"
    e100mH = "100mH"
    e110mH = "110mH"
    e400mH = "400mH"
    e4x100m = "4x100m"
    e4x200m = "4x200m"
    e4x400m = "4x400m"
    e600m = "600m"
    e800m = "800m"
    e1000m = "1000m"
    e1500m = "1500m"
    eMile = "Mile"
    e2000m = "2000m"
    e2000mSC = "2000mSC"
    e3000m = "3000m"
    e3000mSC = "3000mSC"
    e2Miles = "2 Miles"
    e5000m = "5000m"
    e10000m = "10,000m"
    e5km = "5km"
    e10km = "10km"
    e15km = "15km"
    e10Miles = "10 Miles"
    e20km = "20km"
    eHM = "HM"
    e25km = "25km"
    e30km = "30km"
    eMarathon = "Marathon"
    e100km = "100km"
    e3kmW = "3kmW"
    e5kmW = "5kmW"
    e10kmW = "10kmW"
    e15kmW = "15kmW"
    e20kmW = "20kmW"
    e30kmW = "30kmW"
    e35kmW = "35kmW"
    e50kmW = "50kmW"
    e3000mW = "3000mW"
    e5000mW = "5000mW"
    e10000mW = "10,000mW"
    e15000mW = "15,000mW"
    e20000mW = "20,000mW"
    e30000mW = "30,000mW"
    e35000mW = "35,000mW"
    e50000mW = "50,000mW"
    eHJ = "HJ"
    ePV = "PV"
    eLJ = "LJ"
    eTJ = "TJ"
    eSP = "SP"
    eDT = "DT"
    eHT = "HT"
    eJT = "JT"
    eHeptathlon = "Heptathlon"
    eDecathlon = "Decathlon"


class Time(BaseModel):
    hours: int
    minutes: int
    seconds: float

    def __repr__(self) -> str:
        return f"{self.hours}h{self.minutes}min{self.seconds:.2f}s"

    def get_seconds(self) -> float:
        """Convert time to seconds"""
        return self.hours * 3600 + self.minutes * 60 + self.seconds


class Coeff(RootModel[tuple[float, float, float]]):
    """Coefficients for IAAF scoring formula"""

    pass

    def get_iaaf_score(self, time: Time) -> int:
        """
        Calculate the IAAF score based on the given performance time.

        Args:
            time (Time): The Time of the performance.

        Returns:
            int: The IAAF score calculated based on the performance time. The score is
                capped at 1400 and a minimum of 0.
        """
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


class IaafModel(RootModel[dict[Gender, dict[Event, Coeff]]]):
    """IAAF scoring model"""

    pass

    def get_coeffs(self, gender: Gender, event: Event) -> Coeff:
        """
        Retrieve the coefficients for a given gender and event.

        Args:
            gender (Gender): The gender for which to retrieve coefficients.
            event (Event): The event for which to retrieve coefficients.

        Returns:
            Coeff: The coefficients associated with the specified gender and event.

        Raises:
            ValueError: If the specified gender is not found.
            ValueError: If the specified event is not found.
        """
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
