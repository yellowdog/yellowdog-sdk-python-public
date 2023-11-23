from typing import List, Set, Tuple, Optional

from pydispatch import Dispatcher
from yellowdog_client.common.decorators import dispatch_async
from yellowdog_client.model import NamespaceStorageConfiguration
from yellowdog_client.model import ObjectDetail
from yellowdog_client.model import ObjectDownloadRequest
from yellowdog_client.model import ObjectDownloadResponse
from yellowdog_client.model import ObjectPath, ObjectPathsSliceRequest, ObjectPathsRequest
from yellowdog_client.model import ObjectUploadRequest
from yellowdog_client.model import TransferStatusResponse
from yellowdog_client.model.exceptions import ErrorType


class AbstractObjectStoreServiceProxy(Dispatcher):
    ON_ERROR = "on_error"
    _events_ = (ON_ERROR,)

    def start_upload_session(self, namespace: str, object_upload_request: ObjectUploadRequest) -> str:
        raise NotImplementedError("start_upload_session Needs implementation")

    def start_download_session(
            self,
            namespace: str, object_download_request: ObjectDownloadRequest
    ) -> ObjectDownloadResponse:
        raise NotImplementedError("start_download_session Needs implementation")

    def abort_transfer(self, session_id: str) -> None:
        raise NotImplementedError("abort_transfer Needs implementation")

    def complete_transfer(self, session_id: str, summary_hash: str) -> None:
        raise NotImplementedError("complete_transfer Needs implementation")

    def get_transfer_status(self, session_id: str) -> TransferStatusResponse:
        raise NotImplementedError("get_transfer_status Needs implementation")

    def get_object_detail(self, namespace: str, object_name: str) -> ObjectDetail:
        raise NotImplementedError("get_object_detail Needs implementation")

    def check_object_exists(self, namespace: str, name: str) -> bool:
        raise NotImplementedError("check_object_exists Needs implementation")

    def get_namespace_object_paths(self, request: ObjectPathsRequest) -> List[ObjectPath]:
        raise NotImplementedError("get_namespace_object_paths Needs implementation")

    def get_namespace_object_paths_slice(self, request: ObjectPathsSliceRequest) -> List[ObjectPath]:
        raise NotImplementedError("get_namespace_object_paths Needs implementation")

    def delete_objects(self, namespace: str, object_paths: List[ObjectPath]) -> None:
        raise NotImplementedError("delete_objects Needs implementation")

    def upload_chunk(self, session_id: str, chunk_number: int, chunk_data: str, chunk_hash: str) -> None:
        raise NotImplementedError("upload_chunk Needs implementation")

    def download_chunk(
            self,
            session_id: str,
            chunk_number: int,
            chunk_size: int,
            chunk_hash: str
    ) -> Tuple[bytes, Optional[str]]:
        raise NotImplementedError("download_chunk Needs implementation")

    def put_namespace_storage_configuration(
            self,
            namespace_storage_configuration: NamespaceStorageConfiguration
    ) -> None:
        raise NotImplementedError("put_namespace_storage_configuration Needs implementation")

    def delete_namespace_storage_configuration(self, namespace: str) -> None:
        raise NotImplementedError("delete_namespace_storage_configuration Needs implementation")

    def get_namespace_storage_configurations(self) -> List[NamespaceStorageConfiguration]:
        raise NotImplementedError("get_namespace_storage_configurations Needs implementation")

    @dispatch_async
    def _on_error(self, error_type: ErrorType, message: str, detail: Set[str]) -> None:
        self.emit(name=self.ON_ERROR, error_type=error_type, message=message, detail=detail)
