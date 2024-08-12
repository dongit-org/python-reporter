import pytest

from reporter import Reporter


def test_language_operations(rc: Reporter) -> None:
    languages = rc.languages.list()

    assert any(language.name == "English" for language in languages)
