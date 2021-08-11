from dataclasses import dataclass, field

from .named import Named


@dataclass
class AttributeDefinition(Named):
    type: str = field(default=None, init=False)
