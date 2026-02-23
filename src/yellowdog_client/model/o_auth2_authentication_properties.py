from abc import ABC
from typing import Optional



class OAuth2AuthenticationProperties(ABC):
    clientId: Optional[str]
    clientSecret: Optional[str]
