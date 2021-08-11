from datetime import timedelta

from .file_transfer_status import FileTransferStatus
from .file_transfer_event_args import FileTransferEventArgs


class FileTransferProgressEventArgs(FileTransferEventArgs):
    """
    Arguments for file transfer progress

    .. seealso::

        Inherits from :class:`yellowdog_client.object_store.model.FileTransferEventArgs`
    """

    bytes_transferred = None            # type: int
    """
    Total number of bytes transferred
    
    :type: int
    """

    total_file_bytes = None             # type: int
    """
    Total file size in bytes
    
    :type: int
    """

    transfer_percentage = None          # type: float
    """
    Percentage of file transfer
    
    :type: float
    """

    transfer_speed_in_bits = None       # type: float
    """
    Transfer speed in bits per second
    
    :type: float
    """

    estimated_time_left = None          # type: timedelta
    """
    Estimated remaining duration of transfer, based on transfer speed in :attr:`transfer_speed_in_bits`
    
    :type: :class:`datetime.timedelta`
    """

    elapsed_time = None                 # type: timedelta
    """
    Elapsed time since the beginning of transfer
    
    :type: :class:`datetime.timedelta`
    """

    def __init__(self, full_path, file_name, transfer_status, bytes_transferred, total_file_bytes, elapsed_time_delta):
        # type: (str, str, FileTransferStatus, int, int, timedelta) -> None
        super(FileTransferProgressEventArgs, self).__init__(
            full_path=full_path,
            file_name=file_name,
            transfer_status=transfer_status
        )
        self.bytes_transferred = bytes_transferred
        self.total_file_bytes = total_file_bytes
        transfer_percentage = float(self.bytes_transferred) / float(self.total_file_bytes) * 100 \
            if self.total_file_bytes > 0 else 0
        if transfer_percentage > 100:
            transfer_percentage = 100
        self.transfer_percentage = transfer_percentage
        self.transfer_speed_in_bits = float(bytes_transferred) * 8 / float(elapsed_time_delta.seconds) \
            if elapsed_time_delta.seconds > 0 else 0
        self.estimated_time_left = \
            timedelta(seconds=(self.total_file_bytes - bytes_transferred) * 8 / self.transfer_speed_in_bits) \
            if self.transfer_speed_in_bits > 0 else timedelta()
        self.elapsed_time = elapsed_time_delta

    def __eq__(self, other):
        # type: (FileTransferProgressEventArgs) -> bool
        return super(FileTransferProgressEventArgs, self).__eq__(other) and \
                self.bytes_transferred == other.bytes_transferred and \
                self.total_file_bytes == other.total_file_bytes and \
                self.transfer_percentage == other.transfer_percentage and \
                self.transfer_speed_in_bits == other.transfer_speed_in_bits and \
                self.estimated_time_left == other.estimated_time_left and \
                self.elapsed_time == other.elapsed_time
