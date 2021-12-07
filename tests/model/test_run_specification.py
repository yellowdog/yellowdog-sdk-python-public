from yellowdog_client.model import RunSpecification
from .test_utils import should_serde, should_deserialize


def test_deserialize_empty():
    obj_in_raw = RunSpecification(
        taskTypes=[]
    )

    obj_in_dict = {
        'taskTypes': [],
        'instanceTypes': None
    }

    should_deserialize(obj_in_raw, obj_in_dict)


def test_serialize__populated(run_specification_raw, run_specification_dict):
    should_serde(run_specification_raw, run_specification_dict)
