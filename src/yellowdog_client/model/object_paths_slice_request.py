from dataclasses import dataclass
from typing import Optional

from .slice_reference import SliceReference


@dataclass
class ObjectPathsSliceRequest:
    namespace: Optional[str] = None
    flat: bool = False
    prefix: Optional[str] = None
    sliceReference: SliceReference = SliceReference()
