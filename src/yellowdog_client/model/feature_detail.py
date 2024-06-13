from dataclasses import dataclass
from typing import Optional


@dataclass
class FeatureDetail:
    name: Optional[str] = None
    title: Optional[str] = None
