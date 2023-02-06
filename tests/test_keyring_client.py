from typing import List

import pytest

from util.api import MockApi, HttpMethod
from util.data import make, make_string
from yellowdog_client import PlatformClient
from yellowdog_client.account import KeyringClient
from yellowdog_client.model import ServicesSchema, ApiKey, CreateKeyringResponse, KeyringSummary, Keyring, \
    AwsCredential, KeyringCredential


@pytest.fixture
def keyring_client(mock_api: MockApi) -> KeyringClient:
    platform_client = PlatformClient.create(
        ServicesSchema(defaultUrl=mock_api.url()),
        make(ApiKey)
    )
    return platform_client.keyring_client


def test_can_create_keyring(mock_api: MockApi, keyring_client: KeyringClient):
    response = mock_api.mock("/keyrings/", HttpMethod.POST, response_type=CreateKeyringResponse)
    expected = response.keyring

    actual = keyring_client.create_keyring(response.keyring.name, response.keyring.description)

    assert actual == expected
    mock_api.verify_all_requests_called()


def test_can_delete_keyring(mock_api: MockApi, keyring_client: KeyringClient):
    keyring = make(Keyring)
    mock_api.mock(f"/keyrings/{keyring.name}", HttpMethod.DELETE)

    keyring_client.delete_keyring(keyring)

    mock_api.verify_all_requests_called()


def test_can_delete_keyring_by_name(mock_api: MockApi, keyring_client: KeyringClient):
    keyring_name = make_string()
    mock_api.mock(f"/keyrings/{keyring_name}", HttpMethod.DELETE)

    keyring_client.delete_keyring_by_name(keyring_name)

    mock_api.verify_all_requests_called()


def test_can_find_all_keyrings(mock_api: MockApi, keyring_client: KeyringClient):
    expected = mock_api.mock("/keyrings/", HttpMethod.GET, response_type=List[KeyringSummary])

    actual = keyring_client.find_all_keyrings()

    assert actual == expected
    mock_api.verify_all_requests_called()


def test_can_put_credential(mock_api: MockApi, keyring_client: KeyringClient):
    expected = make(Keyring)
    request = make(AwsCredential)
    expected.credentials.append(KeyringCredential(
        name=request.name,
        description=request.description,
        type=request.type
    ))
    mock_api.mock(f"/keyrings/{expected.name}/credentials", HttpMethod.PUT, request=request, response=expected)

    actual = keyring_client.put_credential(expected, request)

    assert actual == expected
    mock_api.verify_all_requests_called()


def test_can_put_credential_by_name(mock_api: MockApi, keyring_client: KeyringClient):
    expected = make(Keyring)
    request = make(AwsCredential)
    expected.credentials.append(KeyringCredential(
        name=request.name,
        description=request.description,
        type=request.type
    ))
    mock_api.mock(f"/keyrings/{expected.name}/credentials", HttpMethod.PUT, request=request, response=expected)

    actual = keyring_client.put_credential_by_name(expected.name, request)

    assert actual == expected
    mock_api.verify_all_requests_called()


def test_can_delete_credential(mock_api: MockApi, keyring_client: KeyringClient):
    keyring = make(Keyring)
    credential_name = make_string()
    mock_api.mock(f"/keyrings/{keyring.name}/credentials/{credential_name}", HttpMethod.DELETE, response=keyring)

    actual = keyring_client.delete_credential(keyring, credential_name)

    assert actual == keyring
    mock_api.verify_all_requests_called()


def test_can_delete_credential_by_name(mock_api: MockApi, keyring_client: KeyringClient):
    keyring = make(Keyring)
    credential_name = make_string()
    mock_api.mock(f"/keyrings/{keyring.name}/credentials/{credential_name}", HttpMethod.DELETE, response=keyring)

    actual = keyring_client.delete_credential_by_name(keyring.name, credential_name)

    assert actual == keyring
    mock_api.verify_all_requests_called()
