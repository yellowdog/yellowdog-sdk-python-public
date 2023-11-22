from dataclasses import dataclass


@dataclass
class EmailChangeRequest:
    newEmail: str
