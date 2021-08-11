from dataclasses import dataclass, field
from typing import List, Optional

from .attribute_preference import AttributePreference


@dataclass
class StringAttributePreference(AttributePreference):
    type: str = field(default="co.yellowdog.platform.model.StringAttributePreference", init=False)
    attribute: str
    weight: float = 1
    preferredValues: Optional[List[str]] = None
    preferredPatterns: Optional[List[str]] = None
