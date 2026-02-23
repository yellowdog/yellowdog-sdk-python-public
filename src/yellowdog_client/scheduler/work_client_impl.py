from typing import Optional, List, Callable

from yellowdog_client.common import SearchClient, check
from yellowdog_client.common.pagination import paginate
from yellowdog_client.common.server_sent_events import SubscriptionEventListener
from yellowdog_client.common.server_sent_events import SubscriptionManager
from yellowdog_client.model import Slice
from yellowdog_client.model import SliceReference
from yellowdog_client.model import Task
from yellowdog_client.model import TaskGroup
from yellowdog_client.model import TaskSearch
from yellowdog_client.model import WorkRequirement
from yellowdog_client.model import WorkRequirementSearch
from yellowdog_client.model import WorkRequirementStatus
from yellowdog_client.model import WorkRequirementSummary
from .work_client import WorkClient
from .work_requirement_helper import WorkRequirementHelper
from .work_service_proxy import WorkServiceProxy


class WorkClientImpl(WorkClient):
    def __init__(self, service_proxy: WorkServiceProxy) -> None:
        self.__service_proxy = service_proxy
        self.__requirement_subscriptions = SubscriptionManager(
            update_events_provider=self.__service_proxy.stream_work_requirement_updates,
            class_type=WorkRequirement
        )

    def add_work_requirement(self, work_requirement: WorkRequirement) -> WorkRequirement:
        return self.__service_proxy.add_work_requirement(work_requirement)

    def update_work_requirement(self, work_requirement: WorkRequirement) -> WorkRequirement:
        check.not_none(work_requirement.id, "work_requirement.id")
        return self.__service_proxy.update_work_requirement(work_requirement)

    def get_work_requirement(self, work_requirement: WorkRequirement) -> WorkRequirement:
        id_ = check.not_none(work_requirement.id, "work_requirement.id")
        return self.get_work_requirement_by_id(id_)

    def get_work_requirement_by_id(self, work_requirement_id: str) -> WorkRequirement:
        return self.__service_proxy.get_work_requirement_by_id(work_requirement_id)

    def get_work_requirement_by_name(self, namespace: str, work_requirement_name: str) -> WorkRequirement:
        return self.__service_proxy.get_work_requirement_by_name(namespace, work_requirement_name)

    def hold_work_requirement(self, work_requirement: WorkRequirement) -> WorkRequirement:
        id_ = check.not_none(work_requirement.id, "work_requirement.id")
        return self.hold_work_requirement_by_id(id_)

    def hold_work_requirement_by_id(self, work_requirement_id: str) -> WorkRequirement:
        return self.__service_proxy.transition_work_requirement(work_requirement_id, WorkRequirementStatus.HELD, False)

    def start_work_requirement(self, work_requirement: WorkRequirement) -> WorkRequirement:
        id_ = check.not_none(work_requirement.id, "work_requirement.id")
        return self.start_work_requirement_by_id(id_)

    def start_work_requirement_by_id(self, work_requirement_id: str) -> WorkRequirement:
        return self.__service_proxy.transition_work_requirement(work_requirement_id, WorkRequirementStatus.RUNNING, False)

    def finish_work_requirement(self, work_requirement: WorkRequirement) -> WorkRequirement:
        id_ = check.not_none(work_requirement.id, "work_requirement.id")
        return self.finish_work_requirement_by_id(id_)

    def finish_work_requirement_by_id(self, work_requirement_id: str) -> WorkRequirement:
        return self.__service_proxy.transition_work_requirement(work_requirement_id, WorkRequirementStatus.FINISHING, False)

    def cancel_work_requirement(self, work_requirement: WorkRequirement, abort: Optional[bool] = False) -> WorkRequirement:
        id_ = check.not_none(work_requirement.id, "work_requirement.id")
        return self.cancel_work_requirement_by_id(id_, abort)

    def cancel_work_requirement_by_id(self, work_requirement_id: str, abort: Optional[bool] = None) -> WorkRequirement:
        if abort is None:
            abort = False
        return self.__service_proxy.transition_work_requirement(work_requirement_id, WorkRequirementStatus.CANCELLING, abort)

    def find_all_work_requirements(self) -> List[WorkRequirementSummary]:
        search = WorkRequirementSearch()
        return paginate(lambda sr: self._get_work_requirements_slice(search, sr))

    def get_work_requirements(self, search: WorkRequirementSearch) -> SearchClient[WorkRequirementSummary]:
        get_next_slice_function = lambda slice_reference: self._get_work_requirements_slice(search, slice_reference)
        return SearchClient(get_next_slice_function)

    def _get_work_requirements_slice(self, search: WorkRequirementSearch, slice_reference: SliceReference) -> Slice[WorkRequirementSummary]:
        return self.__service_proxy.find_work_requirements(search, slice_reference)

    def add_work_requirement_listener(self, work_requirement: WorkRequirement, listener: SubscriptionEventListener[WorkRequirement]) -> None:
        id_ = check.not_none(work_requirement.id, "work_requirement.id")
        self.add_work_requirement_listener_by_id(id_, listener)

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
        id_ = check.not_none(task_group.id, "task_group.id")
        return self.add_tasks_to_task_group_by_id(id_, tasks)

    def add_tasks_to_task_group_by_id(self, task_group_id: str, tasks: List[Task]) -> List[Task]:
        return self.__service_proxy.add_tasks_to_task_group(task_group_id, tasks)

    def add_tasks_to_task_group_by_name(self, namespace: str, requirement_name: str, task_group_name: str, tasks: List[Task]) -> List[Task]:
        return self.__service_proxy.add_tasks_to_task_group_by_name(namespace, requirement_name, task_group_name, tasks)

    def get_task(self, task: Task) -> Task:
        id_ = check.not_none(task.id, "task.id")
        return self.get_task_by_id(id_)

    def get_task_by_id(self, task_id: str) -> Task:
        return self.__service_proxy.get_task_by_id(task_id)

    def cancel_task(self, task: Task, abort: bool) -> Task:
        id_ = check.not_none(task.id, "task.id")
        return self.cancel_task_by_id(id_, abort)

    def cancel_task_by_id(self, task_id: str, abort: bool) -> Task:
        return self.__service_proxy.cancel_task(task_id, abort)

    def find_tasks(self, search: TaskSearch) -> List[Task]:
        return paginate(lambda sr: self.find_tasks_slice(search, sr))

    def find_tasks_slice(self, search: TaskSearch, slice_reference: SliceReference) -> Slice[Task]:
        return self.__service_proxy.search_tasks(search, slice_reference)

    def get_tasks(self, search: TaskSearch) -> SearchClient[Task]:
        get_next_slice_function: Callable[[SliceReference], Slice[Task]] = \
            lambda slice_reference: self.__service_proxy.search_tasks(search, slice_reference)

        return SearchClient(get_next_slice_function)

    def close(self) -> None:
        self.__requirement_subscriptions.close()
