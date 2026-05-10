from __future__ import annotations

from pathlib import Path

import pytest

from activity.parser.strava_csv import parse_strava_csv

FIXTURES_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data"
STRAVA_CSV = FIXTURES_DIR / "activities.csv"


@pytest.fixture
def csv_path() -> Path:
    if not STRAVA_CSV.exists():
        pytest.skip(f"CSV fixture not found: {STRAVA_CSV}")
    return STRAVA_CSV


class TestParseStravaCsv:
    def test_returns_only_running(self, csv_path):
        entries = parse_strava_csv(csv_path)

        assert len(entries) > 0
        for entry in entries:
            assert entry.activity_type == "Course à pied"

    def test_entries_have_names(self, csv_path):
        entries = parse_strava_csv(csv_path)

        for entry in entries:
            assert entry.activity_name != ""

    def test_entries_have_fit_filenames(self, csv_path):
        entries = parse_strava_csv(csv_path)

        for entry in entries:
            assert entry.filename.endswith(".fit") or entry.filename.endswith(".fit.gz")

    def test_excludes_non_running(self, csv_path):
        entries = parse_strava_csv(csv_path)
        names = {e.activity_name for e in entries}

        assert "Reprise de la nat (ca fait 6mois mdr 😂)" not in names
        assert "Au bord des canaux" not in names

    def test_includes_running(self, csv_path):
        entries = parse_strava_csv(csv_path)
        names = {e.activity_name for e in entries}

        assert "Entre les gouttes 🐸" in names
        assert "La spécial VMA" in names

    def test_nonexistent_csv_raises(self):
        with pytest.raises(FileNotFoundError):
            parse_strava_csv("/nonexistent/activities.csv")

    def test_custom_csv_filters_correctly(self, tmp_path):
        csv_content = (
            "ID de l'activité,Date de l'activité,Nom de l'activité,"
            "Type d'activité,Nom du fichier\n"
            "1,2025-01-01,Morning Run,Course à pied,activities/1.fit.gz\n"
            "2,2025-01-02,Swim,Natation,activities/2.fit.gz\n"
            "3,2025-01-03,Trail run,Course à pied,activities/3.fit\n"
            "4,2025-01-04,Walk,Marche,activities/4.fit.gz\n"
            "5,2025-01-05,No file,Course à pied,\n"
        )
        csv_file = tmp_path / "activities.csv"
        csv_file.write_text(csv_content, encoding="utf-8")

        entries = parse_strava_csv(csv_file)

        assert len(entries) == 2
        assert entries[0].activity_name == "Morning Run"
        assert entries[0].filename == "activities/1.fit.gz"
        assert entries[1].activity_name == "Trail run"
        assert entries[1].filename == "activities/3.fit"
