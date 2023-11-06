from typing import Callable

from .abstract_chunk_transfer_task import AbstractChunkTransferTask


class AbstractChunkUploadTask(AbstractChunkTransferTask):
    read_chunk_data: Callable[[], str] = None
