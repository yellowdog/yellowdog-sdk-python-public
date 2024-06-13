from dataclasses import dataclass
from typing import Optional

from .azure_account_authentication_properties import AzureAccountAuthenticationProperties
from .okta_account_authentication_properties import OktaAccountAuthenticationProperties


@dataclass
class AccountAuthenticationProperties:
    azure: Optional[AzureAccountAuthenticationProperties] = None
    okta: Optional[OktaAccountAuthenticationProperties] = None
