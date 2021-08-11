from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ObjectDetail:
    """Describes details about an object stored in the YellowDog Object Store service."""
    namespace: Optional[str] = None
    """The user allocated namespace used to group objects together."""
    objectName: Optional[str] = None
    """The object name which may contain path seperators '/'."""
    objectSize: Optional[int] = None
    """The object size in bytes."""
    lastModified: Optional[datetime] = None
    """When the object was last modified."""
