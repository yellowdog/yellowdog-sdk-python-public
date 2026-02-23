from abc import ABC
from typing import List, Optional

from .attribute_definition import AttributeDefinition
from .attribute_source_type import AttributeSourceType



class AttributeSource(ABC):
    sourceType: Optional[AttributeSourceType]
    attributes: Optional[List[AttributeDefinition]]
