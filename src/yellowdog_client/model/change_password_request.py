from dataclasses import dataclass


@dataclass
class ChangePasswordRequest:
    oldPassword: str
    newPassword: str
