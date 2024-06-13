from dataclasses import dataclass
from typing import Dict, List, Optional

from .credential_availability import CredentialAvailability


@dataclass
class CheckCredentialsResult:
    """The result of checking if the requestor has access to credentials named in Compute Sources within a Compute Requirement."""
    availability: Optional[CredentialAvailability] = None
    """A value summarizing the availability of credentials."""
    missing: Optional[Dict[str, List[str]]] = None
    """A map of source ID to the credentials missing for that source."""
