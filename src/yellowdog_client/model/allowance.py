from dataclasses import dataclass, field


@dataclass
class Allowance:
    type: str = field(default=None, init=False)
