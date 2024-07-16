from dataclasses import dataclass


@dataclass
class UserAgent:
    application_id: str
    application_version: str
    python_version: str
