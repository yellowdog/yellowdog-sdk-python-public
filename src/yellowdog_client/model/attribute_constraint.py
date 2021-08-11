from dataclasses import dataclass, field


@dataclass
class AttributeConstraint:
    type: str = field(default=None, init=False)
