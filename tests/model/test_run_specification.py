from yellowdog_client.model import RunSpecification
from .test_utils import should_serde, should_deserialize


def test_deserialize_empty():
    obj_in_raw = RunSpecification(
        taskTypes=[]
    )

    obj_in_dict = {
        'idealQueueConcurrency': 0,
        'minimumQueueConcurrency': 0,
        'shareWorkers': False,
        'taskTypes': [],
        'instanceTypes': None,
        "workerClaimBehaviour": "STARTUP_ONLY",
        "workerReleaseBehaviour": "NO_PENDING_TASKS"
    }

    should_deserialize(obj_in_raw, obj_in_dict)


def test_serialize__populated(run_specification_raw, run_specification_dict):
    should_serde(run_specification_raw, run_specification_dict)
