from pathlib import Path

import pytest

from util.api import MockApi, HttpMethod
from util.data import make, make_string, make_bytes, make_int, make_datetime
from yellowdog_client import PlatformClient
from yellowdog_client.model import ServicesSchema, ApiKey, ObjectUploadRequest, TransferStatusResponse, \
    ObjectDownloadResponse, ObjectDownloadRequest, Slice, ObjectPath, ObjectDetail, S3NamespaceStorageConfiguration, \
    AzureNamespaceStorageConfiguration
from yellowdog_client.object_store import ObjectStoreClient
from yellowdog_client.object_store.model import FileTransferStatus
from yellowdog_client.object_store.utils import HashUtils


@pytest.fixture
def object_store_client(mock_api: MockApi) -> ObjectStoreClient:
    platform_client = PlatformClient.create(
        ServicesSchema(defaultUrl=mock_api.url()),
        make(ApiKey)
    )
    object_store_client = platform_client.object_store_client
    object_store_client.start_transfers()
    return object_store_client


def create_file(tmp_path: Path, test_file_size: int):
    test_file = tmp_path / make_string()
    with test_file.open("wb") as out:
        out.truncate(test_file_size)
    return test_file


def mock_file_upload(
        mock_api: MockApi,
        namespace: str,
        test_file: Path,
        test_file_size: int,
        chunk_size: int
):
    request = ObjectUploadRequest(
        objectName=str(test_file.name),
        objectSize=test_file_size,
        chunkSize=chunk_size,
        chunkCount=1
    )
    response = TransferStatusResponse(
        namespace=namespace,
        objectName=str(test_file.name),
        objectSize=test_file_size,
        chunkSize=chunk_size,
        chunkCount=1,
        chunksReceived=[1]
    )
    session_id = mock_api.mock(f"/objectstore/objects/{namespace}/startUpload", HttpMethod.POST, request=request,
                               response_type=str)
    mock_api.mock(f"/objectstore/transfers/{session_id}/chunks/1", HttpMethod.PUT)
    mock_api.mock(f"/objectstore/transfers/{session_id}", HttpMethod.GET, response=response)
    mock_api.mock(f"/objectstore/transfers/{session_id}/complete", HttpMethod.POST)


def mock_file_download(
        mock_api: MockApi,
        namespace: str,
        file_name: str,
        file_content: bytes,
        chunk_size: int
):
    content_hash = HashUtils.calculate_md5_in_base_64(input_value=file_content)
    response = TransferStatusResponse(
        namespace=namespace,
        objectName=file_name,
        objectSize=len(file_content),
        chunkSize=chunk_size,
        chunkCount=1,
        chunksReceived=[1]
    )
    start_response = mock_api.mock(
        f"/objectstore/objects/{namespace}/startDownload",
        HttpMethod.POST,
        request=ObjectDownloadRequest(
            objectName=file_name,
            chunkSize=chunk_size
        ),
        response=ObjectDownloadResponse(
            sessionId=make_string(),
            namespace=namespace,
            objectName=file_name,
            objectSize=len(file_content),
            chunkSize=chunk_size,
            chunkCount=1
        )
    )
    session_id = start_response.sessionId

    mock_api.mock(
        f"/objectstore/transfers/{session_id}/chunks/1",
        HttpMethod.GET,
        response=file_content,
        response_headers={"Content-MD5": content_hash}
    )
    mock_api.mock(f"/objectstore/transfers/{session_id}", HttpMethod.GET, response=response)
    mock_api.mock(f"/objectstore/transfers/{session_id}/complete", HttpMethod.POST)


def test_can_upload_objects(tmp_path: Path, mock_api: MockApi, object_store_client: ObjectStoreClient):
    test_file_size = 1024
    test_file = create_file(tmp_path, test_file_size)
    namespace = make_string()
    mock_file_upload(mock_api, namespace, test_file, test_file_size, object_store_client.upload_chunk_size)

    session = object_store_client.create_upload_session(
        file_namespace=namespace,
        source_file_path=str(test_file)
    )
    session.bind(on_error=lambda event_args: print(event_args.message))
    session.start()

    session = session.when_status_matches(lambda status: status.is_finished()).result()
    assert session.status == FileTransferStatus.Completed
    mock_api.verify_all_requests_called()


def test_can_batch_upload_objects(tmp_path: Path, mock_api: MockApi, object_store_client: ObjectStoreClient):
    namespace = make_string()
    test_file_size = 1024
    first_test_file = create_file(tmp_path, test_file_size)
    second_test_file = create_file(tmp_path, test_file_size)

    mock_file_upload(mock_api, namespace, first_test_file, test_file_size, object_store_client.upload_chunk_size)
    mock_file_upload(mock_api, namespace, second_test_file, test_file_size, object_store_client.upload_chunk_size)

    builder = object_store_client.build_upload_batch()
    builder.find_source_objects(source_directory_path=str(tmp_path), source_file_pattern="*")
    builder.namespace = namespace

    batch = builder.get_batch_if_objects_found()
    batch.add_session_error_listener(lambda event_args: print(event_args.message))
    batch.start()
    batch = batch.when_status_matches(lambda status: status.is_finished()).result()
    assert batch.status == FileTransferStatus.Completed
    mock_api.verify_all_requests_called()


def test_can_download_objects(tmp_path: Path, mock_api: MockApi, object_store_client: ObjectStoreClient):
    namespace = make_string()
    file_name = make_string()
    file_content = make_bytes()
    mock_file_download(mock_api, namespace, file_name, file_content, object_store_client.download_chunk_size)

    session = object_store_client.create_download_session(
        file_namespace=namespace,
        file_name=file_name,
        destination_folder_path=str(tmp_path)
    )
    session.bind(on_error=lambda event_args: print(event_args.message))
    session.start()

    session = session.when_status_matches(lambda status: status.is_finished()).result()

    downloaded_file = tmp_path / file_name

    assert session.status == FileTransferStatus.Completed
    assert downloaded_file.exists()
    assert downloaded_file.read_bytes() == file_content
    mock_api.verify_all_requests_called()


def test_can_batch_download_objects(tmp_path: Path, mock_api: MockApi, object_store_client: ObjectStoreClient):
    namespace = make_string()

    first_file_name = make_string()
    first_file_content = make_bytes()

    second_file_name = make_string()
    second_file_content = make_bytes()

    mock_file_download(mock_api, namespace, first_file_name, first_file_content,
                       object_store_client.download_chunk_size)
    mock_file_download(mock_api, namespace, second_file_name, second_file_content,
                       object_store_client.download_chunk_size)
    mock_api.mock(f"/objectstore/objects/{namespace}", HttpMethod.GET, response=Slice([
        ObjectPath(name=first_file_name),
        ObjectPath(name=second_file_name)
    ]))

    builder = object_store_client.build_download_batch()
    builder.find_source_objects(namespace=namespace, object_name_pattern="*")
    builder.destination_folder = str(tmp_path)

    batch = builder.get_batch_if_objects_found()
    batch.add_session_error_listener(lambda event_args: print(event_args.message))
    batch.start()
    batch = batch.when_status_matches(lambda status: status.is_finished()).result()

    assert batch.status == FileTransferStatus.Completed

    first_downloaded_file = tmp_path / first_file_name
    assert first_downloaded_file.exists()
    assert first_downloaded_file.read_bytes() == first_file_content

    second_downloaded_file = tmp_path / second_file_name
    assert second_downloaded_file.exists()
    assert second_downloaded_file.read_bytes() == second_file_content

    mock_api.verify_all_requests_called()


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
