from dataclasses import dataclass, field


@dataclass
class NodeAction:
    action: str = field(default=None, init=False)
