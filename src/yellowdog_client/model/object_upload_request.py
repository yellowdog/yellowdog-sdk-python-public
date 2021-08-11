from dataclasses import dataclass


@dataclass
class ObjectUploadRequest:
    objectName: str
    objectSize: int
    chunkSize: int
    chunkCount: int
