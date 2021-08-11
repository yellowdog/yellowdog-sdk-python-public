from dataclasses import dataclass, field

from .base_custom_exception import BaseCustomException
from .error_type import ErrorType


@dataclass
class SessionNotFoundException(BaseCustomException):
    errorType: ErrorType = field(default=ErrorType.SessionNotFoundException, init=False)
