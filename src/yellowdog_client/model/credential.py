from dataclasses import dataclass, field


@dataclass
class Credential:
    """Interface implemented by classes used to provide cloud provider-specific credentials to YellowDog Compute."""
    type: str = field(default=None, init=False)
