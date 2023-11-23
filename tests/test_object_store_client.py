from __future__ import annotations

from dataclasses import dataclass, field
from math import ceil
from pathlib import Path
from typing import Optional

import pytest
from yellowdog_client import PlatformClient
from yellowdog_client.model import ServicesSchema, ApiKey, ObjectUploadRequest, TransferStatusResponse, \
    ObjectDownloadResponse, ObjectDownloadRequest, Slice, ObjectPath, ObjectDetail, S3NamespaceStorageConfiguration, \
    AzureNamespaceStorageConfiguration, RetryProperties
from yellowdog_client.object_store import ObjectStoreClient
from yellowdog_client.object_store.abstracts import AbstractTransferEngine, AbstractTransferBatch
from yellowdog_client.object_store.model import FileTransferStatus
from yellowdog_client.object_store.utils import HashUtils

from util.api import MockApi, HttpMethod
from util.data import make, make_string, make_bytes, make_int, make_datetime


@dataclass
class TempFile:
    path: Path
    size: int

    def name(self):
        return self.path.name

    def as_posix(self):
        return self.path.as_posix()


@dataclass
class TempDir:
    def __init__(self, path: Path):
        self.path = path

    def create_file(self, size: int) -> TempFile:
        temp_ = self.path / make_string()
        with temp_.open("wb") as out:
            out.truncate(size)
        return TempFile(temp_, size)

    def as_posix(self):
        return self.path.as_posix()


@dataclass
class MockRemoteObject:
    name: str = field(default_factory=make_string)
    content: bytes = field(default_factory=make_bytes)

    @staticmethod
    def with_prefix(prefix: str) -> MockRemoteObject:
        return MockRemoteObject(name=f"{prefix}/{make_string()}")


class MockObjectStoreApi:
    def __init__(self, mock_api: MockApi):
        self._mock_api: MockApi = mock_api

    def verify_all_requests_called(self):
        self._mock_api.verify_all_requests_called()

    def mock_file_upload(
            self,
            namespace: str,
            temp_: TempFile
    ):
        chunk_size = AbstractTransferEngine.DEFAULT_CHUNK_SIZE
        chunk_count = ceil(temp_.size / chunk_size)

        request = ObjectUploadRequest(
            objectName=temp_.name(),
            objectSize=temp_.size,
            chunkSize=chunk_size,
            chunkCount=chunk_count
        )
        response = TransferStatusResponse(
            namespace=namespace,
            objectName=temp_.name(),
            objectSize=temp_.size,
            chunkSize=chunk_size,
            chunkCount=1,
            chunksReceived=[1]
        )
        session_id = self._mock_api.mock(
            f"/objectstore/objects/{namespace}/startUpload",
            HttpMethod.POST,
            request=request,
            response_type=str
        )

        for chunk_number in range(1, chunk_count + 1):
            self._mock_api.mock(f"/objectstore/transfers/{session_id}/chunks/{chunk_number}", HttpMethod.PUT)
        self._mock_api.mock(f"/objectstore/transfers/{session_id}", HttpMethod.GET, response=response)
        self._mock_api.mock(f"/objectstore/transfers/{session_id}/complete", HttpMethod.POST)

    def mock_object_download(
            self,
            namespace: str,
            mock_remote_object: MockRemoteObject,
    ):
        chunk_size = AbstractTransferEngine.DEFAULT_CHUNK_SIZE
        content_hash = HashUtils.calculate_md5_in_base_64(input_value=mock_remote_object.content)
        response = TransferStatusResponse(
            namespace=namespace,
            objectName=mock_remote_object.name,
            objectSize=len(mock_remote_object.content),
            chunkSize=chunk_size,
            chunkCount=1,
            chunksReceived=[1]
        )
        start_response = self._mock_api.mock(
            f"/objectstore/objects/{namespace}/startDownload",
            HttpMethod.POST,
            request=ObjectDownloadRequest(
                objectName=mock_remote_object.name,
                chunkSize=chunk_size
            ),
            response=ObjectDownloadResponse(
                sessionId=make_string(),
                namespace=namespace,
                objectName=mock_remote_object.name,
                objectSize=len(mock_remote_object.content),
                chunkSize=chunk_size,
                chunkCount=1
            )
        )
        session_id = start_response.sessionId

        self._mock_api.mock(
            f"/objectstore/transfers/{session_id}/chunks/1",
            HttpMethod.GET,
            response=mock_remote_object.content,
            response_headers={"Content-MD5": content_hash}
        )
        self._mock_api.mock(f"/objectstore/transfers/{session_id}", HttpMethod.GET, response=response)
        self._mock_api.mock(f"/objectstore/transfers/{session_id}/complete", HttpMethod.POST)

    def mock_search_objects(self, namespace: str, *objects: MockRemoteObject, prefix: Optional[str] = None):
        self._mock_api.mock(
            f"/objectstore/objects/{namespace}",
            HttpMethod.GET,
            params={"prefix": prefix, "flat": True} if prefix else None,
            response=Slice([ObjectPath(object.name) for object in objects])
        )

    def mock_object_exists(self, namespace: str, object: MockRemoteObject):
        self._mock_api.mock(
            f"/objectstore/objects/{namespace}/object/exists",
            HttpMethod.GET,
            params={"name": object.name},
            response=True
        )


def wait_until_batch_completed(batch: AbstractTransferBatch):
    batch = batch.when_status_matches(lambda status: status.is_finished()).result(timeout=2)
    assert batch.status == FileTransferStatus.Completed


def wait_until_session_completed(session):
    session = session.when_status_matches(lambda status: status.is_finished()).result(timeout=2)
    assert session.status == FileTransferStatus.Completed


def assert_object_downloaded(parent_directory: Path, expected_object: MockRemoteObject):
    file = parent_directory / expected_object.name
    assert file.exists()
    assert file.read_bytes() == expected_object.content


@pytest.fixture
def object_store_client(mock_api: MockApi) -> ObjectStoreClient:
    platform_client = PlatformClient.create(
        ServicesSchema(defaultUrl=mock_api.url(), retry=RetryProperties(maxAttempts=0)),
        make(ApiKey)
    )
    object_store_client = platform_client.object_store_client
    object_store_client.start_transfers()
    return object_store_client


@pytest.fixture
def mock_object_store_api(mock_api: MockApi) -> MockObjectStoreApi:
    return MockObjectStoreApi(mock_api)


@pytest.fixture
def temp_dir(tmp_path: Path) -> TempDir:
    return TempDir(tmp_path)


def test_can_upload_objects(
        temp_dir: TempDir,
        mock_object_store_api: MockObjectStoreApi,
        object_store_client: ObjectStoreClient
):
    temp_ = temp_dir.create_file(size=1024)
    namespace = make_string()
    mock_object_store_api.mock_file_upload(namespace, temp_)

    session = object_store_client.create_upload_session(
        file_namespace=namespace,
        source_file_path=temp_.as_posix()
    )
    session.bind(on_error=lambda event_args: print(event_args.message))
    session.start()

    wait_until_session_completed(session)
    mock_object_store_api.verify_all_requests_called()


def test_can_upload_zero_length_objects(
        temp_dir: TempDir,
        mock_object_store_api: MockObjectStoreApi,
        object_store_client: ObjectStoreClient
):
    temp_ = temp_dir.create_file(size=0)
    namespace = make_string()
    mock_object_store_api.mock_file_upload(namespace, temp_)

    session = object_store_client.create_upload_session(
        file_namespace=namespace,
        source_file_path=temp_.path.as_posix()
    )
    session.bind(on_error=lambda event_args: print(event_args.message))
    session.start()

    wait_until_session_completed(session)
    mock_object_store_api.verify_all_requests_called()


def test_can_batch_upload_objects(
        temp_dir: TempDir,
        mock_object_store_api: MockObjectStoreApi,
        object_store_client: ObjectStoreClient
):
    namespace = make_string()
    first_temp_ = temp_dir.create_file(size=1024)
    second_temp_ = temp_dir.create_file(size=1024)

    mock_object_store_api.mock_file_upload(namespace, first_temp_)
    mock_object_store_api.mock_file_upload(namespace, second_temp_)

    builder = object_store_client.build_upload_batch()
    builder.find_source_objects(source_directory_path=temp_dir.as_posix(), source_file_pattern="*")
    builder.namespace = namespace
    batch = builder.get_batch_if_objects_found()
    batch.add_session_error_listener(lambda event_args: print(event_args.message))
    batch.start()

    wait_until_batch_completed(batch)
    mock_object_store_api.verify_all_requests_called()


def test_can_download_objects(
        temp_dir: TempDir,
        mock_object_store_api: MockObjectStoreApi,
        object_store_client: ObjectStoreClient
):
    namespace = make_string()
    expected_object = MockRemoteObject()
    mock_object_store_api.mock_object_download(namespace, expected_object)

    session = object_store_client.create_download_session(
        file_namespace=namespace,
        file_name=expected_object.name,
        destination_folder_path=temp_dir.as_posix()
    )
    session.bind(on_error=lambda event_args: print(event_args.message))
    session.start()

    session = session.when_status_matches(lambda status: status.is_finished()).result()
    assert session.status == FileTransferStatus.Completed

    assert_object_downloaded(temp_dir.path, expected_object)
    mock_object_store_api.verify_all_requests_called()


def test_can_batch_download_objects(
        temp_dir: TempDir,
        mock_object_store_api: MockObjectStoreApi,
        object_store_client: ObjectStoreClient
):
    namespace = make_string()

    first_object = MockRemoteObject()
    second_object = MockRemoteObject()

    mock_object_store_api.mock_object_download(namespace, first_object)
    mock_object_store_api.mock_object_download(namespace, second_object)
    mock_object_store_api.mock_search_objects(namespace, first_object, second_object)

    builder = object_store_client.build_download_batch()
    builder.find_source_objects(namespace=namespace, object_name_pattern="*")
    builder.destination_folder = temp_dir.as_posix()
    batch = builder.get_batch_if_objects_found()
    batch.add_session_error_listener(lambda event_args: print(event_args.message))
    batch.start()

    wait_until_batch_completed(batch)

    assert_object_downloaded(temp_dir.path, first_object)
    assert_object_downloaded(temp_dir.path, second_object)
    mock_object_store_api.verify_all_requests_called()


def test_batch_downloading_with_fixed_pattern_checks_objects_existence_instead_of_searching(
        temp_dir: TempDir,
        mock_object_store_api: MockObjectStoreApi,
        object_store_client: ObjectStoreClient
):
    namespace = make_string()

    first_object = MockRemoteObject()

    mock_object_store_api.mock_object_download(namespace, first_object)
    mock_object_store_api.mock_object_exists(namespace, first_object)

    builder = object_store_client.build_download_batch()
    builder.find_source_objects(namespace=namespace, object_name_pattern=first_object.name)
    builder.destination_folder = temp_dir.as_posix()

    batch = builder.get_batch_if_objects_found()
    batch.add_session_error_listener(lambda event_args: print(event_args.message))
    batch.start()

    wait_until_batch_completed(batch)
    mock_object_store_api.verify_all_requests_called()


def test_batch_uploading_with_fixed_pattern_checks_objects_existence_instead_of_searching(
        temp_dir: TempDir,
        mock_object_store_api: MockObjectStoreApi,
        object_store_client: ObjectStoreClient
):
    namespace = make_string()
    first_temp_ = temp_dir.create_file(size=1024)
    temp_dir.create_file(size=1024)

    mock_object_store_api.mock_file_upload(namespace, first_temp_)

    builder = object_store_client.build_upload_batch()
    builder.find_source_objects(
        source_directory_path=temp_dir.as_posix(),
        source_file_pattern=first_temp_.name()
    )
    builder.namespace = namespace
    batch = builder.get_batch_if_objects_found()
    batch.add_session_error_listener(lambda event_args: print(event_args.message))
    batch.start()

    wait_until_batch_completed(batch)
    mock_object_store_api.verify_all_requests_called()


def test_batch_downloading_with_pattern_search_from_within_fixed_prefix(
        temp_dir: TempDir,
        mock_object_store_api: MockObjectStoreApi,
        object_store_client: ObjectStoreClient
):
    namespace = make_string()
    prefix = "foo"

    first_object = MockRemoteObject.with_prefix(prefix)
    second_object = MockRemoteObject.with_prefix(prefix)

    mock_object_store_api.mock_object_download(namespace, first_object)
    mock_object_store_api.mock_object_download(namespace, second_object)
    mock_object_store_api.mock_search_objects(namespace, first_object, second_object, prefix=f"{prefix}%2F")

    builder = object_store_client.build_download_batch()
    builder.find_source_objects(namespace=namespace, object_name_pattern=f"{prefix}/*")
    builder.destination_folder = temp_dir.as_posix()

    batch = builder.get_batch_if_objects_found()
    batch.add_session_error_listener(lambda event_args: print(event_args.message))
    batch.start()

    wait_until_batch_completed(batch)
    mock_object_store_api.verify_all_requests_called()


def test_can_get_object_detail(mock_api: MockApi, object_store_client: ObjectStoreClient):
    object_name = make_string()
    namespace = make_string()

    expected = mock_api.mock(
        f"/objectstore/objects/{namespace}/object",
        HttpMethod.GET,
        params={"name": object_name},
        response=ObjectDetail(
            namespace=namespace,
            objectName=object_name,
            objectSize=make_int(),
            lastModified=make_datetime()
        )
    )

    actual = object_store_client.get_object_detail(namespace, object_name)

    assert actual == expected
    mock_api.verify_all_requests_called()


def test_can_get_namespace_object_paths(mock_api: MockApi, object_store_client: ObjectStoreClient):
    expected = mock_api.mock("/objectstore/configurations", HttpMethod.GET, response=[
        S3NamespaceStorageConfiguration(
            namespace=make_string(),
            bucketName=make_string(),
            region=make_string(),
            credential=make_string()
        ),
        AzureNamespaceStorageConfiguration(
            namespace=make_string(),
            containerName=make_string(),
            credential=make_string()
        )
    ])

    actual = object_store_client.get_namespace_storage_configurations()

    assert actual == expected
    mock_api.verify_all_requests_called()
