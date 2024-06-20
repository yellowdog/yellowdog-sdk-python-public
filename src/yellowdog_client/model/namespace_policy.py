from dataclasses import dataclass
from typing import Optional


@dataclass
class NamespacePolicy:
    namespace: str
    autoscalingMaxNodes: Optional[int] = None
