from dataclasses import dataclass, field
from typing import Optional

from .aws_instance import AwsInstance


@dataclass
class AwsSpotRequestInstance(AwsInstance):
    """Extends Instance to add fields specific to the AWS Spot compute source."""
    type: str = field(default="co.yellowdog.platform.model.AwsSpotRequestInstance", init=False)
    spotRequestState: Optional[str] = None
    """The state of the Spot Instance Request associated with this instance"""
    spotRequestStatusCode: Optional[str] = None
    """The status code of the Spot Instance Request associated with this instance"""
