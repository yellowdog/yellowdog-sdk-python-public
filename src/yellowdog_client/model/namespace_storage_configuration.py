from abc import ABC
from typing import Optional



class NamespaceStorageConfiguration(ABC):
    type: str
    namespace: Optional[str]
