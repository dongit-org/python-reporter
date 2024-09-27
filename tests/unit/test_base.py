import responses

from reporter import (
    Reporter,
    RestManager,
    RestObject,
)
from reporter.helpers import Polymorphic
from reporter.mixins import GetMixin


class FakeChildObject(RestObject):
    pass


class FakeChildObject2(RestObject):
    pass


class FakeChildManager(RestManager, GetMixin):
    _path = "tests/{obj_id}/child_objs"
    _parent_attrs = {"obj_id": "id"}
    _obj_cls = FakeChildObject


class FakeObject(RestObject):
    child_objs: FakeChildManager
    sameattributes: FakeChildManager


FakeObject._includes = {
    "childObj": FakeChildObject,
    "childObjs": FakeChildObject,
    "items": FakeObject,
    "sameattributes": FakeChildObject,
    "polymorphic_children": Polymorphic(
        [FakeChildObject, FakeChildObject2], "child_type"
    ),
}


class FakeManager(RestManager):
    _path = "tests"
    _obj_cls = FakeObject


def test_object_children(rc: Reporter) -> None:
    obj = FakeObject(rc, {"id": "1234"})

    assert isinstance(obj.child_objs, FakeChildManager)
    assert obj.child_objs.reporter == rc
    assert obj.child_objs._path == "tests/1234/child_objs"


def test_object_includes(rc: Reporter) -> None:
    obj = FakeObject(
        rc,
        {
            "id": "1234",
            "childObj": {"id": "1"},
            "items": [
                {
                    "id": "1",
                    "childObj": {"id": "1"},
                },
                {
                    "id": "2",
                    "childObj": {"id": "2"},
                },
            ],
            "polymorphic_children": [
                {"id": "1", "child_type": "FakeChildObject"},
                {"id": "2", "child_type": "FakeChildObject2"},
            ],
        },
    )

    assert isinstance(obj.childObj, FakeChildObject)
    assert len(obj.items) == 2
    for o in obj.items:
        assert isinstance(o, FakeObject)
        assert isinstance(o.childObj, FakeChildObject)
    assert len(obj.polymorphic_children) == 2
    assert isinstance(obj.polymorphic_children[0], FakeChildObject)
    assert isinstance(obj.polymorphic_children[1], FakeChildObject2)


def test_object_include_same_attribute_as_manager(rc: Reporter) -> None:
    obj = FakeObject(
        rc,
        {
            "id": "1234",
            "sameattributes": [
                {"id": "1"},
                {"id": "2"},
            ],
        },
    )

    assert isinstance(obj.sameattributes, FakeChildManager)
    for o in obj.sameattributes:
        assert isinstance(o, FakeChildObject)
    assert obj.sameattributes[0].id == "1"
    assert obj.sameattributes[1].id == "2"

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url="https://localhost/api/v1/tests/1234/child_objs/5",
            json={"id": "5", "a": 12},
            content_type="application/json",
            status=200,
        )

        child = obj.sameattributes.get("5")
        assert isinstance(child, FakeChildObject)
        assert child.id == "5"
        assert child.a == 12


def test_object_dict(rc: Reporter) -> None:
    obj = FakeObject(
        rc,
        {
            "id": "1234",
            "childObj": {"id": "1"},
            "childObjs": [
                {"id": "1"},
                {"id": "2"},
            ],
        },
    )

    assert dict(obj) == {
        "id": "1234",
        "childObj": {"id": "1"},
        "childObjs": [
            {"id": "1"},
            {"id": "2"},
        ],
    }
