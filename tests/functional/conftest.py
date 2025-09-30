from pathlib import Path
import os
import time
import docker
import pytest
from docker.models.containers import Container
from pytest_docker.plugin import Services
import requests
from urllib3.exceptions import ProtocolError
from reporter import Reporter
from .utils import Artisan


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
def phpfpm(docker_services: Services, reporter_host: str) -> Container:
    """Starts Reporter and returns a Reporter client instance."""
    time.sleep(1)
    url = f"http://{reporter_host}"
    docker_services.wait_until_responsive(
        timeout=600.0,
        pause=1,
        check=lambda: is_up(url),
    )

    docker_client = docker.from_env()
    return docker_client.containers.get("phpfpm")


@pytest.fixture(scope="session")
def artisan(phpfpm: Container) -> Artisan:
    return Artisan(phpfpm)


@pytest.fixture(scope="session")
def rc(phpfpm: Container, reporter_host: str) -> Reporter:
    url = f"http://{reporter_host}"
    sock = phpfpm.exec_run(
        "php artisan user:create --api-token a@a.com a a",
        stdin=True,
        socket=True,
        tty=True,
    ).output
    sock.sendall(b"Password1!\nPassword1!\n")
    output = b""
    start_time = time.time()
    while b"api token is: " not in output:
        if time.time() > start_time + 10:
            raise TimeoutError("API token not found in output within timeout")
        output += sock.recv(100)
        time.sleep(0.1)
    token = output.decode("utf-8").split("api token is: ")[1].splitlines()[0]

    client = Reporter(
        url=url,
        api_token=token,
        ssl_verify=False,
    )

    return client
