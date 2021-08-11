from .file_transfer_status import FileTransferStatus


class FileTransferEventArgs(object):
    """
    Arguments for file transfer status
    """

    full_path = None                # type: str
    """
    Full file path to the file being transferred
    
    :type: str
    """

    file_name = None                # type: str
    """
    File name of file being transferred
    
    :type: str
    """

    transfer_status = None          # type: FileTransferStatus
    """
    Current status of file transfer
    
    :type: :class:`yellowdog_client.object_store.model.FileTransferStatus`
    """

    def __init__(self, full_path, file_name, transfer_status):
        # type: (str, str, FileTransferStatus) -> None
        self.full_path = full_path
        self.file_name = file_name
        self.transfer_status = transfer_status

    def __eq__(self, other):
        # type: (FileTransferStatus) -> bool
        return self.full_path == other.full_path and \
               self.file_name == other.file_name and \
               self.transfer_status == other.transfer_status
