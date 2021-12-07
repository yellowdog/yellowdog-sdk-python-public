from enum import Enum


class AuthenticationProvider(Enum):
    YELLOWDOG = "YELLOWDOG"
    AZURE = "AZURE"

    def __str__(self) -> str:
        return self.name
