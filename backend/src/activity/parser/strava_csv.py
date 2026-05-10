from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass
class StravaCsvEntry:
    activity_name: str
    activity_type: str
    filename: str


RUNNING_TYPES = {"Course à pied"}


def parse_strava_csv(csv_path: str | Path) -> list[StravaCsvEntry]:
    """Parse a Strava activities.csv and return running entries with a FIT file.

    Filters out:
    - Activities that are not "Course à pied"
    - Activities with no filename
    - Activities whose filename is not a .fit or .fit.gz
    """
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    entries: list[StravaCsvEntry] = []
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            activity_type = row.get("Type d'activité", "").strip()
            if activity_type not in RUNNING_TYPES:
                continue

            filename = row.get("Nom du fichier", "").strip()
            if not filename:
                continue

            if not (filename.endswith(".fit") or filename.endswith(".fit.gz")):
                continue

            name = row.get("Nom de l'activité", "").strip()
            entries.append(
                StravaCsvEntry(
                    activity_name=name,
                    activity_type=activity_type,
                    filename=filename,
                )
            )

    return entries
