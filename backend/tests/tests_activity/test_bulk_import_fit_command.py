from __future__ import annotations

import shutil
from pathlib import Path

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError

from activity.models import Activity

User = get_user_model()

FIXTURES_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data"
SEMI_FIT = FIXTURES_DIR / "semi" / "Semi_marathon_1h25min22s_.fit"


def _write_csv(path: Path, rows: list[str]) -> None:
    header = (
        "ID de l'activité,Date de l'activité,Nom de l'activité,"
        "Type d'activité,Nom du fichier"
    )
    path.write_text(header + "\n" + "\n".join(rows), encoding="utf-8")


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="bulk_runner",
        password="testpass123",
        email="bulk_runner@test.com",
    )


@pytest.fixture
def strava_export(tmp_path) -> Path:
    """Simulate a Strava export directory with activities.csv + activities/."""
    if not SEMI_FIT.exists():
        pytest.skip(f"FIT fixture not found: {SEMI_FIT}")

    activities_dir = tmp_path / "activities"
    activities_dir.mkdir()
    shutil.copy(SEMI_FIT, activities_dir / "123.fit")
    shutil.copy(SEMI_FIT, activities_dir / "456.fit")

    _write_csv(
        tmp_path / "activities.csv",
        [
            "1,2025-03-09,Mon super semi,Course à pied,activities/123.fit",
            "2,2025-03-10,Natation tranquille,Natation,activities/456.fit",
        ],
    )
    return tmp_path


class TestBulkImportFitCommand:
    def test_imports_running_from_csv(self, user, strava_export):
        call_command("bulk_import_fit", str(strava_export), str(user.pk))

        assert Activity.objects.count() == 1
        activity = Activity.objects.first()
        assert activity.name == "Mon super semi"

    def test_skips_non_running(self, user, strava_export):
        call_command("bulk_import_fit", str(strava_export), str(user.pk))

        names = list(Activity.objects.values_list("name", flat=True))
        assert "Natation tranquille" not in names

    def test_duplicate_import_skips(self, user, strava_export):
        call_command("bulk_import_fit", str(strava_export), str(user.pk))
        call_command("bulk_import_fit", str(strava_export), str(user.pk))

        assert Activity.objects.count() == 1

    def test_missing_csv_raises(self, user, tmp_path):
        with pytest.raises(CommandError, match="activities.csv not found"):
            call_command("bulk_import_fit", str(tmp_path), str(user.pk))

    def test_nonexistent_user(self, db, strava_export):
        with pytest.raises(CommandError, match="User not found"):
            call_command(
                "bulk_import_fit",
                str(strava_export),
                "00000000-0000-0000-0000-000000000000",
            )

    def test_missing_fit_file_reported(self, user, tmp_path):
        _write_csv(
            tmp_path / "activities.csv",
            ["1,2025-03-09,Ghost run,Course à pied,activities/missing.fit"],
        )
        call_command("bulk_import_fit", str(tmp_path), str(user.pk))

        assert Activity.objects.count() == 0

    def test_empty_csv_no_running(self, user, tmp_path):
        _write_csv(
            tmp_path / "activities.csv",
            ["1,2025-03-09,Swim,Natation,activities/1.fit"],
        )
        call_command("bulk_import_fit", str(tmp_path), str(user.pk))

        assert Activity.objects.count() == 0
