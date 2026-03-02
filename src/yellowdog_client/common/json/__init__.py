from datetime import datetime, timedelta
from typing import TypeVar, Type, List, Union, Optional, Any, ClassVar
import json
import typing

import jsons
from jsons import default_object_serializer, default_list_deserializer, DeserializationError, JsonsError
from jsons._common_impl import get_class_name, NoneType, JSON_KEYS
from jsons._compatibility_impl import get_union_params, get_naked_class
from jsons._load_impl import load
from jsons._dump_impl import dump
from typish import get_args
from yellowdog_client.model import Slice
from yellowdog_client.model.exceptions import BaseCustomException
from yellowdog_client.model.exceptions import ErrorType
from yellowdog_client.common.iso_datetime import iso_format, iso_parse, iso_timedelta_format, iso_timedelta_parse

T = TypeVar('T')


def _determine_subclass(value: dict[str, Type[Any]], cls: type) -> type:
    if "type" in value:
        type_field = "type"
        type_value = value[type_field]
    elif "action" in value:
        type_field = "action"
        type_value = value[type_field]
    elif "errorType" in value and cls is BaseCustomException:
        type_field = "errorType"
        error_type: ErrorType = ErrorType(value[type_field])

        naked_class = get_naked_class(cls)

        subclasses = all_subclasses(naked_class)
        if subclasses:
            return {getattr(x, type_field).value: x for x in subclasses}[error_type.value]
        return cls
    else:
        return cls

    naked_class = get_naked_class(cls)

    subclasses = leaf_subclasses(naked_class)
    if subclasses:
        return {getattr(x, type_field): x for x in subclasses}[type_value]
    return cls


def all_subclasses(cls: type) -> set[type]:
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)])


def leaf_subclasses(cls: type) -> set[type]:
    subclasses = set()

    def recurse(subcls: type) -> None:
        for subclass in subcls.__subclasses__():
            if subclass.__subclasses__():
                recurse(subclass)
            else:
                subclasses.add(subclass)

    recurse(cls)
    return subclasses


def slice_deserializer(value: dict[str, Any], cls: type, **kwargs: Any) -> object:
    slice: Slice[Any] = Slice()
    if "nextSliceId" in value:
        slice.nextSliceId = value["nextSliceId"]

    if "items" in value:
        arg = get_args(cls)[0]
        slice.items = default_list_deserializer(value["items"], List[arg])  # type: ignore[valid-type]  # runtime type construction from get_args()

    return slice


class NestedDeserializationError(JsonsError):  # type: ignore[misc]  # JsonsError is untyped third-party class
    def __init__(self, value: object, class_name: str, attribute_name: str, reason: str):
        message = f"Cannot deserialize '{value}' into {class_name}.{attribute_name}. Reason: {reason}"
        Exception.__init__(self, message)
        self.value = value
        self._message = message
        self.attribute_name = attribute_name
        self.reason = reason


def union_deserializer(obj: object, cls: Union, **kwargs: Any) -> object:
    errors = {}
    for sub_type in get_union_params(cls):
        if obj is not None and sub_type is NoneType:
            continue
        try:
            return load(obj, sub_type, **kwargs)
        except JsonsError as ex:
            errors[get_class_name(sub_type)] = ex
            pass  # Try the next one.
    else:
        if len(errors) == 1:
            raise next(iter(errors.values()))
        args_msg = '\n    * '.join('%s: %s' % (class_name, ex.message) for class_name, ex in errors.items())
        err_msg = ('Could not deserialize to any type of the Union:\n    * {}'.format(args_msg))
        raise NestedDeserializationError(obj, cls, '', err_msg)


def object_deserializer(value: dict[str, Type[Any]], cls: type[Any], **kwargs: Any) -> object:
    subclass = _determine_subclass(value, cls)
    naked_subclass = get_naked_class(subclass)
    type_hints = get_type_hints(subclass, naked_subclass)
    instance = naked_subclass.__new__(naked_subclass)
    class_name = naked_subclass.__name__
    for attr_name, attr_value in value.items():
        attr_name = f"{attr_name}_" if attr_name in keywords else attr_name
        try:
            attr_type = type_hints[attr_name]
        except KeyError:
            # Silently ignore for backwards compatibility with new fields introduced into the API
            continue

        if typing.get_origin(attr_type) is ClassVar:
            continue

        try:
            loaded_attr = load(attr_value, attr_type, **kwargs)
        except DeserializationError as ex:
            raise NestedDeserializationError(attr_value, class_name, attr_name, ex.message) from ex
        except NestedDeserializationError as ex:
            nested_attr_name = attr_name + "." + ex.attribute_name
            raise NestedDeserializationError(ex.value, class_name, nested_attr_name, ex.reason) from ex.__cause__
        setattr(instance, attr_name, loaded_attr)

    return instance


def object_serializer(obj: Any, **kwargs: Any) -> Any:
    class_var_names = _get_class_var_field_names(obj)
    strip_attr = _merge_strip_attrs(class_var_names, kwargs)
    return default_object_serializer(obj, strip_attr=strip_attr, **kwargs)


def _merge_strip_attrs(class_var_names: tuple[Any, ...], kwargs: dict[str, Any]) -> Any:
    inherited_strip = kwargs.pop('strip_attr', ()) or ()
    if isinstance(inherited_strip, str):
        inherited_strip = (inherited_strip,)
    strip_attr = tuple(inherited_strip) + class_var_names
    return strip_attr


def _get_class_var_field_names(obj: Any) -> tuple[Any, ...]:
    type_hints = typing.get_type_hints(type(obj))
    class_var_names = tuple(
        name for name, hint in type_hints.items()
        if typing.get_origin(hint) is ClassVar
    )
    return class_var_names


def dict_serializer(
        obj: dict[str, Any],
        cls: Optional[type] = None,
        **kwargs: Any
) -> dict[str, Any]:
    result = dict()
    for key in obj:
        obj_ = obj[key]
        if not any(issubclass(type(key), json_key) for json_key in JSON_KEYS):
            key = dump(key)

        dumped_elem = dump(obj_, cls=cls, **kwargs)
        result[key] = dumped_elem
    return result


def get_type_hints(cls: Any, naked_cls: Any) -> dict[str, Any]:
    if naked_cls != cls:
        type_hints = typing.get_type_hints(naked_cls)
        type_params = dict(zip(naked_cls.__parameters__, cls.__args__))
        for k, v in type_hints.items():
            if v in type_params:
                type_hints[k] = type_params[v]
        return type_hints
    return typing.get_type_hints(cls)


jsons.set_serializer(lambda value, **kwargs: iso_format(value), datetime)
jsons.set_serializer(lambda value, **kwargs: iso_timedelta_format(value), timedelta)
jsons.set_serializer(
    lambda value, **kwargs: default_object_serializer(value, strip_attr=("args", "with_traceback")),
    BaseCustomException
)
jsons.set_serializer(object_serializer, object, False)
jsons.set_serializer(dict_serializer, typing.Mapping, True)
jsons.set_deserializer(lambda value, cls=datetime, **kwargs: iso_parse(value), datetime)
jsons.set_deserializer(lambda value, cls=datetime, **kwargs: iso_timedelta_parse(value), timedelta)
jsons.set_deserializer(slice_deserializer, Slice)
jsons.set_deserializer(union_deserializer, (Union, Optional))
jsons.set_deserializer(object_deserializer, object, False)

keywords = {'global'}


def deserialization_key_transformer(key: str) -> str:
    return key[:-1] if key[:-1] in keywords else key


class Json:
    @classmethod
    def dumps(cls, value: object) -> str:
        return json.dumps(cls.dump(value))

    @staticmethod
    def dump(value: object) -> object:
        return jsons.dump(value, strip_nulls=True, strip_privates=True, use_enum_name=True, key_transformer=deserialization_key_transformer)

    @classmethod
    def loads(cls, value: str, value_class: Type[T]) -> T:
        return cls.load(json.loads(value), value_class)

    @staticmethod
    def load(value: object, value_class: Type[T]) -> T:
        return typing.cast(T, jsons.load(value, value_class))
