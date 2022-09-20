from dataclasses import dataclass, field

from .identified import Identified


@dataclass
class Instance(Identified):
    """
    Describes a instance provisioned for a compute requirement.

    This class provides common fields shared across all compute provisioners.
    It is generally specialised for each provisioner to add extra fields specific to that provisioner.
    """

    type: str = field(default=None, init=False)
