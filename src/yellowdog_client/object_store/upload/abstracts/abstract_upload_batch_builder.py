from typing import Callable

from yellowdog_client.object_store.model import TransferProperties
from yellowdog_client.object_store.abstracts import AbstractTransferBatch


class AbstractUploadBatchBuilder(object):
    """
    Abstract class for :class:`yellowdog_client.object_store.upload.UploadBatchBuilder`

    .. versionadded:: 0.5.0
    """

    transfer_properties = None      # type: TransferProperties
    """
    Transfer properties to use when creating a new batch
    
    :type: :class:`yellowdog_client.object_store.model.TransferProperties`
    """

    namespace = None                # type: str
    """
    Object store namespace to use for transfer
    
    :type: str
    """

    object_name_mapper = None       # type: Callable[[str], str]
    """
    Function, which renames file name for transfer
    
    :type: Callable[[str], str]
    """

    def find_source_objects(self, source_directory_path, source_file_pattern):
        # type: (str, str) -> None
        raise NotImplementedError("Needs implementation")

    def get_batch_if_objects_found(self):
        # type: () -> AbstractTransferBatch
        raise NotImplementedError("Needs implementation")
