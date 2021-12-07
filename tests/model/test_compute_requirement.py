from .test_utils import should_serde
from yellowdog_client.model import ComputeRequirement
from yellowdog_client.model import SingleSourceProvisionStrategy
from yellowdog_client.model import SplitProvisionStrategy
from yellowdog_client.model import WaterfallProvisionStrategy


def test_serialize__compute_requirement(populated_compute_requirement, populated_compute_requirement_dict):
    should_serde(populated_compute_requirement, populated_compute_requirement_dict)


def test_serialize_single_source_provision_strategy__compute_requirement():
    expected_object = ComputeRequirement(
        name="test_name",
        namespace="test_namespace",
        provisionStrategy=SingleSourceProvisionStrategy(
            sources=[]
        )
    )

    expected_dict = {
        "name": "test_name",
        "namespace": "test_namespace",
        "maintainInstanceCount": False,
        "provisionStrategy": {
            "sources": [],
            "type": "co.yellowdog.platform.model.SingleSourceProvisionStrategy"
        },
        "targetInstanceCount": 0,
        "expectedInstanceCount": 0
    }
    should_serde(expected_object, expected_dict)


def test_serialize_waterfall_provision_strategy__compute_requirement():
    expected_object = ComputeRequirement(
        name="test_name",
        namespace="test_namespace",
        provisionStrategy=WaterfallProvisionStrategy(
            sources=[]
        )
    )

    expected_dict = {
        "name": "test_name",
        "namespace": "test_namespace",
        "maintainInstanceCount": False,
        "provisionStrategy": {
            "sources": [],
            "type": "co.yellowdog.platform.model.WaterfallProvisionStrategy"
        },
        "targetInstanceCount": 0,
        "expectedInstanceCount": 0
    }
    should_serde(expected_object, expected_dict)


def test_serialize_split_provision_strategy__compute_requirement():
    expected_object = ComputeRequirement(
        name="test_name",
        namespace="test_namespace",
        provisionStrategy=SplitProvisionStrategy(
            sources=[]
        )
    )

    expected_dict = {
        "name": "test_name",
        "namespace": "test_namespace",
        "maintainInstanceCount": False,
        "provisionStrategy": {
            "sources": [],
            "type": "co.yellowdog.platform.model.SplitProvisionStrategy"
        },
        "targetInstanceCount": 0,
        "expectedInstanceCount": 0
    }
    should_serde(expected_object, expected_dict)
