from abc import ABC
from datetime import datetime
from typing import Optional



class Credential(ABC):
    """Interface implemented by classes used to provide cloud provider-specific credentials to YellowDog Compute."""
    type: str
    name: Optional[str]
    """Returns the name assigned to the Credential to identify it to the ComputeServiceClient."""
    description: Optional[str]
    expiryTime: Optional[datetime]
