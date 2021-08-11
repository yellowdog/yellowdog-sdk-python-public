from dataclasses import dataclass
from typing import List, Optional

from .attribute_definition import AttributeDefinition
from .attribute_source import AttributeSource
from .attribute_source_type import AttributeSourceType


@dataclass
class InternalAttributeSource(AttributeSource):
    sourceType: Optional[AttributeSourceType] = None
    attributes: Optional[List[AttributeDefinition]] = None
