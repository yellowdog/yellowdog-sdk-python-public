from typing import Callable
# noinspection PyCompatibility
from concurrent.futures import Future

from .compute_requirement_instances_changed_event_listener \
    import ComputeRequirementInstancesChangedEventListener
from .compute_changed_event_data import ComputeChangedEventData
from yellowdog_client.common import SynchronizedPredicatedRunner
from yellowdog_client.model import ComputeRequirement
from yellowdog_client.model import Instance
from yellowdog_client.model.exceptions import ServerErrorException


class ComputeRequirementInstancesChangedEventListenerImpl(ComputeRequirementInstancesChangedEventListener):
    __future = None  # type: Future[ComputeRequirement]
    __predicate = None  # type: Callable[[Instance], bool]
    __runner = None  # type: SynchronizedPredicatedRunner
    __compute_client = None  # type: 'ComputeClient'

    def __init__(self, future, predicate, compute_client):
        # type: (Future[ComputeRequirement], Callable[[Instance], bool], 'ComputeClient') -> None
        super(ComputeRequirementInstancesChangedEventListenerImpl, self).__init__()
        self.__future = future
        self.__predicate = predicate
        self.__runner = SynchronizedPredicatedRunner(predicate=self._runner_predicate)
        self.__compute_client = compute_client

    def _runner_predicate(self):
        # type: () -> bool
        return not self.__future.done()

    def _subscription_error_runnable(self, error):
        # type: (Exception) -> None
        self.__compute_client.remove_compute_requirement_listener(listener=self)
        self.__future.set_exception(exception=error)

    def subscription_error(self, error):
        # type: (Exception) -> None
        self.__runner.run(runnable=lambda: self._subscription_error_runnable(error=error))

    def _subscription_cancelled_runnable(self):
        # type: () -> None
        self.__future.set_exception(exception=ServerErrorException.create_subscription_cancelled_error())

    def subscription_cancelled(self):
        # type: () -> None
        self.__runner.run(runnable=self._subscription_cancelled_runnable)

    def _instances_changed_runnable(self, compute_changed_event_data: ComputeChangedEventData) -> None:
        instances = compute_changed_event_data.compute_requirement.instances
        if not instances or all(self.__predicate(instance) for instance in instances):
            self.__compute_client.remove_compute_requirement_listener(listener=self)
            self.__future.set_result(result=compute_changed_event_data.compute_requirement)

    def _instances_changed(self, compute_changed_event_data):
        # type: (ComputeChangedEventData) -> None
        self.__runner.run(
            runnable=lambda: self._instances_changed_runnable(
                compute_changed_event_data=compute_changed_event_data
            )
        )
