from enum import Enum


class AwsFleetPurchaseOption(Enum):
    ON_DEMAND_THEN_SPOT = "ON_DEMAND_THEN_SPOT"
    """AWS EC2 Fleet will use both On-Demand and Spot instances but prefer On-Demand instances."""
    SPOT_THEN_ON_DEMAND = "SPOT_THEN_ON_DEMAND"
    """AWS EC2 Fleet will use both Spot and On-Demand instances but prefer Spot instances."""
    ON_DEMAND_ONLY = "ON_DEMAND_ONLY"
    """AWS EC2 Fleet will only use On-Demand instances."""
    SPOT_ONLY = "SPOT_ONLY"
    """AWS EC2 Fleet will only use Spot instances."""

    def __str__(self) -> str:
        return self.name
