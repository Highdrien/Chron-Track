import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
import json

import pytest

from src.iaaf import IAAFCalculator
from src.type import EVENT_TYPE, GENDERS_TYPE, Time


class TestIAAFCalculator:
    def setup_method(self):
        self.iaaf = IAAFCalculator()
        self.scoring_table: dict[str, dict[str, list[float]]] = json.loads(
            open(self.iaaf.filepath).read()
        )

    def test_load_coefficients(self):
        for gender in self.scoring_table:
            for event, coeffs in self.scoring_table[gender].items():
                coeff_type = self.iaaf.model.get_coeffs(gender=gender, event=event)
                assert coeff_type.root == tuple(coeffs)

    @pytest.mark.parametrize(
        "gender, event, time, expected",
        [
            ("male", "100m", Time(hours=0, minutes=0, seconds=10.0), 1206),
            ("female", "100m", Time(hours=0, minutes=0, seconds=10.0), 1400),
            ("male", "HM", Time(hours=1, minutes=0, seconds=0.0), 1186),
            ("female", "HM", Time(hours=1, minutes=0, seconds=0.0), 1345),
            ("male", "Marathon", Time(hours=2, minutes=30, seconds=0.0), 853),
            ("female", "Marathon", Time(hours=2, minutes=30, seconds=0.0), 1133),
        ],
    )
    def test_get_iaaf_score(
        self, gender: GENDERS_TYPE, event: EVENT_TYPE, time: Time, expected: int
    ):
        assert self.iaaf.get_iaaf_score(gender, event, time) == expected
