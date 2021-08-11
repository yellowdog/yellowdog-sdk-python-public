from enum import Enum


class AwsFleetOnDemandAllocationStrategy(Enum):
    """Specifies the order of the instance overrides that should be used in fulfilling On-Demand capacity."""
    LOWEST_PRICE = "LOWEST_PRICE"
    """AWS EC2 Fleet will use price to determine the order, launching the lowest price first. This is the default strategy."""
    ORDER_PRIORITIZED = "ORDER_PRIORITIZED"
    """AWS EC2 Fleet will use the priority that YellowDog Compute assigns based on the order of the instanceOverrides in the AwsFleetComputeSource, launching in the order specified."""

    def __str__(self) -> str:
        return self.name
