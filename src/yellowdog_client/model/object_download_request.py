from dataclasses import dataclass


@dataclass
class ObjectDownloadRequest:
    objectName: str
    chunkSize: int
