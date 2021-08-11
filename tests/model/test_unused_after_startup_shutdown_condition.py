from datetime import timedelta

from yellowdog_client.model import UnusedAfterStartupShutdownCondition
from .test_utils import should_serde


def test_serialize_timedelta_30_minutes_15_seconds():
    obj_in_raw = UnusedAfterStartupShutdownCondition(
        delay=timedelta(minutes=30, seconds=15)
    )

    obj_in_dict = {
        "delay": "PT30M15S",
        "type": "co.yellowdog.platform.model.UnusedAfterStartupShutdownCondition",
    }
    should_serde(obj_in_raw, obj_in_dict)
