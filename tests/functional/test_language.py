import pytest  # type: ignore

import reporter
from reporter import Reporter


def test_language_operations(rc: Reporter):
    languages = rc.languages.list()

    assert any(language.name == "English" for language in languages)
