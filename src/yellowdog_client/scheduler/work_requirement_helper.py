from typing import Callable
# noinspection PyCompatibility
from concurrent.futures import Future

from .predicated_work_subscription_event_listener import PredicatedWorkSubscriptionEventListener
from yellowdog_client.scheduler import work_client as wc
from yellowdog_client.model import WorkRequirement
from yellowdog_client.model import WorkRequirementStatus


class WorkRequirementHelper:
    """
    This class provides a number of methods that return a :class:`concurrent.futures.Future` allowing consumers to
    simply wait for the required state of a work requirement before continuing on.

    Constructor accepts the following **arguments**:

    :param work_requirement: The work requirement.
    :type work_requirement: :class:`yellowdog_client.model.WorkRequirement`
    :param work_service_client_impl: The scheduler service client.
    :type work_service_client_impl: :class:`yellowdog_client.scheduler.WorkClient`

    .. seealso::

        Use :meth:`yellowdog_client.scheduler.WorkClientImpl.get_work_requirement_helper` for easier access
        to the :class:`yellowdog_client.scheduler.WorkRequirementHelper`

        .. code-block:: python

            helper = client.work_client.get_work_requirement_helper(work_requirement)
            # WorkRequirementHelper

    .. versionadded:: 0.4.0
    """

    _work_requirement = None  # type: WorkRequirement
    _work_service_client_impl = None  # type: wc.WorkClient

    def __init__(self, work_requirement, work_service_client_impl):
        # type: (WorkRequirement, wc.WorkClient) -> None
        self._work_requirement = work_requirement
        self._work_service_client_impl = work_service_client_impl

    def when_requirement_matches(self, predicate):
        # type: (Callable[[WorkRequirement], bool]) -> Future
        """
        Returns a :class:`concurrent.futures.Future` that is completed when the specified predicate evaluates to true.

        :param predicate: The predicate to test for each work requirement changed event received.
        :type predicate: Callable[[:class:`yellowdog_client.model.WorkRequirement`], :class:`bool`]
        :return: A :class:`concurrent.futures.Future` containing the matching work requirement.
        :rtype: :class:`concurrent.futures.Future`

        .. code-block:: python

            from concurrent import futures
            from yellowdog_client.model import WorkRequirementStatus

            future = helper.when_requirement_matches(lambda req:  req.status == WorkRequirementStatus.COMPLETED)

            futures.wait(fs=(future,))
            future_work_requirement = future.result()
            # WorkRequirement

        """
        future = Future()
        future.set_running_or_notify_cancel()
        listener = PredicatedWorkSubscriptionEventListener(
            future=future,
            predicate=predicate,
            work_client=self._work_service_client_impl
        )
        self._work_service_client_impl.add_work_requirement_listener(
            work_requirement=self._work_requirement,
            listener=listener
        )
        listener.updated(
            obj=self._work_service_client_impl.get_work_requirement(
                work_requirement=self._work_requirement
            )
        )
        return future

    def when_requirement_status_is(self, status):
        # type: (WorkRequirementStatus) -> Future
        """
        Returns a task that is completed when the work requirement status matches the specified status.

        :param status: The work requirement status to wait for.
        :type status: :class:`yellowdog_client.model.WorkRequirementStatus`
        :return: A :class:`concurrent.futures.Future` containing the matching work requirement.
        :rtype: :class:`concurrent.futures.Future`

        .. code-block:: python

            from concurrent import futures
            from yellowdog_client.model import WorkRequirementStatus

            future = helper.when_requirement_status_is(WorkRequirementStatus.COMPLETED)

            futures.wait(fs=(future,))
            future_work_requirement = future.result()
            # WorkRequirement
        """
        return self.when_requirement_matches(lambda requirement: requirement.status == status)
