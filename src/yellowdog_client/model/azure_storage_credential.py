from dataclasses import dataclass, field
from typing import Optional

from .credential import Credential


@dataclass
class AzureStorageCredential(Credential):
    type: str = field(default="co.yellowdog.platform.account.credentials.AzureStorageCredential", init=False)
    name: str
    accountName: str
    """The Azure storage account name"""
    accountKey: str
    """The Azure storage account key"""
    description: Optional[str] = None
