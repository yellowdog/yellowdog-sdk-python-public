from typing import Set, Optional

from yellowdog_client.model.exceptions import ErrorType


class FileTransferException(Exception):
    """
    Custom exception type for errors, related to object store. Inherits :class:`Exception`
    """

    error_type = None               # type: ErrorType
    """
    Type of exception
    
    :type: :class:`yellowdog_client.model.ErrorType`
    """

    detail = None                   # type: Set[str]
    """
    Details of exception
    
    :type: Set[str]
    """

    def __init__(self, error_type, message, detail=None):
        # type: (ErrorType, str, Optional[Set[str]]) -> None
        super(Exception, self).__init__(message)
        self.error_type = error_type
        if detail is not None:
            self.detail = detail
        else:
            self.detail = set()
