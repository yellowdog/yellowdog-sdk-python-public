from dataclasses import dataclass
from typing import Optional


@dataclass
class AwsFleetInstanceOverride:
    instanceType: str
    """The EC2 instance type for the provisioned instances."""
    availabilityZone: Optional[str] = None
    """The AWS availability zone within the region where instances will be provisioned."""
    spotMaxPrice: Optional[float] = None
    """The maximum price that will be paid for spot instances."""
    subnetId: Optional[str] = None
    """The ID of the subnet to use for the provisioned instances."""
