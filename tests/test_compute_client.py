from typing import List

import pytest
from yellowdog_client import PlatformClient
from yellowdog_client.compute import ComputeClient
from yellowdog_client.model import ServicesSchema, ApiKey, ComputeRequirement, SingleSourceProvisionStrategy, \
    SimulatorComputeSource, \
    ComputeRequirementStatus, ComputeRequirementSearch, SortDirection, Slice, Instance, SimulatorInstance, \
    InstanceSearch, InstanceId, ComputeSourceTemplate, ComputeSource, StringAttributeValue, \
    ComputeRequirementDynamicTemplate, ComputeRequirementTemplateSearch, ComputeRequirementTemplateSummary, \
    ComputeSourceTemplateSummary, ComputeSourceTemplateSearch

from util.api import MockApi, HttpMethod
from util.data import make, make_string


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
            "namespace": compute_requirement.namespace,
            "tag": compute_requirement.tag,
            "statuses": [compute_requirement.status],
            "sortField": "name",
            "sortDirection": SortDirection.ASCENDING,
        },
        response=Slice(items=[compute_requirement])
    )

    actual = compute_client.get_compute_requirements(ComputeRequirementSearch(
        sortField="name",
        namespace=compute_requirement.namespace,
        tag=compute_requirement.tag,
        statuses=[compute_requirement.status],
        sortDirection=SortDirection.ASCENDING
    )).list_all()

    assert actual == expected.items
    mock_api.verify_all_requests_called()
    
def test_can_search_compute_requirement_templates(mock_api, compute_client: ComputeClient):
    compute_requirement_template: ComputeRequirementDynamicTemplate = _make_compute_requirement_dynamic_template("test-requirement", "test-namespace")

    expected = mock_api.mock(
        "/compute/templates/requirements",
        HttpMethod.GET,
        params={
            "namespaces": compute_requirement_template.namespace,
            "sliced": "true"
        },
        response=Slice(items=[ComputeRequirementTemplateSummary()])
    )

    actual: List[ComputeRequirementTemplateSummary] = compute_client.get_compute_requirement_templates(ComputeRequirementTemplateSearch(
        namespaces=[compute_requirement_template.namespace]
    )).list_all()

    assert actual == expected.items
    mock_api.verify_all_requests_called()

def test_can_search_compute_source_templates(mock_api, compute_client: ComputeClient):
    compute_source_template: ComputeSourceTemplate = _make_compute_source_template()
    compute_source_template.namespace = "test-namespace"

    expected = mock_api.mock(
        "/compute/templates/sources",
        HttpMethod.GET,
        params={
            "namespaces": compute_source_template.namespace,
            "sliced": "true"
        },
        response=Slice(items=[ComputeSourceTemplateSummary()])
    )

    actual: List[ComputeSourceTemplateSummary] = compute_client.get_compute_source_templates(ComputeSourceTemplateSearch(
        namespaces=[compute_source_template.namespace]
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


def test_can_get_compute_source_template_with_user_attributes(mock_api, compute_client: ComputeClient):
    compute_source_template = _make_compute_source_template()

    expected = mock_api.mock(
        f"/compute/templates/sources/{compute_source_template.id}",
        HttpMethod.GET,
        response=compute_source_template
    )

    actual = compute_client.get_compute_source_template(compute_source_template.id)

    assert actual == expected
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

def _make_compute_requirement_dynamic_template(name: str, namespace: str) -> ComputeRequirementDynamicTemplate:
    compute_requirement_template = ComputeRequirementDynamicTemplate(
        name=name,
        namespace=namespace,
        strategyType="test-strategy"
    )
    compute_requirement_template.id = make_string()
    return compute_requirement_template


def _make_instance() -> Instance:
    instance = SimulatorInstance()
    instance.id = InstanceId(
        instanceId=make_string(),
        sourceId=make_string()
    )
    return instance


def _make_compute_source() -> ComputeSource:
    return SimulatorComputeSource(
        name=make_string()
    )


def _make_compute_source_template() -> ComputeSourceTemplate:
    template = ComputeSourceTemplate(
        source=_make_compute_source(),
        attributes=[
            StringAttributeValue(attribute="key", value=make_string())
        ]
    )

    template.id = make_string()

    return template
