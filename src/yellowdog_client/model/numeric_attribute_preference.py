from dataclasses import dataclass, field
from typing import Optional

from .attribute_preference import AttributePreference
from .numeric_attribute_rank_order import NumericAttributeRankOrder


@dataclass
class NumericAttributePreference(AttributePreference):
    type: str = field(default="co.yellowdog.platform.model.NumericAttributePreference", init=False)
    attribute: str
    weight: float = 1
    rankOrder: Optional[NumericAttributeRankOrder] = None
