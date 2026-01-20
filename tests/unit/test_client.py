import json
import os
import timeit
from typing import cast, Dict, Pattern
from unittest.mock import patch

import pytest
import requests
import responses

from reporter import Reporter, ReporterHttpError
from reporter.base import RestManager, RestObject
from reporter.mixins import ListMixin
from reporter.types import FileSpec


@responses.activate
def test_url_trailing_slash() -> None:
    # Test that trailing slash is stripped
    rc = Reporter(url="https://localhost/", api_token="secret")
    url = "https://localhost/api/v1/tests"

    responses.add(
        method=responses.GET,
        url=url,
        status=200,
    )

    rc.http_request(verb="get", path="tests")


@responses.activate
def test_http_request_headers(rc: Reporter) -> None:
    url = "https://localhost/api/v1/tests"

    responses.add(
        method=responses.GET,
        url=url,
        status=200,
        match=[
            responses.matchers.header_matcher(
                {
                    "Authorization": "Bearer secret",
                    "Accept": "application/json",
                }
            ),
        ],
    )
    responses.add(
        method=responses.POST,
        url=url,
        status=200,
        match=[
            responses.matchers.header_matcher(
                {
                    "Authorization": "Bearer secret",
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                }
            ),
        ],
    )

    rc.http_request(verb="get", path="tests")
    rc.http_request(verb="post", path="tests", post_data={})
    responses.assert_call_count(url, 2)


@responses.activate
def test_http_request_extra_headers(rc: Reporter) -> None:
    url = "https://localhost/api/v1/tests"
    headers = {
        "Authorization": "Bearer test",
        "Content-Type": "foo/bar",
        "Accept": "bar/foo",
        "Extra": "Header",
    }

    responses.add(
        method=responses.POST,
        url=url,
        status=200,
        match=[
            # use cast because responses library uses incorrect type for header_matcher
            responses.matchers.header_matcher(
                cast(Dict[str, str | Pattern[str]], headers)
            ),
        ],
    )

    rc.http_request(
        verb="post",
        path="tests",
        headers=headers,
    )
    rc.http_request(
        verb="post",
        path="tests",
        headers=headers,
        files={"file": "contents"},
    )
    responses.assert_call_count(url, 2)


@responses.activate
def test_http_request_query_string_parameters(rc: Reporter) -> None:
    url = "https://localhost/api/v1/tests"
    params = {
        "foo": "bar",
        "id": 1234,
    }

    responses.add(
        method=responses.GET,
        url=url,
        status=200,
        match=[responses.matchers.query_param_matcher(params)],
    )

    rc.http_request(
        verb="get",
        path="tests",
        query_data=params,
    )
    responses.assert_call_count(f"{url}?foo=bar&id=1234", 1)


@responses.activate
def test_http_request_file_upload(rc: Reporter) -> None:
    url = "https://localhost/api/v1/tests"
    post_data = {"foo": "bar", "id": "1234"}
    file_path = f"{os.path.dirname(os.path.abspath(__file__))}/test_client.py"

    files: dict[str, FileSpec] = {
        "file1": open(file_path, "rb"),
        "file2": "contents2",
        "file3": ("test.json", '{"key": "value"}'),
        "file4": ("test.json", '{"key": "value"}', "application/json"),
        "file5": (
            "test.json",
            '{"key": "value"}',
            "application/json",
            {"X-Header": "value"},
        ),
        "file6": (
            "test.json",
            open(file_path, "rb"),
            "application/json",
            {"X-Header": "value"},
        ),
    }

    responses.add(
        method=responses.POST,
        url=url,
        status=200,
        match=[
            responses.matchers.multipart_matcher(files, post_data),
        ],
    )

    # The file objects in files are read by multipart_matcher.
    # They need to be reopened before passing them to http_request
    files["file1"] = cast(FileSpec, open(file_path, "rb"))
    files["file6"] = (
        "test.json",
        open(file_path, "rb"),
        "application/json",
        {"X-Header": "value"},
    )

    rc.http_request(
        verb="post",
        path="tests",
        post_data=post_data,
        files=files,
    )
    responses.assert_call_count(url, 1)


@responses.activate
def test_http_exception(rc: Reporter) -> None:
    url = "https://localhost/api/v1/tests"
    body = {
        "message": "error",
        "foo": "bar",
    }

    responses.add(
        method=responses.GET,
        url=url,
        json=body,
        status=400,
    )

    with pytest.raises(ReporterHttpError) as e:
        rc.http_request(verb="get", path="tests")

    responses.assert_call_count(url, 1)
    assert e.value.response_code == 400
    assert isinstance(e.value.error_message, str)
    assert json.loads(e.value.error_message) == body
    assert isinstance(e.value.response_body, str | bytes)
    assert json.loads(e.value.response_body) == body


@responses.activate
def test_rate_limit(rc: Reporter) -> None:
    class FakeObject(RestObject):
        pass

    class FakeManager(RestManager, ListMixin):
        _path = "tests"
        _obj_cls = FakeObject

    url = "https://localhost/api/v1/tests"

    for _ in range(4):
        responses.add(
            method=responses.GET,
            url=url,
            status=429,
            headers={"retry-after": "1"},
        )
    responses.add(
        method=responses.GET,
        url=url,
        status=200,
        json={"data": {}, "links": {}, "meta": {}},
    )

    mgr = FakeManager(rc)

    start = timeit.default_timer()
    with pytest.raises(ReporterHttpError) as e:
        mgr.list()
    end = timeit.default_timer()
    assert 1 < end - start < 2
    assert e.value.response_code == 429

    start = timeit.default_timer()
    with pytest.raises(ReporterHttpError) as e:
        mgr.list(obey_rate_limit=False)
    end = timeit.default_timer()
    assert end - start < 1
    assert e.value.response_code == 429

    start = timeit.default_timer()
    mgr.list()
    end = timeit.default_timer()
    assert 1 < end - start < 2

    responses.assert_call_count(url, 5)


@pytest.mark.parametrize("ssl_verify", [None, True, False, "/path/to/cert"])
@responses.activate
def test_ssl_verify_argument(ssl_verify: bool | str) -> None:
    kwargs = {}
    if ssl_verify is not None:
        kwargs["ssl_verify"] = ssl_verify

    rc = Reporter(
        url="https://localhost/",
        api_token="secret",
        **kwargs,
    )

    responses.add(
        responses.GET,
        "https://localhost/api/v1/tests",
        status=200,
    )

    with patch.object(
        requests.Session,
        "request",
        autospec=True,
        wraps=requests.Session.request,
    ) as spy:
        rc.http_request(verb="get", path="tests")

        spy.assert_called_once()
        _, kwargs = spy.call_args

        assert "verify" in kwargs
        assert kwargs["verify"] == ssl_verify if ssl_verify is not None else True
