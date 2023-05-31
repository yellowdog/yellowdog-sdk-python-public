from typing import List

from yellowdog_client.common import Proxy
from yellowdog_client.model import WorkRequirement, WorkRequirementStatus, WorkRequirementSummary, Task, \
    TaskSearch, SliceReference, Slice


class WorkServiceProxy:
    def __init__(self, proxy: Proxy) -> None:
        self._proxy: Proxy = proxy.append_base_url("/work/")

    def update_work_requirement(self, requirement: WorkRequirement) -> WorkRequirement:
        return self._proxy.put(WorkRequirement, requirement, "requirements")

    def add_work_requirement(self, requirement: WorkRequirement) -> WorkRequirement:
        return self._proxy.post(WorkRequirement, requirement, "requirements")

    def get_work_requirement_by_id(self, work_requirement_id: str) -> WorkRequirement:
        return self._proxy.get(WorkRequirement, "requirements/%s" % work_requirement_id)

    def get_work_requirement_by_name(self, namespace: str, work_requirement_name: str) -> WorkRequirement:
        return self._proxy.get(WorkRequirement, "namespaces/%s/requirements/%s" % (namespace, work_requirement_name))

    def transition_work_requirement(self, requirement_id: str,
                                    next_status: WorkRequirementStatus) -> WorkRequirement:
        url = "requirements/%s/transition/%s" % (requirement_id, str(next_status))
        return self._proxy.put(WorkRequirement, url=url)

    def find_all_work_requirements(self) -> List[WorkRequirementSummary]:
        return self._proxy.get(List[WorkRequirementSummary], "requirements")

    def stream_work_requirement_updates(self, requirement_id: str):
        return self._proxy.stream(f"requirements/{requirement_id}/updates")

    def add_tasks_to_task_group(self, task_group_id: str, tasks: List[Task]) -> List[Task]:
        return self._proxy.post(List[Task], tasks, "taskGroups/%s/tasks" % task_group_id)

    def add_tasks_to_task_group_by_name(
            self,
            namespace: str,
            requirement_name: str,
            task_group_name: str,
            tasks: List[Task]
    ) -> List[Task]:
        url = "namespaces/%s/requirements/%s/taskGroups/%s/tasks" % (namespace, requirement_name, task_group_name)
        return self._proxy.post(List[Task], tasks, url)

    def get_task_by_id(self, task_id: str) -> Task:
        return self._proxy.get(Task, "tasks/%s" % task_id)

    def cancel_task(self, task_id: str, abort: bool) -> Task:
        return self._proxy.put(Task, url="tasks/%s/cancel?abort=%s" % (task_id, abort))

    def search_tasks(self, search: TaskSearch, slice_reference: SliceReference) -> Slice[Task]:
        return self._proxy.get(Slice[Task], "tasks", self._proxy.to_params(search, slice_reference))
