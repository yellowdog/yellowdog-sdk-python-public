from dataclasses import dataclass
from typing import List, Optional

from .cloud_provider import CloudProvider
from .instance_type_region import InstanceTypeRegion
from .processor_architecture import ProcessorArchitecture


@dataclass
class InstanceType:
    provider: Optional[CloudProvider] = None
    name: Optional[str] = None
    processorArchitecture: Optional[ProcessorArchitecture] = None
    defaultVcpus: Optional[float] = None
    ramInMib: Optional[int] = None
    regions: Optional[List[InstanceTypeRegion]] = None
