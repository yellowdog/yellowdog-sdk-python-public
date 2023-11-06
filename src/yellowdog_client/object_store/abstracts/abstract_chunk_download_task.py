from typing import Callable

from .abstract_chunk_transfer_task import AbstractChunkTransferTask


class AbstractChunkDownloadTask(AbstractChunkTransferTask):
    write_chunk_data: Callable[[str], None] = None
