from typing import List

from yellowdog_client.object_store.model import FileTransferDirection
from yellowdog_client.object_store.abstracts import AbstractTransferBatch
from yellowdog_client.object_store.abstracts import AbstractSession


class DownloadBatch(AbstractTransferBatch):
    """
    Transfer batch used for download

    .. versionadded:: 0.5.0

    .. seealso::

        Inherits from :class:`yellowdog_client.object_store.abstracts.AbstractTransferBatch`
    """

    def __init__(self, sessions: List[AbstractSession]) -> None:
        super(DownloadBatch, self).__init__(
            transfer_direction=FileTransferDirection.Download,
            sessions=sessions
        )
