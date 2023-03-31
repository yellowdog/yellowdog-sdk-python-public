from dataclasses import dataclass
from typing import List, Optional

from .cloud_provider import CloudProvider
from .double_range import DoubleRange
from .processor_architecture import ProcessorArchitecture
from .sort_direction import SortDirection


@dataclass
class InstanceTypeSearch:
    providers: Optional[List[CloudProvider]] = None
    name: Optional[str] = None
    processorArchitectures: Optional[List[ProcessorArchitecture]] = None
    defaultVcpus: Optional[DoubleRange] = None
    ramInMib: Optional[DoubleRange] = None
    region: Optional[str] = None
    subRegion: Optional[str] = None
    sortField: Optional[str] = None
    sortDirection: Optional[SortDirection] = None
