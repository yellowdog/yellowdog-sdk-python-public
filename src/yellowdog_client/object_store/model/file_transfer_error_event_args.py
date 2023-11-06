from __future__ import annotations

from typing import Set, Optional

from yellowdog_client.model.exceptions import ErrorType

from .file_transfer_event_args import FileTransferEventArgs
from .file_transfer_status import FileTransferStatus


class FileTransferErrorEventArgs(FileTransferEventArgs):
    """
    Arguments for transfer error, which occurred when file was being uploaded or downloaded

    .. seealso::

        Inherits from :class:`yellowdog_client.object_store.model.FileTransferEventArgs`
    """

    error_type: ErrorType = None
    """
    Type of exception
    
    :type: :class:`yellowdog_client.model.ErrorType`
    """

    message: str = None
    """
    Message of the exception
    
    :type: str
    """

    detail: Set[str] = None
    """
    Further details of the exception
    
    :type: Set[str]
    """

    def __init__(self, full_path: str, file_name: str, transfer_status: FileTransferStatus, error_type: ErrorType, message: str, detail: Optional[Set[str]] = None) -> None:
        super(FileTransferErrorEventArgs, self).__init__(
            full_path=full_path,
            file_name=file_name,
            transfer_status=transfer_status
        )
        if not detail:
            detail = []
        self.error_type = error_type
        self.message = message
        self.detail = detail

    def __eq__(self, other: FileTransferErrorEventArgs) -> bool:
        return super(FileTransferErrorEventArgs, self).__eq__(other) and \
               self.error_type == other.error_type and \
               self.message == other.message and \
               self.detail == other.detail
