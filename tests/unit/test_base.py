from reporter import (
    Reporter,
    RESTManager,
    RESTObject,
)


class FakeChildObject(RESTObject):
    pass


class FakeChildManager(RESTManager):
    _path = "tests/{obj_id}/child_objs"
    _parent_attrs = {"obj_id": "id"}
    _obj_cls = FakeChildObject


class FakeObject(RESTObject):
    _children = {
        "child_objs": FakeChildManager,
    }
    _includes = {
        "childObj": FakeChildObject,
        "childObjs": FakeChildObject,
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
