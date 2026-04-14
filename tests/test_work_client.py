import datetime

import pytest

from util.api import MockApi, HttpMethod
from util.data import make, make_string
from util.sse.sse_server import SseServer
from yellowdog_client import PlatformClient
from yellowdog_client.common.json import Json
from yellowdog_client.model import ServicesSchema, ApiKey, WorkRequirement, Slice, Task, TaskSearch, InstantRange, \
    TaskStatus, SortDirection, WorkRequirementStatus, WorkRequirementSummary, WorkRequirementSearch, TaskGroupStatus, DoubleRange, \
    TaskGroup, RunSpecification, TaskSummary, CloudProvider, TaskErrorMatcher
from yellowdog_client.scheduler import WorkClient


@pytest.fixture
def work_client(mock_api: MockApi) -> WorkClient:
    platform_client = PlatformClient.create(
        ServicesSchema(defaultUrl=mock_api.url()),
        make(ApiKey)
    )
    return platform_client.work_client


def now() -> datetime.datetime:
    return datetime.datetime.now().replace(tzinfo=datetime.timezone.utc, microsecond=0)


def work_requirement() -> WorkRequirement:
    task_group = TaskGroup(
        name="group1",
        runSpecification=RunSpecification(
            taskTypes=["type1", "type2"],
            instanceTypes=["foo", "bar"],
            vcpus=DoubleRange(min=1.0, max=4.0),
            ram=DoubleRange(min=0.1, max=0.8),
            minWorkers=1,
            maxWorkers=10,
            tasksPerWorker=1,
            maximumTaskRetries=1,
            taskTimeout=datetime.timedelta(minutes=30),
            providers=[CloudProvider.AWS, CloudProvider.AZURE],
            regions=["us-east-1", "eu-west-1"],
            workerTags=["tag1", "tag2"],
            namespaces=["namespace1", "namespace2"],
            retryableErrors=[TaskErrorMatcher(
                errorTypes=["foo"],
                statusesAtFailure=[TaskStatus.EXECUTING, TaskStatus.READY],
                processExitCodes=[1, 2, 3]
            )]
        ),
        tag="group-tag",
        priority=1.0,
        dependentOn="bar",
        dependencies=["bar", "baz"],
        starved=True,
        waitingOnDependency=True,
        finishIfAllTasksFinished=True,
        finishIfAnyTaskFailed=True,
        completedTaskTtl=datetime.timedelta(hours=1)
    )
    task_group.id = "ydid:taskgroup:000000:000000:12345678-1234-1234-1234-123456789012"
    task_group.status = TaskGroupStatus.COMPLETED
    task_group.statusChangedTime = now()
    task_group.taskSummary = TaskSummary(
        statusCounts={
            TaskStatus.COMPLETED: 1,
            TaskStatus.FAILED: 0,
        },
        taskCount=1,
        lastUpdatedTime=now()
    )
    result = WorkRequirement(
        namespace="test-namespace",
        name="test-work-requirement",
        taskGroups=[task_group],
        tag="foo",
        priority=1.0
    )
    result.id = "ydid:workreq:000000:000000:12345678-1234-1234-1234-123456789012"
    result.createdTime = now()
    result.status = WorkRequirementStatus.COMPLETED
    result.statusChangedTime = now()
    return result


def work_requirement_summary() -> WorkRequirementSummary:
    return WorkRequirementSummary(
        id="ydid:workreq:000000:000000:12345678-1234-1234-1234-123456789012",
        namespace="test-namespace",
        name="test-work-requirement",
        tag="foo",
        createdTime=now(),
        statusChangedTime=now(),
        priority=1.0,
        completedTaskCount=10,
        totalTaskCount=10,
        status=WorkRequirementStatus.COMPLETED,
        healthy=True
    )

def task() -> Task:
    return Task(
        name="test-task",
        taskType="foo",
        startedTime=now(),
    )


def test_can_add_work_requirement(mock_api: MockApi, work_client: WorkClient):
    expected = work_requirement()
    expected = mock_api.mock(f"/work/requirements", HttpMethod.POST, response=expected)

    actual = work_client.add_work_requirement(expected)

    assert actual == expected
    mock_api.verify_all_requests_called()


def test_can_add_update_requirement(mock_api: MockApi, work_client: WorkClient):
    expected = work_requirement()
    expected = mock_api.mock(f"/work/requirements", HttpMethod.PUT, request=expected, response=expected)

    actual = work_client.update_work_requirement(expected)

    assert actual == expected
    mock_api.verify_all_requests_called()


def test_can_get_work_requirement(mock_api: MockApi, work_client: WorkClient):
    expected = work_requirement()
    expected = mock_api.mock(f"/work/requirements/{expected.id}", HttpMethod.GET, response=expected)

    actual = work_client.get_work_requirement(expected)

    assert actual == expected
    mock_api.verify_all_requests_called()


def test_can_find_all_work_requirements(mock_api: MockApi, work_client: WorkClient):
    first_slice = Slice(items=[work_requirement_summary()], nextSliceId=make_string())
    second_slice = Slice(items=[work_requirement_summary()])
    expected = first_slice.items + second_slice.items

    mock_api.mock(f"/work/requirements", HttpMethod.GET, params={
        "sliced": "true"
    }, response=first_slice)

    mock_api.mock(f"/work/requirements", HttpMethod.GET, params={
        "sliceId": first_slice.nextSliceId,
        "sliced": "true"
    }, response=second_slice)

    actual = work_client.find_all_work_requirements()

    assert actual == expected
    mock_api.verify_all_requests_called()


def test_can_get_work_requirements(mock_api: MockApi, work_client: WorkClient):
    first_slice = Slice(items=[work_requirement_summary()], nextSliceId=make_string())
    second_slice = Slice(items=[work_requirement_summary()])
    expected = first_slice.items + second_slice.items
    search = WorkRequirementSearch()

    mock_api.mock(f"/work/requirements", HttpMethod.GET, params={
        "sliced": "true"
    }, response=first_slice)

    mock_api.mock(f"/work/requirements", HttpMethod.GET, params={
        "sliceId": first_slice.nextSliceId,
        "sliced": "true"
    }, response=second_slice)

    actual = work_client.get_work_requirements(search).list_all()

    assert actual == expected
    mock_api.verify_all_requests_called()


def test_can_find_tasks(mock_api: MockApi, work_client: WorkClient):
    first_slice = Slice(items=[task()], nextSliceId=make_string())
    second_slice = Slice(items=[task()])
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
        "startedTime.min": "2020-01-01T00%3A00%3A00.000Z",
        "hasInputs": "True",
        "statuses": ["READY", "FAILED"],
        "sortField": "name",
        "sortDirection": "ASCENDING"
    }

    mock_api.mock(f"/work/tasks", HttpMethod.GET, params={
        **search_params
    }, response=first_slice)

    mock_api.mock(f"/work/tasks", HttpMethod.GET, params={
        **search_params,
        "sliceId": first_slice.nextSliceId
    }, response=second_slice)

    actual = work_client.find_tasks(search)

    assert actual == expected
    mock_api.verify_all_requests_called()


def test_can_wait_for_work_requirement_status(mock_api: MockApi):
    expected = work_requirement()

    with SseServer(f"/work/requirements/{expected.id}/updates") as sse_server:
        platform_client = PlatformClient.create(
            ServicesSchema(defaultUrl=sse_server.get_root_url()),
            make(ApiKey)
        )
        work_client = platform_client.work_client

        sse_server.forward(f"/work/requirements/{expected.id}", mock_api.url())
        mock_api.mock(f"/work/requirements/{expected.id}", HttpMethod.GET, response=expected)

        work_requirement_helper = work_client.get_work_requirement_helper(expected)

        future = work_requirement_helper.when_requirement_status_is(WorkRequirementStatus.COMPLETED)
        expected.status = WorkRequirementStatus.COMPLETED
        sse_server.broadcast(type="entity_updated", data=Json.dumps(expected), id=expected.id)
        expected = future.result(2)
        assert expected.status == WorkRequirementStatus.COMPLETED
