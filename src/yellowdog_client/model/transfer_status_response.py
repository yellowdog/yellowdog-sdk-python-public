from dataclasses import dataclass
from typing import List, Optional


@dataclass
class TransferStatusResponse:
    namespace: Optional[str] = None
    objectName: Optional[str] = None
    objectSize: Optional[int] = None
    chunkSize: Optional[int] = None
    chunkCount: Optional[int] = None
    chunksReceived: Optional[List[int]] = None
