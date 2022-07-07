import pytest  # type: ignore

import reporter
from reporter import Reporter

from . import helpers


def create_random_client(rc: Reporter) -> reporter.Client:
    name = helpers.rand_alphanum(32)
    description = helpers.rand_alphanum(32)
    client = rc.clients.create(
        {
            "name": name,
            "description": description,
        }
    )
    assert isinstance(client, reporter.Client)
    return client


def test_client_create(rc: Reporter):
    n = len(rc.clients.list())
    client = create_random_client(rc)
    assert client.id is not None
    assert len(rc.clients.list()) == n + 1


def test_client_delete(rc: Reporter):
    client = create_random_client(rc)
    rc.clients.delete(client.id)
    with pytest.raises(reporter.ReporterHttpError) as e:
        rc.clients.get(client.id)
        assert e.value.response_code == 404


def test_client_list(rc: Reporter):
    client = create_random_client(rc)
    clients = rc.clients.list()
    for c in clients:
        if c.id == client.id:
            return
    raise Exception("Client not found in list")


def test_client_get(rc: Reporter):
    client = create_random_client(rc)
    c = rc.clients.get(client.id)
    assert client.id == c.id


def test_client_update(rc: Reporter):
    client = create_random_client(rc)
    new_name = helpers.rand_alphanum(32)
    updated = rc.clients.update(client.id, {"name": new_name})
    gotten = rc.clients.get(client.id)
    assert client == updated
    assert gotten == updated


def test_client_create_invalid(rc: Reporter):
    with pytest.raises(reporter.ReporterHttpError):
        rc.clients.create({"asdf": "asdf"})


def test_client_get_invalid(rc: Reporter):
    with pytest.raises(reporter.ReporterHttpError):
        rc.clients.get("does-not-exist")


def test_client_updated_invalid(rc: Reporter):
    client = create_random_client(rc)
    with pytest.raises(reporter.ReporterHttpError):
        rc.clients.update(client.id, {"name": None})
