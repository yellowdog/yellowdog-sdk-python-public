from dataclasses import dataclass


@dataclass
class SetPasswordRequest:
    accountName: str
    username: str
    password: str
    token: str
