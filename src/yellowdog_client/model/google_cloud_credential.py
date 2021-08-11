from dataclasses import dataclass, field
from typing import Optional

from .credential import Credential


@dataclass
class GoogleCloudCredential(Credential):
    type: str = field(default="co.yellowdog.platform.account.credentials.GoogleCloudCredential", init=False)
    name: str
    serviceAccountKeyJson: str
    """The Google Cloud service account key JSON text"""
    description: Optional[str] = None
