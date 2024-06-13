from enum import Enum


class CredentialAvailability(Enum):
    """Summarizes how many credentials are available for a Compute Requirement"""
    ALL = "ALL"
    """All credentials named in the sources in the Compute Requirement are available"""
    PARTIAL = "PARTIAL"
    """Some of the credentials named in the sources in the Compute Requirement are available"""
    NONE = "NONE"
    """None of the credentials named in the sources in the Compute Requirement are available"""

    def __str__(self) -> str:
        return self.name
