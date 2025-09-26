from pathlib import Path
import os
import time
from textwrap import dedent
from typing import Protocol, Optional
import docker
import pytest
from docker.models.containers import Container
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


class Artisan(Protocol):
    def __call__(
        self,
        command: Optional[str | list[str]] = None,
        *,
        execute: Optional[str] = None,
    ) -> str:
        ...


@pytest.fixture(scope="session")
def artisan(phpfpm: Container) -> Artisan:
    def _run(
        command: Optional[str | list[str]] = None, execute: Optional[str | None] = None
    ) -> str:
        if execute is not None:
            execute = dedent(execute).strip()
            command = ["tinker", "--execute=" + execute]

        if command is None:
            raise ValueError(
                "Either an Artisan command or an execute command must be specified."
            )

        if isinstance(command, str):
            full_command: str | list[str] = "php artisan " + command
        else:
            full_command = ["php", "artisan"] + command

        output: bytes = phpfpm.exec_run(full_command).output
        return output.decode("utf-8")

    return _run


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
