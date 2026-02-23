from abc import ABC
from typing import Dict, Optional

from .identified import Identified
from .named import Named



class ComputeRequirementTemplate(Identified, Named, ABC):
    type: str
    id: Optional[str]
    name: Optional[str]
    namespace: Optional[str]
    description: Optional[str]
    strategyType: Optional[str]
    imagesId: Optional[str]
    userData: Optional[str]
    instanceTags: Optional[Dict[str, str]]
