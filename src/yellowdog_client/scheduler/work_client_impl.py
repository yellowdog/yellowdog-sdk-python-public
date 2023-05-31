from typing import Optional, List, Callable

from yellowdog_client.common.pagination import paginate
from yellowdog_client.common.server_sent_events import SubscriptionEventListener
from yellowdog_client.common.server_sent_events import SubscriptionManager
from yellowdog_client.model import Identified
from yellowdog_client.model import Slice
from yellowdog_client.model import SliceReference
from yellowdog_client.model import Task
from yellowdog_client.model import TaskGroup
from yellowdog_client.model import TaskSearch
from yellowdog_client.model import WorkRequirement
from yellowdog_client.model import WorkRequirementStatus
from yellowdog_client.model import WorkRequirementSummary
from .work_client import WorkClient
from .work_requirement_helper import WorkRequirementHelper
from .work_service_proxy import WorkServiceProxy
from yellowdog_client.common import SearchClient


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
        return self.get_work_requirement_by_id(work_requirement.id)

    def get_work_requirement_by_id(self, work_requirement_id: str) -> WorkRequirement:
        return self.__service_proxy.get_work_requirement_by_id(work_requirement_id)

    def get_work_requirement_by_name(self, namespace: str, work_requirement_name: str) -> WorkRequirement:
        return self.__service_proxy.get_work_requirement_by_name(namespace, work_requirement_name)

    def hold_work_requirement(self, work_requirement: WorkRequirement) -> WorkRequirement:
        return self.hold_work_requirement_by_id(work_requirement.id)

    def hold_work_requirement_by_id(self, work_requirement_id: str) -> WorkRequirement:
        return self.__service_proxy.transition_work_requirement(work_requirement_id, WorkRequirementStatus.HELD)

    def start_work_requirement(self, work_requirement: WorkRequirement) -> WorkRequirement:
        return self.start_work_requirement_by_id(work_requirement.id)

    def start_work_requirement_by_id(self, work_requirement_id: str) -> WorkRequirement:
        return self.__service_proxy.transition_work_requirement(work_requirement_id, WorkRequirementStatus.RUNNING)

    def cancel_work_requirement(self, work_requirement: WorkRequirement) -> WorkRequirement:
        return self.cancel_work_requirement_by_id(work_requirement.id)

    def cancel_work_requirement_by_id(self, work_requirement_id: str) -> WorkRequirement:
        return self.__service_proxy.transition_work_requirement(work_requirement_id, WorkRequirementStatus.CANCELLING)

    def find_all_work_requirements(self) -> List[WorkRequirementSummary]:
        return self.__service_proxy.find_all_work_requirements()

    def add_work_requirement_listener(self, work_requirement: WorkRequirement, listener: SubscriptionEventListener[WorkRequirement]) -> None:
        self._check_has_id(work_requirement)
        self.add_work_requirement_listener_by_id(work_requirement.id, listener)

    def add_work_requirement_listener_by_id(self, work_requirement_id: str, listener: SubscriptionEventListener[WorkRequirement]) -> None:
        self.__requirement_subscriptions.add_listener(work_requirement_id, listener)

    def remove_work_requirement_listener(self, listener: SubscriptionEventListener[WorkRequirement]) -> None:
        self.__requirement_subscriptions.remove_listener(listener)

    def get_work_requirement_helper(self, work_requirement: WorkRequirement) -> WorkRequirementHelper:
        return WorkRequirementHelper(work_requirement, self)

    def get_work_requirement_helper_by_id(self, work_requirement_id: str) -> WorkRequirementHelper:
        work_requirement = self.get_work_requirement_by_id(work_requirement_id)
        return self.get_work_requirement_helper(work_requirement)

    def add_tasks_to_task_group(self, task_group: TaskGroup, tasks: List[Task]) -> List[Task]:
        self._check_has_id(task_group)
        return self.add_tasks_to_task_group_by_id(task_group.id, tasks)

    def add_tasks_to_task_group_by_id(self, task_group_id: str, tasks: List[Task]) -> List[Task]:
        return self.__service_proxy.add_tasks_to_task_group(task_group_id, tasks)

    def add_tasks_to_task_group_by_name(self, namespace: str, requirement_name: str, task_group_name: str, tasks: List[Task]) -> List[Task]:
        return self.__service_proxy.add_tasks_to_task_group_by_name(namespace, requirement_name, task_group_name, tasks)

    def get_task(self, task: Task) -> Task:
        return self.get_task_by_id(task.id)

    def get_task_by_id(self, task_id: str) -> Task:
        return self.__service_proxy.get_task_by_id(task_id)

    def cancel_task(self, task: Task, abort: bool) -> Task:
        self._check_has_id(task)
        return self.cancel_task_by_id(task.id, abort)

    def cancel_task_by_id(self, task_id: str, abort: bool) -> Task:
        return self.__service_proxy.cancel_task(task_id, abort)

    def find_tasks(self, search: TaskSearch) -> List[Task]:
        return paginate(lambda sr: self.find_tasks_slice(search, sr))

    def find_tasks_slice(self, search: TaskSearch, slice_reference: SliceReference) -> Slice:
        return self.__service_proxy.search_tasks(search, slice_reference)

    def get_tasks(self, search: TaskSearch) -> SearchClient[Task]:
        get_next_slice_function: Callable[[SliceReference], Slice[Task]] = \
            lambda slice_reference: self.__service_proxy.search_tasks(search, slice_reference)

        return SearchClient(get_next_slice_function)

    def close(self) -> None:
        self.__requirement_subscriptions.close()
