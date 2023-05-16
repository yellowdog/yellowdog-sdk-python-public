import pytest

from util.api import MockApi, HttpMethod
from util.data import make, make_string
from yellowdog_client import PlatformClient
from yellowdog_client.compute import ComputeClient
from yellowdog_client.model import ServicesSchema, ApiKey, ComputeRequirement, SingleSourceProvisionStrategy, \
    SimulatorComputeSource, \
    ComputeRequirementStatus, ComputeRequirementSearch, SortDirection, Slice, Instance, SimulatorInstance, \
    InstanceSearch, InstanceId


@pytest.fixture
def compute_client(mock_api: MockApi) -> ComputeClient:
    platform_client = PlatformClient.create(
        ServicesSchema(defaultUrl=mock_api.url()),
        make(ApiKey)
    )
    return platform_client.compute_client


def test_can_stop_compute_requirement(mock_api: MockApi, compute_client: ComputeClient):
    compute_requirement = _make_compute_requirement()
    compute_requirement.status = ComputeRequirementStatus.STOPPED

    expected = mock_api.mock(
        f"/compute/requirements/{compute_requirement.id}/transition/{ComputeRequirementStatus.STOPPED}",
        HttpMethod.PUT,
        response=compute_requirement
    )

    actual = compute_client.stop_compute_requirement(compute_requirement)

    assert actual == expected
    mock_api.verify_all_requests_called()


def test_can_search_compute_requirements(mock_api, compute_client: ComputeClient):
    compute_requirement = _make_compute_requirement()
    compute_requirement.tag = make_string()
    compute_requirement.status = ComputeRequirementStatus.RUNNING

    expected = mock_api.mock(
        "/compute/requirements",
        HttpMethod.GET,
        params={
            "sortField": "name",
            "sortDirection": SortDirection.ASCENDING,
            "namespace": compute_requirement.namespace,
            "tag": compute_requirement.tag,
            "statuses": [compute_requirement.status]
        },
        response=Slice(items=[compute_requirement])
    )

    actual = compute_client.get_compute_requirements(ComputeRequirementSearch(
        sortField="name",
        sortDirection=SortDirection.ASCENDING,
        namespace=compute_requirement.namespace,
        tag=compute_requirement.tag,
        statuses=[compute_requirement.status]
    )).list_all()

    assert actual == expected.items
    mock_api.verify_all_requests_called()


def test_can_search_instances(mock_api, compute_client: ComputeClient):
    instance = _make_instance()

    expected = mock_api.mock(
        "/compute/instances",
        HttpMethod.GET,
        response=Slice(items=[instance])
    )

    actual = compute_client.get_instances(InstanceSearch()).list_all()

    assert actual == expected.items
    mock_api.verify_all_requests_called()


def _make_compute_requirement() -> ComputeRequirement:
    compute_requirement = ComputeRequirement(
        name=make_string(),
        namespace=make_string(),
        provisionStrategy=SingleSourceProvisionStrategy(
            sources=[
                SimulatorComputeSource(
                    name=make_string()
                )
            ]
        )
    )
    compute_requirement.id = make_string()
    return compute_requirement


def _make_instance() -> Instance:
    instance = SimulatorInstance()
    instance.id = InstanceId(
        instanceId=make_string(),
        sourceId=make_string()
    )
    return instance
