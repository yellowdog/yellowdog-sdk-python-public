from dataclasses import dataclass
from typing import List

from .attribute_definition import AttributeDefinition


@dataclass
class ExternalAttributeDefinition:
    inputs: List[str]
    definition: AttributeDefinition
