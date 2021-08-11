from .test_utils import should_serde
from yellowdog_client.model import Task
from yellowdog_client.model import FlattenPath


def test_serialize_empty():
    obj_in_raw = Task(
        name="my_name",
        tag="my_tag",
        taskType="my_task_type",
        taskData="my_data",
        flattenInputPaths=FlattenPath.REPLACE_PATH_SEPERATOR,
    )

    obj_in_dict = {
        'retryCount': 0,
        "name": "my_name",
        "tag": "my_tag",
        "taskType": "my_task_type",
        "taskData": "my_data",
        "flattenInputPaths": "REPLACE_PATH_SEPERATOR",
    }

    should_serde(obj_in_raw, obj_in_dict)


def test_serialize_populated(task_raw, task_dict):
    should_serde(task_raw, task_dict)
