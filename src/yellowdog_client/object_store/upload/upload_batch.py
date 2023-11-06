from typing import List

from yellowdog_client.object_store.model import FileTransferDirection
from yellowdog_client.object_store.abstracts import AbstractTransferBatch
from yellowdog_client.object_store.abstracts import AbstractSession


class UploadBatch(AbstractTransferBatch):
    """
    Transfer batch used for upload

    .. versionadded:: 0.5.0

    .. seealso::

        Inherits from :class:`yellowdog_client.object_store.abstracts.AbstractTransferBatch`
    """

    def __init__(self, sessions: List[AbstractSession]) -> None:
        super(UploadBatch, self).__init__(
            transfer_direction=FileTransferDirection.Upload,
            sessions=sessions
        )
