from dataclasses import dataclass, field


@dataclass
class Sort:
    unsorted: bool = field(default=None, init=False)
    sorted: bool = False
    empty: bool = True
