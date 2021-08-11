from typing import Callable, Tuple
from concurrent.futures import Future

from .predicated_compute_subscription_event_listener import PredicatedComputeSubscriptionEventListener \
    as ComputeSubscriptionListener
from .compute_requirement_instances_changed_event_listener \
    import ComputeRequirementInstancesChangedEventListener as InstancesChangedListener
from .compute_requirement_instances_changed_event_listener_impl \
    import ComputeRequirementInstancesChangedEventListenerImpl
from yellowdog_client.model import ComputeRequirement
from yellowdog_client.model import ComputeRequirementStatus
from yellowdog_client.model import InstanceStatus
from yellowdog_client.model import Instance


class ComputeRequirementHelper:
    """
    This class provides a number of methods that return a :class:`concurrent.futures.Future` allowing consumers to
    simply wait for the required state of a compute requirement before continuing on.

    Constructor accepts the following **arguments**:

    :param compute_requirement: The compute requirement.
    :param compute_service_client_impl: The compute service client.
    """

    __compute_requirement = None  # type: ComputeRequirement
    __compute_service_client_impl = None  # type: 'ComputeClient'

    def __init__(self, compute_requirement, compute_service_client_impl):
        # type: (ComputeRequirement, 'ComputeClient') -> None
        self.__compute_requirement = compute_requirement
        self.__compute_service_client_impl = compute_service_client_impl

    def _build_requirement_listener(self, future, predicate):
        # type: (Future, Callable[[ComputeRequirement], bool]) -> ComputeSubscriptionListener
        return ComputeSubscriptionListener(
            future=future,
            predicate=predicate,
            compute_client=self.__compute_service_client_impl
        )

    def _build_instances_listener(self, future, predicate):
        # type: (Future, Callable[[Instance], bool]) -> InstancesChangedListener
        return ComputeRequirementInstancesChangedEventListenerImpl(
            future=future,
            predicate=predicate,
            compute_client=self.__compute_service_client_impl
        )

    def when_requirement_matches(self, predicate):
        # type: (Callable[[ComputeRequirement], bool]) -> Future
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

    def when_all_instances_match(self, predicate):
        # type: (Callable[[Instance], bool]) -> Future
        """
        Returns a task that is completed when the specified predicate evaluates to true for all instances contained
        in the requirement.

        :param predicate: The predicate to test for each compute requirement instances changed event received.
        :type predicate: Callable[[:class:`yellowdog_client.model.Instance`], :class:`bool`]
        :return: A :class:`concurrent.futures.Future` containing the matching compute requirement.
        :rtype: :class:`concurrent.futures.Future`

        .. code-block:: python

            from concurrent import futures
            from yellowdog_client.model import InstanceStatus

            future = helper.when_all_instances_match(lambda instance: instance.status == InstanceStatus.RUNNING)

            futures.wait(fs=(future,))
            future_compute_requirement = future.result()
            # ComputeRequirement
        """
        future = Future()
        future.set_running_or_notify_cancel()
        listener = self._build_instances_listener(future=future, predicate=predicate)
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
    def _requirement_status_predicate(status, requirement):
        # type: (ComputeRequirementStatus, ComputeRequirement) -> bool
        return requirement.status == status

    def when_requirement_status_is(self, status):
        # type: (ComputeRequirementStatus) -> Future
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

    @staticmethod
    def _when_all_instance_statuses_not_in_predicate(disallowed_statuses, instance):
        # type: (Tuple[InstanceStatus, ...], Instance) -> bool
        return instance.status not in disallowed_statuses

    def when_all_instance_statuses_not_in(self, disallowed_statuses):
        # type: (Tuple[InstanceStatus, ...]) -> Future
        """
        Returns a :class:`concurrent.futures.Future` that is completed when no instances contained in the compute
        requirement have a disallowed status. This method is typically used when starting or adding further instances
        to a compute requirement where it would be used to wait until no instances are still
        :class:`yellowdog_client.model.InstanceStatus.PENDING`

        :param disallowed_statuses: the disallowed instance status values.
        :type disallowed_statuses: list of :class:`yellowdog_client.model.InstanceStatus`
        :return: A :class:`concurrent.futures.Future` containing the matching compute requirement.
        :rtype: :class:`concurrent.futures.Future`

        .. code-block:: python

            from concurrent import futures
            from yellowdog_client.model import InstanceStatus

            future = helper.when_all_instance_statuses_not_in([InstanceStatus.PENDING, InstanceStatus.TERMINATING])

            futures.wait(fs=(future,))
            future_compute_requirement = future.result()
            # ComputeRequirement
        """
        return self.when_all_instances_match(
            predicate=lambda instance: self._when_all_instance_statuses_not_in_predicate(
                disallowed_statuses=disallowed_statuses,
                instance=instance
            )
        )

    @staticmethod
    def _when_all_instance_statuses_in_predicate(allowed_statuses, instance):
        # type: (Tuple[InstanceStatus, ...], Instance) -> bool
        return instance.status in allowed_statuses

    def when_all_instance_statuses_in(self, allowed_statuses):
        # type: (Tuple[InstanceStatus, ...]) -> Future
        """
        Returns a :class:`concurrent.futures.Future` that is completed when all instances contained in the compute
        requirement have an allowed status.

        :param allowed_statuses: the allowed instance status values.
        :type allowed_statuses: list of :class:`yellowdog_client.model.InstanceStatus`
        :return: A :class:`concurrent.futures.Future` containing the matching compute requirement.
        :rtype: :class:`concurrent.futures.Future`

        .. code-block:: python

            from concurrent import futures
            from yellowdog_client.model import InstanceStatus

            future = helper.when_all_instance_statuses_in([InstanceStatus.TERMINATING, InstanceStatus.TERMINATED])

            futures.wait(fs=(future,))
            future_compute_requirement = future.result()
            # ComputeRequirement
        """
        return self.when_all_instances_match(
            predicate=lambda instance: self._when_all_instance_statuses_in_predicate(
                allowed_statuses=allowed_statuses,
                instance=instance
            )
        )
