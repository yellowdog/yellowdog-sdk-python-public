from dataclasses import dataclass


@dataclass
class UserLoginRequest:
    accountName: str
    username: str
    password: str
