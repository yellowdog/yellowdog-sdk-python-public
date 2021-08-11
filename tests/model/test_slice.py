from yellowdog_client.model import Task
from yellowdog_client.model import Slice
from .test_utils import should_serde


def test_serialize_populated(task_raw, task_dict):
    obj_in_raw = Slice(
        items=[task_raw, task_raw],
        nextSliceId="example"
    )

    obj_in_dict = {
        "items": [task_dict, task_dict],
        "nextSliceId": "example"
    }

    should_serde(obj_in_raw, obj_in_dict, Slice[Task])
