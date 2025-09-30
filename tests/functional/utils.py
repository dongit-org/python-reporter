from textwrap import dedent
from docker.models.containers import Container


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

        output: bytes = self.container.exec_run(full_command).output
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
