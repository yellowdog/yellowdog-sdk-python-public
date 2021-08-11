from datetime import datetime, timezone, timedelta

import isodate


def iso_format(input: datetime) -> str:
    input_with_tz = input if input.tzinfo else input.astimezone(timezone.utc)
    return input_with_tz.isoformat(timespec='milliseconds').replace("+00:00", "Z")


def iso_parse(input: str) -> datetime:
    output = datetime.fromisoformat(input.replace("Z", "+00:00"))
    return output if output.tzinfo else output.astimezone(timezone.utc)


def iso_timedelta_format(input: timedelta) -> str:
    return isodate.duration_isoformat(input)


def iso_timedelta_parse(input: str) -> timedelta:
    return isodate.parse_duration(input)
