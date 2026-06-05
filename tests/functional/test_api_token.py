import pytest

import reporter
from reporter import Reporter


def test_api_token_operations(rc: Reporter) -> None:
    created = rc.api_tokens.create(
        {
            "name": "test_api_token_operations",
            "abilities": ["assessment:read"],
        }
    )

    # The plaintext token is included once in the create response.
    assert isinstance(created.token, str)
    assert created.token

    gotten = rc.api_tokens.get(created.id)
    assert gotten.id == created.id
    assert gotten.name == "test_api_token_operations"

    assert created in rc.api_tokens.list(filter={"id": created.id})

    me = rc.api_tokens.me(include=["creator"])
    assert me.id is not None
    assert isinstance(me.creator, reporter.User)

    rc.api_tokens.delete(created.id)
    with pytest.raises(reporter.ReporterHttpError) as e:
        rc.api_tokens.delete(created.id)
        assert e.value.response_code == 404
