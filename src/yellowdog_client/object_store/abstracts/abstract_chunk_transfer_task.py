from typing import Callable
from threading import Lock

from cancel_token import CancellationToken

from yellowdog_client.common import CountdownEvent


class AbstractChunkTransferTask(object):
    session_id: str = None
    chunk_number: int = None
    chunk_size: int = None
    abort_token: CancellationToken = None
    abort_lock: Lock = None
    transfer_countdown: CountdownEvent = None
    notify_chunk_transferred: Callable[[str], None] = None
    notify_exception: Callable[[Exception], None] = None
