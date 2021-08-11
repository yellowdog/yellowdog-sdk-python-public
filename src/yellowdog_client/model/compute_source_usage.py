from dataclasses import dataclass
from typing import Optional


@dataclass
class ComputeSourceUsage:
    sourceTemplateId: str
    instanceType: Optional[str] = None
    imageId: Optional[str] = None
