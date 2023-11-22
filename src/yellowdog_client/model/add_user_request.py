from dataclasses import dataclass


@dataclass
class AddUserRequest:
    username: str
    name: str
    email: str
