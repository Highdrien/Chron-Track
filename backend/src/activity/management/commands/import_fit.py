from __future__ import annotations

from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from activity.services import ActivityAlreadyExists, import_fit_file

User = get_user_model()


class Command(BaseCommand):
    help = "Import a .fit or .fit.gz file as an Activity for a given user."

    def add_arguments(self, parser):
        parser.add_argument("path", type=str, help="Path to a .fit or .fit.gz file")
        parser.add_argument(
            "user_id", type=str, help="User ID (UUID) to assign the activity to"
        )

    def handle(self, *args, **options):
        fit_path = Path(options["path"]).expanduser().resolve()
        user_id = options["user_id"]

        if not fit_path.exists():
            raise CommandError(f"File not found: {fit_path}")

        suffix = "".join(fit_path.suffixes).lower()
        if suffix not in (".fit", ".fit.gz"):
            raise CommandError(
                f"Unsupported file format: {suffix}. Expected .fit or .fit.gz"
            )

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise CommandError(f"User not found: {user_id}")

        try:
            activity = import_fit_file(user, fit_path)
        except ActivityAlreadyExists as e:
            self.stdout.write(
                self.style.WARNING(
                    f"Skipped (already imported): {e.activity.name} "
                    f"({e.activity.start_time:%Y-%m-%d %H:%M}) "
                    f"[id={e.activity.pk}]"
                )
            )
            return
        except ValueError as e:
            raise CommandError(f"Invalid FIT file: {e}")

        lap_count = activity.laps.count()
        self.stdout.write(
            self.style.SUCCESS(
                f"Imported: {activity.name}\n"
                f"  Date:      {activity.start_time:%Y-%m-%d %H:%M}\n"
                f"  Distance:  {activity.distance_km} km\n"
                f"  Duration:  {activity.duration}\n"
                f"  Avg HR:    {activity.avg_hr or '-'} bpm\n"
                f"  D+:        {activity.elevation_gain or '-'} m\n"
                f"  Laps:      {lap_count}\n"
                f"  ID:        {activity.pk}"
            )
        )
