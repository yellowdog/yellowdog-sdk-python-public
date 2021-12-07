from dataclasses import dataclass
from typing import Optional

from .o_auth2_authentication_properties import OAuth2AuthenticationProperties


@dataclass
class AzureAccountAuthenticationProperties(OAuth2AuthenticationProperties):
    tenantId: str
    clientId: str
    enabled: bool = False
    clientSecret: Optional[str] = None
