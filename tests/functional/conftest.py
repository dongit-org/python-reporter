import pathlib

import docker  # type: ignore
import pytest  # type: ignore
import requests

from reporter import Reporter


@pytest.fixture(scope="session")
def base_path() -> pathlib.Path:
    return pathlib.Path(__file__).parent


@pytest.fixture(scope="session")
def docker_compose_file(base_path):
    return base_path / "docker-compose/docker-compose.yml"


def is_up(url):
    try:
        response = requests.get(f"{url}/login")
        if response.status_code == 200:
            return True
    except ConnectionError:
        return False


@pytest.fixture(scope="session")
def rc(docker_services) -> Reporter:
    """Starts Reporter and returns a Reporter client instance."""
    url = "http://localhost:8080"
    docker_services.wait_until_responsive(
        timeout=300.0,
        pause=1,
        check=lambda: is_up(url),
    )

    docker_client = docker.from_env()
    phpfpm = docker_client.containers.get("phpfpm")
    sock = phpfpm.exec_run(  # type: ignore
        "php artisan user:create --api-token a@a.com a a",
        stdin=True,
        socket=True,
    ).output
    sock._sock.sendall(b"Password1!\nPassword1!\n")
    token = sock.readlines()[-1].split()[-1].decode("utf-8")

    client = Reporter(
        url=url,
        api_token=token,
        ssl_verify=False,
    )

    return client
