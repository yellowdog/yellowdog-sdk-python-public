from dataclasses import dataclass, field
from typing import Any, List, Optional

from .attribute_value import AttributeValue
from .compute_source import ComputeSource
from .identified import Identified


@dataclass
class ComputeSourceTemplate(Identified):
    id: Optional[str] = field(default=None, init=False)
    source: ComputeSource
    namespace: Optional[str] = None
    description: Optional[str] = None
    attributes: Optional[List[AttributeValue[Any]]] = None
