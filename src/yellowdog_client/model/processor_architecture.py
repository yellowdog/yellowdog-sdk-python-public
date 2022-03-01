from enum import Enum


class ProcessorArchitecture(Enum):
    X86_64 = "X86_64"
    ARM64 = "ARM64"

    def __str__(self) -> str:
        return self.name
