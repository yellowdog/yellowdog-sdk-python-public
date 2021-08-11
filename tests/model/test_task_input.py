from yellowdog_client.model import TaskInput
from yellowdog_client.model import TaskInputSource
from .test_utils import should_serde


def test_serialize_populated():
    obj_in_raw = TaskInput(
        source=TaskInputSource.OTHER_NAMESPACE,
        namespace="my_namespace",
        objectNamePattern="my_objectNamePattern"
    )

    obj_in_dict = {
        "source": "OTHER_NAMESPACE",
        "namespace": "my_namespace",
        "objectNamePattern": "my_objectNamePattern"
    }

    should_serde(obj_in_raw, obj_in_dict)
