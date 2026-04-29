"""Example model classes used by tests/common/test_json.py."""
import dataclasses
from abc import ABC
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, List, Set, Generic, TypeVar, ClassVar


@dataclass
class ExampleWithString:
    field: str


@dataclass
class ExampleWithBool:
    field: bool


@dataclass
class ExampleWithFloat:
    field: float


@dataclass
class ExampleWithDateTime:
    field: datetime


@dataclass
class ExampleWithTimeDelta:
    field: timedelta


@dataclass
class ExampleWithOptional:
    field: Optional[str]


@dataclass
class ExampleWithList:
    field: List[str]


@dataclass
class ExampleWithSet:
    field: Set[str]


@dataclass
class ExampleWithDefaultValue:
    field: Optional[str]
    fieldWithDefault: str = "some default"


@dataclass
class ExampleWithFieldNotInInit:
    field: str = dataclasses.field(init=False)

    @staticmethod
    def create(field: str) -> "ExampleWithFieldNotInInit":
        value = ExampleWithFieldNotInInit()
        value.field = field
        return value


@dataclass
class ExampleWithNested:
    field: ExampleWithString


class ExampleEnum(Enum):
    EXAMPLE = "EXAMPLE"


@dataclass
class ExampleWithEnum:
    field: ExampleEnum


@dataclass
class ExampleWithClassVar:
    classField: ClassVar[str] = "foo"


class ExampleBaseClass(ABC):
    classField: ClassVar[str] = "foo"
    type: str = dataclasses.field(default=None, init=False)


@dataclass
class FirstExampleSubclass(ExampleBaseClass):
    type: str = dataclasses.field(default="first", init=False)
    fieldFromFirst: str


@dataclass
class SecondExampleSubclass(ExampleBaseClass):
    type: str = dataclasses.field(default="second", init=False)
    fieldFromSecond: str


@dataclass
class ExampleWithKeyword:
    global_: str


ET = TypeVar('ET', bound=ExampleBaseClass)


@dataclass
class ExampleGeneric(Generic[ET]):
    field: ET


EL = TypeVar('EL')


@dataclass
class ExampleSlice(Generic[EL]):
    items: Optional[List[EL]]
    nextSliceId: Optional[str] = None


EU = TypeVar('EU')


class ExampleGenericBaseClass(ABC, Generic[EU]):
    type: str


@dataclass
class ExampleFirstSubclassOfGeneric(ExampleGenericBaseClass):
    type: str = dataclasses.field(default="first", init=False)
    fieldFromFirst: str


@dataclass
class ExampleSecondSubclassOfGeneric(ExampleGenericBaseClass):
    type: str = dataclasses.field(default="second", init=False)
    fieldFromSecond: str
