from enum import Enum


class ErrorType(Enum):
    """
    Enum for error types
    """

    InvalidOperationException = "InvalidOperationException"
    """"""
    InvalidRequestException = "InvalidRequestException"
    """"""
    InternalServerException = "InternalServerException"
    """"""
    NotAuthorisedException = "NotAuthorisedException"
    """"""

    def __str__(self) -> str:
        return self.name
