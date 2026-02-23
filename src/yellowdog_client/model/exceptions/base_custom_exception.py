from dataclasses import dataclass, field
from typing import Tuple, Any, Optional

from .error_type import ErrorType


@dataclass
class BaseCustomException(Exception):
    errorType: ErrorType = field(init=False)
    message: Optional[str] = None
    detail: Tuple[str, ...] = tuple()

    def __init__(self, message: str, detail: Tuple[str, ...] = ()) -> None:
        super().__init__()
        self.message = message
        self.detail = detail
        detail = detail if detail is not None else tuple()
        args = tuple([message] + list(detail))
        self.args: tuple[Any, ...] = args

    def __str__(self) -> str:
        return "%s: %s" % (str(self.errorType), ". ".join(tuple(x for x in [self.message] + list(self.detail) if x is not None)))