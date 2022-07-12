import responses

from reporter import (
    Reporter,
    RESTList,
    RESTManager,
    RESTObject,
    CreateMixin,
    DeleteMixin,
    GetMixin,
    ListMixin,
    SearchMixin,
    UpdateMixin,
)


class FakeObject(RESTObject):
    pass


class FakeManager(RESTManager):
    _path = "tests"
    _obj_cls = FakeObject


def test_create_mixin(rc: Reporter):
    class M(FakeManager, CreateMixin):  # type: ignore
        pass

    manager = M(rc)
    url = "https://localhost/api/v1/tests"

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.POST,
            url=url,
            json={"id": "1234", "a": 12},
            content_type="application/json",
            status=200,
            match=[
                responses.matchers.header_matcher({"Accept": "application/json"}),
                responses.matchers.query_param_matcher({}),
                responses.matchers.json_params_matcher({"a": 12}),
            ],
        )
        obj = manager.create({"a": 12})

        rsps.assert_call_count(url, 1)
        assert isinstance(obj, FakeObject)
        assert obj.id == "1234"
        assert obj.a == 12


def test_delete_mixin(rc: Reporter):
    class M(FakeManager, DeleteMixin):  # type: ignore
        pass

    manager = M(rc)
    url = "https://localhost/api/v1/tests/1234"

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.DELETE,
            url=url,
            json={"success": True},
            content_type="application/json",
            status=200,
            match=[
                responses.matchers.header_matcher({"Accept": "application/json"}),
                responses.matchers.query_param_matcher({}),
            ],
        )
        manager.delete("1234")

        rsps.assert_call_count(url, 1)


def test_get_mixin(rc: Reporter):
    class M(FakeManager, GetMixin):  # type: ignore
        pass

    manager = M(rc)
    url = "https://localhost/api/v1/tests/1234"

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url=url,
            json={"id": "1234", "a": 12},
            content_type="application/json",
            status=200,
            match=[
                responses.matchers.header_matcher({"Accept": "application/json"}),
                responses.matchers.query_param_matcher({}),
            ],
        )
        obj = manager.get("1234")

        rsps.assert_call_count(url, 1)
        assert isinstance(obj, FakeObject)
        assert obj.id == "1234"
        assert obj.a == 12


def test_list_mixin(rc: Reporter):
    class M(FakeManager, ListMixin):  # type: ignore
        pass

    manager = M(rc)
    url = "https://localhost/api/v1/tests"
    json = {
        "data": [
            {"id": "1234", "a": 12},
            {"id": "1235", "a": 13},
        ],
        "links": {
            "foo": "bar",
        },
        "meta": {
            "foo": "bar",
        },
    }

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url=url,
            json=json,
            status=200,
            match=[
                responses.matchers.header_matcher({"Accept": "application/json"}),
                responses.matchers.query_param_matcher({}),
            ],
        )
        objs = manager.list()

        rsps.assert_call_count(url, 1)
        assert isinstance(objs, RESTList)
        assert len(objs) == 2
        for obj in objs:
            assert isinstance(obj, FakeObject)
        assert objs[0].id == "1234"
        assert objs[1].a == 13
        assert objs.links["foo"] == "bar"
        assert objs.meta["foo"] == "bar"


def test_search_mixin(rc: Reporter):
    class M(FakeManager, SearchMixin):  # type: ignore
        pass

    manager = M(rc)
    url = "https://localhost/api/v1/tests/search"
    json = {
        "data": [
            {"id": "1234", "a": 12},
            {"id": "1235", "a": 13},
        ],
        "links": {
            "foo": "bar",
        },
        "meta": {
            "foo": "bar",
        },
    }

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url=url,
            json=json,
            status=200,
            match=[
                responses.matchers.header_matcher({"Accept": "application/json"}),
                responses.matchers.query_param_matcher({"term": "asdf"}),
            ],
        )
        objs = manager.search(term="asdf")

        rsps.assert_call_count(f"{url}?term=asdf", 1)
        assert isinstance(objs, RESTList)
        assert len(objs) == 2
        for obj in objs:
            assert isinstance(obj, FakeObject)
        assert objs[0].id == "1234"
        assert objs[1].a == 13
        assert objs.links["foo"] == "bar"
        assert objs.meta["foo"] == "bar"


def test_update_mixin(rc: Reporter):
    class M(FakeManager, UpdateMixin):  # type: ignore
        pass

    manager = M(rc)
    url = "https://localhost/api/v1/tests/1234"

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.PATCH,
            url=url,
            json={"id": "1234", "a": 12},
            status=200,
            match=[
                responses.matchers.header_matcher({"Accept": "application/json"}),
                responses.matchers.query_param_matcher({}),
                responses.matchers.json_params_matcher({"a": 12}),
            ],
        )
        obj = manager.update("1234", {"a": 12})

        rsps.assert_call_count(url, 1)
        assert isinstance(obj, FakeObject)
        assert obj.id == "1234"
        assert obj.a == 12
