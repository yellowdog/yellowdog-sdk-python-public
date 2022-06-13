from enum import Enum


class PasswordState(Enum):
    USER_PROVIDED = "USER_PROVIDED"
    UNSET = "UNSET"

    def __str__(self) -> str:
        return self.name
