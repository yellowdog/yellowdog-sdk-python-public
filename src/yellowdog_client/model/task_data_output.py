from dataclasses import dataclass


@dataclass
class TaskDataOutput:
    source: str
    destination: str
    alwaysUpload: bool = False
