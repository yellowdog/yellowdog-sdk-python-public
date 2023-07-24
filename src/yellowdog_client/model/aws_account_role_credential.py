from dataclasses import dataclass, field
from typing import Optional

from .credential import Credential


@dataclass
class AwsAccountRoleCredential(Credential):
    """Holds the Role ARN and External ID required to allow YellowDog Platform to assume an assigned role in an external AWS account."""
    type: str = field(default="co.yellowdog.platform.account.credentials.AwsAccountRoleCredential", init=False)
    name: str
    externalRoleArn: str
    """The ARN of the IAM role in the external account."""
    externalId: str
    """The external ID required to assume the external role."""
    description: Optional[str] = None
