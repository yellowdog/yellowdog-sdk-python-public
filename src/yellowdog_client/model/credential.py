from abc import ABC
from datetime import datetime
from typing import Optional



class Credential(ABC):
    """Interface implemented by classes used to provide cloud provider-specific credentials to YellowDog Compute."""
    type: str
    name: Optional[str]
    """Returns the name that uniquely identifies the Credential within its keyring."""
    description: Optional[str]
    expiryTime: Optional[datetime]
