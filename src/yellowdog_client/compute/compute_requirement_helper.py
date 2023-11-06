from __future__ import annotations

import typing
from concurrent.futures import Future
from typing import Callable

from yellowdog_client.model import ComputeRequirement
from yellowdog_client.model import ComputeRequirementStatus

if typing.TYPE_CHECKING:
    from yellowdog_client.compute import ComputeClient

from .predicated_compute_subscription_event_listener import PredicatedComputeSubscriptionEventListener \
    as ComputeSubscriptionListener


class ComputeRequirementHelper:
    """
    This class provides a number of methods that return a :class:`concurrent.futures.Future` allowing consumers to
    simply wait for the required state of a compute requirement before continuing on.

    Constructor accepts the following **arguments**:

    :param compute_requirement: The compute requirement.
    :param compute_service_client_impl: The compute service client.
    """

    __compute_requirement: ComputeRequirement = None
    __compute_service_client_impl: ComputeClient = None

    def __init__(self, compute_requirement: ComputeRequirement, compute_service_client_impl: ComputeClient) -> None:
        self.__compute_requirement = compute_requirement
        self.__compute_service_client_impl = compute_service_client_impl

    def _build_requirement_listener(self, future: Future,
                                    predicate: Callable[[ComputeRequirement], bool]) -> ComputeSubscriptionListener:
        return ComputeSubscriptionListener(
            future=future,
            predicate=predicate,
            compute_client=self.__compute_service_client_impl
        )

    def when_requirement_matches(self, predicate: Callable[[ComputeRequirement], bool]) -> Future:
        """
        Returns a :class:`concurrent.futures.Future` that is completed when the specified predicate evaluates to true.

        :param predicate: The predicate to test for each compute requirement changed event received.
        :type predicate: Callable[[:class:`yellowdog_client.model.ComputeRequirement`], :class:`bool`]
        :return: A :class:`concurrent.futures.Future` containing the matching compute requirement.
        :rtype: :class:`concurrent.futures.Future`

        .. code-block:: python

            from concurrent import futures
            from yellowdog_client.model import ComputeRequirementStatus

            future = helper.when_requirement_matches(lambda req:  req.status == ComputeRequirementStatus.TERMINATED)

            futures.wait(fs=(future,))
            future_compute_requirement = future.result()
            # ComputeRequirement

        """
        future = Future()
        future.set_running_or_notify_cancel()
        listener = self._build_requirement_listener(future=future, predicate=predicate)
        self.__compute_service_client_impl.add_compute_requirement_listener(
            compute_requirement=self.__compute_requirement,
            listener=listener
        )
        listener.updated(
            obj=self.__compute_service_client_impl.get_compute_requirement(
                compute_requirement=self.__compute_requirement
            )
        )
        return future

    @staticmethod
    def _requirement_status_predicate(status: ComputeRequirementStatus, requirement: ComputeRequirement) -> bool:
        return requirement.status == status

    def when_requirement_status_is(self, status: ComputeRequirementStatus) -> Future:
        """
        Returns a task that is completed when the compute requirement status matches the specified status.

        :param status: The compute requirement status to wait for.
        :type status: :class:`yellowdog_client.model.ComputeRequirementStatus`
        :return: A :class:`concurrent.futures.Future` containing the matching compute requirement.
        :rtype: :class:`concurrent.futures.Future`

        .. code-block:: python

            from concurrent import futures
            from yellowdog_client.model import ComputeRequirementStatus

            future = helper.when_requirement_status_is(ComputeRequirementStatus.RUNNING)

            futures.wait(fs=(future,))
            future_compute_requirement = future.result()
            # ComputeRequirement
        """
        return self.when_requirement_matches(
            predicate=lambda requirement: self._requirement_status_predicate(
                status=status,
                requirement=requirement
            )
        )
