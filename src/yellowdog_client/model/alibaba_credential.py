from dataclasses import dataclass, field
from typing import Optional

from .credential import Credential


@dataclass
class AlibabaCredential(Credential):
    """Holds the Access Key ID and Secret Access Key which form a set of credentials for Alibaba Cloud."""
    type: str = field(default="co.yellowdog.platform.account.credentials.AlibabaCredential", init=False)
    name: str
    accessKeyId: str
    """The Alibaba Cloud Access Key ID"""
    secretAccessKey: str
    """The Alibaba Cloud Secret Access Key"""
    description: Optional[str] = None
