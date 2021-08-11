from dataclasses import dataclass, field
from typing import List, Optional

from .attribute_definition import AttributeDefinition
from .attribute_source import AttributeSource
from .attribute_source_type import AttributeSourceType


@dataclass
class ExternalAttributeSource(AttributeSource):
    sourceType: Optional[AttributeSourceType] = field(default=None, init=False)
    name: Optional[str] = None
    healthy: bool = False
    attributes: Optional[List[AttributeDefinition]] = None
