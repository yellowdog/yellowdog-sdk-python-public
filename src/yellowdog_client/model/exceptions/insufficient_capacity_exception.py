from dataclasses import dataclass, field

from .base_custom_exception import BaseCustomException
from .error_type import ErrorType


@dataclass
class InsufficientCapacityException(BaseCustomException):
    errorType: ErrorType = field(default=ErrorType.InsufficientCapacityException, init=False)
