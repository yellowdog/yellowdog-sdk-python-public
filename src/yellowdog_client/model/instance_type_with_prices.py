from dataclasses import dataclass
from typing import Optional

from .price import Price
from .processor_architecture import ProcessorArchitecture


@dataclass
class InstanceTypeWithPrices:
    instanceTypeName: Optional[str] = None
    processorArchitecture: Optional[ProcessorArchitecture] = None
    defaultVcpus: Optional[float] = None
    ramInMib: Optional[int] = None
    offered: Optional[bool] = None
    spotPrice: Optional[Price] = None
    onDemandPrice: Optional[Price] = None
