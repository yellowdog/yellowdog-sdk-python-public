from dataclasses import dataclass, field


@dataclass
class AttributePreference:
    type: str = field(default=None, init=False)
