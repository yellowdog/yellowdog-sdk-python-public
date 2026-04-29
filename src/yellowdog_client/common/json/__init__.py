"""
JSON serialization/deserialization for YellowDog SDK model classes.

We use cattrs as the backbone and layer three customizations on top.

  1. ``datetime`` / ``timedelta``: ISO 8601 wire format instead of cattrs' default.

  2. All ``yellowdog_client`` model classes get a shared predicate hook that handles:

       **None omission** — None-valued fields are dropped from the serialized dict.

       **Keyword field renaming** — Python fields whose names shadow keywords (e.g.
       ``global_``) are mapped to their JSON equivalents (e.g. ``global``) using
       cattrs' ``override(rename=…)`` mechanism.

       **Polymorphic dispatch** — classes that carry a ``type``, ``action``, or
       ``errorType`` discriminator field are routed to the correct concrete subclass
       during deserialization.  The dispatch table is built lazily on first use by
       scanning all loaded subclasses.

"""
import dataclasses
import json
import typing
from datetime import datetime, timedelta
from enum import Enum
from functools import lru_cache
from typing import TypeVar, Type, Any, ClassVar, Optional, get_origin

from cattrs import Converter
from cattrs.cols import is_any_set, iterable_unstructure_factory
from cattrs.gen import make_dict_structure_fn, make_dict_unstructure_fn, override

from yellowdog_client.common.iso_datetime import iso_format, iso_parse, iso_timedelta_format, iso_timedelta_parse
from yellowdog_client.model.exceptions import BaseCustomException

T = TypeVar('T')

_keywords = {'global'}


def _is_yellowdog_class(cls: Any) -> bool:
    """True for non-enum yellowdog_client model classes; False for everything else."""
    raw_cls = get_origin(cls) or cls
    if not isinstance(raw_cls, type):
        return False
    if issubclass(raw_cls, Enum):
        return False
    module: str = getattr(raw_cls, '__module__', '') or ''
    return module.startswith('yellowdog_client')


# ── Field naming ──────────────────────────────────────────────────────────────

def _field_to_json_key(field_name: str) -> str:
    """Map a Python attribute name to its JSON key (strips trailing _ from keywords)."""
    if field_name.endswith('_') and field_name[:-1] in _keywords:
        return field_name[:-1]
    return field_name


def _field_to_json_key_overrides(cls: Any) -> dict[str, Any]:
    """cattrs ``override(rename=…)`` entries for keyword-shadowed fields (e.g. ``global_``)."""
    return {
        f.name: override(rename=_field_to_json_key(f.name))
        for f in dataclasses.fields(cls)
        if _field_to_json_key(f.name) != f.name
    }


# ── Subclass discovery (for polymorphic dispatch) ─────────────────────────────

def _all_subclasses(cls: type) -> set[type]:
    return set(cls.__subclasses__()).union(
        s for c in cls.__subclasses__() for s in _all_subclasses(c)
    )


def _leaf_subclasses(cls: type[T]) -> set[type[T]]:
    result: set[type[T]] = set()

    def _recurse(subcls: type[T]) -> None:
        for subclass in subcls.__subclasses__():
            if subclass.__subclasses__():
                _recurse(subclass)
            else:
                result.add(subclass)

    _recurse(cls)
    return result


@dataclasses.dataclass
class PolymorphicDispatch(typing.Generic[T]):
    discriminator_field: str
    subclasses: dict[str, type[T]]

def _get_polymorphic_dispatch(raw_cls: Type[T], hints: dict[str, Any]) -> Optional[PolymorphicDispatch[T]]:
    """Return ``(discriminator_field, {value: subclass})`` for polymorphic classes, or ``None``."""
    for disc in ('type', 'action'):
        if disc in hints:
            return PolymorphicDispatch(disc, {
                getattr(s, disc): s for s in _leaf_subclasses(raw_cls)
                if hasattr(s, disc) and getattr(s, disc) is not None
            })
    if 'errorType' in hints:
        return PolymorphicDispatch('errorType', {
            getattr(s, 'errorType').value: s for s in _leaf_subclasses(raw_cls)
            if hasattr(s, 'errorType') and getattr(s, 'errorType') is not None
        })
    return None


# ── Structure / unstructure function factories ────────────────────────────────

@lru_cache(maxsize=None)
def _make_structure_fn(cls: Any) -> Any:
    """
    Build and cache a ``(dict, type) → object`` structure function for *cls*.

    **Dataclass** (concrete or parameterized generic e.g. ``Slice[WorkerPoolSummary]``)
    — delegates to ``make_dict_structure_fn`` passing the full type (including type
    arguments), which cattrs resolves correctly.  Handles field renaming, ``init=False``
    fields, and defaults.

    **Non-dataclass** (typically an ABC used as a polymorphic parent type) — structure
    by attribute assignment via ``__new__``.  In practice ``_polymorphic_dispatch``
    routes these to a concrete dataclass subclass before this path is reached.

    If the class uses a discriminator field the returned function first checks the
    discriminator and delegates to ``_converter.structure`` for the concrete subclass.
    """
    origin = get_origin(cls)
    raw_cls = origin if (origin is not None and isinstance(origin, type)) else cls
    hints = typing.get_type_hints(raw_cls)

    # ── Base structure function (no dispatch) ──────────────────────────────────

    if dataclasses.is_dataclass(raw_cls):
        # Delegate to cattrs, passing the full type so it resolves any type arguments.
        _cattrs_fn = make_dict_structure_fn(
            cls, _converter,
            _cattrs_include_init_false=True,
            **_field_to_json_key_overrides(raw_cls),
        )

        def _structure(d: Any, t: Any) -> Any:
            return _cattrs_fn(d, t)

    else:
        # Non-dataclass: structure by attribute assignment.
        _field_map = {
            _field_to_json_key(name): (name, hint)
            for name, hint in hints.items()
            if typing.get_origin(hint) is not ClassVar
        }

        def _structure(d: Any, t: Any) -> Any:
            instance = raw_cls.__new__(raw_cls)
            for json_k, (fname, ftype) in _field_map.items():
                if json_k not in d:
                    continue
                v = d[json_k]
                if v is None:
                    setattr(instance, fname, None)
                elif ftype is not None:
                    setattr(instance, fname, _converter.structure(v, ftype))
                else:
                    setattr(instance, fname, v)
            return instance

    # ── Wrap with polymorphic dispatch if needed ───────────────────────────────

    polymorphic_dispatch = _get_polymorphic_dispatch(raw_cls, hints)
    if polymorphic_dispatch is None:
        return _structure

    dispatch = polymorphic_dispatch
    def _structure_with_dispatch(d: Any, t: Any) -> Any:
        if not isinstance(d, dict):
            return d
        discriminator = d.get(dispatch.discriminator_field)
        if discriminator is not None and isinstance(discriminator, str) and discriminator in dispatch.subclasses:
            return _converter.structure(d, dispatch.subclasses[discriminator])
        return _structure(d, t)

    return _structure_with_dispatch


@lru_cache(maxsize=None)
def _make_unstructure_fn(cls: Any) -> Any:
    """
    Build and cache an ``object → dict`` unstructure function for *cls*.

    For dataclasses: delegates to ``make_dict_unstructure_fn``, then drops ``None``
    values from the result dict.

    For non-dataclasses: walks ``__dict__`` and class-level hints, dropping ``None``
    values.

    Unstructuring always uses ``type(obj)`` (the concrete class), so TypeVar
    resolution is not required — each field value is unstructured by its actual
    runtime type via the converter.
    """
    origin = get_origin(cls)
    raw_cls = origin if (origin is not None and isinstance(origin, type)) else cls

    if dataclasses.is_dataclass(raw_cls):
        _cattrs_fn = make_dict_unstructure_fn(
            raw_cls, _converter,  # type: ignore[arg-type]
            _cattrs_include_init_false=True,
            **_field_to_json_key_overrides(raw_cls),
        )

        def _unstructure(obj: Any) -> Any:
            return {k: v for k, v in _cattrs_fn(obj).items() if v is not None}

    else:
        hints = typing.get_type_hints(raw_cls)

        def _unstructure(obj: Any) -> Any:
            result: dict[str, Any] = {}
            instance_dict = vars(obj)
            for attr_name, v in instance_dict.items():
                if attr_name.startswith('_') or v is None:
                    continue
                result[_field_to_json_key(attr_name)] = _converter.unstructure(v)
            for name, hint in hints.items():
                if name.startswith('_') or name in instance_dict:
                    continue
                if typing.get_origin(hint) is ClassVar:
                    continue
                v = getattr(obj, name, None)
                if v is None:
                    continue
                result[_field_to_json_key(name)] = _converter.unstructure(v)
            return result

    return _unstructure


# ── Converter ─────────────────────────────────────────────────────────────────

_converter = Converter()

# Exact-class hooks take priority over predicate hooks, so these fire before the
# user-class predicate hook even though user-class includes datetime/timedelta.
_converter.register_structure_hook(datetime, lambda v, _: iso_parse(v))
_converter.register_unstructure_hook(datetime, iso_format)
_converter.register_structure_hook(timedelta, lambda v, _: iso_timedelta_parse(v))
_converter.register_unstructure_hook(timedelta, iso_timedelta_format)

# sets are not JSON-serialisable; unstructure them as lists.
_converter.register_unstructure_hook_factory(
    is_any_set,
    lambda cl: iterable_unstructure_factory(cl, _converter, unstructure_to=list),
)

# All yellowdog_client model classes: None omission, field renaming, and polymorphic dispatch.
_converter.register_structure_hook_func(
    _is_yellowdog_class,
    lambda value, cls: _make_structure_fn(cls)(value, cls),
)
_converter.register_unstructure_hook_func(
    _is_yellowdog_class,
    # ignore[arg-type] because type(obj) is always a class object, and all classes are hashable. mypy can't
    # prove this for type[Any] because a class could set __hash__ = None, but that
    # doesn't apply to class objects themselves (only to their instances).
    lambda obj: _make_unstructure_fn(type(obj))(obj)  # type: ignore[arg-type]
)


# ── Public API ────────────────────────────────────────────────────────────────

class Json:
    @classmethod
    def dumps(cls, value: object) -> str:
        return json.dumps(cls.dump(value))

    @staticmethod
    def dump(value: object) -> object:
        return _converter.unstructure(value)

    @classmethod
    def loads(cls, value: str, value_class: Type[T]) -> T:
        return cls.load(json.loads(value), value_class)

    @staticmethod
    def load(value: object, value_class: Type[T]) -> T:
        return _converter.structure(value, value_class)
