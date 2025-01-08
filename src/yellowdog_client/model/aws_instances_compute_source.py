from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set

from .aws_capacity_reservation import AwsCapacityReservation
from .aws_compute_source import AwsComputeSource
from .aws_placement_group import AwsPlacementGroup
from .aws_secondary_network_interface import AwsSecondaryNetworkInterface
from .compute_source_exhaustion import ComputeSourceExhaustion
from .compute_source_status import ComputeSourceStatus
from .compute_source_traits import ComputeSourceTraits
from .instance_pricing import InstancePricing
from .instance_summary import InstanceSummary


@dataclass
class AwsInstancesComputeSource(AwsComputeSource):
    """Defines a source of compute composed of AWS EC2 instances using the RunInstances API."""
    type: str = field(default="co.yellowdog.platform.model.AwsInstancesComputeSource", init=False)
    traits: Optional[ComputeSourceTraits] = field(default=None, init=False)
    instancePricing: Optional[InstancePricing] = field(default=None, init=False)
    credentials: Optional[Set[str]] = field(default=None, init=False)
    id: Optional[str] = field(default=None, init=False)
    createdFromId: Optional[str] = field(default=None, init=False)
    instanceSummary: Optional[InstanceSummary] = field(default=None, init=False)
    status: Optional[ComputeSourceStatus] = field(default=None, init=False)
    statusMessage: Optional[str] = field(default=None, init=False)
    exhaustion: Optional[ComputeSourceExhaustion] = field(default=None, init=False)
    supportingResourceCreated: Optional[bool] = field(default=None, init=False)
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
    availabilityZone: Optional[str] = None
    """The AWS availability zone within the region where instances will be provisioned."""
    subnetId: Optional[str] = None
    """The ID of the subnet to use for the provisioned instances."""
    userData: Optional[str] = None
    instanceTags: Optional[Dict[str, str]] = None
    iamInstanceProfileArn: Optional[str] = None
    """The ARN of the IAM Instance Profile to use for the provisioned instances."""
    keyName: Optional[str] = None
    """The name of the EC2 key pair to use when logging into any instances provisioned from this source."""
    enableDetailedMonitoring: Optional[bool] = None
    """Indicates if provisioned instances should have detailed CloudWatch monitoring enabled."""
    enableInstanceMetadataTags: Optional[bool] = None
    """Indicates if provisioned instances should expose their tags via instance metadata."""
    useCapacityBlock: Optional[bool] = None
    """Indicates if instances should be provisioned within a reserved capacity block."""
    assignPublicIp: bool = False
    """Indicates if provisioned instances should be assigned public IP addresses."""
    createClusterPlacementGroup: Optional[bool] = None
    """Indicates if instances should be provisioned within a cluster placement group."""
    existingPlacementGroup: Optional[AwsPlacementGroup] = None
    """Indicates an existing placement group within which instances should be provisioned."""
    createElasticFabricAdapter: Optional[bool] = None
    """Indicates if instances should be provisioned with an Elastic Fabric Adapter network interface."""
    secondaryNetworkInterfaces: Optional[List[AwsSecondaryNetworkInterface]] = None
    """Secondary network interfaces to create on provisioned instances."""
    capacityReservation: Optional[AwsCapacityReservation] = None
    """Specifies the capacity reservation to target for provisioned instances."""
    limit: int = 0
    specifyMinimum: bool = False
    """
    Indicates if YellowDog Compute should specify the minimum when requesting instances from AWS.
    If true, then no instances are provisioned unless all requested instances are available;
    otherwise, if false, YellowDog Compute will provision as many instances as possible up to the number requested from this compute source.
    """

    spot: bool = False
    """Indicates if spot instances should be requested rather than on-demand."""
    spotMaxPrice: Optional[float] = None
    """The maximum price that will be paid for instances provisioned from this source."""
