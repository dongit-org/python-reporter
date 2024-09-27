from pathlib import Path
import os
import platform
import time

import docker  # type: ignore
import pytest
from pytest_docker.plugin import Services
import requests
from urllib3.exceptions import ProtocolError

from reporter import Reporter


@pytest.fixture(scope="session")
def base_path() -> Path:
    return Path(__file__).parent


@pytest.fixture(scope="session")
def docker_compose_file(base_path: Path) -> Path:
    return base_path / "docker-compose/docker-compose.yml"


@pytest.fixture(scope="session")
def reporter_host() -> str:
    if "REPORTER_HOST" in os.environ:
        return os.environ["REPORTER_HOST"]
    else:
        return "localhost:8080"


def is_up(url: str) -> bool:
    try:
        response = requests.get(f"{url}/login")
        return response.status_code == 200
    except (ConnectionError, ConnectionRefusedError, ProtocolError):
        return False


@pytest.fixture(scope="session")
def rc(docker_services: Services, reporter_host: str) -> Reporter:
    """Starts Reporter and returns a Reporter client instance."""
    time.sleep(1)
    url = f"http://{reporter_host}"
    docker_services.wait_until_responsive(
        timeout=600.0,
        pause=1,
        check=lambda: is_up(url),
    )

    docker_client = docker.from_env()
    phpfpm = docker_client.containers.get("phpfpm")
    sock = phpfpm.exec_run(
        "php artisan user:create --api-token a@a.com a a",
        stdin=True,
        socket=True,
    ).output
    if platform.system() == "Linux":
        sock._sock.sendall(b"Password1!\nPassword1!\n")
        token = sock.readlines()[-1].split()[-1].decode("utf-8")
    elif platform.system() == "Windows":
        sock.sendall(b"Password1!\nPassword1!\n")
        # ensure that reporter has time to process
        # the password before trying to retrieve output
        time.sleep(3)
        token = sock.recv(500)[8:].decode("utf-8").split("\n")[-2].split()[-1]
    else:
        raise Exception(f"Unsupported platform {platform.system()}")

    client = Reporter(
        url=url,
        api_token=token,
        ssl_verify=False,
    )

    return client
