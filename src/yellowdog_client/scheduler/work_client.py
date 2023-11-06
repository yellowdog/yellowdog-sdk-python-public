from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from .work_requirement_helper import WorkRequirementHelper
from yellowdog_client.common import Closeable, SearchClient
from yellowdog_client.common.server_sent_events import SubscriptionEventListener
from yellowdog_client.model import Slice, SliceReference, Task, TaskGroup, TaskSearch, WorkRequirement, WorkRequirementSummary


class WorkClient(ABC, Closeable):
    """Client interface containing methods for accessing YellowDog Scheduler functions."""

    @abstractmethod
    def add_work_requirement(self, work_requirement: WorkRequirement) -> WorkRequirement:
        """
        Submits a NEW work requirement to the YellowDog Scheduler service to be initialised and started.

        :param work_requirement: the work requirement to submit
        :return: the latest state of the work requirement after it has been submitted
        """

        pass

    @abstractmethod
    def update_work_requirement(self, work_requirement: WorkRequirement) -> WorkRequirement:
        """
        Submits an existing work requirement to the YellowDog Scheduler service to be updated.

        :param work_requirement: the work requirement to submit
        :return: the latest state of the work requirement after it has been submitted
        """

        pass

    @abstractmethod
    def get_work_requirement(self, work_requirement: WorkRequirement) -> WorkRequirement:
        """
        Gets the latest state of the supplied work requirement.

        :param work_requirement: the work requirement for which to get the latest state
        :return: the latest state of the work requirement
        """

        pass

    @abstractmethod
    def get_work_requirement_by_id(self, work_requirement_id: str) -> WorkRequirement:
        """
        Gets the latest state of the supplied work requirement.

        :param work_requirement_id: the ID of the work requirement
        :return: the latest state of the work requirement
        """

        pass

    @abstractmethod
    def get_work_requirement_by_name(self, namespace: str, work_requirement_name: str) -> WorkRequirement:
        """
        Gets the latest state of the supplied work requirement.

        :param namespace:           the namespace containing the requirement
        :param work_requirement_name: the name of the requirement
        :return: the latest state of the work requirement
        """

        pass

    @abstractmethod
    def hold_work_requirement(self, work_requirement: WorkRequirement) -> WorkRequirement:
        """
        Instructs the Scheduler to hold the supplied work requirement, no further tasks will be executed until the work requirement is started again.

        :param work_requirement: the work requirement to hold
        :return: the latest state of the work requirement after the hold instruction was submitted
        """

        pass

    @abstractmethod
    def hold_work_requirement_by_id(self, work_requirement_id: str) -> WorkRequirement:
        """
        Instructs the Scheduler to hold the supplied work requirement, no further tasks will be executed until the work requirement is started again.

        :param work_requirement_id: the ID of the work requirement to hold
        :return: the latest state of the work requirement after the hold instruction was submitted
        """

        pass

    @abstractmethod
    def start_work_requirement(self, work_requirement: WorkRequirement) -> WorkRequirement:
        """
        Instructs the Scheduler to start the supplied work requirement after it was held.

        :param work_requirement: the work requirement to start after being held
        :return: the latest state of the work requirement after the start instruction was submitted
        """

        pass

    @abstractmethod
    def start_work_requirement_by_id(self, work_requirement_id: str) -> WorkRequirement:
        """
        Instructs the Scheduler to start the supplied work requirement after it was held.

        :param work_requirement_id: the ID of the work requirement to start after being held
        :return: the latest state of the work requirement after the start instruction was submitted
        """

        pass

    @abstractmethod
    def cancel_work_requirement(self, work_requirement: WorkRequirement) -> WorkRequirement:
        """
        Instructs the Scheduler to cancel the supplied work requirement, no further tasks will be executed and all workers shall be released.

        :param work_requirement: the work requirement to cancel
        :return: the latest state of the work requirement after the cancel instruction was submitted
        """

        pass

    @abstractmethod
    def cancel_work_requirement_by_id(self, work_requirement_id: str) -> WorkRequirement:
        """
        Instructs the Scheduler to cancel the supplied work requirement, no further tasks will be executed and all workers shall be released.

        :param work_requirement_id: the ID of the work requirement to cancel
        :return: the latest state of the work requirement after the cancel instruction was submitted
        """

        pass

    @abstractmethod
    def add_work_requirement_listener(self, work_requirement: WorkRequirement, listener: SubscriptionEventListener[WorkRequirement]) -> None:
        """
        Adds an event listener to receive notifications of changes for the specified work requirement.
        The client manages subscriptions to YellowDog Scheduler such that the first listener created for a requirement will cause a Server-Sent Events subscription to be initiated; additional listeners for the same requirement share that subscription.

        :param work_requirement: the work requirement for which to receive notifications
        :param listener:        the event listener that will be invoked for notifications
        """

        pass

    @abstractmethod
    def add_work_requirement_listener_by_id(self, work_requirement_id: str, listener: SubscriptionEventListener[WorkRequirement]) -> None:
        """
        Adds an event listener to receive notifications of changes for the specified work requirement.
        The client manages subscriptions to YellowDog Scheduler such that the first listener created for a requirement will cause a Server-Sent Events subscription to be initiated; additional listeners for the same requirement share that subscription.

        :param work_requirement_id: the ID of the work requirement for which to receive notifications
        :param listener:          the event listener that will be invoked for notifications
        """

        pass

    @abstractmethod
    def remove_work_requirement_listener(self, listener: SubscriptionEventListener[WorkRequirement]) -> None:
        """
        Removes the specified event listener.
        The client manages subscriptions to YellowDog Scheduler such that when the last listener for a requirement is removed, the associated Server-Sent Events subscription is cancelled.

        :param listener: the event listener that will no longer be invoked for notifications
        """

        pass

    @abstractmethod
    def get_work_requirement_helper(self, work_requirement: WorkRequirement) -> WorkRequirementHelper:
        """
        Constructs a new work requirement helper for the specified requirement.

        :param work_requirement: the work requirement for which the helper will be constructed
        :return: a new work requirement helper
        """

        pass

    @abstractmethod
    def get_work_requirement_helper_by_id(self, work_requirement_id: str) -> WorkRequirementHelper:
        """
        Constructs a new work requirement helper for the specified requirement.

        :param work_requirement_id: the ID of the work requirement for which the helper will be constructed
        :return: a new work requirement helper
        """

        pass

    @abstractmethod
    def find_all_work_requirements(self) -> List[WorkRequirementSummary]:
        """
        Returns summaries of all existing work requirements within the system for the requesting user.

        :return: a list of work requirement summaries
        """

        pass

    @abstractmethod
    def add_tasks_to_task_group(self, task_group: TaskGroup, tasks: List[Task]) -> List[Task]:
        """
        Submits NEW tasks to the YellowDog Scheduler service to be added to the specified task group.

        :param task_group: the task group to add the tasks to
        :param tasks:     the submitted tasks
        :return: the latest state of the tasks after they have been submitted
        """

        pass

    @abstractmethod
    def add_tasks_to_task_group_by_id(self, task_group_id: str, tasks: List[Task]) -> List[Task]:
        """
        Submits NEW tasks to the YellowDog Scheduler service to be added to the specified task group.

        :param task_group_id: the ID of the task group to add the tasks to
        :param tasks:       the submitted tasks
        :return: the latest state of the tasks after they have been submitted
        """

        pass

    @abstractmethod
    def add_tasks_to_task_group_by_name(self, namespace: str, work_requirement_name: str, task_group_name: str, tasks: List[Task]) -> List[Task]:
        """
        Submits NEW tasks to the YellowDog Scheduler service to be added to the specified task group.

        :param namespace:           the namespace
        :param work_requirement_name: the work requirement name
        :param task_group_name:       the task group name
        :param tasks:               the submitted tasks
        :return: the latest state of the tasks after they have been submitted
        """

        pass

    @abstractmethod
    def get_task(self, task: Task) -> Task:
        """
        Gets the latest state of the supplied task.

        :param task: the task for which to get the latest state
        :return: the latest state of the task
        """

        pass

    @abstractmethod
    def get_task_by_id(self, task_id: str) -> Task:
        """
        Gets the latest state of the supplied task.

        :param task_id: the ID of the task
        :return: the latest state of the task
        """

        pass

    @abstractmethod
    def cancel_task(self, task: Task, abort: bool) -> Task:
        """
        Instructs the Scheduler to cancel the specified task.

        :param task:  the task to cancel
        :param abort: if the task should be aborted if it has been allocated to a worker
        :return: the latest state of the task after the cancel instruction was submitted
        """

        pass

    @abstractmethod
    def cancel_task_by_id(self, task_id: str, abort: bool) -> Task:
        """
        Instructs the Scheduler to cancel the specified task.

        :param task_id: the ID of the task to cancel
        :param abort:  if the task should be aborted if it has been allocated to a worker
        :return: the latest state of the task after the cancel instruction was submitted
        """

        pass

    @abstractmethod
    def find_tasks(self, search: TaskSearch) -> List[Task]:
        """
        Returns tasks within the system that match the specified search.
        WARNING: If your search matches too many tasks to fit into your application's memory limits, consider using
        #streamTasks(TaskSearch) or #findTasks(TaskSearch, SliceReference).

        :param search: the search
        :return: a list of tasks
        @deprecated use #getTasks(TaskSearch) instead to search tasks.
        """

        pass

    @abstractmethod
    def find_tasks_slice(self, search: TaskSearch, slice_reference: SliceReference) -> Slice[Task]:
        """
        Returns a slice of tasks that match the specified search and slice reference.

        :param search:         the search
        :param slice_reference: the slice reference
        :return: a slice of tasks
        @deprecated use #getTasks(TaskSearch) instead to search tasks.
        """

        pass

    @abstractmethod
    def get_tasks(self, search: TaskSearch) -> SearchClient[Task]:
        """
        Returns a SearchClient that offers the ability to search tasks.

        :param search: the search
        :return: the search client
        """

        pass
