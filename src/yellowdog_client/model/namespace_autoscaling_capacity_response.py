from dataclasses import dataclass
from typing import Optional


@dataclass
class NamespaceAutoscalingCapacityResponse:
    namespace: Optional[str] = None
    capacityLimited: bool = False
    remainingCapacity: Optional[int] = None
