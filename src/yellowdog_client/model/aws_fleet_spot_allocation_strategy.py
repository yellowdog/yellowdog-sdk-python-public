from enum import Enum


class AwsFleetSpotAllocationStrategy(Enum):
    LOWEST_PRICE = "LOWEST_PRICE"
    """AWS EC2 Fleet will launch instances from the Spot instance pools with the lowest price. This is the default strategy."""
    DIVERSIFIED = "DIVERSIFIED"
    """AWS EC2 Fleet will launch Spot instances distributed across all Spot capacity pools."""
    CAPACITY_OPTIMIZED = "CAPACITY_OPTIMIZED"
    """AWS EC2 Fleet will launch instances from Spot instance pools with optimal capacity for the number of instances that are launching."""
    CAPACITY_OPTIMIZED_ORDER_PRIORITIZED = "CAPACITY_OPTIMIZED_ORDER_PRIORITIZED"
    """AWS EC2 Fleet will launch instances optimizing for capacity first, but honor priority based on the order of the instanceOverrides in the AwsFleetComputeSource on a best-effort basis."""

    def __str__(self) -> str:
        return self.name
