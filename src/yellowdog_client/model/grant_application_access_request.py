from dataclasses import dataclass

from .api_key import ApiKey


@dataclass
class GrantApplicationAccessRequest:
    applicationApiKey: ApiKey
