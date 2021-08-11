from dataclasses import dataclass, field
from typing import Optional, Set

from .attribute_constraint import AttributeConstraint


@dataclass
class StringAttributeConstraint(AttributeConstraint):
    type: str = field(default="co.yellowdog.platform.model.StringAttributeConstraint", init=False)
    attribute: str
    anyOf: Optional[Set[str]] = None
    noneOf: Optional[Set[str]] = None
    pattern: Optional[str] = None
