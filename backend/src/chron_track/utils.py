import sys
from typing import Literal


def determine_mode() -> Literal[
    "testing", "collecting_static", "development", "production"
]:
    """Determine the mode of the application."""
    if "test" in sys.argv or "pytest" in sys.modules:
        return "testing"
    if "collectstatic" in sys.argv:
        return "collecting_static"
    if "runserver" in sys.argv:
        return "development"
    return "production"
