import pytest

import reporter
from reporter import Reporter


def test_user_operations(rc: Reporter) -> None:
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

    me = rc.users.me(include=["roles"])
    assert len(me.roles) == 1
    assert me.roles[0].name == "admin"
    assert me.email == "a@a.com"


def test_client_operations(rc: Reporter) -> None:
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


def test_team_operations(rc: Reporter) -> None:
    client = rc.clients.create(
        {
            "name": "test_team_operations",
            "description": "foo",
        }
    )
    user1 = rc.users.create(
        {
            "first_name": "First",
            "last_name": "Last",
            "email": "test_team_operations_1@example.com",
            "clients": [client.id],
        }
    )
    user2 = rc.users.create(
        {
            "first_name": "First",
            "last_name": "Last",
            "email": "test_team_operations_2@example.com",
            "clients": [client.id],
        }
    )

    team = client.teams.create(
        {
            "name": "test_team_operations",
            "color": "#000000",
            "type": 0,
            "assessment_access_scope": 1,
        }
    )

    client_with_teams = rc.clients.get(client.id, include="teams")
    assert team in client_with_teams.teams

    rc.teams.update(team.id, {"color": "#111111"})
    client_with_teams = rc.clients.get(client.id, include="teams")
    updated = next(t for t in client_with_teams.teams if t.id == team.id)
    assert updated.color == "#111111"
    assert updated.name == team.name

    tu1 = team.users.create({"user_id": user1.id, "type": 0})
    assert tu1.user_id == user1.id
    assert tu1.team_id == team.id
    assert tu1.type == 0
    assert tu1.read_only is False

    tu2 = team.users.create({"user_id": user2.id, "type": 3})
    assert tu2.user_id == user2.id
    assert tu2.type == 3

    updated_tu2 = team.users.update(user2.id, {"type": 0, "read_only": True})
    assert updated_tu2.type == 0
    assert updated_tu2.read_only is True

    client_with_team_users = rc.clients.get(client.id, include="teams.users")
    team_with_users = next(t for t in client_with_team_users.teams if t.id == team.id)
    assert {u.id for u in team_with_users.users} == {user1.id, user2.id}

    team.users.delete(user1.id)

    rc.teams.delete(team.id)
    client_with_teams = rc.clients.get(client.id, include="teams")
    assert team not in client_with_teams.teams
