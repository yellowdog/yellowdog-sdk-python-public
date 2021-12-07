from datetime import timedelta

from yellowdog_client.model import AllWorkersReleasedShutdownCondition
from .test_utils import should_serde


def test_serialize_timedelta_0():
    obj_in_raw = AllWorkersReleasedShutdownCondition(delay=timedelta())
    obj_in_dict = {
        "delay": "P0D",
        "type": "co.yellowdog.platform.model.AllWorkersReleasedShutdownCondition",
    }
    should_serde(obj_in_raw, obj_in_dict)


def test_serialize_timedelta_30_minutes_15_seconds():
    obj_in_raw = AllWorkersReleasedShutdownCondition(delay=timedelta(minutes=30, seconds=15))

    obj_in_dict = {
        "delay": "PT30M15S",
        "type": "co.yellowdog.platform.model.AllWorkersReleasedShutdownCondition",
    }
    should_serde(obj_in_raw, obj_in_dict)
