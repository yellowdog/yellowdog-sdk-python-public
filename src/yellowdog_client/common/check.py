from typing import Any, Union
from typing import TypeVar

T = TypeVar('T')

def not_none(value: Union[T, None], name: str) -> T:
    if value is None:
        raise ValueError(f"{name} cannot be None")
    return value
