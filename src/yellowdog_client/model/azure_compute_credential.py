from dataclasses import dataclass, field

from .credential import Credential


@dataclass
class AzureComputeCredential(Credential):
    type: str = field(default="co.yellowdog.platform.account.credentials.AzureComputeCredential", init=False)
