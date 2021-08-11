from dataclasses import dataclass
from typing import Optional

from .aws_fleet_spot_allocation_strategy import AwsFleetSpotAllocationStrategy


@dataclass
class AwsFleetSpotOptions:
    allocationStrategy: Optional[AwsFleetSpotAllocationStrategy] = None
    """Determines the order of the instance overrides to use in fulfilling Spot capacity."""
    instancePoolsToUseCount: Optional[int] = None
    """The number of Spot pools across which AWS EC2 Fleet should allocate Spot capacity when using LOWEST_PRICE Spot allocation strategy."""
    launchReplacementInstanceOnRebalance: Optional[bool] = None
    """Allow AWS EC2 Fleet to launch a replacement Spot instance when an instance rebalance notification is emitted for an existing Spot instance."""
    maxTotalPrice: Optional[float] = None
    """The maximum amount per hour for Spot instances."""
    minInstanceCount: Optional[int] = None
    """The minimum number of Spot instances that must be provisioned in the fleet."""
    singleAvailabilityZone: Optional[bool] = None
    """Indicates that AWS EC2 Fleet should provision all Spot instances into a single availability zone."""
    singleInstanceType: Optional[bool] = None
    """Indicates that AWS EC2 Fleet should use a single instance type to provision all Spot instances."""
