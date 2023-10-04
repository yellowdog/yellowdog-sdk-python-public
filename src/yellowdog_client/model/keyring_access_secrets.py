from dataclasses import dataclass


@dataclass
class KeyringAccessSecrets:
    keyringPassword: str
    accessorSecret: str
