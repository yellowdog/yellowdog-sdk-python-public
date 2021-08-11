from dataclasses import dataclass, field


@dataclass
class WorkerPoolProperties:
    type: str = field(default=None, init=False)
