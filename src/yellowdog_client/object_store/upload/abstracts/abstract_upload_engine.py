from typing import Optional

from yellowdog_client.object_store.abstracts import AbstractTransferEngine
from yellowdog_client.object_store.abstracts import AbstractSession
from yellowdog_client.object_store.model import TransferProperties
from .abstract_upload_batch_builder import AbstractUploadBatchBuilder


class AbstractUploadEngine(AbstractTransferEngine):
    def build_upload_batch(self) -> AbstractUploadBatchBuilder:
        raise NotImplementedError("Needs implementation")

    def create_upload_session(self, file_namespace, source_file_path, destination_file_name, transfer_properties=None):
        # type: (str, str, str, Optional[TransferProperties]) -> AbstractSession
        raise NotImplementedError("Needs implementation")
