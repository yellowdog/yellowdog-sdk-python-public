from yellowdog_client.model import NoRegisteredWorkersShutdownCondition
from .test_utils import should_serde


def test_serialize():
    obj_in_raw = NoRegisteredWorkersShutdownCondition()
    obj_in_dict = {
        "type": "co.yellowdog.platform.model.NoRegisteredWorkersShutdownCondition"
    }

    should_serde(obj_in_raw, obj_in_dict)
