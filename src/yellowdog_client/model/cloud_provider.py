from enum import Enum


class CloudProvider(Enum):
    """Enumerates Cloud Compute Providers."""
    ALIBABA = "ALIBABA"
    """Alibaba Cloud"""
    AWS = "AWS"
    """Amazon Web Services (AWS)"""
    GOOGLE = "GOOGLE"
    """Google Cloud"""
    AZURE = "AZURE"
    """Microsoft Azure"""
    OCI = "OCI"
    """Oracle Cloud Infrastructure"""
    ON_PREMISE = "ON_PREMISE"
    """Indicates that the source of compute is not cloud-based, but is on-premise."""

    def __str__(self) -> str:
        return self.name
