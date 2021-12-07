from dataclasses import dataclass


@dataclass
class NewPasswordRequest:
    password: str
