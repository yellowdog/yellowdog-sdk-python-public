from dataclasses import dataclass


@dataclass
class UserLoginRequest:
    username: str
    password: str
