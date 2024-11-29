from dataclasses import dataclass
from typing import Optional

from .aws_network_interface_type import AwsNetworkInterfaceType


@dataclass
class AwsSecondaryNetworkInterface:
    networkInterfaceType: AwsNetworkInterfaceType
    """Determines the type of the network interface."""
    subnetId: Optional[str] = None
    """Optional subnetId for this network interface. If not specified the subnetId of the parent source is used."""
    securityGroupId: Optional[str] = None
    """Optional securityGroupId for this network interface. If not specified the subnetId of the parent source is used."""
