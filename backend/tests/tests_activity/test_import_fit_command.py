from __future__ import annotations

from pathlib import Path

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError

from activity.models import Activity

User = get_user_model()

FIXTURES_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data" / "semi"
SEMI_FIT = FIXTURES_DIR / "Semi_marathon_1h25min22s_.fit"


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="cmd_runner",
        password="testpass123",
        email="cmd_runner@test.com",
    )


@pytest.fixture
def semi_fit_path() -> Path:
    if not SEMI_FIT.exists():
        pytest.skip(f"FIT fixture not found: {SEMI_FIT}")
    return SEMI_FIT


class TestImportFitCommand:
    def test_import_creates_activity(self, user, semi_fit_path):
        call_command("import_fit", str(semi_fit_path), str(user.pk))

        assert Activity.objects.count() == 1
        activity = Activity.objects.first()
        assert activity.user == user
        assert activity.name == "Course"

    def test_import_duplicate_skips(self, user, semi_fit_path):
        call_command("import_fit", str(semi_fit_path), str(user.pk))
        call_command("import_fit", str(semi_fit_path), str(user.pk))

        assert Activity.objects.count() == 1

    def test_import_nonexistent_file(self, user):
        with pytest.raises(CommandError, match="File not found"):
            call_command("import_fit", "/nonexistent/file.fit", str(user.pk))

    def test_import_nonexistent_user(self, db, semi_fit_path):
        with pytest.raises(CommandError, match="User not found"):
            call_command(
                "import_fit", str(semi_fit_path), "00000000-0000-0000-0000-000000000000"
            )

    def test_import_wrong_format(self, user, tmp_path):
        bad_file = tmp_path / "test.csv"
        bad_file.write_text("not a fit file")

        with pytest.raises(CommandError, match="Unsupported file format"):
            call_command("import_fit", str(bad_file), str(user.pk))
