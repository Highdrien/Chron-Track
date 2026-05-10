from __future__ import annotations

from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from activity.parser.strava_csv import parse_strava_csv
from activity.services import ActivityAlreadyExists, import_fit_file

User = get_user_model()


class Command(BaseCommand):
    help = (
        "Bulk-import FIT activities from a Strava export. "
        "Reads activities.csv to get titles and filter running activities, "
        "then imports each .fit/.fit.gz file."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "export_dir",
            type=str,
            help="Path to the Strava export directory (containing activities.csv and activities/)",
        )
        parser.add_argument(
            "user_id", type=str, help="User ID (UUID) to assign the activities to"
        )

    def handle(self, *args, **options):
        export_dir = Path(options["export_dir"]).expanduser().resolve()
        user_id = options["user_id"]

        csv_path = export_dir / "activities.csv"
        if not csv_path.exists():
            raise CommandError(f"activities.csv not found in {export_dir}")

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise CommandError(f"User not found: {user_id}")

        entries = parse_strava_csv(csv_path)
        if not entries:
            self.stdout.write(self.style.WARNING("No running activities found in CSV"))
            return

        self.stdout.write(f"Found {len(entries)} running activities in CSV\n")

        imported = 0
        skipped = 0
        missing = 0
        errors = 0

        for entry in entries:
            fit_path = export_dir / entry.filename
            if not fit_path.exists():
                missing += 1
                self.stdout.write(
                    self.style.WARNING(f"  MISS {entry.filename} (file not found)")
                )
                continue

            try:
                activity = import_fit_file(user, fit_path, name=entry.activity_name)
                imported += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"  OK   {entry.activity_name} "
                        f"({activity.start_time:%Y-%m-%d}) "
                        f"{activity.distance_km} km"
                    )
                )
            except ActivityAlreadyExists:
                skipped += 1
                self.stdout.write(
                    self.style.WARNING(
                        f"  SKIP {entry.activity_name} (already imported)"
                    )
                )
            except Exception as e:
                errors += 1
                self.stdout.write(self.style.ERROR(f"  FAIL {entry.filename}: {e}"))

        self.stdout.write(
            f"\nDone: {imported} imported, {skipped} skipped, "
            f"{missing} missing files, {errors} errors "
            f"(total: {len(entries)} running activities in CSV)"
        )
