from yellowdog_client.model import WaterfallProvisionStrategy
from yellowdog_client.model import SimulatorComputeSource
from yellowdog_client.model import ComputeSourceStatus
from .test_utils import should_serde


def test_serialize__split_provision_strategy():
    compute_source_simulator = SimulatorComputeSource(
        name="simulator_name",
        limit=20,
        instanceStartupTimeSeconds=30,
        instanceStartupTimeVariance=40.0,
        instanceShutdownTimeSeconds=50,
        instanceShutdownTimeVariance=60.0,
        unexpectedInstanceTerminationProbabilityPerSecond=70.0
    )
    compute_source_simulator.id = "simulator_id"
    compute_source_simulator.status = ComputeSourceStatus.ERRORED
    compute_source_simulator.statusMessage = "simulator_message"

    obj_in_raw = WaterfallProvisionStrategy(
        sources=[compute_source_simulator]
    )

    obj_in_dict = {
        "sources": [
            {
                "status": "ERRORED",
                "type": "co.yellowdog.platform.model.SimulatorComputeSource",
                "name": "simulator_name",
                "limit": 20,
                "instanceStartupTimeSeconds": 30,
                "instanceStartupTimeVariance": 40.0,
                "instanceShutdownTimeSeconds": 50,
                "instanceShutdownTimeVariance": 60.0,
                "unexpectedInstanceTerminationProbabilityPerSecond": 70.0,
                "region": "sim-region",
                "instanceType": "sim-instance",
                "imageId": "sim-image",
                "id": "simulator_id",
                "statusMessage": "simulator_message"
            },
        ],
        "type": "co.yellowdog.platform.model.WaterfallProvisionStrategy"
    }
    should_serde(obj_in_raw, obj_in_dict)
