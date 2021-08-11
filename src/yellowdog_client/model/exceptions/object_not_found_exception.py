from dataclasses import dataclass

from .base_custom_exception import BaseCustomException
from .error_type import ErrorType


@dataclass
class ObjectNotFoundException(BaseCustomException):
    errorType: ErrorType = ErrorType.ObjectNotFoundException
