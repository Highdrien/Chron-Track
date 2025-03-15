import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.iaaf import IAAFCalculator
import json

class TestIAAFCalculator:
    def setup_method(self):
        self.iaaf = IAAFCalculator()
        self.scoring_table: dict[str, dict[str, list[float]]] = json.loads(open(self.iaaf.filepath).read())
    
    # def test_get_score(self):
    #     pass

    def test_load_coefficients(self):
        coeff = self.iaaf._load_coefficients("male", "100m")
        expected_score = self.scoring_table["male"]["100m"]
        assert coeff.a == expected_score[0]
        assert coeff.b == expected_score[1]
        assert coeff.c == expected_score[2]
        