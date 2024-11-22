import pytest

from util.api import MockApi, HttpMethod
from util.data import make, make_string
from yellowdog_client import PlatformClient
from yellowdog_client.model import ServicesSchema, ApiKey, Slice, WorkerPoolSearch, WorkerPoolSummary
from yellowdog_client.scheduler import WorkerPoolClient


@pytest.fixture
def worker_pool_client(mock_api: MockApi) -> WorkerPoolClient:
    platform_client = PlatformClient.create(
        ServicesSchema(defaultUrl=mock_api.url()),
        make(ApiKey)
    )
    return platform_client.worker_pool_client


def test_can_find_all_worker_pools(mock_api: MockApi, worker_pool_client: WorkerPoolClient):
    first_slice = Slice(items=[make(WorkerPoolSummary)], nextSliceId=make_string())
    second_slice = Slice(items=[make(WorkerPoolSummary)])
    expected = first_slice.items + second_slice.items

    mock_api.mock(f"/workerPools/", HttpMethod.GET, params={
        "sliced": "true"
    }, response=first_slice)

    mock_api.mock(f"/workerPools/", HttpMethod.GET, params={
        "sliceId": first_slice.nextSliceId,
        "sliced": "true"
    }, response=second_slice)

    actual = worker_pool_client.find_all_worker_pools()

    assert actual == expected
    mock_api.verify_all_requests_called()


def test_can_get_worker_pools(mock_api: MockApi, worker_pool_client: WorkerPoolClient):
    first_slice = Slice(items=[make(WorkerPoolSummary)], nextSliceId=make_string())
    second_slice = Slice(items=[make(WorkerPoolSummary)])
    expected = first_slice.items + second_slice.items
    search = WorkerPoolSearch()

    mock_api.mock(f"/workerPools/", HttpMethod.GET, params={
        "sliced": "true"
    }, response=first_slice)

    mock_api.mock(f"/workerPools/", HttpMethod.GET, params={
        "sliceId": first_slice.nextSliceId,
        "sliced": "true"
    }, response=second_slice)

    actual = worker_pool_client.get_worker_pools(search).list_all()

    assert actual == expected
    mock_api.verify_all_requests_called()
