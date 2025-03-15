import json
from pathlib import Path

from type import Event, Gender, IaafModel, Time


class IAAFCalculator:
    def __init__(self, data_path: Path = Path("data")) -> None:
        self.filepath = data_path / "iaaf_scoring_formulas.json"
        if not self.filepath.exists():
            raise FileNotFoundError(
                f"IAAF scoring formulas not found at {self.filepath}"
            )
        self.model = IaafModel.model_validate(json.loads(open(self.filepath).read()))

    def get_iaaf_score(self, gender: Gender, event: Event, time: Time) -> int:
        coeffs = self.model.get_coeffs(gender, event)
        return coeffs.get_iaaf_score(time)
