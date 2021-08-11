from .compute_changed_event_data import ComputeChangedEventData
from yellowdog_client.common.server_sent_events import TrackingSubscriptionEventListener
from yellowdog_client.model import ComputeRequirement


class ComputeRequirementInstancesChangedEventListener(TrackingSubscriptionEventListener):
    def _instances_changed(self, compute_changed_event_data):
        # type: (ComputeChangedEventData) -> None
        raise NotImplementedError("Needs implementation")

    def _tracking_initialised(self, obj):
        # type: (ComputeRequirement) -> None
        self._instances_changed(
            compute_changed_event_data=ComputeChangedEventData(
                compute_requirement=obj,
                changed_instances=obj.instances
            )
        )

    def _changed(self, previous, latest):
        # type: (ComputeRequirement, ComputeRequirement) -> None
        changed_instances = []

        for latest_instance in latest.instances:
            if latest_instance not in previous.instances:
                changed_instances.append(latest_instance)

        if len(changed_instances) > 0:
            self._instances_changed(
                compute_changed_event_data=ComputeChangedEventData(
                    compute_requirement=latest,
                    changed_instances=changed_instances
                )
            )

    def subscription_error(self, error):
        super(ComputeRequirementInstancesChangedEventListener, self).subscription_error(error=error)

    def subscription_cancelled(self):
        super(ComputeRequirementInstancesChangedEventListener, self).subscription_cancelled()
