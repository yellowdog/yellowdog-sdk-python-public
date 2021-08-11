from datetime import datetime, timezone

from yellowdog_client.common.iso_datetime import iso_format
from yellowdog_client.model import WorkRequirementSummary
from yellowdog_client.model import WorkRequirementStatus
from .test_utils import should_serde


def test_serialize_populated():
    obj_in_raw = WorkRequirementSummary()
    obj_in_raw.id = "my_id"
    obj_in_raw.namespace = "my_namespace"
    obj_in_raw.name = "my_name"
    obj_in_raw.tag = "my_tag"
    obj_in_raw.status = WorkRequirementStatus.UNFULFILLED
    obj_in_raw.completedTaskCount = 5
    obj_in_raw.totalTaskCount = 10
    obj_in_raw.createdTime = datetime(2014, 12, 31, 18, 30, 45, 123000, timezone.utc)
    obj_in_raw.healthy = True

    obj_in_dict = {
        "id": "my_id",
        "namespace": "my_namespace",
        "name": "my_name",
        "tag": "my_tag",
        'priority': 0.0,
        "status": "UNFULFILLED",
        "completedTaskCount": 5,
        "totalTaskCount": 10,
        "createdTime": iso_format(datetime(2014, 12, 31, 18, 30, 45, 123456)),
        "healthy": True
    }

    should_serde(obj_in_raw, obj_in_dict)
