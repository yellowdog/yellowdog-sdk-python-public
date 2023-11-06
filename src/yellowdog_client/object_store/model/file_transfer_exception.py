from typing import Set, Optional

from yellowdog_client.model.exceptions import ErrorType


class FileTransferException(Exception):
    """
    Custom exception type for errors, related to object store. Inherits :class:`Exception`
    """

    error_type: ErrorType = None
    """
    Type of exception
    
    :type: :class:`yellowdog_client.model.ErrorType`
    """

    detail: Set[str] = None
    """
    Details of exception
    
    :type: Set[str]
    """

    def __init__(self, error_type: ErrorType, message: str, detail: Optional[Set[str]] = None):
        super().__init__(message)
        self.message = message
        self.error_type = error_type
        if detail is not None:
            self.detail = detail
        else:
            self.detail = set()
