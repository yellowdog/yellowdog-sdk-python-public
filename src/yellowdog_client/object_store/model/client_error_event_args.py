from __future__ import annotations

from typing import Set, Optional

from yellowdog_client.model.exceptions import ErrorType


class ClientErrorEventArgs(object):
    """
    Arguments for client error, which occurred when using service
    """
    error_type: ErrorType = None
    """
    Type of the error
    
    :type: :class:`yellowdog_client.model.ErrorType`
    """

    message: str = None
    """
    Message, describing the exception
    
    :type: str
    """

    detail: Set[str] = None
    """
    Further details about the exception
    
    :type: Set[str]
    """

    def __init__(self, error_type: ErrorType, message: str, detail: Optional[Set[str]] = None) -> None:
        if not detail:
            detail = set()
        self.error_type = error_type
        self.message = message
        self.detail = detail

    def __eq__(self, other: ClientErrorEventArgs) -> bool:
        return self.error_type == other.error_type and \
            self.message == other.message and \
            self.detail == other.detail
