from abc import ABC
from typing import Optional



class Identified(ABC):
    """Interface implemented by all model types that have a system generated ID field for identification"""
    id: Optional[str]
    """Returns the ID"""
