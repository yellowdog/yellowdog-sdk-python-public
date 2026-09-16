from abc import ABC
from typing import Optional



class ClusterProvider(ABC):
    type: str
    region: Optional[str]
