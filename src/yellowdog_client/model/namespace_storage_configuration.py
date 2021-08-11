from dataclasses import dataclass, field


@dataclass
class NamespaceStorageConfiguration:
    type: str = field(default=None, init=False)
