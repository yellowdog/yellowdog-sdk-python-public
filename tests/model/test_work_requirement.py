from yellowdog_client.model import WorkRequirement
from .test_utils import should_serde


def test_serialize_empty():
    obj_in_raw = WorkRequirement(
        namespace="my_namespace",
        name="my_name",
        tag="my_tag",
        taskGroups=[],
        priority=0
    )

    obj_in_dict = {
        'fulfilOnSubmit': False,
        "namespace": "my_namespace",
        "name": "my_name",
        "tag": "my_tag",
        "taskGroups": [],
        "priority": 0
    }

    should_serde(obj_in_raw, obj_in_dict)


def test_serialize_populated(work_requirement_raw, work_requirement_dict):
    should_serde(work_requirement_raw, work_requirement_dict)
