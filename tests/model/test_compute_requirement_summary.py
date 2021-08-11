from datetime import datetime, timezone

from .test_utils import should_serde
from yellowdog_client.common.iso_datetime import iso_format
from yellowdog_client.model import ComputeRequirementSummary
from yellowdog_client.model import ComputeRequirementStatus


def test_serialize__compute_requirement_summary():
    obj_in_raw = ComputeRequirementSummary()
    obj_in_raw.id = "req_id"
    obj_in_raw.namespace = "req_namespace"
    obj_in_raw.name = "req_name"
    obj_in_raw.tag = "req_tag"
    obj_in_raw.status = ComputeRequirementStatus.RUNNING
    obj_in_raw.aliveInstanceCount = 100
    obj_in_raw.hasErroredSource = True
    obj_in_raw.createdTime = datetime(2010, 12, 31, 18, 30, 45, 123000, timezone.utc)

    obj_in_dict = {
        'id': 'req_id',
        'namespace': 'req_namespace',
        'name': 'req_name',
        'tag': 'req_tag',
        'status': 'RUNNING',
        'aliveInstanceCount': 100,
        'hasErroredSource': True,
        "createdTime": iso_format(datetime(2010, 12, 31, 18, 30, 45, 123456))
    }

    should_serde(obj_in_raw, obj_in_dict)
