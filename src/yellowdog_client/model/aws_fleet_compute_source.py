from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set

from .aws_compute_source import AwsComputeSource
from .aws_fleet_instance_override import AwsFleetInstanceOverride
from .aws_fleet_on_demand_options import AwsFleetOnDemandOptions
from .aws_fleet_purchase_option import AwsFleetPurchaseOption
from .aws_fleet_spot_options import AwsFleetSpotOptions
from .compute_source_exhaustion import ComputeSourceExhaustion
from .compute_source_status import ComputeSourceStatus
from .compute_source_traits import ComputeSourceTraits
from .instance_summary import InstanceSummary


@dataclass
class AwsFleetComputeSource(AwsComputeSource):
    """Defines a source of compute provisioned using an AWS EC2 Fleet request."""
    type: str = field(default="co.yellowdog.platform.model.AwsFleetComputeSource", init=False)
    traits: Optional[ComputeSourceTraits] = field(default=None, init=False)
    credentials: Optional[Set[str]] = field(default=None, init=False)
    id: Optional[str] = field(default=None, init=False)
    createdFromId: Optional[str] = field(default=None, init=False)
    fleetId: Optional[str] = field(default=None, init=False)
    """The ID of the AWS EC2 Fleet."""
    instanceSummary: Optional[InstanceSummary] = field(default=None, init=False)
    status: Optional[ComputeSourceStatus] = field(default=None, init=False)
    statusMessage: Optional[str] = field(default=None, init=False)
    exhaustion: Optional[ComputeSourceExhaustion] = field(default=None, init=False)
    name: str
    credential: str
    region: str
    """The AWS region where instances will be provisioned."""
    securityGroupId: str
    """The ID of the AWS Security Group for the provisioned instances."""
    instanceType: str
    """The EC2 instance type for the provisioned instances."""
    imageId: str
    """The region-specific Amazon Machine Image (AMI) ID for the image to use for the provisioned instances."""
    purchaseOption: AwsFleetPurchaseOption
    """Determines which instance purchase options (On-Demand and/or Spot) are available to AWS EC2 Fleet."""
    availabilityZone: Optional[str] = None
    """The AWS availability zone within the region where instances will be provisioned."""
    subnetId: Optional[str] = None
    """The ID of the subnet to use for the provisioned instances."""
    userData: Optional[str] = None
    instanceTags: Optional[Dict[str, str]] = None
    iamRoleArn: Optional[str] = None
    """The ARN of the IAM role to use for the provisioned instances."""
    keyName: Optional[str] = None
    """The name of the EC2 key pair to use when logging into any instances provisioned from this source."""
    enableDetailedMonitoring: Optional[bool] = None
    """Indicates if provisioned instances should have detailed CloudWatch monitoring enabled."""
    assignPublicIp: bool = False
    """Indicates if provisioned instances should be assigned public IP addresses."""
    createClusterPlacementGroup: Optional[bool] = None
    """Indicates if instances should be provisioned within a cluster placement group."""
    createElasticFabricAdapter: Optional[bool] = None
    """Indicates if instances should be provisioned with an Elastic Fabric Adapter network interface."""
    limit: int = 0
    maintainCapacity: bool = False
    """Indicates if AWS EC2 Fleet should maintain the instance count independently of YellowDog Compute, replacing the reprovision functionality."""
    instanceOverrides: Optional[List[AwsFleetInstanceOverride]] = None
    """Extra instance provision options that can override the main parameters set in this source."""
    onDemandOptions: Optional[AwsFleetOnDemandOptions] = None
    """Options related to provisioning On-Demand instances."""
    spotOptions: Optional[AwsFleetSpotOptions] = None
    """Options related to provisioning Spot instances."""
