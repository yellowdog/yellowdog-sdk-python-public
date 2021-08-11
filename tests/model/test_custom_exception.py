import pytest

from yellowdog_client.model.exceptions import ChunkTransferException
from yellowdog_client.model.exceptions import FileTransferFailure
from yellowdog_client.model.exceptions import InvalidSessionException
from yellowdog_client.model.exceptions import InvalidRequestException
from yellowdog_client.model.exceptions import InternalServerException
from yellowdog_client.model.exceptions import NotAuthorisedException
from yellowdog_client.model.exceptions import ObjectNotFoundException
from yellowdog_client.model.exceptions import SessionCloseException
from yellowdog_client.model.exceptions import SessionNotFoundException
from yellowdog_client.model.exceptions import InsufficientCapacityException
from yellowdog_client.model.exceptions import UnknownException
from .test_utils import should_serde


def test_str():
    ex = SessionCloseException(message="some message", detail=("detail1", "detail2", "detail3"))

    assert str(ex) == "SessionCloseException: some message. detail1. detail2. detail3"


@pytest.mark.parametrize(
    "exception_type,exception_type_str",
    [
        (ChunkTransferException, "ChunkTransferException"),
        (FileTransferFailure, "FileTransferFailure"),
        (InvalidSessionException, "InvalidSessionException"),
        (InvalidRequestException, "InvalidRequestException"),
        (InternalServerException, "InternalServerException"),
        (NotAuthorisedException, "NotAuthorisedException"),
        (ObjectNotFoundException, "ObjectNotFoundException"),
        (SessionCloseException, "SessionCloseException"),
        (SessionNotFoundException, "SessionNotFoundException"),
        (InsufficientCapacityException, "InsufficientCapacityException"),
        (UnknownException, "Unknown")
    ]
)
def test_chunk_transfer(exception_type, exception_type_str):
    obj_in_raw = exception_type(message="MY_MESSAGE", detail=("detail1", "detail2", "detail3"))

    obj_in_dict = {
        "message": "MY_MESSAGE",
        "detail": ["detail1", "detail2", "detail3"],
        "errorType": exception_type_str,
    }

    should_serde(obj_in_raw, obj_in_dict)
