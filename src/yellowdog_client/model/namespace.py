from dataclasses import dataclass


@dataclass
class Namespace:
    id: str
    namespace: str
    deletable: bool = False
