from .file_transfer_status import FileTransferStatus


class BatchTransferEventArgs(object):
    """
    Arguments for batch transfer status
    """

    transfer_status = None          # type: FileTransferStatus
    """
    Status of batch transfer
    
    :type: :class:`yellowdog_client.object_store.model.FileTransferStatus`
    """

    def __init__(self, status):
        # type: (FileTransferStatus) -> None
        self.transfer_status = status

    def __eq__(self, other):
        # type: (BatchTransferEventArgs) -> bool
        return self.transfer_status == other.transfer_status
