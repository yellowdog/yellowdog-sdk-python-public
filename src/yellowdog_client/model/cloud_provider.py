from __future__ import annotations

from enum import Enum


class CloudProvider(Enum):
    """Enumerates Cloud Compute Providers."""
    display_name: str

    AWS = "AWS", "AWS"
    """Amazon Web Services (AWS)"""
    GOOGLE = "GOOGLE", "Google Cloud"
    """Google Cloud"""
    AZURE = "AZURE", "Azure"
    """Microsoft Azure"""
    OCI = "OCI", "OCI"
    """Oracle Cloud Infrastructure"""
    ON_PREMISE = "ON_PREMISE", "On Premise"
    """Indicates that the source of compute is not cloud-based, but is on-premise."""

    def __new__(cls, value: str, display_name: str) -> CloudProvider:
        obj = object.__new__(cls)
        obj._value_ = value
        obj.display_name = display_name
        return obj

    def __str__(self) -> str:
        return self.name
