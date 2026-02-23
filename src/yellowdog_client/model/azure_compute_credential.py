from abc import ABC
from datetime import datetime
from typing import Optional

from .credential import Credential



class AzureComputeCredential(Credential, ABC):
    type: str
    name: Optional[str]
    """Returns the name assigned to the Credential to identify it to the ComputeServiceClient."""
    description: Optional[str]
    expiryTime: Optional[datetime]
