import enum
import os
import random
import string
import typing
from datetime import datetime, timedelta, timezone
from typing import Type, TypeVar

import typing_compat

T = TypeVar('T')


def make_enum(enum_class: Type[T]) -> T:
    return random.choice(list(enum_class))


def make_int(min_value: int = 0, max_value=100) -> int:
    return random.randint(min_value, max_value)


def make_datetime(min_year=1900, max_year=datetime.now().year) -> datetime:
    start = datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    result = start + (end - start) * random.random()
    return result.replace(tzinfo=timezone.utc, microsecond=0)


def make_string(length: int = 10) -> str:
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


def make_bytes(length: int = 10) -> bytes:
    return os.urandom(length)


def make(cls: Type[T]) -> T:
    return _make_value(cls)


def _make_value(cls: Type[T]):
    origin = typing_compat.get_origin(cls)

    if origin is typing.Union:
        type_args = typing_compat.get_args(cls)
        # Return first type in the Union that isn't None
        type_arg = next(type_arg for type_arg in type_args if type_arg is not type(None))
        return _make_value(type_arg)
    elif origin is list:
        type_arg = typing_compat.get_args(cls)[0]
        return [_make_value(type_arg), _make_value(type_arg)]
    elif origin is dict:
        key_cls, value_cls = typing_compat.get_args(cls)
        return {
            _make_value(key_cls): _make_value(value_cls),
            _make_value(key_cls): _make_value(value_cls)
        }
    elif cls is str:
        return make_string()
    elif cls is bytes:
        return make_bytes()
    elif cls is datetime:
        return make_datetime()
    elif cls is int:
        return make_int()
    elif issubclass(cls, enum.Enum):
        return make_enum(cls)

    return _make_object(cls)


def _make_object(cls: Type[T]):
    type_hints = typing.get_type_hints(cls)
    try:
        instance = cls.__new__(cls)
    except TypeError:
        raise RuntimeError(f"Unable to make {cls}")

    for attr_name, attr_type in type_hints.items():
        attr_value = _make_value(attr_type)
        setattr(instance, attr_name, attr_value)
    return instance
