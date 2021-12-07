from dataclasses import dataclass
from typing import Optional

from .azure_account_authentication_properties import AzureAccountAuthenticationProperties


@dataclass
class AccountAuthenticationProperties:
    azure: Optional[AzureAccountAuthenticationProperties] = None
