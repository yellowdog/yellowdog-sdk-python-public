from dataclasses import dataclass
from typing import Optional

from .api_key import ApiKey
from .application import Application


@dataclass
class AddApplicationResponse:
    apiKey: Optional[ApiKey] = None
    application: Optional[Application] = None
