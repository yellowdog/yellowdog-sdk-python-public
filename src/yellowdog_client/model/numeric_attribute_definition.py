from dataclasses import dataclass, field
from typing import List, Optional

from .attribute_definition import AttributeDefinition
from .numeric_attribute_range import NumericAttributeRange
from .numeric_attribute_rank_order import NumericAttributeRankOrder


@dataclass
class NumericAttributeDefinition(AttributeDefinition):
    type: str = field(default="co.yellowdog.platform.model.NumericAttributeDefinition", init=False)
    name: str
    title: str
    defaultRankOrder: NumericAttributeRankOrder
    description: Optional[str] = None
    units: Optional[str] = None
    range: Optional[NumericAttributeRange] = None
    options: Optional[List[float]] = None
