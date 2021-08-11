from dataclasses import dataclass, field
from typing import Optional

from .credential import Credential


@dataclass
class AwsCredential(Credential):
    """Holds the Access Key ID and Secret Access Key which form a set of credentials for Amazon Web Services (AWS)."""
    type: str = field(default="co.yellowdog.platform.account.credentials.AwsCredential", init=False)
    name: str
    accessKeyId: str
    """The AWS Access Key ID"""
    secretAccessKey: str
    """The AWS Secret Access Key"""
    description: Optional[str] = None
