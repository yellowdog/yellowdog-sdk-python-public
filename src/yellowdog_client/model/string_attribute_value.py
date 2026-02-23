from dataclasses import dataclass, field
from typing import Optional

from .attribute_value import AttributeValue


@dataclass
class StringAttributeValue(AttributeValue[str]):
    type: str = field(default="co.yellowdog.platform.model.StringAttributeValue", init=False)
    attribute: str
    value: Optional[str] = None
