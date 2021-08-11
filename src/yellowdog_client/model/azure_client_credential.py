from dataclasses import dataclass, field
from typing import Optional

from .azure_compute_credential import AzureComputeCredential


@dataclass
class AzureClientCredential(AzureComputeCredential):
    """Holds the properties that form a set of credentials for Microsoft Azure."""
    type: str = field(default="co.yellowdog.platform.account.credentials.AzureClientCredential", init=False)
    name: str
    clientId: str
    """The Azure Client ID"""
    tenantId: str
    """The Azure Tenant ID"""
    subscriptionId: str
    """The Azure Subscription ID"""
    key: str
    """The Azure Key"""
    description: Optional[str] = None
