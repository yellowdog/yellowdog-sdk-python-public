from abc import ABC
from typing import Optional

from .named import Named



class AttributeDefinition(Named, ABC):
    type: str
    name: Optional[str]
    title: Optional[str]
    description: Optional[str]
