from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from .cloud_provider import CloudProvider
from .image_os_type import ImageOsType
from .metadata_filter import MetadataFilter


@dataclass
class MachineImageFamilySearch:
    includePublic: bool = False
    namespace: Optional[str] = None
    familyName: Optional[str] = None
    groupName: Optional[str] = None
    osType: Optional[ImageOsType] = None
    familyCreatedTimeFrom: Optional[datetime] = None
    familyCreatedTimeTo: Optional[datetime] = None
    groupCreatedTimeFrom: Optional[datetime] = None
    groupCreatedTimeTo: Optional[datetime] = None
    imageCreatedTimeFrom: Optional[datetime] = None
    imageCreatedTimeTo: Optional[datetime] = None
    providers: Optional[List[CloudProvider]] = None
    regions: Optional[List[str]] = None
    supportedInstanceTypes: Optional[List[str]] = None
    metadataFilters: Optional[List[MetadataFilter]] = None
