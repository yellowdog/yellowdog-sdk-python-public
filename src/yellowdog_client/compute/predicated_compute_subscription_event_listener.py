from __future__ import annotations

import typing
from concurrent.futures import Future
from typing import Callable

from yellowdog_client.common import SynchronizedPredicatedRunner
from yellowdog_client.common.server_sent_events import SubscriptionEventListener
from yellowdog_client.model import ComputeRequirement
from yellowdog_client.model.exceptions import ServerErrorException

if typing.TYPE_CHECKING:
    from yellowdog_client.compute import ComputeClient


class PredicatedComputeSubscriptionEventListener(SubscriptionEventListener):
    __runner: SynchronizedPredicatedRunner = None

    def __init__(
            self,
            future: Future[ComputeRequirement],
            predicate: Callable[[ComputeRequirement], bool],
            compute_client: ComputeClient
    ) -> None:
        super(PredicatedComputeSubscriptionEventListener, self).__init__()
        self.__future = future
        self.__predicate = predicate
        self.__runner = SynchronizedPredicatedRunner(predicate=self._runner_predicate)
        self.__compute_client = compute_client

    def _runner_predicate(self) -> bool:
        return not self.__future.done()

    def _updated_action(self, obj: ComputeRequirement) -> None:
        if self.__predicate(obj):
            self.__compute_client.remove_compute_requirement_listener(listener=self)
            self.__future.set_result(result=obj)

    def updated(self, obj: ComputeRequirement) -> None:
        self.__runner.run(runnable=lambda: self._updated_action(obj=obj))

    def _subscription_error_action(self, error: Exception) -> None:
        self.__compute_client.remove_compute_requirement_listener(listener=self)
        self.__future.set_exception(exception=error)

    def subscription_error(self, error: Exception) -> None:
        self.__runner.run(runnable=lambda: self._subscription_error_action(error=error))

    def _subscription_cancelled_action(self) -> None:
        self.__future.set_exception(exception=ServerErrorException.create_subscription_cancelled_error())

    def subscription_cancelled(self) -> None:
        self.__runner.run(runnable=self._subscription_cancelled_action)
