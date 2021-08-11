from typing import Set, Optional

from yellowdog_client.model.exceptions import ErrorType


class ClientErrorEventArgs(object):
    """
    Arguments for client error, which occurred when using service
    """
    error_type = None               # type: ErrorType
    """
    Type of the error
    
    :type: :class:`yellowdog_client.model.ErrorType`
    """

    message = None                  # type: str
    """
    Message, describing the exception
    
    :type: str
    """

    detail = None                   # type: Set[str]
    """
    Further details about the exception
    
    :type: Set[str]
    """

    def __init__(self, error_type, message, detail=None):
        # type: (ErrorType, str, Optional[Set[str]]) -> None
        if not detail:
            detail = set()
        self.error_type = error_type
        self.message = message
        self.detail = detail

    def __eq__(self, other):
        # type: (ClientErrorEventArgs) -> bool
        return self.error_type == other.error_type and \
               self.message == other.message and \
               self.detail == other.detail
