from __future__ import annotations

import typing
from concurrent.futures import Future
from typing import Callable

from yellowdog_client.common import SynchronizedPredicatedRunner
from yellowdog_client.common.server_sent_events import SubscriptionEventListener
from yellowdog_client.model import WorkRequirement
from yellowdog_client.model.exceptions import ServerErrorException

if typing.TYPE_CHECKING:
    from yellowdog_client.scheduler import WorkClient


class PredicatedWorkSubscriptionEventListener(SubscriptionEventListener):
    def __init__(
            self,
            future: Future[WorkRequirement],
            predicate: Callable[[WorkRequirement], bool],
            work_client: WorkClient
    ) -> None:
        super(PredicatedWorkSubscriptionEventListener, self).__init__()
        self.__future = future
        self.__predicate = predicate
        self.__runner = SynchronizedPredicatedRunner(predicate=self._runner_predicate)
        self.__work_client = work_client

    def _runner_predicate(self) -> bool:
        return not self.__future.done()

    def _updated_action(self, obj: WorkRequirement) -> None:
        if self.__predicate(obj):
            self.__work_client.remove_work_requirement_listener(listener=self)
            self.__future.set_result(result=obj)

    def updated(self, obj: WorkRequirement) -> None:
        self.__runner.run(runnable=lambda: self._updated_action(obj=obj))

    def _subscription_error_action(self, error: Exception) -> None:
        self.__work_client.remove_work_requirement_listener(listener=self)
        self.__future.set_exception(exception=error)

    def subscription_error(self, error: Exception) -> None:
        self.__runner.run(runnable=lambda: self._subscription_error_action(error=error))

    def _subscription_cancelled_action(self) -> None:
        self.__future.set_exception(exception=ServerErrorException.create_subscription_cancelled_error())

    def subscription_cancelled(self) -> None:
        self.__runner.run(runnable=self._subscription_cancelled_action)
