from dataclasses import dataclass


@dataclass
class ExistingPasswordRequest:
    password: str
