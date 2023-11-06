from enum import Enum


class ErrorType(Enum):
    """
    Enum for file transfer error type
    """

    ChunkTransferException = "ChunkTransferException"
    """"""
    FileTransferFailure = "FileTransferFailure"
    """"""
    InvalidSessionException = "InvalidSessionException"
    """"""
    InvalidRequestException = "InvalidRequestException"
    """"""
    InternalServerException = "InternalServerException"
    """"""
    NotAuthorisedException = "NotAuthorisedException"
    """"""
    ObjectNotFoundException = "ObjectNotFoundException"
    """"""
    SessionCloseException = "SessionCloseException"
    """"""
    SessionNotFoundException = "SessionNotFoundException"
    """"""
    InsufficientCapacityException = "InsufficientCapacityException"
    """"""
    Unknown = "Unknown"
    """"""

    def is_fatal_session_error(self) -> bool:
        """
        Method, which returns True, if error type is fatal for session to continue or complete. The fatal statuses are
        the following:

        - :attr:`FileTransferFailure`
        - :attr:`NotAuthorisedException`
        - :attr:`ObjectNotFoundException`
        - :attr:`SessionNotFoundException`
        - :attr:`InsufficientCapacityException`

        :return: True, if error is fatal and transfer session cannot continue
        :rtype: bool
        """
        if self in (self.FileTransferFailure, self.NotAuthorisedException, self.ObjectNotFoundException,
                    self.SessionNotFoundException, self.InsufficientCapacityException):
            return True
        else:
            return False

    def __str__(self):
        return self.name
