from typing import List

from yellowdog_client.common import Proxy
from yellowdog_client.model import WorkRequirement, WorkRequirementStatus, WorkRequirementSummary, TaskGroup, Task, \
    TaskSearch, SliceReference, Slice


class WorkServiceProxy:
    def __init__(self, proxy: Proxy) -> None:
        self._proxy: Proxy = proxy.append_base_url("/work/")

    def update_work_requirement(self, requirement: WorkRequirement) -> WorkRequirement:
        return self._proxy.put(WorkRequirement, requirement, "requirements")

    def add_work_requirement(self, requirement: WorkRequirement) -> WorkRequirement:
        return self._proxy.post(WorkRequirement, requirement, "requirements")

    def get_work_requirement(self, work_requirement: WorkRequirement) -> WorkRequirement:
        return self._proxy.get(WorkRequirement, "requirements/%s" % work_requirement.id)

    def transition_work_requirement(self, requirement: WorkRequirement,
                                    next_status: WorkRequirementStatus) -> WorkRequirement:
        url = "requirements/%s/transition/%s" % (requirement.id, str(next_status))
        return self._proxy.put(WorkRequirement, url=url)

    def find_all_work_requirements(self) -> List[WorkRequirementSummary]:
        return self._proxy.get(List[WorkRequirementSummary], "requirements")

    def get_work_requirement_by_id(self, work_requirement_id: str) -> WorkRequirement:
        return self._proxy.get(WorkRequirement, "requirements/%s" % work_requirement_id)

    def get_work_requirement_by_name(self, namespace: str, work_requirement_name: str) -> WorkRequirement:
        return self._proxy.get(WorkRequirement, "namespaces/%s/requirements/%s" % (namespace, work_requirement_name))

    def stream_work_requirement_updates(self, requirement):
        return self._proxy.stream("requirements/%s/updates" % requirement.id)

    def add_tasks_to_task_group(self, task_group: TaskGroup, tasks: List[Task]) -> List[Task]:
        return self._proxy.post(List[Task], tasks, "taskGroups/%s/tasks" % task_group.id)

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

    def cancel_task(self, task: Task) -> Task:
        return self._proxy.put(Task, url="tasks/%s/cancel" % task.id)

    def find_tasks_slice(self, search: TaskSearch, slice_reference: SliceReference) -> Slice[Task]:
        return self._proxy.get(Slice[Task], "tasks", self._proxy.to_params(search, slice_reference))
