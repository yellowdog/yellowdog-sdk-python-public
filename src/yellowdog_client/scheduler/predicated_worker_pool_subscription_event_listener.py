from typing import Callable
# noinspection PyCompatibility
from concurrent.futures import Future

from yellowdog_client.scheduler import worker_pool_client as wpc
from yellowdog_client.common import SynchronizedPredicatedRunner
from yellowdog_client.common.server_sent_events import SubscriptionEventListener
from yellowdog_client.model.exceptions import ServerErrorException
from yellowdog_client.model import WorkerPool


class PredicatedWorkerPoolSubscriptionEventListener(SubscriptionEventListener):
    def __init__(self, future: Future, predicate: Callable[[WorkerPool], bool],
                 worker_pool_client: wpc.WorkerPoolClient):
        super(PredicatedWorkerPoolSubscriptionEventListener, self).__init__()
        self.__future = future
        self.__predicate = predicate
        self.__runner = SynchronizedPredicatedRunner(predicate=self._runner_predicate)
        self.__worker_pool_client = worker_pool_client

    def _runner_predicate(self):
        # type: () -> bool
        return not self.__future.done()

    def _updated_action(self, obj: WorkerPool) -> None:
        if self.__predicate(obj):
            self.__worker_pool_client.remove_worker_pool_listener(listener=self)
            self.__future.set_result(result=obj)

    def updated(self, obj: WorkerPool) -> None:
        self.__runner.run(runnable=lambda: self._updated_action(obj=obj))

    def _subscription_error_action(self, error: Exception) -> None:
        self.__worker_pool_client.remove_worker_pool_listener(listener=self)
        self.__future.set_exception(exception=error)

    def subscription_error(self, error: Exception) -> None:
        self.__runner.run(runnable=lambda: self._subscription_error_action(error=error))

    def _subscription_cancelled_action(self) -> None:
        self.__future.set_exception(exception=ServerErrorException.create_subscription_cancelled_error())

    def subscription_cancelled(self) -> None:
        self.__runner.run(runnable=self._subscription_cancelled_action)
