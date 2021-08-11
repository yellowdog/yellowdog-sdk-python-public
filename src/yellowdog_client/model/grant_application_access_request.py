from dataclasses import dataclass
from typing import Optional

from .api_key import ApiKey


@dataclass
class GrantApplicationAccessRequest:
    applicationId: Optional[str] = None
    applicationApiKey: Optional[ApiKey] = None
