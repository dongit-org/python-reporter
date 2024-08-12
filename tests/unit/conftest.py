import pytest

from reporter import Reporter


@pytest.fixture
def rc() -> Reporter:
    return Reporter(
        url="https://localhost",
        api_token="secret",
    )
