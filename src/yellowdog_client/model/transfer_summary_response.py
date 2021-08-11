from dataclasses import dataclass
from typing import Optional


@dataclass
class TransferSummaryResponse:
    sessionId: Optional[str] = None
    accountId: Optional[str] = None
    namespace: Optional[str] = None
    objectName: Optional[str] = None
    objectSize: Optional[int] = None
    chunkSize: Optional[int] = None
    chunkCount: Optional[int] = None
    transferredChunkCount: Optional[int] = None
