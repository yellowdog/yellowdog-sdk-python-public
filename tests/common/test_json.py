import json
from datetime import datetime, timezone, timedelta
from typing import Type, TypeVar, List, Any

import pytest
from yellowdog_client.common.json import Json
from yellowdog_client.model.exceptions import BaseCustomException, InvalidRequestException
from yellowdog_client_test.fixtures import (
    ExampleWithString, ExampleWithBool, ExampleWithFloat,
    ExampleWithDateTime, ExampleWithTimeDelta, ExampleWithOptional,
    ExampleWithList, ExampleWithSet, ExampleWithDefaultValue, ExampleWithFieldNotInInit,
    ExampleWithNested, ExampleEnum, ExampleWithEnum,
    ExampleBaseClass, FirstExampleSubclass, SecondExampleSubclass,
    ExampleWithKeyword, ExampleGeneric, ExampleSlice,
    ExampleGenericBaseClass, ExampleFirstSubclassOfGeneric, ExampleSecondSubclassOfGeneric, ExampleWithClassVar,
)

T = TypeVar('T')

symmetric_operations = [
    pytest.param('{"field": "some text"}', ExampleWithString, ExampleWithString("some text"), id="string field"),
    pytest.param('{"field": true}', ExampleWithBool, ExampleWithBool(True), id="bool field"),
    pytest.param('{"field": 1.1}', ExampleWithFloat, ExampleWithFloat(1.1), id="float field"),
    pytest.param('{"field": "2023-01-01T12:01:01.000Z"}', ExampleWithDateTime, ExampleWithDateTime(
        datetime(year=2023, month=1, day=1, hour=12, minute=1, second=1, tzinfo=timezone.utc)
    ), id="datetime field"),
    pytest.param('{"field": "P1DT4H5M"}', ExampleWithTimeDelta, ExampleWithTimeDelta(
        timedelta(days=1, hours=4, minutes=5)
    ), id="timedelta field"),
    pytest.param('{"field": "EXAMPLE"}', ExampleWithEnum, ExampleWithEnum(ExampleEnum.EXAMPLE), id="enum field"),
    pytest.param('{"field": "some text"}', ExampleWithOptional, ExampleWithOptional(
        "some text"
    ), id="optional field"),
    pytest.param('{"field": ["first", "second"]}', ExampleWithList, ExampleWithList(
        ["first", "second"]
    ), id="list field"),
    pytest.param('{"field": ["a"]}', ExampleWithSet, ExampleWithSet({"a"}), id="set field"),
    pytest.param('{"field": []}', ExampleWithList, ExampleWithList([]), id="empty list field"),
    pytest.param('["first", "second"]', List[str], ["first", "second"], id="list of strings"),
    pytest.param('[{"field": "first"}, {"field": "second"}]', List[ExampleWithString], [
        ExampleWithString("first"),
        ExampleWithString("second")
    ], id="list of objects"),
    pytest.param('{"field": {"field": "some text"}}', ExampleWithNested, ExampleWithNested(
        ExampleWithString("some text")
    ), id="nested object"),
    pytest.param('{"fieldFromFirst": "some text", "type": "first"}', ExampleBaseClass, FirstExampleSubclass(
        "some text"
    ), id="subclass with type"),
    pytest.param('{"field": "some text"}', ExampleWithFieldNotInInit, ExampleWithFieldNotInInit.create(
        "some text"
    ), id="field not in init"),
    pytest.param('{"global": "some text"}', ExampleWithKeyword, ExampleWithKeyword(global_="some text"), id="keyword field"),
]

deserialization_operations = [
    pytest.param('{"field": null}', ExampleWithOptional, ExampleWithOptional(None), id="null optional field"),
    pytest.param('{"field": "some text"}', ExampleWithDefaultValue, ExampleWithDefaultValue(
        "some text", "some default"
    ), id="field with default value"),
    pytest.param("""{
        "field": {
            "type": "second",
            "fieldFromSecond": "some text"
        }
    }""", ExampleGeneric[SecondExampleSubclass], ExampleGeneric(
        SecondExampleSubclass("some text")
    ), id="generic field"),
    pytest.param("""{
        "type": "first",
        "fieldFromFirst": "some text"
    }""", ExampleGenericBaseClass, ExampleFirstSubclassOfGeneric("some text"), id="subclass of generic case class"),
    pytest.param("""[
        {"type": "first", "fieldFromFirst": "first text"},
        {"type": "second", "fieldFromSecond": "second text"}
    ]""", List[ExampleGenericBaseClass[Any]], [
        ExampleFirstSubclassOfGeneric("first text"),
        ExampleSecondSubclassOfGeneric("second text")
    ], id="list of subclasses of generic case class"),
    pytest.param(
        '{"items": [{"field": "first"}, {"field": "second"}], "nextSliceId": "abc"}',
        ExampleSlice[ExampleWithString],
        ExampleSlice(items=[ExampleWithString("first"), ExampleWithString("second")], nextSliceId="abc"),
        id="generic slice with list of objects",
    ),
    pytest.param(
        '{"items": [{"field": "first"}]}',
        ExampleSlice[ExampleWithString],
        ExampleSlice(items=[ExampleWithString("first")], nextSliceId=None),
        id="generic slice without optional field",
    ),
    pytest.param(
        '{"items": null}',
        ExampleSlice[ExampleWithString],
        ExampleSlice(items=None, nextSliceId=None),
        id="generic slice with null list",
    )
]

serialization_operations = [
    pytest.param('{}', ExampleWithOptional, ExampleWithOptional(None), id="null field ignored"),
    pytest.param('{}', ExampleWithClassVar, ExampleWithClassVar(), id="class var field ignored")
]


@pytest.mark.parametrize("serialized,deserialized_type,deserialized", symmetric_operations + deserialization_operations)
def test_deserialization(serialized: str, deserialized_type: Type[T], deserialized: object):
    actual = Json.loads(serialized, deserialized_type)
    assert actual == deserialized


@pytest.mark.parametrize("serialized,deserialized_type,deserialized", symmetric_operations + serialization_operations)
def test_serialization(serialized: str, deserialized_type: Type[T], deserialized: object):
    actual = Json.dumps(deserialized)
    assert json.loads(actual) == json.loads(serialized)


def test_invalid_request_exception_serde():
    exc = InvalidRequestException("bad request", ("detail one", "detail two"))
    serialized = Json.dumps(exc)
    assert json.loads(serialized) == {
        "errorType": "InvalidRequestException",
        "message": "bad request",
        "detail": ["detail one", "detail two"],
    }
    deserialized = Json.loads(serialized, BaseCustomException)
    assert isinstance(deserialized, InvalidRequestException)
    assert deserialized.message == "bad request"
    assert deserialized.detail == ("detail one", "detail two")
