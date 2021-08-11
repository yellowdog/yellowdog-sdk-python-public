from typing import Callable
from threading import Lock

from cancel_token import CancellationToken

from yellowdog_client.common import CountdownEvent


class AbstractChunkTransferTask(object):
    session_id = None  # type: str
    chunk_number = None  # type: int
    chunk_size = None  # type: int
    abort_token = None  # type: CancellationToken
    abort_lock = None  # type: Lock
    transfer_countdown = None           # type: CountdownEvent
    notify_chunk_transferred = None     # type: Callable[[str], None]
    notify_exception = None             # type: Callable[[Exception], None]
