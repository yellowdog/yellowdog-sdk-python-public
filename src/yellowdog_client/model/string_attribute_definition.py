from dataclasses import dataclass, field
from typing import List, Optional

from .attribute_definition import AttributeDefinition


@dataclass
class StringAttributeDefinition(AttributeDefinition):
    type: str = field(default="co.yellowdog.platform.model.StringAttributeDefinition", init=False)
    name: str
    title: str
    description: Optional[str] = None
    options: Optional[List[str]] = None
