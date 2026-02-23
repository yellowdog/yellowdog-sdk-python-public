from abc import ABC
from typing import ClassVar, Optional



class Tagged(ABC):
    """Interface implemented by all model types that have a tag field for user defined information"""
    MAX_TAG_LENGTH: ClassVar[int] = 200
    """The maximum length of a tag value"""
    tag: Optional[str]
    """Gets the user defined tag"""
