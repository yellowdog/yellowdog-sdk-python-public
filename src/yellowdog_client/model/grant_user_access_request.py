from dataclasses import dataclass


@dataclass
class GrantUserAccessRequest:
    userPassword: str
