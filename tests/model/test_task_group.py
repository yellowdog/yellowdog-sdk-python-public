from yellowdog_client.model.task_summary import TaskSummary

from .test_utils import should_serde, should_deserialize
from yellowdog_client.model import TaskGroup, RunSpecification, TaskStatus


def test_serialize_empty():
    obj_in_raw = TaskGroup(
        name="my_name",
        tag="my_tag",
        runSpecification=RunSpecification(taskTypes=[]),
        priority=0,
        dependentOn="my_dependent_on"
    )
    obj_in_raw.taskSummary = TaskSummary()
    obj_in_raw.taskSummary.statusCounts = {
        TaskStatus.FAILED: 0,
        TaskStatus.RUNNING: 0,
        TaskStatus.DISCARDED: 0,
        TaskStatus.UPLOADING: 0,
        TaskStatus.COMPLETED: 0,
        TaskStatus.PENDING: 0,
        TaskStatus.CANCELLED: 0,
        TaskStatus.DOWNLOADING: 0,
        TaskStatus.ALLOCATED: 0
    }

    obj_in_dict = {
        "name": "my_name",
        "tag": "my_tag",
        'runSpecification': {
            'idealQueueConcurrency': 0,
            'minimumQueueConcurrency': 0,
            'shareWorkers': False,
            'taskTypes': [],
            'instanceTypes': None,
            'workerClaimBehaviour': 'STARTUP_ONLY',
            'workerReleaseBehaviour': 'NO_PENDING_TASKS'
        },
        "priority": 0,
        "dependentOn": "my_dependent_on",
        "taskSummary": {
            'statusCounts': {
                'FAILED': 0,
                'RUNNING': 0,
                'DISCARDED': 0,
                'UPLOADING': 0,
                'COMPLETED': 0,
                'PENDING': 0,
                'CANCELLED': 0,
                'DOWNLOADING': 0,
                'ALLOCATED': 0
            },
            'lastUpdatedTime': None
        }

    }

    should_deserialize(obj_in_raw, obj_in_dict)


def test_serialize_populated(task_group_raw, task_group_dict):
    should_serde(task_group_raw, task_group_dict)
