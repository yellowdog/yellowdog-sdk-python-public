from dataclasses import dataclass, field
from typing import Optional

from .credential import Credential


@dataclass
class OciCredential(Credential):
    """Holds the properties that form a set of credentials for Oracle Cloud Infrastructure (OCI)."""
    type: str = field(default="co.yellowdog.platform.account.credentials.OciCredential", init=False)
    name: str
    userId: str
    """The OCI User ID (ocid)."""
    tenantId: str
    """The OCI tenant ID (ocid)."""
    fingerprint: str
    """The OCI public key fingerprint."""
    privateKey: str
    """The OCI private key."""
    description: Optional[str] = None
    passphrase: Optional[str] = None
    """The OCI private key passphrase."""
