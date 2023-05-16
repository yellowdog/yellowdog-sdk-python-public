from dataclasses import dataclass


@dataclass
class InstanceId:
    """Represents the composite ID for an Instance"""
    sourceId: str
    """The ID of the compute source from which this instance was provisioned."""
    instanceId: str
    """The provider supplied ID for this instance."""
