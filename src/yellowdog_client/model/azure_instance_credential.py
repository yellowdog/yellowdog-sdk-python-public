from dataclasses import dataclass, field
from typing import Optional

from .azure_compute_credential import AzureComputeCredential


@dataclass
class AzureInstanceCredential(AzureComputeCredential):
    """Holds an admin user name and password to be used for created instances in Microsoft Azure."""
    type: str = field(default="co.yellowdog.platform.account.credentials.AzureInstanceCredential", init=False)
    name: str
    adminUsername: str
    """The admin username"""
    description: Optional[str] = None
    adminPassword: Optional[str] = None
    """The admin password"""
