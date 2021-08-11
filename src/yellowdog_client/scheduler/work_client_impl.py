from typing import Optional, List

from .work_client import WorkClient
from .work_service_proxy import WorkServiceProxy
from .work_requirement_helper import WorkRequirementHelper
from yellowdog_client.common.server_sent_events import SubscriptionManager
from yellowdog_client.common.server_sent_events import SubscriptionEventListener
from yellowdog_client.model import Identified
from yellowdog_client.model import WorkRequirement
from yellowdog_client.model import WorkRequirementStatus
from yellowdog_client.model import WorkRequirementSummary
from yellowdog_client.model import TaskGroup
from yellowdog_client.model import Task
from yellowdog_client.model import TaskSearch
from yellowdog_client.model import SliceReference
from yellowdog_client.model import Slice


class WorkClientImpl(WorkClient):
    def __init__(self, service_proxy: WorkServiceProxy) -> None:
        self.__service_proxy = service_proxy
        self.__requirement_subscriptions = SubscriptionManager(
            update_events_provider=self.__service_proxy.stream_work_requirement_updates,
            class_type=WorkRequirement
        )

    @staticmethod
    def _check_has_id(identified: Optional[Identified]) -> None:
        if not identified:
            raise ValueError("Provided entity may not be None")

        if not identified.id:
            raise ValueError(
                "Provided %s has not yet been submitted to YellowDog Scheduler" % identified.__class__.__name__
            )

    def add_work_requirement(self, work_requirement: WorkRequirement) -> WorkRequirement:
        return self.__service_proxy.add_work_requirement(work_requirement)

    def update_work_requirement(self, work_requirement: WorkRequirement) -> WorkRequirement:
        self._check_has_id(work_requirement)
        return self.__service_proxy.update_work_requirement(work_requirement)

    def get_work_requirement(self, work_requirement: WorkRequirement) -> WorkRequirement:
        return self.__service_proxy.get_work_requirement(work_requirement)

    def hold_work_requirement(self, work_requirement: WorkRequirement) -> WorkRequirement:
        return self.__service_proxy.transition_work_requirement(work_requirement, WorkRequirementStatus.HELD)

    def start_work_requirement(self, work_requirement: WorkRequirement) -> WorkRequirement:
        return self.__service_proxy.transition_work_requirement(work_requirement, WorkRequirementStatus.WORKING)

    def cancel_work_requirement(self, work_requirement: WorkRequirement) -> WorkRequirement:
        return self.__service_proxy.transition_work_requirement(work_requirement, WorkRequirementStatus.CANCELLING)

    def find_all_work_requirements(self) -> List[WorkRequirementSummary]:
        return self.__service_proxy.find_all_work_requirements()

    def get_work_requirement_by_name(self, namespace: str, work_requirement_name: str) -> WorkRequirement:
        return self.__service_proxy.get_work_requirement_by_name(namespace, work_requirement_name)

    def get_work_requirement_by_id(self, work_requirement_id: str) -> WorkRequirement:
        return self.__service_proxy.get_work_requirement_by_id(work_requirement_id)

    def add_work_requirement_listener(self, work_requirement: WorkRequirement, listener: SubscriptionEventListener[WorkRequirement]) -> None:
        self._check_has_id(work_requirement)
        self.__requirement_subscriptions.add_listener(work_requirement, listener)

    def remove_work_requirement_listener(self, listener: SubscriptionEventListener[WorkRequirement]) -> None:
        self.__requirement_subscriptions.remove_listener(listener)

    def get_work_requirement_helper(self, work_requirement: WorkRequirement) -> WorkRequirementHelper:
        return WorkRequirementHelper(work_requirement, self)

    def add_tasks_to_task_group(self, task_group: TaskGroup, tasks: List[Task]) -> List[Task]:
        self._check_has_id(task_group)
        return self.__service_proxy.add_tasks_to_task_group(task_group, tasks)

    def add_tasks_to_task_group_by_name(self, namespace: str, requirement_name: str, task_group_name: str, tasks: List[Task]) -> List[Task]:
        return self.__service_proxy.add_tasks_to_task_group_by_name(namespace, requirement_name, task_group_name, tasks)

    def get_task(self, task: Task) -> Task:
        return self.get_task_by_id(task.id)

    def get_task_by_id(self, task_id: str) -> Task:
        return self.__service_proxy.get_task_by_id(task_id)

    def cancel_task(self, task: Task) -> Task:
        self._check_has_id(task)
        return self.__service_proxy.cancel_task(task)

    def find_tasks(self, search: TaskSearch) -> List[Task]:
        slice = self.find_tasks_slice(search, SliceReference())
        items = slice.items

        while slice.nextSliceId is not None:
            slice = self.find_tasks_slice(search, SliceReference(slice.nextSliceId))
            items += slice.items

        return items

    def find_tasks_slice(self, search: TaskSearch, slice_reference: SliceReference) -> Slice:
        return self.__service_proxy.find_tasks_slice(search, slice_reference)

    def close(self) -> None:
        self.__requirement_subscriptions.close()
