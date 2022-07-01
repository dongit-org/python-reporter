import pytest

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


def test_client_create_invalid(rc: Reporter):
    with pytest.raises(reporter.ReporterHttpError):
        rc.clients.create({"asdf": "asdf"})


def test_client_get_invalid(rc: Reporter):
    with pytest.raises(reporter.ReporterHttpError):
        rc.clients.get("does-not-exist")
