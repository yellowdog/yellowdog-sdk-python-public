from enum import Enum


class FileTransferStatus(Enum):
    """
    Enum for file transfer status
    """

    Ready = "Ready"
    """"""
    Uploading = "Uploading"
    """"""
    Downloading = "Downloading"
    """"""
    Aborted = "Aborted"
    """"""
    Completed = "Completed"
    """"""
    Validating = "Validating"
    """"""
    Failed = "Failed"
    """"""

    def is_active(self) -> bool:
        """
        Method, which returns True, if status is considered active. The statuses are
        the following:

        - :attr:`Ready`
        - :attr:`Uploading`
        - :attr:`Downloading`

        :return: True, if status is active
        :rtype: bool
        """
        if self in (FileTransferStatus.Ready, FileTransferStatus.Uploading, FileTransferStatus.Downloading):
            return True
        else:
            return False

    def is_finished(self) -> bool:
        """
        Method, which returns True, if status is considered finished. The statuses are
        the following:

        - :attr:`Aborted`
        - :attr:`Completed`
        - :attr:`Failed`

        :return: True, if status is finished
        :rtype: bool
        """
        if self in (FileTransferStatus.Aborted, FileTransferStatus.Completed, FileTransferStatus.Failed):
            return True
        else:
            return False
