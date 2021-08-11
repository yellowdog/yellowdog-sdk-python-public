from dataclasses import dataclass, field
from typing import Optional

from .attribute_constraint import AttributeConstraint


@dataclass
class NumericAttributeConstraint(AttributeConstraint):
    type: str = field(default="co.yellowdog.platform.model.NumericAttributeConstraint", init=False)
    attribute: str
    min: Optional[float] = None
    max: Optional[float] = None
