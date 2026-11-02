from abc import ABC
from datetime import datetime
from typing import Optional

from .credential import Credential



class AzureComputeCredential(Credential, ABC):
    type: str
    name: Optional[str]
    """Returns the name that uniquely identifies the Credential within its keyring."""
    description: Optional[str]
    expiryTime: Optional[datetime]
