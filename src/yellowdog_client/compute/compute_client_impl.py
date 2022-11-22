from typing import List, Optional

from yellowdog_client.common.server_sent_events import SubscriptionEventListener
from yellowdog_client.common.server_sent_events import SubscriptionManager
from yellowdog_client.model import BestComputeSourceReport
from yellowdog_client.model import ComputeRequirement, ComputeRequirementTemplateUsage
from yellowdog_client.model import ComputeRequirementStatus
from yellowdog_client.model import ComputeRequirementSummary
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
        self.__requirement_subscriptions = SubscriptionManager(self.__service_proxy.stream_compute_requirement_updates,
                                                               ComputeRequirement)

    @staticmethod
    def _check_requirement_has_id(compute_requirement: Optional[ComputeRequirement]) -> None:
        if not compute_requirement or not compute_requirement.id:
            raise ValueError(
                "Provided compute requirement has not been initialised. "
                "Have you captured the return value from compute_client.add_compute_requirement()?"
            )

    @staticmethod
    def _get_instance_ids(instances: List[Instance]) -> List[str]:
        return [instance.id for instance in instances]

    def add_compute_requirement(self, compute_requirement: ComputeRequirement) -> ComputeRequirement:
        return self.__service_proxy.add_compute_requirement(compute_requirement)

    def update_compute_requirement(self, compute_requirement: ComputeRequirement, reprovision: bool = False) -> ComputeRequirement:
        return self.__service_proxy.update_compute_requirement(compute_requirement, reprovision)

    def get_compute_requirement(self, compute_requirement: ComputeRequirement) -> ComputeRequirement:
        self._check_requirement_has_id(compute_requirement)
        return self.get_compute_requirement_by_id(compute_requirement.id)

    def get_compute_requirement_by_id(self, compute_requirement_id: str) -> ComputeRequirement:
        return self.__service_proxy.get_compute_requirement_by_id(compute_requirement_id)

    def get_compute_requirement_by_name(self, namespace: str, compute_requirement_name: str) -> ComputeRequirement:
        return self.__service_proxy.get_compute_requirement_by_name(namespace, compute_requirement_name)

    def stop_compute_requirement(self, compute_requirement: ComputeRequirement) -> ComputeRequirement:
        self._check_requirement_has_id(compute_requirement)
        return self.stop_compute_requirement_by_id(compute_requirement.id)

    def stop_compute_requirement_by_id(self, compute_requirement_id: str) -> ComputeRequirement:
        return self.__service_proxy.transition_compute_requirement(compute_requirement_id, ComputeRequirementStatus.STOPPED)

    def start_compute_requirement(self, compute_requirement: ComputeRequirement) -> ComputeRequirement:
        self._check_requirement_has_id(compute_requirement)
        return self.start_compute_requirement_by_id(compute_requirement.id)

    def start_compute_requirement_by_id(self, compute_requirement_id: str) -> ComputeRequirement:
        return self.__service_proxy.transition_compute_requirement(compute_requirement_id, ComputeRequirementStatus.RUNNING)

    def terminate_compute_requirement(self, compute_requirement: ComputeRequirement) -> ComputeRequirement:
        self._check_requirement_has_id(compute_requirement)
        return self.terminate_compute_requirement_by_id(compute_requirement.id)

    def terminate_compute_requirement_by_id(self, compute_requirement_id: str) -> ComputeRequirement:
        return self.__service_proxy.transition_compute_requirement(compute_requirement_id, ComputeRequirementStatus.TERMINATED)

    def reprovision_compute_requirement(self, compute_requirement: ComputeRequirement) -> ComputeRequirement:
        self._check_requirement_has_id(compute_requirement)
        return self.reprovision_compute_requirement_by_id(compute_requirement.id)

    def reprovision_compute_requirement_by_id(self, compute_requirement_id: str) -> ComputeRequirement:
        return self.__service_proxy.transition_compute_requirement(compute_requirement_id,
                                                                   ComputeRequirementStatus.PROVISIONING)

    def stop_instances(self, compute_requirement: ComputeRequirement, instances: List[Instance]) -> None:
        self._transition_instances(compute_requirement, InstanceStatus.STOPPED, instances)

    def start_instances(self, compute_requirement: ComputeRequirement, instances: List[Instance]) -> None:
        self._transition_instances(compute_requirement, InstanceStatus.RUNNING, instances)

    def terminate_instances(self, compute_requirement: ComputeRequirement, instances: List[Instance]) -> None:
        self._transition_instances(compute_requirement, InstanceStatus.TERMINATED, instances)

    def restart_instances(self, compute_requirement: ComputeRequirement, instances: List[Instance]) -> None:
        self._transition_instances(compute_requirement, InstanceStatus.PENDING, instances)

    def deprovision_instances(self, compute_requirement: ComputeRequirement, instances: List[Instance]) -> None:
        self._check_requirement_has_id(compute_requirement)
        self._check_all_instances_belong_to_compute_requirement(compute_requirement, instances)
        self.__service_proxy.deprovision_instances(compute_requirement, self._get_instance_ids(instances))

    def is_compute_requirement_updating(self, compute_requirement: ComputeRequirement) -> bool:
        self._check_requirement_has_id(compute_requirement)
        return self.is_compute_requirement_updating_by_id(compute_requirement.id)

    def is_compute_requirement_updating_by_id(self, compute_requirement_id: str) -> bool:
        return self.__service_proxy.is_compute_requirement_updating(compute_requirement_id)

    def add_compute_requirement_listener(self, compute_requirement: ComputeRequirement, listener: SubscriptionEventListener) -> None:
        self._check_requirement_has_id(compute_requirement)
        self.add_compute_requirement_listener_by_id(compute_requirement.id, listener)

    def add_compute_requirement_listener_by_id(self, compute_requirement_id: str, listener: SubscriptionEventListener) -> None:
        self.__requirement_subscriptions.add_listener(compute_requirement_id, listener)

    def remove_compute_requirement_listener(self, listener: SubscriptionEventListener[ComputeRequirement]):
        self.__requirement_subscriptions.remove_listener(listener)

    def get_compute_requirement_helper(self, compute_requirement: ComputeRequirement) -> ComputeRequirementHelper:
        self._check_requirement_has_id(compute_requirement)
        return ComputeRequirementHelper(compute_requirement, self)

    def get_compute_requirement_helper_by_id(self, compute_requirement_id: str) -> ComputeRequirementHelper:
        compute_requirement = self.get_compute_requirement_by_id(compute_requirement_id)
        return self.get_compute_requirement_helper(compute_requirement)

    def find_all_compute_requirements(self) -> List[ComputeRequirementSummary]:
        return self.__service_proxy.find_all_compute_requirements()

    def add_compute_source_template(self, compute_source_template: ComputeSourceTemplate) -> ComputeSourceTemplate:
        return self.__service_proxy.add_compute_source_template(compute_source_template)

    def update_compute_source_template(self, compute_source_template: ComputeSourceTemplate) -> ComputeSourceTemplate:
        return self.__service_proxy.update_compute_source_template(compute_source_template)

    def delete_compute_source_template(self, compute_source_template: ComputeSourceTemplate) -> None:
        self.delete_compute_source_template_by_id(compute_source_template.id)

    def delete_compute_source_template_by_id(self, compute_source_template_id: str) -> None:
        self.__service_proxy.delete_compute_source_template(compute_source_template_id)

    def get_compute_source_template(self, compute_source_template_id: str) -> ComputeSourceTemplate:
        return self.__service_proxy.get_compute_source_template_by_id(compute_source_template_id)

    def find_all_compute_source_templates(self) -> List[ComputeSourceTemplateSummary]:
        return self.__service_proxy.find_all_compute_source_templates()

    def add_compute_requirement_template(self, template: ComputeRequirementTemplate) -> ComputeRequirementTemplate:
        return self.__service_proxy.add_compute_requirement_template(template)

    def update_compute_requirement_template(self, compute_requirement_template: ComputeRequirementTemplate) -> ComputeRequirementTemplate:
        return self.__service_proxy.update_compute_requirement_template(compute_requirement_template)

    def delete_compute_requirement_template(self, compute_requirement_template: ComputeRequirementTemplate) -> None:
        self.delete_compute_requirement_template_by_id(compute_requirement_template.id)

    def delete_compute_requirement_template_by_id(self, compute_requirement_template_id: str) -> None:
        self.__service_proxy.delete_compute_requirement_template(compute_requirement_template_id)

    def get_compute_requirement_template(self, compute_requirement_template_id: str) -> ComputeRequirementTemplate:
        return self.__service_proxy.get_compute_requirement_template_by_id(compute_requirement_template_id)

    def find_all_compute_requirement_templates(self) -> List[ComputeRequirementTemplateSummary]:
        return self.__service_proxy.find_all_compute_requirement_templates()

    def provision_compute_requirement_template(self, template_request: ComputeRequirementTemplateUsage) -> ComputeRequirement:
        return self.__service_proxy.provision_compute_requirement_template(template_request)

    def test_compute_requirement_template(self, template_usage: ComputeRequirementTemplateUsage) -> ComputeRequirementTemplateTestResult:
        return self.__service_proxy.test_compute_requirement_template(template_usage)

    def get_best_compute_source_report_by_compute_requirement(self, provisioned_requirement_id: str) -> BestComputeSourceReport:
        return self.__service_proxy.get_best_compute_source_report_by_requirement_id(provisioned_requirement_id)

    def close(self) -> None:
        self.__requirement_subscriptions.close()

    def _check_all_instances_belong_to_compute_requirement(self, compute_requirement, instances):
        compute_requirement_instance_ids = self._get_instance_ids(compute_requirement.instances)
        request_instance_ids = self._get_instance_ids(instances)

        all_request_instances_are_part_of_compute_requirement = True
        for request_instance_id in request_instance_ids:
            if request_instance_id not in compute_requirement_instance_ids:
                all_request_instances_are_part_of_compute_requirement = False

        if not all_request_instances_are_part_of_compute_requirement:
            raise ValueError("Instances must be part of the specified compute requirement")

    def _transition_instances(self, compute_requirement: ComputeRequirement, next_status: InstanceStatus, instances: List[Instance]) -> None:
        self._check_requirement_has_id(compute_requirement)
        self._check_all_instances_belong_to_compute_requirement(compute_requirement, instances)
        self.__service_proxy.transition_instances(compute_requirement, next_status, self._get_instance_ids(instances))
