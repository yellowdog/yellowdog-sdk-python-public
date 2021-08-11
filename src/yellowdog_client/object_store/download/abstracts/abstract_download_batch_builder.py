from typing import Callable, Optional

from yellowdog_client.object_store.model import TransferProperties
from yellowdog_client.object_store.abstracts import AbstractTransferBatch
from yellowdog_client.model import FlattenPath


class AbstractDownloadBatchBuilder(object):
    """
    Abstract class for :class:`yellowdog_client.object_store.download.DownloadBatchBuilder`

    .. versionadded:: 0.5.0
    """

    flatten_file_name_mapper = None         # type: Optional[Callable[[str], str]]
    """
    Custom function, which flattens file name after download
    
    :type: Callable[[str], str]
    """

    file_name_mapper = None                 # type: Callable[[str], str]
    """
    Custom function, which renames file name after download

    :type: Callable[[str], str]
    """

    transfer_properties = None              # type: TransferProperties
    """
    Transfer properties to use when creating a new batch

    :type: :class:`yellowdog_client.object_store.model.TransferProperties`
    """

    destination_folder = None               # type: str
    """
    Target directory, where files need to be downloaded

    :type: str
    """

    def set_flatten_file_name_mapper(self, value):
        # type: (Optional[FlattenPath]) -> None
        raise NotImplementedError("set_flatten_file_name_mapper needs implementation")

    def find_source_objects(self, namespace, object_name_pattern):
        # type: (str, str) -> None
        raise NotImplementedError("find_source_objects needs implementation")

    def get_batch_if_objects_found(self):
        # type: () -> Optional[AbstractTransferBatch]
        raise NotImplementedError("get_batch_if_objects_found needs implementation")
