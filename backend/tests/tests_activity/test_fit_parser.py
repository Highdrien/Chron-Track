from __future__ import annotations

import gzip
import shutil
from datetime import timedelta
from decimal import Decimal
from pathlib import Path

import pytest

from activity.parser import parse_fit

FIXTURES_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data" / "semi"
SEMI_FIT = FIXTURES_DIR / "Semi_marathon_1h25min22s_.fit"


@pytest.fixture
def semi_fit_path() -> Path:
    if not SEMI_FIT.exists():
        pytest.skip(f"FIT fixture not found: {SEMI_FIT}")
    return SEMI_FIT


@pytest.fixture
def semi_fit_gz(semi_fit_path: Path, tmp_path: Path) -> Path:
    gz_path = tmp_path / "semi.fit.gz"
    with open(semi_fit_path, "rb") as f_in, gzip.open(gz_path, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    return gz_path


class TestParseFit:
    def test_parse_returns_activity_data(self, semi_fit_path: Path):
        result = parse_fit(semi_fit_path)

        assert "Semi-marathon" in result.name
        assert "1h25" in result.name
        assert result.sport_type == "running"
        assert result.distance > Decimal("21000")
        assert result.duration > timedelta(hours=1)
        assert result.start_time is not None

    def test_parse_session_fields(self, semi_fit_path: Path):
        result = parse_fit(semi_fit_path)

        assert result.avg_hr == 166
        assert result.max_hr == 184
        assert result.avg_cadence == 87
        assert result.calories == 1160
        assert result.elevation_gain == Decimal("98")
        assert result.elevation_loss == Decimal("93")

    def test_parse_external_id(self, semi_fit_path: Path):
        result = parse_fit(semi_fit_path)

        assert result.external_id is not None
        assert result.external_id.startswith("fit_")
        assert "3467968002" in result.external_id

    def test_parse_laps(self, semi_fit_path: Path):
        result = parse_fit(semi_fit_path)

        assert len(result.laps) == 22
        assert result.laps[0].lap_number == 1
        assert result.laps[0].distance == Decimal("1000.00")
        assert result.laps[0].avg_hr == 130
        assert result.laps[0].max_hr == 149
        assert result.laps[0].elevation_gain == Decimal("4")

    def test_laps_numbering_is_sequential(self, semi_fit_path: Path):
        result = parse_fit(semi_fit_path)
        numbers = [lap.lap_number for lap in result.laps]
        assert numbers == list(range(1, 23))

    def test_parse_gz_file(self, semi_fit_gz: Path):
        result = parse_fit(semi_fit_gz)

        assert "Semi-marathon" in result.name
        assert result.distance > Decimal("21000")
        assert len(result.laps) == 22

    def test_parse_binary_stream(self, semi_fit_path: Path):
        with open(semi_fit_path, "rb") as f:
            result = parse_fit(f)

        assert "Semi-marathon" in result.name
        assert result.distance > Decimal("21000")

    def test_parse_nonexistent_file_raises(self):
        with pytest.raises(FileNotFoundError):
            parse_fit("/nonexistent/file.fit")

    def test_last_lap_is_remainder(self, semi_fit_path: Path):
        """The last lap of a semi-marathon is less than 1km (~97.5m)."""
        result = parse_fit(semi_fit_path)
        last_lap = result.laps[-1]
        assert last_lap.distance < Decimal("1000")

    def test_total_distance_matches_sum_of_laps(self, semi_fit_path: Path):
        result = parse_fit(semi_fit_path)
        total_from_laps = sum(lap.distance for lap in result.laps)
        assert abs(result.distance - total_from_laps) < Decimal("50")
