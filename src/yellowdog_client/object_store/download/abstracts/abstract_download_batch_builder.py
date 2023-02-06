from typing import Callable, Optional

from yellowdog_client.model import FlattenPath
from yellowdog_client.object_store.abstracts import AbstractTransferBatch
from yellowdog_client.object_store.model import TransferProperties


class AbstractDownloadBatchBuilder:
    """
    Abstract class for :class:`yellowdog_client.object_store.download.DownloadBatchBuilder`

    .. versionadded:: 0.5.0
    """

    flatten_file_name_mapper: Optional[Callable[[str], str]] = None
    """Custom function, which flattens file name after download"""

    file_name_mapper: Callable[[str], str] = None
    """Custom function, which renames file name after download"""

    transfer_properties: TransferProperties = None
    """Transfer properties to use when creating a new batch"""

    destination_folder: str = None
    """Target directory, where files need to be downloaded"""

    def set_flatten_file_name_mapper(self, value: Optional[FlattenPath]) -> None:
        raise NotImplementedError("set_flatten_file_name_mapper needs implementation")

    def find_source_objects(self, namespace: str, object_name_pattern: str) -> None:
        raise NotImplementedError("find_source_objects needs implementation")

    def get_batch_if_objects_found(self) -> Optional[AbstractTransferBatch]:
        raise NotImplementedError("get_batch_if_objects_found needs implementation")
