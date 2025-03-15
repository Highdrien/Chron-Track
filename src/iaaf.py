import json
from pathlib import Path

from type import IAAFMODEL, GENDERS_TYPE, EVENT_TYPE, TIME, COEFFS


class IAAFCalculator:
    def __init__(self, data_path: Path = Path("data")) -> None:
        self.filepath = data_path / "iaaf_scoring_formulas.json"
        if not self.filepath.exists():
            raise FileNotFoundError(
                f"IAAF scoring formulas not found at {self.filepath}"
            )
        self.models = IAAFMODEL(**json.loads(open(self.filepath).read()))
        print(self.models)
    
    def get_iaaf_score(self, gender: GENDERS_TYPE, event: EVENT_TYPE, time: TIME) -> int:
        coeffs = self._load_coefficients(gender, event)
        return coeffs.get_iaaf_score(time)

    
    def _load_coefficients(self, gender: GENDERS_TYPE, event: str) -> COEFFS:
        if gender == "female":
            return self.models.female.get_coeffs(event)
        elif gender == "male":
            return self.models.male.get_coeffs(event)
        else:
            raise ValueError(f"Invalid gender: {gender}")


if __name__ == "__main__":
    iaaf = IAAFCalculator()
    
