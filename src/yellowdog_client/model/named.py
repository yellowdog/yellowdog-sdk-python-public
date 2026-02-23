from abc import ABC
from typing import Optional



class Named(ABC):
    """Interface implemented by all model types that have a name field"""
    name: Optional[str]
    """Returns the name"""
