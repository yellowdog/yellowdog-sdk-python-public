from enum import Enum


class AuthenticationProvider(Enum):
    YELLOWDOG = "YELLOWDOG"
    AZURE = "AZURE"
    OKTA = "OKTA"

    def __str__(self) -> str:
        return self.name
