from textwrap import dedent
from typing import Optional, TypeVar, Callable

from docker.models.containers import Container
import time


T = TypeVar("T")


class Artisan:
    """Helper class for running Laravel Artisan commands in the phpfpm container."""

    def __init__(self, container: Container):
        self.container = container

    def command(self, command: str | list[str]) -> str:
        """
        Run an artisan command.

        Args:
            command: The artisan command to run. Can be a string like "migrate"
                     or a list like ["migrate", "--force"].

        Returns:
            The output of the command as a string.

        Example:
            artisan.command("migrate")
            artisan.command(["migrate", "--force"])
        """
        if isinstance(command, str):
            full_command: str | list[str] = "php artisan " + command
        else:
            full_command = ["php", "artisan"] + command

        result = self.container.exec_run(full_command)
        output: bytes = result.output
        if result.exit_code != 0:
            raise Exception(
                f"Artisan command failed: {full_command}\n{output.decode('utf-8')}"
            )
        return output.decode("utf-8")

    def execute(self, php_code: str) -> str:
        """
        Execute PHP code using artisan tinker.

        Args:
            php_code: The PHP code to execute. Will be automatically dedented and stripped.

        Returns:
            The output of the code execution as a string.

        Example:
            artisan.execute('''
                $user = \\App\\Models\\User::factory()->create();
                echo $user->id;
            ''')
        """
        php_code = dedent(php_code).strip()
        command = ["tinker", "--execute=" + php_code]
        return self.command(command)


def wait_for(
    assertion: Callable[[], T], timeout: float = 5.0, interval: float = 0.1
) -> T:
    """Retry assertion until timeout. Raises last error if still failing."""
    end = time.time() + timeout
    last_error: Optional[AssertionError] = None
    while time.time() < end:
        try:
            return assertion()
        except AssertionError as e:
            last_error = e
        time.sleep(interval)
    if last_error is None:
        last_error = AssertionError("Timeout")
    raise last_error
