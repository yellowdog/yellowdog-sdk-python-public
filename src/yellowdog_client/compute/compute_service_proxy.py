import copy
from typing import List

from yellowdog_client.common import Proxy
from yellowdog_client.common.server_sent_events.sse4python import EventSource
from yellowdog_client.model import ComputeRequirementTemplate, ComputeRequirementStatus
from yellowdog_client.model import InstanceStatus, ComputeRequirementSummary, \
    ComputeRequirement, ComputeRequirementTemplateSummary, ComputeSourceTemplate, ComputeRequirementTemplateUsage, \
    ComputeSourceTemplateSummary, ComputeRequirementTemplateTestResult, BestComputeSourceReport


class ComputeServiceProxy:
    def __init__(self, proxy: Proxy) -> None:
        self._proxy: Proxy = proxy.append_base_url("/compute/")

    def add_compute_requirement(self, compute_requirement: ComputeRequirement) -> ComputeRequirement:
        return self._proxy.post(ComputeRequirement, compute_requirement, "requirements")

    def update_compute_requirement(self, compute_requirement: ComputeRequirement, reprovision: bool):
        copied = copy.deepcopy(compute_requirement)
        copied.instances = None

        return self._proxy.put(ComputeRequirement, copied, "requirements?reprovision=%s" % reprovision)

    def get_compute_requirement_by_id(self, compute_requirement_id: str) -> ComputeRequirement:
        return self._proxy.get(ComputeRequirement, "requirements/%s" % compute_requirement_id)

    def get_compute_requirement_by_name(self, namespace: str, compute_requirement_name: str) -> ComputeRequirement:
        url = "namespaces/%s/requirements/%s" % (namespace, compute_requirement_name)
        return self._proxy.get(ComputeRequirement, url)

    def transition_compute_requirement(self, compute_requirement_id: str, next_status: ComputeRequirementStatus):
        url = "requirements/%s/transition/%s" % (compute_requirement_id, next_status.value)
        return self._proxy.put(ComputeRequirement, url=url)

    def deprovision_instances(self, compute_requirement: ComputeRequirement, instance_ids: List[str]) -> None:
        self._proxy.put(data=instance_ids, url="requirements/%s/instances/deprovision" % compute_requirement.id)

    def transition_instances(
            self,
            compute_requirement: ComputeRequirement,
            next_status: InstanceStatus,
            instance_ids: List[str]
    ) -> None:
        url = "requirements/%s/instances/transition/%s" % (compute_requirement.id, next_status.name)
        self._proxy.put(data=instance_ids, url=url)

    def stream_compute_requirement_updates(self, compute_requirement_id: str) -> EventSource:
        return self._proxy.stream("requirements/%s/updates" % compute_requirement_id)

    def is_compute_requirement_updating(self, compute_requirement_id: str) -> bool:
        return self._proxy.raw_execute("GET", "requirements/%s/updating" % compute_requirement_id).json()

    def find_all_compute_requirements(self) -> List[ComputeRequirementSummary]:
        return self._proxy.get(List[ComputeRequirementSummary], "requirements")

    def add_compute_source_template(self, compute_source_template: ComputeSourceTemplate) -> ComputeSourceTemplate:
        return self._proxy.post(ComputeSourceTemplate, compute_source_template, "templates/sources")

    def update_compute_source_template(self, compute_source_template: ComputeSourceTemplate) -> ComputeSourceTemplate:
        return self._proxy.put(ComputeSourceTemplate, compute_source_template, "templates/sources")

    def delete_compute_source_template(self, compute_source_template_id: str) -> None:
        self._proxy.delete("templates/sources/%s" % compute_source_template_id)

    def get_compute_source_template_by_id(self, compute_source_template_id: str) -> ComputeSourceTemplate:
        return self._proxy.get(ComputeSourceTemplate, "templates/sources/%s" % compute_source_template_id)

    def find_all_compute_source_templates(self) -> List[ComputeSourceTemplateSummary]:
        return self._proxy.get(List[ComputeSourceTemplateSummary], "templates/sources")

    def add_compute_requirement_template(
            self,
            template: ComputeRequirementTemplate
    ) -> ComputeRequirementTemplate:
        return self._proxy.post(ComputeRequirementTemplate, template, "templates/requirements")

    def update_compute_requirement_template(
            self,
            template: ComputeRequirementTemplate
    ) -> ComputeRequirementTemplate:
        return self._proxy.put(ComputeRequirementTemplate, template, "templates/requirements")

    def delete_compute_requirement_template(self, template_id: str) -> None:
        self._proxy.delete("templates/requirements/%s" % template_id)

    def get_compute_requirement_template_by_id(self, template_id: str) -> ComputeRequirementTemplate:
        return self._proxy.get(ComputeRequirementTemplate, "templates/requirements/%s" % template_id)

    def find_all_compute_requirement_templates(self) -> List[ComputeRequirementTemplateSummary]:
        return self._proxy.get(List[ComputeRequirementTemplateSummary], "templates/requirements")

    def provision_compute_requirement_template(self, usage: ComputeRequirementTemplateUsage) -> ComputeRequirement:
        return self._proxy.post(ComputeRequirement, usage, "templates/provision")

    def test_compute_requirement_template(self, template_usage: ComputeRequirementTemplateUsage) -> ComputeRequirementTemplateTestResult:
        return self._proxy.put(ComputeRequirementTemplateTestResult, template_usage, "templates/test")

    def get_best_compute_source_report_by_requirement_id(self, provisioned_requirement_id: str) -> BestComputeSourceReport:
        return self._proxy.get(BestComputeSourceReport, "templates/provision/report/%s" % provisioned_requirement_id)
