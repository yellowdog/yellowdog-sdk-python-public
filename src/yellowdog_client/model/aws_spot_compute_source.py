from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional, Set

from .aws_compute_source import AwsComputeSource
from .compute_source_exhaustion_status import ComputeSourceExhaustionStatus
from .compute_source_status import ComputeSourceStatus
from .compute_source_traits import ComputeSourceTraits


@dataclass
class AwsSpotComputeSource(AwsComputeSource):
    """Defines a source of compute composed of AWS Spot Request (non-persistent) instances."""
    type: str = field(default="co.yellowdog.platform.model.AwsSpotComputeSource", init=False)
    traits: Optional[ComputeSourceTraits] = field(default=None, init=False)
    credentials: Optional[Set[str]] = field(default=None, init=False)
    id: Optional[str] = field(default=None, init=False)
    createdFromId: Optional[str] = field(default=None, init=False)
    requestedInstanceCount: Optional[int] = field(default=None, init=False)
    expectedInstanceCount: Optional[int] = field(default=None, init=False)
    status: Optional[ComputeSourceStatus] = field(default=None, init=False)
    statusMessage: Optional[str] = field(default=None, init=False)
    exhaustionStatus: Optional[ComputeSourceExhaustionStatus] = field(default=None, init=False)
    expectedExhaustionTermination: Optional[datetime] = field(default=None, init=False)
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
    limit: int = 0
    spotPriceMax: Optional[float] = None
    """The maximum price that will be paid for instances provisioned from this source."""
    assignPublicIp: bool = False
    """Indicates if provisioned instances should be assigned public IP addresses."""
    createClusterPlacementGroup: Optional[bool] = None
    """Indicates if instances should be provisioned within a cluster placement group."""
    createElasticFabricAdapter: Optional[bool] = None
    """Indicates if instances should be provisioned with an Elastic Fabric Adapter network interface."""
    enableDetailedMonitoring: Optional[bool] = None
    """Indicates if provisioned instances should have detailed CloudWatch monitoring enabled."""
    keyName: Optional[str] = None
    """The name of the EC2 key pair to use when logging into any instances provisioned from this source."""
    iamRoleArn: Optional[str] = None
    """The ARN of the IAM role to use for the provisioned instances."""
    subnetId: Optional[str] = None
    """The ID of the subnet to use for the provisioned instances."""
    userData: Optional[str] = None
    instanceTags: Optional[Dict[str, str]] = None
