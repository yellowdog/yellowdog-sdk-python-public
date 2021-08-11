from dataclasses import dataclass, field

from .base_custom_exception import BaseCustomException
from .error_type import ErrorType


@dataclass
class InvalidRequestException(BaseCustomException):
    errorType: ErrorType = field(default=ErrorType.InvalidRequestException, init=False)
