from abc import ABC, abstractmethod
from typing import List

from .compute_requirement_helper import ComputeRequirementHelper
from yellowdog_client.common import Closeable
from yellowdog_client.common.server_sent_events import SubscriptionEventListener
from yellowdog_client.model import BestComputeSourceReport, ComputeRequirement, ComputeRequirementSummary, ComputeRequirementTemplate, ComputeRequirementTemplateSummary, ComputeRequirementTemplateTestResult, ComputeRequirementTemplateUsage, ComputeSourceTemplate, ComputeSourceTemplateSummary, Instance


class ComputeClient(ABC, Closeable):
    """The API interface exposed by the YellowDog Compute Service"""

    @abstractmethod
    def add_compute_requirement(self, compute_requirement: ComputeRequirement) -> ComputeRequirement:
        """
        Submits a NEW requirement to YellowDog Compute to be initialised and provisioned.

        :param compute_requirement: the requirement to submit to YellowDog Compute
        :return: the initialised requirement returned from YellowDog Compute
        """

        pass

    @abstractmethod
    def update_compute_requirement(self, compute_requirement: ComputeRequirement) -> ComputeRequirement:
        """
        Submits an existing requirement to YellowDog Compute in order to provision any changes.

        :param compute_requirement: the requirement to submit to YellowDog Compute
        :return: the latest view of the requirement returned from YellowDog Compute
        """

        pass

    @abstractmethod
    def get_compute_requirement(self, compute_requirement: ComputeRequirement) -> ComputeRequirement:
        """
        Requests the latest view of the specified requirement from YellowDog Compute.

        :param compute_requirement: the requirement for which to get the latest view
        :return: the latest view of the requirement returned from YellowDog Compute
        """

        pass

    @abstractmethod
    def get_compute_requirement_by_id(self, compute_requirement_id: str) -> ComputeRequirement:
        """
        Requests the latest view of the specified requirement from YellowDog Compute.

        :param compute_requirement_id: the ID of the requirement
        :return: the latest view of the requirement returned from YellowDog Compute
        """

        pass

    @abstractmethod
    def get_compute_requirement_by_name(self, namespace: str, compute_requirement_name: str) -> ComputeRequirement:
        """
        Requests the latest view of the specified requirement from YellowDog Compute.

        :param namespace:              the namespace containing the requirement
        :param compute_requirement_name: the name of the requirement
        :return: the latest view of the requirement returned from YellowDog Compute
        """

        pass

    @abstractmethod
    def stop_compute_requirement(self, compute_requirement: ComputeRequirement) -> ComputeRequirement:
        """
        Instructs YellowDog Compute to stop all running instances provisioned for the specified requirement.

        :param compute_requirement: the requirement to stop
        :return: the latest view of the requirement returned from YellowDog Compute
        """

        pass

    @abstractmethod
    def start_compute_requirement(self, compute_requirement: ComputeRequirement) -> ComputeRequirement:
        """
        Instructs YellowDog Compute to start all stopped instances provisioned for the specified requirement.

        :param compute_requirement: the requirement to start
        :return: the latest view of the requirement returned from YellowDog Compute
        """

        pass

    @abstractmethod
    def terminate_compute_requirement(self, compute_requirement: ComputeRequirement) -> ComputeRequirement:
        """
        Instructs YellowDog Compute to terminate the specified requirement.

        :param compute_requirement: the requirement to terminate
        :return: the latest view of the requirement returned from YellowDog Compute
        """

        pass

    @abstractmethod
    def reprovision_compute_requirement(self, compute_requirement: ComputeRequirement) -> ComputeRequirement:
        """
        Instructs YellowDog Compute to provision more instances if required such that the number of running instances meets the targetInstanceCount.

        :param compute_requirement: the requirement to terminate
        :return: the latest view of the requirement returned from YellowDog Compute
        """

        pass

    @abstractmethod
    def stop_instances(self, compute_requirement: ComputeRequirement, instances: List[Instance]) -> None:
        """
        Instructs YellowDog Compute to stop the specified instances provisioned for the specified requirement.
        YellowDog Compute will only attempt to stop instances that are InstanceStatus#RUNNING or InstanceStatus#UNKNOWN.

        :param compute_requirement: the requirement containing the instances
        :param instances:          The instances to stop
        """

        pass

    @abstractmethod
    def start_instances(self, compute_requirement: ComputeRequirement, instances: List[Instance]) -> None:
        """
        Instructs YellowDog Compute to start the specified instances provisioned for the specified requirement.
        YellowDog Compute will only attempt to start instances that are InstanceStatus#STOPPED or InstanceStatus#UNKNOWN.

        :param compute_requirement: the requirement containing the instances
        :param instances:          the instances to start
        """

        pass

    @abstractmethod
    def terminate_instances(self, compute_requirement: ComputeRequirement, instances: List[Instance]) -> None:
        """
        Instructs YellowDog Compute to terminate the specified instances provisioned for the specified requirement.
        YellowDog Compute will not attempt to terminate instances that are already InstanceStatus#TERMINATING.

        :param compute_requirement: the requirement containing the instances
        :param instances:          the instances to terminate
        """

        pass

    @abstractmethod
    def restart_instances(self, compute_requirement: ComputeRequirement, instances: List[Instance]) -> None:
        """
        Instructs YellowDog Compute to restart (reboot) the specified instances provisioned for the specified requirement.
        YellowDog Compute will only attempt to restart instances that are InstanceStatus#RUNNING, InstanceStatus#STOPPED or InstanceStatus#UNKNOWN.

        :param compute_requirement: the requirement containing the instances
        :param instances:          the instances to restart
        """

        pass

    @abstractmethod
    def deprovision_instances(self, compute_requirement: ComputeRequirement, instances: List[Instance]) -> None:
        """
        Instructs YellowDog Compute to terminate the specified instances provisioned for the specified requirement and reduce the requirement's instance count accordingly.
        YellowDog Compute will not attempt to deprovision instances that are already InstanceStatus#TERMINATING.

        :param compute_requirement: the requirement containing the instances
        :param instances:          the instances to deprovision
        """

        pass

    @abstractmethod
    def is_compute_requirement_updating(self, compute_requirement: ComputeRequirement) -> bool:
        """
        Checks the current busy state of the specified requirement, returning true if the requirement is being updated by YellowDog Compute; otherwise, false.

        :param compute_requirement: the requirement to check
        :return: true, if the requirement is being updated by YellowDog Compute; otherwise, false
        """

        pass

    @abstractmethod
    def add_compute_requirement_listener(self, compute_requirement: ComputeRequirement, listener: SubscriptionEventListener[ComputeRequirement]) -> None:
        """
        Adds an event listener to receive notifications of changes for the specified requirement.
        The client manages subscriptions to YellowDog Compute such that the first listener created for a requirement will cause a Server-Sent Events subscription to be initiated; additional listeners for the same requirement share that subscription.

        :param compute_requirement: the requirement for which to receive notifications
        :param listener:           the event listener that will be invoked for notifications
        """

        pass

    @abstractmethod
    def remove_compute_requirement_listener(self, listener: SubscriptionEventListener[ComputeRequirement]) -> None:
        """
        Removes the specified event listener.
        The client manages subscriptions to YellowDog Compute such that when the last listener for a requirement is removed, the associated Server-Sent Events subscription is cancelled.

        :param listener: the event listener that will no longer be invoked for notifications
        """

        pass

    @abstractmethod
    def get_compute_requirement_helper(self, compute_requirement: ComputeRequirement) -> ComputeRequirementHelper:
        """
        Constructs a new compute requirement helper for the specified requirement.

        :param compute_requirement: the requirement for which the helper will be constructed
        :return: a new compute requirement helper
        """

        pass

    @abstractmethod
    def find_all_compute_requirements(self) -> List[ComputeRequirementSummary]:
        """
        Returns summaries of all existing compute requirements within the system for the requesting user.

        :return: a list of compute requirement summaries
        """

        pass

    @abstractmethod
    def add_compute_source_template(self, source_template: ComputeSourceTemplate) -> ComputeSourceTemplate:
        pass

    @abstractmethod
    def update_compute_source_template(self, source_template: ComputeSourceTemplate) -> ComputeSourceTemplate:
        pass

    @abstractmethod
    def delete_compute_source_template(self, source_template: ComputeSourceTemplate) -> None:
        pass

    @abstractmethod
    def get_compute_source_template_by_id(self, source_template_id: str) -> ComputeSourceTemplate:
        pass

    @abstractmethod
    def find_all_compute_source_templates(self) -> List[ComputeSourceTemplateSummary]:
        pass

    @abstractmethod
    def add_compute_requirement_template(self, requirement_template: ComputeRequirementTemplate) -> ComputeRequirementTemplate:
        pass

    @abstractmethod
    def update_compute_requirement_template(self, requirement_template: ComputeRequirementTemplate) -> ComputeRequirementTemplate:
        pass

    @abstractmethod
    def delete_compute_requirement_template(self, requirement_template: ComputeRequirementTemplate) -> None:
        pass

    @abstractmethod
    def get_compute_requirement_template_by_id(self, requirement_template_id: str) -> ComputeRequirementTemplate:
        pass

    @abstractmethod
    def find_all_compute_requirement_templates(self) -> List[ComputeRequirementTemplateSummary]:
        """
        Returns summaries of all existing compute requirement templates within the system for the requesting user.

        :return: a list of compute requirement template summaries
        """

        pass

    @abstractmethod
    def provision_compute_requirement_template(self, template_usage: ComputeRequirementTemplateUsage) -> ComputeRequirement:
        """
        Provisions a new compute requirement based on the specified template and requirement properties.

        :param template_usage: An object defining the template ID and requirement properties
        :return: the provisioned compute requirement
        """

        pass

    @abstractmethod
    def test_compute_requirement_template(self, template_usage: ComputeRequirementTemplateUsage) -> ComputeRequirementTemplateTestResult:
        """
        Generates a new compute requirement based on the specified template and requirement properties.
        Includes other related information such as a BestComputeSourceReport if relevant.

        :param template_usage: An object defining the template ID and requirement properties
        :return: the template test result
        """

        pass

    @abstractmethod
    def get_best_compute_source_report_by_requirement_id(self, provisioned_requirement_id: str) -> BestComputeSourceReport:
        """
        Gets the provision report for a compute requirement provisioned from a dynamic template.

        :param provisioned_requirement_id: the ID of the provisioned compute requirement
        :return: the provision report for a compute requirement provisioned from a dynamic template
        """

        pass
