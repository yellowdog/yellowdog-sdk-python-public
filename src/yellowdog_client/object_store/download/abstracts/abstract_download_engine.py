from typing import Optional

from yellowdog_client.object_store.abstracts import AbstractTransferEngine
from yellowdog_client.object_store.abstracts import AbstractSession
from yellowdog_client.object_store.model import TransferProperties
from .abstract_download_batch_builder import AbstractDownloadBatchBuilder


class AbstractDownloadEngine(AbstractTransferEngine):
    def build_download_batch(self) -> AbstractDownloadBatchBuilder:
        raise NotImplementedError("Needs implementation")

    def create_download_session(self, file_namespace, file_name, destination_folder_path, destination_file_name=None,
                                transfer_properties=None):
        # type: (str, str, str, Optional[str], Optional[TransferProperties]) -> AbstractSession
        raise NotImplementedError("Needs implementation")
