import responses
from urllib.parse import quote

from reporter import (
    Reporter,
    RestList,
    RestManager,
    RestObject,
)
from reporter.mixins import (
    CreateMixin,
    DeleteMixin,
    GetMixin,
    GetRawMixin,
    ListMixin,
    SearchMixin,
    UpdateMixin,
)


class FakeObject(RestObject):
    pass


class FakeManager(RestManager):
    _path = "tests"
    _obj_cls = FakeObject


def test_create_mixin(rc: Reporter) -> None:
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


def test_delete_mixin(rc: Reporter) -> None:
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


def test_get_mixin(rc: Reporter) -> None:
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


def test_get_raw_mixin(rc: Reporter) -> None:
    class M(FakeManager, GetRawMixin):  # type: ignore
        pass

    manager = M(rc)
    url = "https://localhost/api/v1/tests/1234"

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url=url,
            body=b"12345",
            content_type="application/octet-stream",
            status=200,
            match=[
                responses.matchers.header_matcher({"Accept": "*/*"}),
                responses.matchers.query_param_matcher({}),
            ],
        )
        obj = manager.get("1234")

        rsps.assert_call_count(url, 1)
        assert isinstance(obj, bytes)
        assert obj == b"12345"


def test_list_mixin(rc: Reporter) -> None:
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
        assert isinstance(objs, RestList)
        assert len(objs) == 2
        for obj in objs:
            assert isinstance(obj, FakeObject)
        assert objs[0].id == "1234"
        assert objs[1].a == 13
        assert objs.links["foo"] == "bar"
        assert objs.meta["foo"] == "bar"


def test_search_mixin(rc: Reporter) -> None:
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
        assert isinstance(objs, RestList)
        assert len(objs) == 2
        for obj in objs:
            assert isinstance(obj, FakeObject)
        assert objs[0].id == "1234"
        assert objs[1].a == 13
        assert objs.links["foo"] == "bar"
        assert objs.meta["foo"] == "bar"


def test_update_mixin(rc: Reporter) -> None:
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


def test_mixin_filter_include_sort(rc: Reporter) -> None:
    class M(FakeManager, ListMixin):  # type: ignore
        pass

    manager = M(rc)
    url = "https://localhost/api/v1/tests"

    with responses.RequestsMock() as rsps:
        rsps.add(
            method=responses.GET,
            url=url,
            json={
                "data": [
                    {"id": "1234", "a": 12, "foo": {}, "bar": {}},
                    {"id": "1234", "a": 12, "foo": {}, "bar": {}},
                ],
                "links": {
                    "foo": "bar",
                },
                "meta": {
                    "foo": "bar",
                },
            },
            content_type="application/json",
            status=200,
            match=[
                responses.matchers.header_matcher({"Accept": "application/json"}),
            ],
        )

        # Test that sort can be passed as either an array or a comma-separated string
        query_string = quote("sort[]=foo&sort[]=bar", safe="&=")
        manager.list(sort=["foo", "bar"])
        rsps.assert_call_count(f"{url}?{query_string}", 1)

        query_string = quote("sort=foo,bar", safe="&=")
        manager.list(sort="foo,bar")
        rsps.assert_call_count(f"{url}?{query_string}", 1)

        # Test that include can be passed as either an array or a comma-separated string
        query_string = quote("include[]=foo&include[]=bar", safe="&=")
        manager.list(include=["foo", "bar"])
        rsps.assert_call_count(f"{url}?{query_string}", 1)

        query_string = quote("include=foo,bar", safe="&=")
        manager.list(include="foo,bar")
        rsps.assert_call_count(f"{url}?{query_string}", 1)

        # Test that filters can be passed as either arrays or comma-separated strings
        query_string = quote(
            "filter[foo][]=a&filter[foo][]=b&filter[bar]=c,d", safe="&="
        )
        manager.list(filter={"foo": ["a", "b"], "bar": "c,d"})
        rsps.assert_call_count(f"{url}?{query_string}", 1)
