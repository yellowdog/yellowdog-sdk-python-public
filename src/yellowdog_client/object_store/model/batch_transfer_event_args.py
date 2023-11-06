from __future__ import annotations

from .file_transfer_status import FileTransferStatus


class BatchTransferEventArgs(object):
    """
    Arguments for batch transfer status
    """

    transfer_status: FileTransferStatus = None
    """
    Status of batch transfer
    
    :type: :class:`yellowdog_client.object_store.model.FileTransferStatus`
    """

    def __init__(self, status: FileTransferStatus) -> None:
        self.transfer_status = status

    def __eq__(self, other: BatchTransferEventArgs) -> bool:
        return self.transfer_status == other.transfer_status
