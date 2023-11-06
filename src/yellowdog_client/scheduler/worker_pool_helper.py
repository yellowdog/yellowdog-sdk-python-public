from __future__ import annotations

import typing
from concurrent.futures import Future
from typing import Callable

from yellowdog_client.model import WorkerPool, WorkerPoolStatus
from yellowdog_client.scheduler import predicated_worker_pool_subscription_event_listener as pwpsel

if typing.TYPE_CHECKING:
    from yellowdog_client.scheduler.worker_pool_client import WorkerPoolClient

class WorkerPoolHelper:
    def __init__(self, worker_pool: WorkerPool, worker_pool_client: WorkerPoolClient):
        self._worker_pool: WorkerPool = worker_pool
        self._worker_pool_client: WorkerPoolClient = worker_pool_client

    def when_worker_pool_matches(self, predicate: Callable[[WorkerPool], bool]) -> Future:
        future = Future()
        future.set_running_or_notify_cancel()
        listener = pwpsel.PredicatedWorkerPoolSubscriptionEventListener(
            future=future,
            predicate=predicate,
            worker_pool_client=self._worker_pool_client
        )
        self._worker_pool_client.add_worker_pool_listener(self._worker_pool, listener)
        listener.updated(self._worker_pool_client.get_worker_pool(self._worker_pool))
        return future

    def when_worker_pool_status_is(self, status: WorkerPoolStatus) -> Future:
        return self.when_worker_pool_matches(lambda pool: pool.status == status)
