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

    assert user in rc.users.list(filter_={"id": user.id})

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

    assert client in rc.clients.list(filter_={"id": client.id})

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


def test_user_group_operations(rc: Reporter):
    client = rc.clients.create(
        {
            "name": "test_user_group_operations",
            "description": "foo",
        }
    )
    user1 = rc.users.create(
        {
            "first_name": "First",
            "last_name": "Last",
            "email": "test_user_group_operations_1@example.com",
            "clients": [client.id],
        }
    )
    user2 = rc.users.create(
        {
            "first_name": "First",
            "last_name": "Last",
            "email": "test_user_group_operations_2@example.com",
            "clients": [client.id],
        }
    )

    group = client.user_groups.create(
        {
            "name": "test_user_group_operations",
            "color": "#000000",
            "users": [user1.id, user2.id],
        }
    )

    assert group in rc.user_groups.list(filter_={"id": group.id})

    rc.user_groups.update(group.id, {"color": "#111111"})
    gotten = rc.user_groups.get(group.id)

    assert group == gotten
    assert group.name == gotten.name
    assert gotten.color == "#111111"

    rc.user_groups.delete(group.id)
    with pytest.raises(reporter.ReporterHttpError) as e:
        rc.user_groups.get(group.id)
        assert e.value.response_code == 404
