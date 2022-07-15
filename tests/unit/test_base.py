import responses

from reporter import (
    Reporter,
    RESTManager,
    RESTObject,
    GetMixin,
)


class FakeChildObject(RESTObject):
    pass


class FakeChildManager(RESTManager, GetMixin):
    _path = "tests/{obj_id}/child_objs"
    _parent_attrs = {"obj_id": "id"}
    _obj_cls = FakeChildObject


class FakeObject(RESTObject):
    _children = {
        "child_objs": FakeChildManager,
        "sameattributes": FakeChildManager,
    }
    _includes = {
        "childObj": FakeChildObject,
        "childObjs": FakeChildObject,
        "sameattributes": FakeChildObject,
    }


class FakeManager(RESTManager):
    _path = "tests"
    _obj_cls = FakeObject


def test_object_children(rc: Reporter):
    obj = FakeObject(rc, {"id": "1234"})

    assert isinstance(obj.child_objs, FakeChildManager)
    assert obj.child_objs.reporter == rc
    assert obj.child_objs._path == "tests/1234/child_objs"


def test_object_includes(rc: Reporter):
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

    assert isinstance(obj.childObj, FakeChildObject)
    assert len(obj.childObjs) == 2
    for o in obj.childObjs:
        assert isinstance(o, FakeChildObject)


def test_object_include_same_attribute_as_manager(rc: Reporter):
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