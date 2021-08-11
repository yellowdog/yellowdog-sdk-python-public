from typing import Callable
# noinspection PyCompatibility
from concurrent.futures import Future

from yellowdog_client.common import SynchronizedPredicatedRunner
from yellowdog_client.model import ComputeRequirement
from yellowdog_client.common.server_sent_events import SubscriptionEventListener
from yellowdog_client.model.exceptions import ServerErrorException


class PredicatedComputeSubscriptionEventListener(SubscriptionEventListener):
    __runner = None  # type: SynchronizedPredicatedRunner

    def __init__(self, future, predicate, compute_client):
        # type: (Future[ComputeRequirement], Callable[[ComputeRequirement], bool], 'ComputeClient') -> None
        super(PredicatedComputeSubscriptionEventListener, self).__init__()
        self.__future = future
        self.__predicate = predicate
        self.__runner = SynchronizedPredicatedRunner(predicate=self._runner_predicate)
        self.__compute_client = compute_client

    def _runner_predicate(self):
        # type: () -> bool
        return not self.__future.done()

    def _updated_action(self, obj):
        # type: (ComputeRequirement) -> None
        if self.__predicate(obj):
            self.__compute_client.remove_compute_requirement_listener(listener=self)
            self.__future.set_result(result=obj)

    def updated(self, obj):
        # type: (ComputeRequirement) -> None
        self.__runner.run(runnable=lambda: self._updated_action(obj=obj))

    def _subscription_error_action(self, error):
        # type: (Exception) -> None
        self.__compute_client.remove_compute_requirement_listener(listener=self)
        self.__future.set_exception(exception=error)

    def subscription_error(self, error):
        # type: (Exception) -> None
        self.__runner.run(runnable=lambda: self._subscription_error_action(error=error))

    def _subscription_cancelled_action(self):
        # type: () -> None
        self.__future.set_exception(exception=ServerErrorException.create_subscription_cancelled_error())

    def subscription_cancelled(self):
        # type: () -> None
        self.__runner.run(runnable=self._subscription_cancelled_action)
