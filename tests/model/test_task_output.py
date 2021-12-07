from yellowdog_client.model import TaskOutput
from yellowdog_client.model import TaskOutputSource
from .test_utils import should_serde


def test_serialize_populated():
    obj_in_raw = TaskOutput(
        source=TaskOutputSource.PROCESS_OUTPUT,
        directoryName="my_directoryName",
        filePattern="my_filePattern",
        uploadOnFailed=True
    )

    obj_in_dict = {
        "source": "PROCESS_OUTPUT",
        "directoryName": "my_directoryName",
        "filePattern": "my_filePattern",
        "uploadOnFailed": True,
        "required": False
    }

    should_serde(obj_in_raw, obj_in_dict)
