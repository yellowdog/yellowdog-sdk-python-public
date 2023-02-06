from typing import Callable

from yellowdog_client.object_store.model import TransferProperties
from ..upload_batch import UploadBatch


class AbstractUploadBatchBuilder(object):
    """Abstract class for :class:`yellowdog_client.object_store.upload.UploadBatchBuilder`"""

    transfer_properties: TransferProperties = None
    """Transfer properties to use when creating a new batch"""

    namespace: str = None
    """Object store namespace to use for transfer"""

    object_name_mapper: Callable[[str], str] = None
    """Function, which renames file name for transfer"""

    def find_source_objects(self, source_directory_path: str, source_file_pattern: str) -> None:
        raise NotImplementedError("Needs implementation")

    def get_batch_if_objects_found(self) -> UploadBatch:
        raise NotImplementedError("Needs implementation")
