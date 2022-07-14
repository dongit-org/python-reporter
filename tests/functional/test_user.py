import pytest  # type: ignore

import reporter
from reporter import Reporter


def test_user_operations(rc: Reporter):
    user_data = {
        "first_name": "First",
        "last_name": "Last",
        "email": "test_user_operations@example.com",
    }
    user = rc.users.create(user_data)

    assert user in rc.users.list(filter={"id": user.id})

    rc.users.update(user.id, {"phone": "foo"})
    gotten = rc.users.get(user.id)

    assert user == gotten
    for attr in user_data:
        assert getattr(user, attr) == getattr(gotten, attr)
    assert gotten.phone == "foo"


def test_client_operations(rc: Reporter):
    client = rc.clients.create(
        {
            "name": "test_client_operations",
            "description": "foo",
        }
    )

    assert client in rc.clients.list(filter={"id": client.id})

    rc.clients.update(client.id, {"website": "https://example.com"})
    gotten = rc.clients.get(client.id)

    assert client == gotten
    for attr in ["name", "description"]:
        assert getattr(client, attr) == getattr(gotten, attr)
    assert gotten.website == "example.com"

    rc.clients.delete(client.id)
    with pytest.raises(reporter.ReporterHttpError) as e:
        rc.clients.get(client.id)
        assert e.value.response_code == 404
