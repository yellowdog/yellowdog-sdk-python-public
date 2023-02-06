import datetime

import pytest

from util.api import MockApi, HttpMethod
from util.data import make, make_string
from yellowdog_client import PlatformClient
from yellowdog_client.model import ServicesSchema, ApiKey, WorkRequirement, Slice, Task, TaskSearch, InstantRange, \
    TaskStatus, SortDirection
from yellowdog_client.scheduler import WorkClient


@pytest.fixture
def work_client(mock_api: MockApi) -> WorkClient:
    platform_client = PlatformClient.create(
        ServicesSchema(defaultUrl=mock_api.url()),
        make(ApiKey)
    )
    return platform_client.work_client


def test_can_add_work_requirement(mock_api: MockApi, work_client: WorkClient):
    expected = mock_api.mock(f"/work/requirements", HttpMethod.POST, response_type=WorkRequirement)

    actual = work_client.add_work_requirement(expected)

    assert actual == expected
    mock_api.verify_all_requests_called()


def test_can_add_update_requirement(mock_api: MockApi, work_client: WorkClient):
    expected = make(WorkRequirement)
    expected = mock_api.mock(f"/work/requirements", HttpMethod.PUT, request=expected, response=expected)

    actual = work_client.update_work_requirement(expected)

    assert actual == expected
    mock_api.verify_all_requests_called()


def test_can_get_work_requirement(mock_api: MockApi, work_client: WorkClient):
    expected = make(WorkRequirement)
    expected = mock_api.mock(f"/work/requirements/{expected.id}", HttpMethod.GET, response=expected)

    actual = work_client.get_work_requirement(expected)

    assert actual == expected
    mock_api.verify_all_requests_called()


def test_can_find_tasks(mock_api: MockApi, work_client: WorkClient):
    first_slice = Slice(items=[make(Task)], nextSliceId=make_string())
    second_slice = Slice(items=[make(Task)])
    expected = first_slice.items + second_slice.items
    search = TaskSearch(
        workRequirementId=make_string(),
        hasInputs=True,
        startedTime=InstantRange(min=datetime.datetime(2020, 1, 1)),
        statuses=[TaskStatus.READY, TaskStatus.FAILED],
        sortField="name",
        sortDirection=SortDirection.ASCENDING
    )

    search_params = {
        "workRequirementId": search.workRequirementId,
        "startedTime.min": "2020-01-01+00%3A00%3A00",
        "hasInputs": "True",
        "statuses": ["READY", "FAILED"],
        "sortField": "name",
        "sortDirection": "ASCENDING"
    }

    mock_api.mock(f"/work/tasks", HttpMethod.GET, params={
        **search_params,
        "size": "1000"
    }, response=first_slice)

    mock_api.mock(f"/work/tasks", HttpMethod.GET, params={
        **search_params,
        "sliceId": first_slice.nextSliceId,
        "size": "1000",
    }, response=second_slice)

    actual = work_client.find_tasks(search)

    assert actual == expected
    mock_api.verify_all_requests_called()
