from dataclasses import dataclass
from typing import Optional


@dataclass
class ObjectDownloadResponse:
    sessionId: Optional[str] = None
    namespace: Optional[str] = None
    objectName: Optional[str] = None
    objectSize: Optional[int] = None
    chunkSize: Optional[int] = None
    chunkCount: Optional[int] = None
