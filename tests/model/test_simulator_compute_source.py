from yellowdog_client.model import SimulatorComputeSource
from yellowdog_client.model import ComputeSourceStatus
from .test_utils import should_serde


def test_serialize__simulator_compute_source():
    obj_in_raw = SimulatorComputeSource(
        name="simulator_name",
        limit=10,
        instanceStartupTimeSeconds=20,
        instanceStartupTimeVariance=30.0,
        instanceShutdownTimeSeconds=40,
        instanceShutdownTimeVariance=50.0,
        unexpectedInstanceTerminationProbabilityPerSecond=60.0
    )
    obj_in_raw.status = ComputeSourceStatus.UPDATING
    obj_in_raw.statusMessage = "simulator_statusMessage"
    obj_in_raw.id = "simulator_id"

    obj_in_dict = {
        "status": "UPDATING",
        "type": "co.yellowdog.platform.model.SimulatorComputeSource",
        "name": "simulator_name",
        "limit": 10,
        "instanceStartupTimeSeconds": 20,
        "instanceStartupTimeVariance": 30.0,
        "instanceShutdownTimeSeconds": 40,
        "instanceShutdownTimeVariance": 50.0,
        "unexpectedInstanceTerminationProbabilityPerSecond": 60.0,
        "region": "sim-region",
        "instanceType": "sim-instance",
        "imageId": "sim-image",
        "statusMessage": "simulator_statusMessage",
        "id": "simulator_id"
    }

    should_serde(obj_in_raw, obj_in_dict)
