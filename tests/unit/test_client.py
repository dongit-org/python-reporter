import pytest  # type: ignore
import responses

from reporter import Reporter, ReporterHttpError


@responses.activate
def test_http_request_headers(rc: Reporter):
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
def test_http_request_extra_headers(rc: Reporter):
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
            responses.matchers.header_matcher(headers),
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
def test_http_request_query_string_parameters(rc: Reporter):
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
def test_http_request_file_upload(rc: Reporter):
    url = "https://localhost/api/v1/tests"
    post_data = {"foo": "bar", "id": "1234"}
    files = {"file1": "contents1", "file2": "contents2"}

    responses.add(
        method=responses.POST,
        url=url,
        status=200,
        match=[
            responses.matchers.multipart_matcher(files, post_data),
        ],
    )

    rc.http_request(
        verb="post",
        path="tests",
        post_data=post_data,
        files=files,
    )
    responses.assert_call_count(url, 1)


@responses.activate
def test_http_exception(rc: Reporter):
    url = "https://localhost/api/v1/tests"
    json = {
        "message": "error",
        "foo": "bar",
    }

    responses.add(
        method=responses.GET,
        url=url,
        json=json,
        status=400,
    )

    with pytest.raises(ReporterHttpError) as e:
        rc.http_request(verb="get", path="tests")

        responses.assert_call_count(url, 1)
        assert e.value.response_code == 400
        assert e.value.error_message == json
        assert e.value.response_body == json
