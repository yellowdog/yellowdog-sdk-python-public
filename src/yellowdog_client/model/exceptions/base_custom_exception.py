from dataclasses import dataclass, field
from typing import Tuple

from .error_type import ErrorType


@dataclass
class BaseCustomException(Exception):
    errorType: ErrorType = field(init=False)
    message: str = None
    detail: Tuple[str, ...] = tuple()

    def __init__(self, message, detail=None):
        super(Exception, self).__init__()
        self.message = message
        self.detail = detail
        detail = detail if detail is not None else tuple()
        args = tuple([message] + list(detail))
        self.args = args

    def __str__(self):
        return "%s: %s" % (str(self.errorType), ". ".join(tuple([self.message] + list(self.detail))))
