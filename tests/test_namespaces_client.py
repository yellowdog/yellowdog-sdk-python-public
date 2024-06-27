import pytest
from yellowdog_client import PlatformClient
from yellowdog_client.model import ServicesSchema, ApiKey, Slice, SortDirection, NamespacePolicy, NamespacePolicySearch
from yellowdog_client.namespaces import NamespacesClient

from util.api import MockApi, HttpMethod
from util.data import make, make_string


@pytest.fixture
def namespaces_client(mock_api: MockApi) -> NamespacesClient:
    platform_client = PlatformClient.create(
        ServicesSchema(defaultUrl=mock_api.url()),
        make(ApiKey)
    )
    return platform_client.namespaces_client


def test_can_save_policy(mock_api: MockApi, namespaces_client: NamespacesClient):
    request = NamespacePolicy(namespace="foo", autoscalingMaxNodes=10)
    mock_api.mock(f"/namespaces/foo/policy", HttpMethod.PUT, request=request)

    namespaces_client.save_namespace_policy(request)

    mock_api.verify_all_requests_called()


def test_can_get_policy(mock_api: MockApi, namespaces_client: NamespacesClient):
    expected = NamespacePolicy(namespace="foo", autoscalingMaxNodes=10)
    expected = mock_api.mock(f"/namespaces/foo/policy", HttpMethod.GET, response=expected)

    actual = namespaces_client.get_namespace_policy("foo")

    assert actual == expected
    mock_api.verify_all_requests_called()


def test_can_delete_policy(mock_api: MockApi, namespaces_client: NamespacesClient):
    mock_api.mock(f"/namespaces/foo/policy", HttpMethod.DELETE)

    namespaces_client.delete_namespace_policy("foo")

    mock_api.verify_all_requests_called()


def test_can_get_policies(mock_api: MockApi, namespaces_client: NamespacesClient):
    first_slice = Slice(items=[NamespacePolicy("foo")], nextSliceId=make_string())
    second_slice = Slice(items=[NamespacePolicy("foobar")])
    expected = first_slice.items + second_slice.items
    search = NamespacePolicySearch(
        namespace="foo",
        sortDirection=SortDirection.ASCENDING
    )

    search_params = {
        "sortDirection": "ASCENDING",
        "namespace": "foo"
    }

    mock_api.mock(f"/namespaces/policies", HttpMethod.GET, params={
        **search_params
    }, response=first_slice)

    mock_api.mock(f"/namespaces/policies", HttpMethod.GET, params={
        **search_params,
        "sliceId": first_slice.nextSliceId
    }, response=second_slice)

    actual = namespaces_client.get_namespace_policies(search).list_all()

    assert actual == expected
    mock_api.verify_all_requests_called()
