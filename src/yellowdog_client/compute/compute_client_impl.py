from typing import List, Optional


from yellowdog_client.common import SearchClient, check
from yellowdog_client.common.server_sent_events import SubscriptionEventListener
from yellowdog_client.common.server_sent_events import SubscriptionManager
from yellowdog_client.model import BestComputeSourceReport, ComputeRequirementSearch, SliceReference, Slice, \
    InstanceSearch, InstanceId, ComputeSourceTemplateSearch, ComputeRequirementTemplateSearch
from yellowdog_client.model import ComputeRequirement, ComputeRequirementTemplateUsage
from yellowdog_client.model import ComputeRequirementStatus
from yellowdog_client.model import ComputeRequirementSummary
from yellowdog_client.model import ComputeRequirementSummarySearch
from yellowdog_client.model import ComputeRequirementTemplateSummary
from yellowdog_client.model import ComputeRequirementTemplateTestResult
from yellowdog_client.model import ComputeSourceTemplate
from yellowdog_client.model import ComputeSourceTemplateSummary
from yellowdog_client.model import Instance, ComputeRequirementTemplate
from yellowdog_client.model import InstanceStatus
from .compute_client import ComputeClient
from .compute_requirement_helper import ComputeRequirementHelper
from .compute_service_proxy import ComputeServiceProxy


class ComputeClientImpl(ComputeClient):
    def __init__(self, service_proxy: ComputeServiceProxy) -> None:
        self.__service_proxy: ComputeServiceProxy = service_proxy
        self.__requirement_subscriptions = SubscriptionManager(self.__service_proxy.stream_compute_requirement_updates, ComputeRequirement)

    @staticmethod
    def _get_instance_ids(instances: List[Instance]) -> List[InstanceId]:
        return [instance.id for instance in instances if instance.id is not None]

    def add_compute_requirement(self, compute_requirement: ComputeRequirement) -> ComputeRequirement:
        return self.__service_proxy.add_compute_requirement(compute_requirement)

    def update_compute_requirement(self, compute_requirement: ComputeRequirement, reprovision: Optional[bool] = None) -> ComputeRequirement:
        if reprovision is None:
            reprovision = False
        return self.__service_proxy.update_compute_requirement(compute_requirement, reprovision)

    def get_compute_requirement(self, compute_requirement: ComputeRequirement) -> ComputeRequirement:
        id_ = check.not_none(compute_requirement.id, "compute_requirement.id")
        return self.get_compute_requirement_by_id(id_)

    def get_compute_requirement_by_id(self, compute_requirement_id: str) -> ComputeRequirement:
        return self.__service_proxy.get_compute_requirement_by_id(compute_requirement_id)

    def get_compute_requirement_by_name(self, namespace: str, compute_requirement_name: str) -> ComputeRequirement:
        return self.__service_proxy.get_compute_requirement_by_name(namespace, compute_requirement_name)

    def stop_compute_requirement(self, compute_requirement: ComputeRequirement) -> ComputeRequirement:
        id_ = check.not_none(compute_requirement.id, "compute_requirement.id")
        return self.stop_compute_requirement_by_id(id_)

    def stop_compute_requirement_by_id(self, compute_requirement_id: str) -> ComputeRequirement:
        return self.__service_proxy.transition_compute_requirement(compute_requirement_id,
                                                                   ComputeRequirementStatus.STOPPED)

    def start_compute_requirement(self, compute_requirement: ComputeRequirement) -> ComputeRequirement:
        id_ = check.not_none(compute_requirement.id, "compute_requirement.id")
        return self.start_compute_requirement_by_id(id_)

    def start_compute_requirement_by_id(self, compute_requirement_id: str) -> ComputeRequirement:
        return self.__service_proxy.transition_compute_requirement(compute_requirement_id,
                                                                   ComputeRequirementStatus.RUNNING)

    def terminate_compute_requirement(self, compute_requirement: ComputeRequirement) -> ComputeRequirement:
        id_ = check.not_none(compute_requirement.id, "compute_requirement.id")
        return self.terminate_compute_requirement_by_id(id_)

    def terminate_compute_requirement_by_id(self, compute_requirement_id: str) -> ComputeRequirement:
        return self.__service_proxy.transition_compute_requirement(compute_requirement_id,
                                                                   ComputeRequirementStatus.TERMINATED)

    def reprovision_compute_requirement(self, compute_requirement: ComputeRequirement) -> ComputeRequirement:
        id_ = check.not_none(compute_requirement.id, "compute_requirement.id")
        return self.reprovision_compute_requirement_by_id(id_)

    def reprovision_compute_requirement_by_id(self, compute_requirement_id: str) -> ComputeRequirement:
        return self.__service_proxy.transition_compute_requirement(compute_requirement_id,
                                                                   ComputeRequirementStatus.PROVISIONING)

    def get_instances(self, instance_search: InstanceSearch) -> SearchClient[Instance]:
        def get_next_slice_function(slice_reference: SliceReference) -> Slice[Instance]:
            return self.__service_proxy.search_instances(instance_search, slice_reference)

        return SearchClient(get_next_slice_function)

    def stop_instances(self, compute_requirement: ComputeRequirement, instances: List[Instance]) -> None:
        self.stop_instances_by_id(compute_requirement, self._get_instance_ids(instances))

    def stop_instances_by_id(self, compute_requirement: ComputeRequirement, instance_ids: List[InstanceId]) -> None:
        self._transition_instances(compute_requirement, InstanceStatus.STOPPED, instance_ids)

    def start_instances(self, compute_requirement: ComputeRequirement, instances: List[Instance]) -> None:
        self.start_instances_by_id(compute_requirement, self._get_instance_ids(instances))

    def start_instances_by_id(self, compute_requirement: ComputeRequirement, instance_ids: List[InstanceId]) -> None:
        self._transition_instances(compute_requirement, InstanceStatus.RUNNING, instance_ids)

    def terminate_instances(self, compute_requirement: ComputeRequirement, instances: List[Instance]) -> None:
        self.terminate_instances_by_id(compute_requirement, self._get_instance_ids(instances))

    def terminate_instances_by_id(self, compute_requirement: ComputeRequirement,
                                  instance_ids: List[InstanceId]) -> None:
        self._transition_instances(compute_requirement, InstanceStatus.TERMINATED, instance_ids)

    def restart_instances(self, compute_requirement: ComputeRequirement, instances: List[Instance]) -> None:
        self.restart_instances_by_id(compute_requirement, self._get_instance_ids(instances))

    def restart_instances_by_id(self, compute_requirement: ComputeRequirement, instance_ids: List[InstanceId]) -> None:
        self._transition_instances(compute_requirement, InstanceStatus.PENDING, instance_ids)

    def deprovision_instances(self, compute_requirement: ComputeRequirement, instances: List[Instance]) -> None:
        self.deprovision_instances_by_id(compute_requirement, self._get_instance_ids(instances))

    def deprovision_instances_by_id(self, compute_requirement: ComputeRequirement,
                                    instance_ids: List[InstanceId]) -> None:
        check.not_none(compute_requirement.id, "compute_requirement.id")
        self.__service_proxy.deprovision_instances(compute_requirement, instance_ids)

    def is_compute_requirement_updating(self, compute_requirement: ComputeRequirement) -> bool:
        id_ = check.not_none(compute_requirement.id, "compute_requirement.id")
        return self.is_compute_requirement_updating_by_id(id_)

    def is_compute_requirement_updating_by_id(self, compute_requirement_id: str) -> bool:
        return self.__service_proxy.is_compute_requirement_updating(compute_requirement_id)

    def add_compute_requirement_listener(self, compute_requirement: ComputeRequirement,
                                         listener: SubscriptionEventListener[ComputeRequirement]) -> None:
        id_ = check.not_none(compute_requirement.id, "compute_requirement.id")
        self.add_compute_requirement_listener_by_id(id_, listener)

    def add_compute_requirement_listener_by_id(self, compute_requirement_id: str,
                                               listener: SubscriptionEventListener[ComputeRequirement]) -> None:
        self.__requirement_subscriptions.add_listener(compute_requirement_id, listener)

    def remove_compute_requirement_listener(self, listener: SubscriptionEventListener[ComputeRequirement]) -> None:
        self.__requirement_subscriptions.remove_listener(listener)

    def get_compute_requirement_helper(self, compute_requirement: ComputeRequirement) -> ComputeRequirementHelper:
        check.not_none(compute_requirement.id, "compute_requirement.id")
        return ComputeRequirementHelper(compute_requirement, self)

    def get_compute_requirement_helper_by_id(self, compute_requirement_id: str) -> ComputeRequirementHelper:
        compute_requirement = self.get_compute_requirement_by_id(compute_requirement_id)
        return self.get_compute_requirement_helper(compute_requirement)

    def get_compute_requirements(
            self,
            compute_requirement_search: ComputeRequirementSearch
    ) -> SearchClient[ComputeRequirement]:
        def get_next_slice_function(slice_reference: SliceReference) -> Slice[ComputeRequirement]:
            return self.__service_proxy.search_compute_requirements(
                compute_requirement_search,
                slice_reference
            )

        return SearchClient(get_next_slice_function)

    def get_compute_requirement_summaries(
            self,
            compute_requirement_summary_search: ComputeRequirementSummarySearch
    ) -> SearchClient[ComputeRequirementSummary]:
        def get_next_slice_function(slice_reference: SliceReference) -> Slice[ComputeRequirementSummary]:
            return self.__service_proxy.search_compute_requirement_summaries(
                compute_requirement_summary_search,
                slice_reference
            )

        return SearchClient(get_next_slice_function)

    def add_compute_source_template(self, compute_source_template: ComputeSourceTemplate) -> ComputeSourceTemplate:
        return self.__service_proxy.add_compute_source_template(compute_source_template)

    def update_compute_source_template(self, compute_source_template: ComputeSourceTemplate) -> ComputeSourceTemplate:
        return self.__service_proxy.update_compute_source_template(compute_source_template)

    def delete_compute_source_template(self, compute_source_template: ComputeSourceTemplate) -> None:
        id_ = check.not_none(compute_source_template.id, "compute_source_template.id")
        self.delete_compute_source_template_by_id(id_)

    def delete_compute_source_template_by_id(self, compute_source_template_id: str) -> None:
        self.__service_proxy.delete_compute_source_template(compute_source_template_id)

    def get_compute_source_template(self, compute_source_template_id: str) -> ComputeSourceTemplate:
        return self.__service_proxy.get_compute_source_template_by_id(compute_source_template_id)

    def get_compute_source_template_by_name(self, namespace: str, compute_source_template_name: str) -> ComputeSourceTemplate:
        return self.__service_proxy.get_compute_source_template_by_name(namespace, compute_source_template_name)

    def find_all_compute_source_templates(self) -> List[ComputeSourceTemplateSummary]:
        return self.__service_proxy.find_all_compute_source_templates()

    def get_compute_source_templates(self, search: ComputeSourceTemplateSearch) -> SearchClient[ComputeSourceTemplateSummary]:
        def get_next_slice_function(slice_reference: SliceReference) -> Slice[ComputeSourceTemplateSummary]:
            return self.__service_proxy.search_compute_source_templates(search, slice_reference)

        return SearchClient(get_next_slice_function)

    def add_compute_requirement_template(self, template: ComputeRequirementTemplate) -> ComputeRequirementTemplate:
        return self.__service_proxy.add_compute_requirement_template(template)

    def update_compute_requirement_template(
            self,
            compute_requirement_template: ComputeRequirementTemplate
    ) -> ComputeRequirementTemplate:
        return self.__service_proxy.update_compute_requirement_template(compute_requirement_template)

    def delete_compute_requirement_template(self, compute_requirement_template: ComputeRequirementTemplate) -> None:
        if compute_requirement_template.id is None:
            raise ValueError("compute_requirement_template.id must not be None")
        self.delete_compute_requirement_template_by_id(compute_requirement_template.id)

    def delete_compute_requirement_template_by_id(self, compute_requirement_template_id: str) -> None:
        self.__service_proxy.delete_compute_requirement_template(compute_requirement_template_id)

    def get_compute_requirement_template(self, compute_requirement_template_id: str) -> ComputeRequirementTemplate:
        return self.__service_proxy.get_compute_requirement_template_by_id(compute_requirement_template_id)

    def get_compute_requirement_template_by_id(self, compute_requirement_template_id: str) -> ComputeRequirementTemplate:
        return self.__service_proxy.get_compute_requirement_template_by_id(compute_requirement_template_id)

    def get_compute_requirement_template_by_name(self, namespace: str, name: str) -> ComputeRequirementTemplate:
        return self.__service_proxy.get_compute_requirement_template_by_name(namespace, name)

    def find_all_compute_requirement_templates(self) -> List[ComputeRequirementTemplateSummary]:
        return self.__service_proxy.find_all_compute_requirement_templates()

    def get_compute_requirement_templates(self, search: ComputeRequirementTemplateSearch) -> SearchClient[ComputeRequirementTemplateSummary]:
        def get_next_slice_function(slice_reference: SliceReference) -> Slice[ComputeRequirementTemplateSummary]:
            return self.__service_proxy.search_compute_requirement_templates(search, slice_reference)

        return SearchClient(get_next_slice_function)

    def provision_compute_requirement_template(self,
                                               template_request: ComputeRequirementTemplateUsage) -> ComputeRequirement:
        return self.__service_proxy.provision_compute_requirement_template(template_request)

    def test_compute_requirement_template(self,
                                          template_usage: ComputeRequirementTemplateUsage) -> ComputeRequirementTemplateTestResult:
        return self.__service_proxy.test_compute_requirement_template(template_usage)

    def get_best_compute_source_report_by_compute_requirement(self,
                                                              provisioned_requirement_id: str) -> BestComputeSourceReport:
        return self.__service_proxy.get_best_compute_source_report_by_requirement_id(provisioned_requirement_id)

    def close(self) -> None:
        self.__requirement_subscriptions.close()

    def _transition_instances(
            self,
            compute_requirement: ComputeRequirement,
            next_status: InstanceStatus,
            instance_ids: List[InstanceId]
    ) -> None:
        self.__service_proxy.transition_instances(compute_requirement, next_status, instance_ids)
