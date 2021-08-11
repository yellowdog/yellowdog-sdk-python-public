from typing import List

from typish import get_args
import jsons
from jsons import default_list_deserializer

from yellowdog_client.common.json import object_deserializer
from .images_client import ImagesClient
from .images_client_impl import ImagesClientImpl
from .images_service_proxy import ImagesServiceProxy
from .page import Page
from .pageable import Pageable
from .sort import Sort


def page_deserializer(value: dict, cls: type, **kwargs) -> object:
    p = object_deserializer(value, Page)

    if "content" in value:
        arg = get_args(cls)[0]
        p.content = default_list_deserializer(value["content"], List[arg])

    return p


jsons.set_deserializer(page_deserializer, Page)

__all__ = [
    "ImagesClient",
    "ImagesClientImpl",
    "ImagesServiceProxy",
    "Page",
    "Pageable",
    "Sort"
]
