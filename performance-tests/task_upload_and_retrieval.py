#!/usr/bin/env python3
import os
import random
import string
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, TypeVar, List, Any

from yellowdog_client import PlatformClient
from yellowdog_client.model import WorkRequirement, TaskGroup, RunSpecification, Task, TaskSearch, TaskTemplate, ServicesSchema, ApiKey
from yellowdog_client.scheduler import WorkClient

T = TypeVar("T")


def timed(fn: Callable[[], Any]) -> float:
    start = time.monotonic()
    fn()
    elapsed = time.monotonic() - start
    return elapsed


def upload_tasks(client: WorkClient, task_group: TaskGroup, tasks: List[Task], batch_size: int, batch_concurrency: int) -> List[Task]:
    results = []
    batches = [tasks[i:i + batch_size] for i in range(0, len(tasks), batch_size)]

    with ThreadPoolExecutor(max_workers=batch_concurrency) as executor:
        futures = [executor.submit(client.add_tasks_to_task_group, task_group, batch) for batch in batches]
        for future in as_completed(futures):
            try:
                results.extend(future.result())
            except Exception as e:
                print(f"Error uploading tasks: {e}")
                raise
    return results


def build_requirement(client: WorkClient, task_data_size) -> WorkRequirement:
    name = "yd-" + str(uuid.uuid4()).lower()
    namespace = "test"
    task_type = "python"
    requirement = WorkRequirement(
        name=name,
        namespace=namespace,
        taskGroups=[(TaskGroup(
            name=name,
            runSpecification=RunSpecification(taskTypes=[task_type], namespaces=[namespace]),
            taskTemplate=TaskTemplate(taskType=task_type, taskData=generate_str(task_data_size))
        ))],
    )
    requirement = client.add_work_requirement(requirement)
    return requirement


def generate_str(size: int) -> str:
    return random.choice(string.ascii_lowercase) + ''.join(random.choices(string.ascii_lowercase + string.digits, k=size - 1))


class Config:
    REQUIRED_ENV_VARS = ["YD_PLATFORM_URL", "YD_API_KEY_ID", "YD_API_KEY_SECRET"]

    def __init__(self) -> None:
        missing = [v for v in self.REQUIRED_ENV_VARS if not os.environ.get(v)]
        if missing:
            raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")
        self.platform_url: str = os.environ["YD_PLATFORM_URL"]
        self.api_key_id: str = os.environ["YD_API_KEY_ID"]
        self.api_key_secret: str = os.environ["YD_API_KEY_SECRET"]


def main() -> None:
    config = Config()
    client = PlatformClient.create(
        ServicesSchema(defaultUrl=config.platform_url),
        ApiKey(config.api_key_id, config.api_key_secret),
    ).work_client

    task_data_size = 5 * 1025
    task_argument_count = 5
    task_argument_size = 100
    task_name_size = 60
    task_tag_size = 60
    upload_batch_size = 10000
    upload_batch_concurrency = 20

    for task_count in [1000, 10000, 100000]:
        requirement = build_requirement(client, task_data_size)
        assert requirement.taskGroups is not None
        task_group = requirement.taskGroups[0]

        try:
            tasks = [Task(
                name=generate_str(task_name_size),
                tag=generate_str(task_tag_size),
                arguments=[generate_str(task_argument_size) for _ in range(task_argument_count)]
            ) for _ in range(task_count)]
            task_upload = timed(lambda: upload_tasks(client, task_group, tasks, upload_batch_size, upload_batch_concurrency))
            task_retrieval = timed(lambda: client.get_tasks(TaskSearch(taskGroupId=task_group.id)).list_all())

            print(f"tasks: {task_count}. upload: {task_upload:.2f}s ({task_count / task_upload:.0f} tasks/s). retrieval: {task_retrieval:.2f}s ({task_count / task_retrieval:.0f} tasks/s).")

        finally:
            client.cancel_work_requirement(requirement)


if __name__ == "__main__":
    main()
