from dataclasses import dataclass


@dataclass
class NamespaceRef:
    id: str
    namespace: str
