from __future__ import annotations

from pathlib import Path

import pytest
from django.contrib.auth import get_user_model

from activity.models import Activity, ActivityLap
from activity.services import ActivityAlreadyExists, import_fit_file

User = get_user_model()

FIXTURES_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data" / "semi"
SEMI_FIT = FIXTURES_DIR / "Semi_marathon_1h25min22s_.fit"


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="runner_activity",
        password="testpass123",
        email="runner_activity@test.com",
    )


@pytest.fixture
def semi_fit_path() -> Path:
    if not SEMI_FIT.exists():
        pytest.skip(f"FIT fixture not found: {SEMI_FIT}")
    return SEMI_FIT


class TestImportFitFile:
    def test_creates_activity(self, user, semi_fit_path):
        activity = import_fit_file(user, semi_fit_path)

        assert activity.pk is not None
        assert activity.user == user
        assert activity.source == "fit"
        assert activity.name == "Course"
        assert activity.sport_type == "running"
        assert activity.distance > 21000
        assert activity.avg_hr == 166

    def test_creates_laps(self, user, semi_fit_path):
        activity = import_fit_file(user, semi_fit_path)

        laps = list(activity.laps.all().order_by("lap_number"))
        assert len(laps) == 22
        assert laps[0].lap_number == 1
        assert laps[0].distance == 1000
        assert laps[0].avg_hr == 130

    def test_duplicate_import_raises(self, user, semi_fit_path):
        import_fit_file(user, semi_fit_path)

        with pytest.raises(ActivityAlreadyExists):
            import_fit_file(user, semi_fit_path)

    def test_duplicate_does_not_create_extra_records(self, user, semi_fit_path):
        import_fit_file(user, semi_fit_path)

        with pytest.raises(ActivityAlreadyExists):
            import_fit_file(user, semi_fit_path)

        assert Activity.objects.count() == 1
        assert ActivityLap.objects.count() == 22

    def test_activity_properties(self, user, semi_fit_path):
        activity = import_fit_file(user, semi_fit_path)

        assert activity.distance_km > 21
        assert activity.pace is not None
        assert activity.speed_kmh is not None
        assert float(activity.speed_kmh) > 14  # ~14.9 km/h for a 1h25 semi

    def test_external_id_set(self, user, semi_fit_path):
        activity = import_fit_file(user, semi_fit_path)

        assert activity.external_id is not None
        assert activity.external_id.startswith("fit_")

    def test_file_not_found(self, user):
        with pytest.raises(FileNotFoundError):
            import_fit_file(user, "/nonexistent/file.fit")
