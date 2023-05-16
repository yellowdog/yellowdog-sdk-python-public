from typing import List

from yellowdog_client.common import Proxy
from yellowdog_client.common.server_sent_events.sse4python import EventSource
from yellowdog_client.model import ComputeRequirementTemplate, ComputeRequirementStatus, ComputeRequirementSearch, \
    SliceReference, Slice, InstanceSearch, Instance, InstanceId
from yellowdog_client.model import InstanceStatus, \
    ComputeRequirement, ComputeRequirementTemplateSummary, ComputeSourceTemplate, ComputeRequirementTemplateUsage, \
    ComputeSourceTemplateSummary, ComputeRequirementTemplateTestResult, BestComputeSourceReport


class ComputeServiceProxy:
    def __init__(self, proxy: Proxy) -> None:
        self._proxy: Proxy = proxy.append_base_url("/compute/")

    def add_compute_requirement(self, compute_requirement: ComputeRequirement) -> ComputeRequirement:
        return self._proxy.post(ComputeRequirement, compute_requirement, "requirements")

    def update_compute_requirement(self, compute_requirement: ComputeRequirement, reprovision: bool):
        return self._proxy.put(ComputeRequirement, compute_requirement, "requirements?reprovision=%s" % reprovision)

    def get_compute_requirement_by_id(self, compute_requirement_id: str) -> ComputeRequirement:
        return self._proxy.get(ComputeRequirement, "requirements/%s" % compute_requirement_id)

    def get_compute_requirement_by_name(self, namespace: str, compute_requirement_name: str) -> ComputeRequirement:
        url = "namespaces/%s/requirements/%s" % (namespace, compute_requirement_name)
        return self._proxy.get(ComputeRequirement, url)

    def transition_compute_requirement(self, compute_requirement_id: str, next_status: ComputeRequirementStatus):
        url = "requirements/%s/transition/%s" % (compute_requirement_id, next_status.value)
        return self._proxy.put(ComputeRequirement, url=url)

    def deprovision_instances(self, compute_requirement: ComputeRequirement, instance_ids: List[InstanceId]) -> None:
        self._proxy.put(data=instance_ids, url="requirements/%s/instances/deprovision" % compute_requirement.id)

    def search_instances(self, search: InstanceSearch, slice_reference: SliceReference) -> Slice[Instance]:
        return self._proxy.get(
            Slice[Instance], "instances",
            self._proxy.to_params(search, slice_reference)
        )

    def transition_instances(
            self,
            compute_requirement: ComputeRequirement,
            next_status: InstanceStatus,
            instance_ids: List[InstanceId]
    ) -> None:
        url = "requirements/%s/instances/transition/%s" % (compute_requirement.id, next_status.name)
        self._proxy.put(data=instance_ids, url=url)

    def stream_compute_requirement_updates(self, compute_requirement_id: str) -> EventSource:
        return self._proxy.stream("requirements/%s/updates" % compute_requirement_id)

    def is_compute_requirement_updating(self, compute_requirement_id: str) -> bool:
        return self._proxy.raw_execute("GET", "requirements/%s/updating" % compute_requirement_id).json()

    def search_compute_requirements(
            self,
            search: ComputeRequirementSearch,
            slice_reference: SliceReference
    ) -> Slice[ComputeRequirement]:
        return self._proxy.get(Slice[ComputeRequirement], "requirements",
                               self._proxy.to_params(search, slice_reference))

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

    def test_compute_requirement_template(self,
                                          template_usage: ComputeRequirementTemplateUsage) -> ComputeRequirementTemplateTestResult:
        return self._proxy.put(ComputeRequirementTemplateTestResult, template_usage, "templates/test")

    def get_best_compute_source_report_by_requirement_id(self,
                                                         provisioned_requirement_id: str) -> BestComputeSourceReport:
        return self._proxy.get(BestComputeSourceReport, "templates/provision/report/%s" % provisioned_requirement_id)
