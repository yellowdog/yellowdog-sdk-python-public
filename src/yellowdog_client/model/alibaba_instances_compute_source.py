from dataclasses import dataclass, field
from typing import Dict, Optional, Set

from .alibaba_compute_source import AlibabaComputeSource
from .alibaba_instance_charge_type import AlibabaInstanceChargeType
from .alibaba_spot_strategy import AlibabaSpotStrategy
from .compute_source_exhaustion import ComputeSourceExhaustion
from .compute_source_status import ComputeSourceStatus
from .compute_source_traits import ComputeSourceTraits
from .instance_summary import InstanceSummary


@dataclass
class AlibabaInstancesComputeSource(AlibabaComputeSource):
    """Defines a source of compute composed of Alibaba Cloud ECS instances."""
    type: str = field(default="co.yellowdog.platform.model.AlibabaInstancesComputeSource", init=False)
    traits: Optional[ComputeSourceTraits] = field(default=None, init=False)
    credentials: Optional[Set[str]] = field(default=None, init=False)
    id: Optional[str] = field(default=None, init=False)
    createdFromId: Optional[str] = field(default=None, init=False)
    instanceSummary: Optional[InstanceSummary] = field(default=None, init=False)
    status: Optional[ComputeSourceStatus] = field(default=None, init=False)
    statusMessage: Optional[str] = field(default=None, init=False)
    exhaustion: Optional[ComputeSourceExhaustion] = field(default=None, init=False)
    name: str
    """The name of the compute source. This must be unique within a compute requirement."""
    credential: str
    region: str
    """The Alibaba Cloud region where instances will be provisioned."""
    vSwitchId: str
    """The ID of the virtual switch to use for the provisioned instances."""
    securityGroupId: str
    """The ID of the Alibaba Cloud Security Group for the provisioned instances."""
    instanceType: str
    """The Alibaba Cloud instance type for the provisioned instances."""
    imageId: str
    """The region-specific Alibaba Cloud ID for the image to use for the provisioned instances."""
    availabilityZone: Optional[str] = None
    """The Alibaba Cloud availability zone within the region where instances will be provisioned."""
    userData: Optional[str] = None
    instanceTags: Optional[Dict[str, str]] = None
    ramRoleName: Optional[str] = None
    """The name of the RAM Role to use for the provisioned instances."""
    keyName: Optional[str] = None
    """The name of the Alibaba Cloud key pair to use when logging into any instances provisioned from this source."""
    instanceChargeType: Optional[AlibabaInstanceChargeType] = None
    """The Alibaba Cloud charge type to use for the provisioned instances."""
    assignPublicIp: bool = False
    """Indicates if provisioned instances should be assigned public IP addresses."""
    spotStrategy: Optional[AlibabaSpotStrategy] = None
    """The Alibaba Cloud spot strategy to use when provisioning instances."""
    spotPriceLimit: Optional[float] = None
    """The Alibaba Cloud spot price limit to use with SPOT_WITH_PRICE_LIMIT spot strategy."""
    limit: int = 0
    specifyMinimum: bool = False
    """
    Indicates if YellowDog Compute should specify the minimum when requesting instances from Alibaba Cloud.
    If true, then no instances are provisioned unless all requested instances are available;
    otherwise, if false, YellowDog Compute will provision as many instances as possible up to the number requested from this compute source.
    """

