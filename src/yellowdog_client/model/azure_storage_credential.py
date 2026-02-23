from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from .credential import Credential


@dataclass
class AzureStorageCredential(Credential):
    type: str = field(default="co.yellowdog.platform.account.credentials.AzureStorageCredential", init=False)
    expiryTime: Optional[datetime] = field(default=None, init=False)
    name: str
    accountName: str
    """The Azure storage account name"""
    accountKey: str
    """The Azure storage account key"""
    description: Optional[str] = None
