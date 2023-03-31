from dataclasses import dataclass
from typing import List, Optional

from .cloud_provider import CloudProvider
from .image_os_type import ImageOsType
from .instant_range import InstantRange
from .metadata_filter import MetadataFilter
from .sort_direction import SortDirection


@dataclass
class MachineImageFamilySearch:
    sortField: Optional[str] = None
    sortDirection: Optional[SortDirection] = None
    includePublic: bool = False
    namespace: Optional[str] = None
    familyName: Optional[str] = None
    groupName: Optional[str] = None
    osType: Optional[ImageOsType] = None
    familyCreatedTime: Optional[InstantRange] = None
    groupCreatedTime: Optional[InstantRange] = None
    imageCreatedTime: Optional[InstantRange] = None
    providers: Optional[List[CloudProvider]] = None
    regions: Optional[List[str]] = None
    supportedInstanceTypes: Optional[List[str]] = None
    metadataFilters: Optional[List[MetadataFilter]] = None
