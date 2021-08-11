from dataclasses import dataclass
from typing import Optional

from .aws_fleet_on_demand_allocation_strategy import AwsFleetOnDemandAllocationStrategy


@dataclass
class AwsFleetOnDemandOptions:
    allocationStrategy: Optional[AwsFleetOnDemandAllocationStrategy] = None
    """Determines the order of the instance overrides to use in fulfilling On-Demand capacity."""
    useCapacityReservationsFirst: Optional[bool] = None
    """Indicates if AWS EC2 Fleet should use unused Capacity Reservations to fulfill On-Demand capacity."""
    maxTotalPrice: Optional[float] = None
    """The maximum amount per hour for On-Demand instances."""
    minInstanceCount: Optional[int] = None
    """The minimum number of On-Demand instances that must be provisioned in the fleet."""
    singleAvailabilityZone: Optional[bool] = None
    """Indicates that AWS EC2 Fleet should provision all On-Demand instances into a single availability zone."""
    singleInstanceType: Optional[bool] = None
    """Indicates that AWS EC2 Fleet should use a single instance type to provision all On-Demand instances."""
