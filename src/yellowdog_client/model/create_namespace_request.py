from dataclasses import dataclass


@dataclass
class CreateNamespaceRequest:
    namespace: str
