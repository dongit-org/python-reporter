import pytest  # type: ignore

import reporter
from reporter import Reporter

from . import helpers


def create_random_user(rc: Reporter) -> reporter.User:
    first_name = helpers.rand_alphanum(32)
    last_name = helpers.rand_alphanum(32)
    email = f"{helpers.rand_alphanum(32)}@example.com"
    user = rc.users.create(
        {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
        }
    )
    assert isinstance(user, reporter.User)
    return user


def test_user_create(rc: Reporter):
    user = create_random_user(rc)
    assert user.id is not None
    rc.users.get(user.id)


def test_user_list(rc: Reporter):
    user = create_random_user(rc)
    users = rc.users.list()
    for u in users:
        if u == user:
            return
    raise Exception("User not found in list")


def test_user_get(rc: Reporter):
    user = create_random_user(rc)
    u = rc.users.get(user.id)
    assert user == u


def test_user_create_invalid(rc: Reporter):
    with pytest.raises(reporter.ReporterHttpError):
        rc.users.create({"asdf": "asdf"})


def test_finding_get_invalid(rc: Reporter):
    with pytest.raises(reporter.ReporterHttpError):
        rc.users.get("does-not-exist")
