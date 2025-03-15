import json
from pathlib import Path

from .basic_class import Event, Gender, IaafModel, Time


class IAAFCalculator:
    def __init__(self, data_path: Path = Path("data")) -> None:
        """
        Initializes the IAAF scoring formulas.

        Args:
            data_path (Path, optional): The path to the directory containing the IAAF
                scoring formulas JSON file. Defaults to "data".

        Raises:
            FileNotFoundError: If the IAAF scoring formulas JSON file does not exist at
                the specified path.
        """
        self.filepath = data_path / "iaaf_scoring_formulas.json"
        if not self.filepath.exists():
            raise FileNotFoundError(
                f"IAAF scoring formulas not found at {self.filepath}"
            )
        self.model = IaafModel.model_validate(json.loads(open(self.filepath).read()))

    def get_iaaf_score(self, gender: Gender, event: Event, time: Time) -> int:
        """
        Calculate the IAAF score for a given gender, event, and time.

        Args:
            gender (Gender): The gender of the athlete.
            event (Event): The event for which the score is being calculated.
            time (Time): The performance time of the athlete.

        Returns:
            int: The calculated IAAF score.
        """
        coeffs = self.model.get_coeffs(gender, event)
        return coeffs.get_iaaf_score(time)
