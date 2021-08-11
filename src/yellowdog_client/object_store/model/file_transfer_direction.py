from enum import Enum


class FileTransferDirection(Enum):
    """
    Enum for file transfer direction
    """

    Upload = "Upload"
    """"""
    Download = "Download"
    """"""

    def __str__(self):
        return self.name
