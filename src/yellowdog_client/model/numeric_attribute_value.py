from dataclasses import dataclass, field

from .attribute_value import AttributeValue


@dataclass
class NumericAttributeValue(AttributeValue):
    type: str = field(default="co.yellowdog.platform.model.NumericAttributeValue", init=False)
    attribute: str
    value: float
