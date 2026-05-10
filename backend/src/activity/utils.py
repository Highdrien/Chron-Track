from datetime import timedelta


def format_duration(td: timedelta | None) -> str:
    if td is None:
        return "-"
    total = int(td.total_seconds())
    h, remainder = divmod(total, 3600)
    m, s = divmod(remainder, 60)
    if h:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def format_pace(td: timedelta | None) -> str:
    if td is None:
        return "-"
    total = int(td.total_seconds())
    m, s = divmod(total, 60)
    return f"{m}'{s:02d}\"/km"
